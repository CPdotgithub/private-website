from flask import  Blueprint,flash, redirect, current_app,render_template,url_for
from cpblog.models import VideoHistory,Admin
from flask_login import login_required, current_user
from cpblog.forms.videos import SearchVideoForm
video_bp = Blueprint('videos',__name__)
from cpblog.extensions import csrf
from datetime import datetime
from cpblog.extensions import db

#@csrf.exempt
@video_bp.route('/',methods=['GET', 'POST'])
def index():

    form = SearchVideoForm()
    if current_user.is_authenticated:
        user_id = current_user.id
        videos = VideoHistory.query.filter_by(user_id=user_id).order_by(VideoHistory.lasttime.desc()).limit(7).all()
        
    else :
        videos=None

    if form.validate_on_submit():
        videoname = form.videoname.data
        remember = form.remember.data
        url = 'https://z1.m1907.cn/?jx='+videoname
        if current_user.is_authenticated:
            user_id = current_user.id
            videoname = form.videoname.data
            if remember == True:
            
                video = VideoHistory.query.filter_by(user_id = current_user.id,videoname=videoname).first()
                if not video:
                    video = VideoHistory(user_id = current_user.id,videoname = form.videoname.data,url = url,lasttime=datetime.now())
                    db.session.add(video)
                    db.session.commit()
                else:
                    video.lasttime=datetime.now()
                    db.session.commit()
                return redirect(location=url)
                
                      
        
                
            else:
                return redirect(location=url)
              
                
        else:
            return redirect(location=url)
          
            
    else:
        return render_template('videos/index.html',form=form,videos=videos)

@video_bp.route('/player/<videoname>')

def player(videoname):
    url =  'https://z1.m1907.cn/?jx='+videoname
    return render_template('videos/player.html',url=url )            
        
    
@video_bp.route('/history/<videoname>')
@login_required
def history(videoname):
        
    user_id = current_user.id
    video = VideoHistory.query.filter_by (user_id = current_user.id,videoname = videoname).first()
  
    video.lasttime=datetime.now()
    
    db.session.commit()
    url = 'https://z1.m1907.cn/?jx='+videoname
    return redirect(location=url)

@video_bp.route('/history/<videoname>/delete')
@login_required
def delete_history(videoname):
    video = VideoHistory.query.filter_by (user_id = current_user.id,videoname = videoname).delete()
    
    db.session.commit()
    return redirect(url_for('.index'))


@video_bp.route('/history/clear')
@login_required
def clear_history():
    video = VideoHistory.query.filter_by (user_id = current_user.id).delete()   
    db.session.commit()
    return redirect(url_for('.index'))




