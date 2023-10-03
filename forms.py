from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, ValidationError
from wtforms.validators import DataRequired, URL, InputRequired

class DownloadForm(FlaskForm):
    url = StringField('Youtube Url',validators=[InputRequired(),URL()])
    opt = SelectField('Select an Option', choices=[ ('mp4', 'Video'), ('mp3', 'Audio'),])

    def validate_url(self, field):
            if not is_valid_url(field.data):
                raise ValidationError('Invalid URL or URL does not exist')

def is_valid_url(url):
    return url.startswith('http://') or url.startswith('https://') or "youtu" in url
