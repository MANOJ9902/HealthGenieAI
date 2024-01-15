import smtplib
from flask import Flask, request, render_template, jsonify
import io
import os
from google.cloud import vision_v1, vision
from google.cloud.vision_v1 import types
import openai
from google.oauth2 import service_account
openai.api_key = "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"


# Set up Google Cloud Vision API client
#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "ServiceAccountToken.json"
#client = vision_v1.ImageAnnotatorClient()


#import os
#from google.cloud import vision_v1


# Set up Google Cloud Vision API client with credentials
credentials = service_account.Credentials.from_service_account_info({
  "type": "service_account",
  "project_id": "handwrittenrecognise",
  "private_key_id": "78301784537c220f43820a564a679af27c4127be",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDk3LNavQlh8Jt5\nPHGKDUQ4tHv7F0Hn+NCzf5HjJXnFI50muWnwLe9AXQ9zF7mU3miKBG0qCXZdHDAQ\nQhii1C4noRQl+EO92Du/LuoLwMRO0qV8Qs+0iphI6OTsObYtOv9PrNxRP/bBWioM\nnWIgnIMPcUIWWPU47YOs0M7qVMVHnOacdobrzLJnXEuTzcikfsNFAQmgmLXIn/KC\nqQKu9ZZHDS2tfevJOh6sl3f+R7NFRDXAAqgUhsWMOzlanGBcvea94TTn+1oQMBaH\n85X+fdFruxgj2yK4j9vVzTYI0FxtagEBKlrg7bjNUM+CtDNO7unUTkMduFUFq+6p\ncaERx4/PAgMBAAECggEAJRHiiJYKCQUnXxHSn4vakFzGSuYk1LrRWIxsnaBFAxDr\ntDQK3CPJ7GD7zvv5drWNCp4A7fLZFefU7oKQ6amjTY6ibCwJvPG4wRTg8Bpp3GKe\nT2xQUcFekqC2mSoX6hJI/HzWtYpoy5TGhC3nO7peODLI2O8meUbE3J8jL4L07s5F\nfdY6gJ/i7bvtn6+z0ZrI1zLnlfptm/yUkz3cI7oCaG2xhI/HwCOkGOHUJKkzRLxg\nxILzjC7VagcVkLUk9/9tGjLLXRsr7RM74ZUrHVqgHGiEQ4+YpKlCacfLsoavHD0K\nNNkQWNuUoixWpECtEKyyJ19bUTCZ9XTL26lg+Z22EQKBgQD4pzOaZt9Vucm2Pky2\n806vvDhC7MVD5iD6lOURUZk/LaNgRn/ItcsWnFftbYpEB/GMlgDFrDirGxKJhvAy\n8ITZyNBZW4QmLzxFiVh5hEkNGrptcHfjnU6N95zCga9J1BplqKZh38ORfy8z78Cd\nG6QLH7FhwlFNhXkk57l6+n1EAwKBgQDrn80FNagH9ZxXekHZRvtxv4SOmnB/oxDv\n/afKSmLEl3k4ywLKu5HI+rTRKlfLipEufQWIVKpZUOEvOp1tHB2pD8G8P5pWxtjQ\nxA8XuNFTPEOEMYzZjjoLHytBOuWs73toLJf57D/vP9TFN1vt4sx/diXgAmqJ4wo5\nsUIoXbVpRQKBgQDcyhLfKjNrenIq+bzCwt7+2oGWo4kyFlj4SFfyfeM2nz6v0UnM\nHeh8Zk0JDTg12lvYuqVq4Nbc0Egwh/onMTy16UNf5Qw9n7nEAQXnuNfo4+/gF3rN\nSLQlCVZPvDm6s7TQyeUbiUatniJ62ovMtWt/WR/3r0TkMf11ELG5Ck1KowKBgQCg\nydGsRms90zs27rTUwn1/p8ObVISEdRBv1NaVUqGHqh4MxWxIUCsxzPNq8Mwsl4hv\nAt2tpKkCfhDMm+ElvdP3tEruXTDDGrqF6+SouXQOqscgBHgrVcUCJejsgHaOxnWe\nJyAmajNO3m4hjp9q/CO0rzk1XjC5m3c022NcDGZpSQKBgQCAF5ZJVQyNvx+VrKwB\nzHKSvttoD+OneiIVpUCkKu29sMygEd2ycEdr77opyPc4pWQ6PH6ERnBD0HdUzsVL\nuWv9JhdH2JICOqvgItSfjZNlRbSd/Vgr22lj1Y/B+JqusWGdoxBhEJM6i2lQo8xw\nONHq4l//lZECqwslbQllna+35g==\n-----END PRIVATE KEY-----\n",
  "client_email": "handwritten-recognition-servic@handwrittenrecognise.iam.gserviceaccount.com",
  "client_id": "110088426347664765957",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/handwritten-recognition-servic%40handwrittenrecognise.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
})

#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = None

client = vision_v1.ImageAnnotatorClient(credentials=credentials)





app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze_image', methods=['POST'])
def analyze_image():
    # Get the image from the request
    file = request.files['image']
    content = file.read()

    # Call the Google Cloud Vision API to analyze the image
    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)
    text = response.full_text_annotation.text

    # Return the result as JSON
    return jsonify({'text': text})

@app.route('/api/suggest_remedies', methods=['POST'])
def suggest_remedies():
    input_text = request.form["feeling"]

    # Generate response using OpenAI GPT-3 API
    model_engine = "text-davinci-002"
    prompt = f"What can I do to feel better if I'm {input_text}?"
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=60,
        n=1,
        stop=None,
        temperature=0.7,
    )
    suggestions = completions.choices[0].text.strip()
    return jsonify({'suggestions': suggestions})
@app.route('/send_email', methods=['POST'])
def send_email():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    to = 'your_mail'
    subject = 'New message from website'
    body = f'Name: {name}\nEmail: {email}\nMessage:\n{message}'

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('your_mail', 'password')
        server.sendmail('your_email@gmail.com', to, body)
        server.quit()
        return 'Email sent successfully!'
    except:
        return 'Error sending email'

if __name__ == '__main__':
    app.run()
