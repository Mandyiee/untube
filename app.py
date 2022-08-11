from flask import Flask, render_template,request,redirect, url_for, send_file
import pytube, moviepy.editor, os
from pathlib import Path
from time import time
app = Flask(__name__)

@app.route('/',methods = ['GET','POST'])
def index():
  urls = None
  thumbnail_url = None
  thumbnail_title = None
  if request.method == 'POST':
    url = request.form['url']
    opt = request.form['option']
    if opt == 'mp4':
      path = 'uploads'
      folder = os.path.join(Path.home(),'uploads')
      yt = pytube.YouTube(url)
      ytName = yt.streams[0].default_filename
      thumbnail_url = yt.thumbnail_url
      index = ytName.index('.')
      ytName = ytName[:index]
      thumbnail_title = ytName
      file = ytName + '.mp3'
      audioFolder = os.path.join(folder, file)
      fileP = os.path.join(folder, file)
      
      
      video = pytube.YouTube(url).streams.get_highest_resolution().download(path)
      
      
      urls = video
    else:
      path = 'uploads'
      folder = os.path.join(Path.home(),'uploads')
      yt = pytube.YouTube(url)
      ytName = yt.streams[0].default_filename
      thumbnail_url = yt.thumbnail_url
      index = ytName.index('.')
      ytName = ytName[:index]
      thumbnail_title = ytName
      file = ytName + '.mp3'
      audioFolder = os.path.join(folder, file)
      fileP = os.path.join(folder, file)
      
      
      video = pytube.YouTube(url).streams.get_highest_resolution().download(path)
      
      vid = moviepy.editor.VideoFileClip(video)
      
      audio = vid.audio
      
      audio.write_audiofile(audioFolder)
      urls = audioFolder
  return render_template('index.html'urls=urls,thumbnail_url=thumbnail_url,thumbnail_title=thumbnail_title)

@app.route('/download')
def downloadFile ():
  #For windows you need to use drive name [ex: F:/Example.pdf] 
  path = request.args.get('path') 
  return send_file(path, as_attachment=True) 

@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")

if __name__ == '__main__':
  app.run(debug=True)
  
  