from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,BooleanField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length



class SearchVideoForm(FlaskForm):
    videoname = StringField('剧名或播放链接', validators=[DataRequired(), Length(1, 256)])
    remember = BooleanField("服务器记录历史",default=True)
    submit = SubmitField('搜索')
    