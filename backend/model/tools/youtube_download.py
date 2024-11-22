from pytube import YouTube
from pytubefix import YouTube
from pytubefix.cli import on_progress
import moviepy.editor
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

def download_audio(url):
    yt = YouTube(url, on_progress_callback = on_progress)
    ys = yt.streams.get_highest_resolution()
    audio_file = ys.download(filename="audio.mp4")
    
    renamed_file = audio_file[:-4] + ".mp3"
    video = moviepy.editor.VideoFileClip(audio_file)
    video.audio.write_audiofile(renamed_file)
    return renamed_file

def transcribe_audio(audio_path):
    audio_file = open(audio_path, "rb")
    transcript = client.audio.transcriptions.create(
        file=audio_file,
        model="whisper-1",
        language="ko",
        response_format="text",
        temperature=0.0,
    )

    return transcript


if __name__ == "__main__":

    video_url = "https://www.youtube.com/watch?v=bN8XdNQuRVU"
    audio_path = download_audio(video_url)
    transcribed_text = transcribe_audio(audio_path)
    print(transcribed_text)