from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from utils import fetch_reply
import google.cloud.dialogflow as dialogflow
from twilio.rest import Client

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, Berhasil Nih!"

@app.route("/webhook", methods=["POST"])
def webhook():
    message = request.form.get("Body")
    sender = request.form.get("From")

    # Kirim pesan ke Dialogflow untuk memperoleh respons
    response = send_to_dialogflow(message)

    # Kirim respons ke pengguna WhatsApp
    send_whatsapp_message(sender, response)

    return "Success"

def send_to_dialogflow(message):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path("citimclean-bot-no9n", "+14155238886")  # Ganti dengan ID proyek dan ID sesi Anda

    text_input = dialogflow.TextInput(text=message, language_code="en")
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(session=session, query_input=query_input)

    return response.query_result.fulfillment_text

def send_whatsapp_message(receiver, message):
    resp = MessagingResponse()
    resp.message(message)

    message = resp.to_xml()

    client = Client("ACc4d61ca19d1f74e01a409aa757f4bb87", "46a6284d8adf0c7a8cd8be27e2369322")  # Ganti dengan SID akun Twilio Anda dan token otentikasi
    client.messages.create(body=message, from_="+14155238886", to=receiver)  # Ganti dengan nomor telepon Twilio dan penerima

    return "Success"


if __name__ == "__main__":
    # Konfigurasi host dan port
    host = '0.0.0.0'  # Mengubah host menjadi 0.0.0.0
    port = 5000  # Mengubah port menjadi nomor port yang Anda inginkan (misalnya 5000)

    # Menjalankan aplikasi
    app.run(host=host, port=port)
    app.run(debug=True)
