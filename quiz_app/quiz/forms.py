from flask_wtf import FlaskForm
from wtforms import TextAreaField, IntegerField, RadioField, SubmitField
from wtforms.validators import DataRequired, NumberRange, ValidationError, Length

class QuizCreateForm(FlaskForm):
    topic = TextAreaField('Quiz Topic or Notes', 
                         validators=[DataRequired(), Length(min=2, max=1000)],
                         render_kw={"rows": 6, "placeholder": "Enter a topic or paste your notes here..."})
    num_questions = IntegerField('Number of Questions', 
                                validators=[DataRequired(), 
                                            NumberRange(min=1, max=10, 
                                                        message="Please choose between 1 and 10 questions.")])
    difficulty = RadioField('Difficulty', 
                           choices=[('easy', 'Easy'), 
                                    ('medium', 'Medium'), 
                                    ('hard', 'Hard')],
                           default='medium')
    submit = SubmitField('Generate Quiz')

class QuizResponseForm(FlaskForm):
    # dynamically generated based on the quiz questions
    submit = SubmitField('Submit Answers')