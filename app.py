from flask import Flask, render_template, request, redirect, url_for, session
import yt_dlp
import assemblyai as aai
from transformers import pipeline
import time
import os
import secrets
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# AssemblyAI API Key
ASSEMBLYAI_API_KEY = '452837939d2b4902808668041543d53d'
aai.settings.api_key = ASSEMBLYAI_API_KEY

# MySQL Database connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',  
            database='ytsum',  
            user='root',  
            password=''  
        )
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Download audio from YouTube
def download_audio_from_youtube(video_url, output_file='audio'):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_file
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    return output_file + '.mp3'

# Transcribe audio using AssemblyAI
def transcribe_audio(file_path):
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(file_path)

    while transcript.status not in {aai.TranscriptStatus.completed, aai.TranscriptStatus.error}:
        time.sleep(5)
        transcript = transcriber.get_transcript(transcript.id)

    if transcript.status == aai.TranscriptStatus.error:
        raise Exception(f"Transcription failed: {transcript.error}")

    return transcript.text

# Summarize transcript using transformer model
def summarize_text(transcript):
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    max_chunk_length = 1024
    chunks = [transcript[i:i + max_chunk_length] for i in range(0, len(transcript), max_chunk_length)]
    summaries = [summarizer(chunk)[0]['summary_text'] for chunk in chunks]
    return " ".join(summaries)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()

            if user:
                return "Email already exists!", 400

            cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, hashed_password))
            conn.commit()
            conn.close()

            return redirect(url_for('login'))
        else:
            return "Database connection failed!", 500

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()

            if user and check_password_hash(user[2], password):
                session['user'] = email
                return redirect(url_for('dashboard'))
            conn.close()

            return "Invalid credentials!", 400
        else:
            return "Database connection failed!", 500

    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    summary = ""
    if request.method == 'POST':
        url = request.form['url']
        audio_file = download_audio_from_youtube(url)
        transcription = transcribe_audio(audio_file)
        summary = summarize_text(transcription)

        with open('summary.txt', 'w') as f:
            f.write(summary)

    return render_template('dashboard.html', summary=summary)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
