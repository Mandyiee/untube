from flask import Flask, render_template,request,redirect, url_for, send_file, flash
import os
import validators
import yt_dlp
import io
from forms import DownloadForm
from dotenv import load_dotenv
import uuid
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
#if validators.url(url):


@app.route('/',methods = ['GET','POST'])
def index():
  urls = None
  thumbnail_url = None
  thumbnail_title = None
  url = None
  opt=None
  
  form = DownloadForm()
  if request.method == 'POST' and form.validate_on_submit():
    url = form.url.data
    opt = form.opt.data
    try:
      ydl_opts = {}
      with yt_dlp.YoutubeDL(ydl_opts) as ydl:
          info = ydl.extract_info(url, download=False)
          thumbnail_title = info.get('title')
          thumbnail_url = info.get('thumbnails')[0]['url']
          
          flash('You can now download your file','success')
    except Exception as e:
          flash('An error occured, Try again','error')
  return render_template('index.html',form=form,thumbnail_url=thumbnail_url,thumbnail_title=thumbnail_title,url=url,opt=opt)

def generate_id():
  return str(uuid.uuid4())

@app.route('/download')   
def downloadFile():
    url = request.args.get('url')
    opt = request.args.get('opt')
    id = generate_id()
      
    try: 
      ydl_opts = {
            'outtmpl': f'{basedir}/{id}.%(ext)s'
        }

      if opt == 'mp3':
          ydl_opts['format'] = 'bestaudio/best'
          ydl_opts['postprocessors'] = [{
              'key': 'FFmpegExtractAudio',
              'preferredcodec': 'mp3',
              'nopostoverwrites': True,
          }]
      elif opt == 'mp4':
          ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best'


      
      with yt_dlp.YoutubeDL(ydl_opts) as ydl:
          info = ydl.extract_info(url, download=False)
          file_extension = info.get('ext')
          title = info.get('title')
          if title:
            title = title.split(' ')
            filename = '-'.join(title)
          else:
            filename = 'file'
          ydl.download([url])
      file_path = f'{basedir}/{id}.{file_extension}'  # Use the actual file extension
      
      with io.open(file_path, 'rb', buffering=0) as file:
          file_bytes = file.read()    
      os.remove(file_path)
          
      
      return send_file(io.BytesIO(file_bytes),attachment_filename=f'{filename}.{file_extension}', as_attachment=True)
    except Exception as e:
      flash('An error occured, Try again','error')
      return redirect(url_for('index'))
  

@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")

@app.errorhandler(500)
def internal_server_error(e):
  return render_template("404.html")

if __name__ == '__main__':
  app.run(debug=True,port=35607)
  

