import os
from flask import Flask, render_template, request, jsonify
import yt_dlp
import openai

app = Flask(__name__)

# OpenAI API Key ကို Railway Variables ထဲမှာ ထည့်ထားပါ
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_youtube_transcript(url):
    # yt-dlp ဖြင့် YouTube မှ အသံ/စာသားရယူခြင်း
    ydl_opts = {'writesubtitles': True, 'skip_download': True, 'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info.get('description', 'No transcript found.')

def ask_ai(prompt):
    # OpenAI GPT ကို မေးခွန်းမေးခြင်း
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    tool = data.get('tool')
    text = data.get('text')
    
    try:
        if tool == 'recap' or tool == 'yt':
            transcript = get_youtube_transcript(text)
            result = ask_ai(f"Summarize this video content: {transcript}")
        elif tool == 'translate':
            result = ask_ai(f"Translate this to Burmese: {text}")
        elif tool == 'chat':
            result = ask_ai(text)
        else:
            result = "ဤ Tool ကို မလုပ်ဆောင်နိုင်သေးပါ။"
    except Exception as e:
        result = f"Error: {str(e)}"
    
    return jsonify({"result": result})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
    
