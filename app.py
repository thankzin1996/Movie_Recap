from flask import Flask, render_template, request
import whisper
import yt_dlp
from openai import OpenAI
import os

app = Flask(__name__)
# API Key ကို Environment Variable ကနေပဲ ယူပါ (မှန်ကန်ပါတယ်)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def process_video(url):
    ydl_opts = {'format': 'bestaudio/best', 'outtmpl': 'audio.mp3'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    model = whisper.load_model("base")
    result = model.transcribe("audio.mp3")
    text = result["text"]
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a movie recap expert."},
            {"role": "user", "content": f"Summarize this movie transcript: {text}"}
        ]
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
    # Railway က ပေးတဲ့ port ကို သုံးဖို့ OS ကနေ ယူရပါမယ်
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    # Railway က ပေးတဲ့ Port ကို အသုံးပြုပါ၊ မရှိရင် 5000 ကို သုံးပါ
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
