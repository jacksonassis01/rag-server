import requests
import json
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import os


load_dotenv()

TK=os.getenv("TK", "")
BASEURL=os.getenv("BASEURL", "")

def rag(question):

    # Defina a URL de destino da requisição
    url = BASEURL

    # Defina os headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {TK}'  # Substitua <YOUR_APPLICATION_TOKEN> pelo seu token real
    }

    # Defina o corpo da requisição (payload) como um dicionário Python
    payload = {
        "input_value": question,
        "output_type": "chat",
        "input_type": "chat",
        "tweaks": {
            "ChatInput-Wty2J": {},
            "ParseData-59kyn": {},
            "Prompt-bN6qk": {},
            "SplitText-laCU8": {},
            "ChatOutput-thpkj": {},
            "OpenAIEmbeddings-g2Spc": {},
            "OpenAIEmbeddings-imWyO": {},
            "File-95YLS": {},
            "OpenAIModel-gXSAB": {},
            "AstraDB-EZ0S8": {},
            "AstraDB-YMSbi": {},
            "Directory-baYG9": {}
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        return response.json().get('outputs')[0].get('outputs')[0].get('results').get('message').get('data').get('text')
    else:
        return None

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return 'Hello World!'

@app.route('/bot', methods=['POST'])
def webhook():
    question = request.values.get('Body', '')
    rag_response = rag(question)

    resp = MessagingResponse()
    msg = resp.message()
    msg.body(rag_response)
    
    return str(resp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
