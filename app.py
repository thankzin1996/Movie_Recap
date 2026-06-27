from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    tool = data.get('tool')
    text = data.get('text')
    
    # ဤနေရာတွင် Tool အမျိုးအစားအလိုက် လုပ်ဆောင်ချက်များကို ထည့်ပါ
    # ဥပမာ - if tool == 'recap': ...
    
    result_text = f"သင်ရွေးချယ်ထားသော Tool: {tool.upper()}. သင်ထည့်သွင်းသော အချက်အလက်: {text}. ဤအပိုင်းကို AI ဖြင့် ဆက်လက်တည်ဆောက်နိုင်ပါသည်။"
    
    return jsonify({"result": result_text})

if __name__ == '__main__':
    # Railway အတွက် Port သတ်မှတ်ချက်
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
    
