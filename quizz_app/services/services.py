
import multiprocessing
import os

import torch
import yt_dlp
from faster_whisper import WhisperModel
from google import genai
from pydantic import BaseModel


def download_youtube_audio(youtube_url: str, output_filename: str = "audio") -> str:
    """Download audio from YouTube video using yt-dlp.

    Extracts the best available audio from a YouTube video and converts
    it to MP3 format.

    Args:
        youtube_url: URL of the YouTube video
        output_filename: Base filename for the output file (default: "audio")

    Returns:
        str: Path to the downloaded MP3 file
    """
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
    """Transcribe audio file to text using Faster Whisper model.

    Converts audio content to text using the Whisper turbo model. Automatically
    detects GPU availability and selects appropriate compute settings for optimal
    performance. Falls back to CPU with reduced precision if GPU is unavailable
    or if GPU precision types are not supported.

    Args:
        file_path: Path to the audio file to transcribe

    Returns:
        str: Transcribed text from the audio file
    """
    cpu_cores = multiprocessing.cpu_count()

    if torch.cuda.is_available():
        device = "cuda"
        compute_type = "float16"
        threads = 4
    else:
        device = "cpu"
        compute_type = "int8"
        threads = max(1, cpu_cores - 2)

    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found: {file_path}")

        try:
            model = WhisperModel(
                "turbo",
                device=device,
                compute_type=compute_type,
                cpu_threads=threads,
                num_workers=2
            )
        except ValueError as e:
            if device == "cuda" and compute_type == "float16":
                print("GPU does not support float16. Switching to int8...")
                try:
                    model = WhisperModel(
                        "turbo",
                        device=device,
                        compute_type="int8",
                        cpu_threads=threads,
                        num_workers=2
                    )
                except Exception:
                    print("int8 failed. Falling back to float32...")
                    model = WhisperModel(
                        "turbo",
                        device=device,
                        compute_type="float32",
                        cpu_threads=threads,
                        num_workers=2
                    )
            else:
                raise e

        segments, info = model.transcribe(
            file_path,
            beam_size=5,
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=500)
        )

        result_text = "".join([segment.text for segment in segments]).strip()

        if not result_text:
            raise ValueError("Transcription returned no text result")

        return result_text

    except Exception as e:
        raise RuntimeError(f"Transcription error: {str(e)}") from e


class QuestionSchema(BaseModel):
    """Schema for a quiz question with options.

    Attributes:
        question_title: The question text
        question_options: List of possible answers
        correct_answer_index: Index of the correct answer (0-3 for 4 options)
    """
    question_title: str
    question_options: list[str]
    correct_answer_index: int


class QuizSchema(BaseModel):
    """Schema for a complete quiz with multiple questions.

    Attributes:
        title: Title of the quiz
        description: Description of the quiz content
        questions: List of questions in the quiz
    """
    title: str
    description: str
    questions: list[QuestionSchema]


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
