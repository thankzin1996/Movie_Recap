
from flask import Flask, render_template, request
import whisper
import yt_dlp
from openai import OpenAI
import os

app = Flask(__name__)
client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

def process_video(url):
    # YouTube audio download
    ydl_opts = {'format': 'bestaudio/best', 'outtmpl': 'audio.mp3'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    # Transcription
    model = whisper.load_model("base")
    result = model.transcribe("audio.mp3")
    text = result["text"]
    
    # AI Summary
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": f"Summarize this movie transcript: {text}"}]
    )
    return response.choices[0].message.content

@app.route('/', methods=['GET', 'POST'])
def index():
    recap = ""
    if request.method == 'POST':
        url = request.form['url']
        recap = process_video(url)
    return render_template('index.html', recap=recap)

if __name__ == '__main__':
    app.run(debug=True)
