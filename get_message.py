import requests

api_url = 'http://localhost:5000/send_message'

# Send a message to the API
user_message = "Tóm tắt bài báo sau và nhận xét tích cực hay tiêu cực theo định dạng json (summary, sentiment, explanation): https://dantri.com.vn/xa-hoi/bien-dong-sap-hung-bao-huong-vao-mien-bac-20231017224018307.htm"
response = requests.post(api_url, json={'message': user_message})

# Get the assistant's response
if response.status_code == 200:
    data = response.json()
    assistant_response = data['assistant_response']
    print(f"User: {user_message}")
    print(f"Assistant: {assistant_response}")
else:
    print("Error sending the message.")