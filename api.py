from flask import Flask, request, jsonify
import streamlit as st
from Hello import main  # Import your Streamlit app code

app = Flask(__name__)

@app.route('/get_messages', methods=['GET'])
def get_messages():
    if "messages" in st.session_state:
        messages = st.session_state.messages
        return jsonify(messages)
    else:
        return jsonify([])

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    message = data.get("message")
    
    if message:
        st.session_state.messages.append({"role": "user", "content": message})
        main()  # Call your Streamlit app function to process the message
        return jsonify({"status": "Message sent"})
    else:
        return jsonify({"status": "No message provided"})

if __name__ == '__main__':
    app.run()