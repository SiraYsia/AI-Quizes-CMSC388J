import google.generativeai as genai
from flask import current_app
import json

def configure_genai():
    """Configure the Google Generative AI with API key."""
    genai.configure(api_key=current_app.config['GEMINI_API_KEY'])
def generate_quiz(topic, num_questions, difficulty):

    try:
        configure_genai()
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        is_notes = len(topic) > 100
        
        if is_notes:
            prompt = f"""
            Create a multiple-choice quiz based on the following notes/content with {num_questions} questions at {difficulty} difficulty.
            
            CONTENT:
            {topic}
            
            Format the response as a JSON array of question objects, where each object has:
            - "question": the question text
            - "options": an array of 4 possible answers
            - "correct_answer": the index (0-3) of the correct answer in the options array
            - "explanation": a brief explanation of why the answer is correct
            
            The questions should test understanding of key concepts from the provided content.
            Return ONLY the JSON array, no other text or formatting.
            """
        else:
            prompt = f"""
            Create a multiple-choice quiz about {topic} with {num_questions} questions at {difficulty} difficulty.
            Format the response as a JSON array of question objects, where each object has:
            - "question": the question text
            - "options": an array of 4 possible answers
            - "correct_answer": the index (0-3) of the correct answer in the options array
            - "explanation": a brief explanation of why the answer is correct
            
            Return ONLY the JSON array, no other text or formatting.
            """
        
        response = model.generate_content(prompt)
        
        response_text = response.text
        
        # sometimes the AI includes markdown code blocks so clean that up
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
            
        quiz_data = json.loads(response_text)
        
        for question in quiz_data:
            if not all(key in question for key in ["question", "options", "correct_answer", "explanation"]):
                raise ValueError("Invalid question format in response")
                
        return quiz_data
        
    except Exception as e:
        print(f"Error generating quiz: {e}")
        raise Exception(f"Could not generate quiz: {str(e)}")