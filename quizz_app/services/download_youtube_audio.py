import yt_dlp


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
