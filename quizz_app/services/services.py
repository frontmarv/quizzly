
import yt_dlp
import whisper
from google import genai
from pydantic import BaseModel
import os
import torch


def download_youtube_audio(youtube_url: str, output_filename: str = "audio") -> str:
    """Lädt das Audio per yt-dlp herunter und gibt den Dateipfad zurück."""
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{output_filename}.%(ext)s',
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
    return f"{output_filename}.mp3"


def transcribe_audio(file_path: str) -> str:
    """Nutzt lokales Whisper, um Text zu generieren."""
    if torch.cuda.is_available():
        device = "cuda"
    elif torch.backends.mps.is_available():
        device = "mps"
    else:
        device = "cpu"
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audiodatei nicht gefunden: {file_path}")
        model = whisper.load_model("turbo")
        result = model.transcribe(file_path)
        if not result or "text" not in result:
            raise ValueError(
                "Transkription hat kein Text-Ergebnis zurückgegeben")
        return result["text"]
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Fehler: {str(e)}") from e
    except ValueError as e:
        raise ValueError(f"Fehler bei Validierung: {str(e)}") from e
    except Exception as e:
        raise RuntimeError(
            f"Unerwarteter Fehler bei Transkription: {str(e)}") from e


class QuestionSchema(BaseModel):
    question_title: str
    question_options: list[str]
    correct_answer_index: int


class QuizSchema(BaseModel):
    title: str
    description: str
    questions: list[QuestionSchema]


def generate_quiz_from_text(text: str) -> str:
    """Schickt den Text an Gemini und fordert das Quiz-JSON an."""
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    prompt = f"""
        Du bist ein Experte für Wissensvermittlung. Erstelle ein anspruchsvolles Quiz 
        mit genau 10 Fragen aus dem folgenden Transkript eines Videos.
        
        Regeln:
        - Jede Frage muss genau 4 Antwortmöglichkeiten (question_options) haben.
        - Gib unter 'correct_answer_index' an, welche Option richtig ist (0, 1, 2 oder 3).
        - Formuliere einen passenden Quiz-Titel und eine kurze Beschreibung.
        
        Transkript:
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
