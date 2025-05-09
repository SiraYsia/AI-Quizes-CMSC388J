from flask_login import login_required, current_user
from quiz_app import mongo, bcrypt
from quiz_app.user.forms import UpdateProfileForm
from bson.objectid import ObjectId
from flask import render_template, redirect, url_for, flash, request
from . import user

@user.route('/dashboard')
@login_required
def dashboard():

    recent_attempts = list(mongo.db.attempts.find({'user_id': current_user.id}).sort('completed_at', -1).limit(5))
    
    for attempt in recent_attempts:
        quiz_data = mongo.db.quizzes.find_one({'_id': ObjectId(attempt['quiz_id'])})
        if quiz_data:
            attempt['topic'] = quiz_data['topic']
            attempt['difficulty'] = quiz_data['difficulty']
        else:
            attempt['topic'] = 'Unknown'
            attempt['difficulty'] = 'Unknown'
    
    total_attempts = mongo.db.attempts.count_documents({'user_id': current_user.id})
    total_quizzes = mongo.db.quizzes.count_documents({'user_id': current_user.id})
    
    if total_attempts > 0:
        pipeline = [
            {'$match': {'user_id': current_user.id}},
            {'$group': {'_id': None, 'avg_score': {'$avg': '$percentage'}}}
        ]
        avg_result = list(mongo.db.attempts.aggregate(pipeline))
        avg_score = round(avg_result[0]['avg_score'], 1) if avg_result else 0
    else:
        avg_score = 0
    
    return render_template('user/dashboard.html', 
                          title='Dashboard',
                          recent_attempts=recent_attempts,
                          total_attempts=total_attempts,
                          total_quizzes=total_quizzes,
                          avg_score=avg_score)

@user.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    
    if form.validate_on_submit():
        mongo.db.users.update_one(
            {'_id': ObjectId(current_user.id)},
            {'$set': {
                'username': form.username.data,
                'email': form.email.data
            }}
        )
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('user.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    
    return render_template('user/profile.html', title='Profile', form=form)
