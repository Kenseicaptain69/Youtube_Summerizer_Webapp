import yt_dlp
import assemblyai as aai
from transformers import pipeline
import time
import sys
import os

# Set your API keys
ASSEMBLYAI_API_KEY = '452837939d2b4902808668041543d53d'
aai.settings.api_key = ASSEMBLYAI_API_KEY

def download_audio_from_youtube(video_url, output_file='audio'):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_file  # Let yt-dlp handle the extension
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    return output_file + '.mp3'

def transcribe_audio(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file not found: {file_path}")
    
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(file_path)
    
    while transcript.status not in {aai.TranscriptStatus.completed, aai.TranscriptStatus.error}:
        time.sleep(5)
        transcript = transcriber.get_transcript(transcript.id)
    
    if transcript.status == aai.TranscriptStatus.error:
        raise Exception(f"Transcription failed: {transcript.error}")
    
    return transcript.text

def summarize_text(transcript):
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    max_chunk_length = 1024
    chunks = [transcript[i:i + max_chunk_length] for i in range(0, len(transcript), max_chunk_length)]
    summaries = [summarizer(chunk)[0]['summary_text'] for chunk in chunks]
    return " ".join(summaries)

if __name__ == '__main__':
    video_url = sys.argv[1]  # Get the YouTube URL from the command line
    audio_file = download_audio_from_youtube(video_url)
    transcription = transcribe_audio(audio_file)
    summary = summarize_text(transcription)
    
    with open('summary.txt', 'w') as f:
        f.write(summary)

    print("Summary saved to summary.txt")
