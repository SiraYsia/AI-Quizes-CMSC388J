from flask import render_template, redirect, url_for, request, flash, session, jsonify
from flask_login import login_required, current_user
from quiz_app import mongo
from quiz_app.quiz.forms import QuizCreateForm, QuizResponseForm
from quiz_app.quiz.utils import generate_quiz
from . import quiz
from bson.objectid import ObjectId
from datetime import datetime

@quiz.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = QuizCreateForm()
    if form.validate_on_submit():
        topic = form.topic.data
        num_questions = form.num_questions.data
        difficulty = form.difficulty.data
        
        try:
            questions = generate_quiz(topic, num_questions, difficulty)
            
            if not questions or len(questions) == 0:
                raise ValueError("No questions were generated")
            
            if len(questions) == 1 and "We couldn't generate a quiz" in questions[0]['question']:
                flash("We encountered an error generating your quiz. Please try again or choose a different topic.", "danger")
                return render_template('quiz/create.html', title='Create Quiz', form=form)
            
            quiz_data = {
                'user_id': current_user.id,
                'topic': topic,
                'difficulty': difficulty,
                'questions': questions,
                'created_at': datetime.utcnow()
            }
            
            result = mongo.db.quizzes.insert_one(quiz_data)
            quiz_id = result.inserted_id
            
            return redirect(url_for('quiz.take', quiz_id=quiz_id))
            
        except Exception as e:
            error_message = str(e)
            print(f"Error generating quiz: {error_message}")
            flash(f"We couldn't generate a quiz: {error_message}. Please try again or choose a different topic.", "danger")
            return render_template('quiz/create.html', title='Create Quiz', form=form)
    
    return render_template('quiz/create.html', title='Create Quiz', form=form)

    

@quiz.route('/take/<quiz_id>', methods=['GET', 'POST'])
@login_required
def take(quiz_id):
    # get the quiz from the database
    quiz_data = mongo.db.quizzes.find_one({'_id': ObjectId(quiz_id)})
    
    if not quiz_data:
        flash('Quiz not found.', 'danger')
        return redirect(url_for('main.index'))
    
    # create a form for CSRF protection
    form = QuizResponseForm()
    
    if request.method == 'POST':
        user_answers = []
        score = 0
        
        for i, question in enumerate(quiz_data['questions']):
            selected_option = request.form.get(f'question_{i}')
            
            if selected_option is not None:

                selected_option_int = int(selected_option)
                is_correct = selected_option_int == question['correct_answer']
                
                if is_correct:
                    score += 1
                
                user_answers.append({
                    'question_index': i,
                    'selected_option': selected_option_int,
                    'is_correct': is_correct
                })
            else:

                user_answers.append({
                    'question_index': i,
                    'selected_option': -1,
                    'is_correct': False
                })
        
        # calculate percentage score
        total_questions = len(quiz_data['questions'])
        percentage = (score / total_questions) * 100 if total_questions > 0 else 0
        
        # save the attempt to the database
        attempt_data = {
            'user_id': current_user.id,
            'quiz_id': quiz_id,
            'answers': user_answers,
            'score': score,
            'total_questions': total_questions,
            'percentage': percentage,
            'completed_at': datetime.utcnow()
        }
        

        result = mongo.db.attempts.insert_one(attempt_data)
        attempt_id = result.inserted_id
        
        return redirect(url_for('quiz.results', attempt_id=attempt_id))
    
    return render_template('quiz/take.html', title=f'Quiz: {quiz_data["topic"]}', quiz=quiz_data, form=form)


@quiz.route('/results/<attempt_id>')
@login_required
def results(attempt_id):

    attempt = mongo.db.attempts.find_one({'_id': ObjectId(attempt_id)})
    
    if not attempt:
        flash('Quiz attempt not found.', 'danger')
        return redirect(url_for('main.index'))
    
    # check if the user has permission to view these results
    if str(attempt['user_id']) != current_user.id:
        flash('You do not have permission to view these results.', 'danger')
        return redirect(url_for('main.index'))
    
    quiz_data = mongo.db.quizzes.find_one({'_id': ObjectId(attempt['quiz_id'])})
    
    if not quiz_data:
        flash('Quiz not found.', 'danger')
        return redirect(url_for('main.index'))
    
    user_answers_dict = {}
    for answer in attempt['answers']:
        user_answers_dict[answer['question_index']] = answer['selected_option']
    
    return render_template('quiz/results.html', 
                          title='Quiz Results', 
                          attempt=attempt, 
                          quiz=quiz_data,
                          user_answers_dict=user_answers_dict)


@quiz.route('/history')
@login_required
def history():

    attempts = list(mongo.db.attempts.find({'user_id': current_user.id}).sort('completed_at', -1))
    
    for attempt in attempts:
        quiz_data = mongo.db.quizzes.find_one({'_id': ObjectId(attempt['quiz_id'])})
        if quiz_data:
            attempt['topic'] = quiz_data['topic']
            attempt['difficulty'] = quiz_data['difficulty']
        else:
            attempt['topic'] = 'Unknown'
            attempt['difficulty'] = 'Unknown'
    
    return render_template('quiz/history.html', title='Quiz History', attempts=attempts)