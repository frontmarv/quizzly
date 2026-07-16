import os
import torch
from faster_whisper import WhisperModel


def transcribe_audio(file_path: str) -> str:
    """Transcribe audio file to text using Whisper model.

    Converts audio content to text using the Whisper turbo model. Automatically
    detects GPU availability and selects appropriate compute settings for optimal
    performance. Falls back to CPU with reduced precision if GPU is unavailable
    or if GPU precision types are not supported.

    Args:
        file_path: Path to the audio file to transcribe

    Returns:
        str: Transcribed text from the audio file
    """
    if torch.cuda.is_available():
        device = "cuda"
        compute_type = "float16"
    else:
        device = "cpu"
        compute_type = "int8"

    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found: {file_path}")

        model = WhisperModel("turbo", device=device, compute_type=compute_type)
        segments, info = model.transcribe(file_path, beam_size=5)

        result_text = "".join([segment.text for segment in segments]).strip()

        if not result_text:
            raise ValueError("Transcription returned no text result")

        return result_text

    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: {str(e)}") from e
    except ValueError as e:
        raise ValueError(f"Validation error: {str(e)}") from e
    except Exception as e:
        raise RuntimeError(f"Unexpected transcription error: {str(e)}") from e
