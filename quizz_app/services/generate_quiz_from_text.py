import os
from google import genai
from .schemas import QuizSchema


def generate_quiz_from_text(text: str) -> str:
    """Generate a quiz from video transcript using Gemini API.

    Sends the transcript to Google Gemini and requests a structured quiz
    in JSON format with 10 challenging questions.

    Args:
        text: Transcript text from the video

    Returns:
        str: JSON string containing quiz data with questions and answers
    """
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    prompt = f"""
        You are an expert in knowledge transfer. Create a challenging quiz
        with exactly 10 questions based on the following video transcript.
        
        Rules:
        - Each question must have exactly 4 answer options (question_options).
        - Specify under 'correct_answer_index' which option is correct (0, 1, 2, or 3).
        - Formulate an appropriate quiz title and a brief description.
        
        Transcript:
        {text}
        """

    try:
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": QuizSchema,
            },
        )
        return response.text
    except Exception as e:
        print(
            f"Error with gemini-3.5-flash: {str(e)}. Trying model gemini-3.1-flash-lite...")
        response = client.models.generate_content(
            model='gemini-3.1-flash-lite',
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": QuizSchema,
            },
        )
        return response.text
