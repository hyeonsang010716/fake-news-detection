from pytube import YouTube
from pytubefix import YouTube
from pytubefix.cli import on_progress
import moviepy.editor
from moviepy.editor import VideoFileClip
from dotenv import load_dotenv
from openai import OpenAI , AzureOpenAI
import openai
import os
load_dotenv()

client = OpenAI()

# client = AzureOpenAI(
#     api_key = os.getenv('AZURE_OPENAI_API_KEY'),  #Azure Open AI Key
#     api_version = "2024-05-01-preview",  #Azue OpenAI API model
#     azure_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT') #Azure Open AI end point(매직에꼴)
# )

def download_audio(url):
    yt = YouTube(url, on_progress_callback = on_progress)
    ys = yt.streams.get_highest_resolution()
    audio_file = ys.download(filename="audio.mp4")
    
    renamed_file = audio_file[:-4] + ".mp3"

    with VideoFileClip(audio_file) as video:
        video.audio.write_audiofile(renamed_file)
    
    os.remove(audio_file)
    
    return renamed_file, yt.title

def transcribe_audio(audio_path):
    
    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    
    # 파일 삭제
    os.remove(audio_path)

    return transcript.text
    

if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=bN8XdNQuRVU"
    audio_path = download_audio(video_url)
    transcribed_text = transcribe_audio(audio_path)
    print(transcribed_text)