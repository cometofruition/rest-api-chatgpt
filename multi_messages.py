import requests
import argparse
import concurrent.futures
import json
import unicodedata

def send_message(message, endpoint):
    try:
        response = requests.post(
            endpoint,
            json={"message": message},
            headers={"Content-Type": "application/json"}
        )
        response_data = {
            "message": message,
            "response_status_code": response.status_code,
            "response_text": convert_unicode_to_vietnamese(response.text)
        }
        return response_data
    except Exception as e:
        return {
            "message": convert_unicode_to_vietnamese(message),
            "error": str(e)
        }

def convert_unicode_to_vietnamese(text):
    decoded_text = text.encode('utf-8').decode('unicode_escape')
    return decoded_text

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--endpoint", type=str, required=True, help="The URL of the endpoint")
    parser.add_argument("-l", "--list_messages", type=str, required=True, help="Path to a text file containing messages (one message per line)")
    parser.add_argument("-o", "--output_file", type=str, required=True, help="Path to the JSON output file")

    args = parser.parse_args()

    with open(args.list_messages, "r") as file:
        messages = [line.strip() for line in file]

    results = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(send_message, message, args.endpoint) for message in messages]

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)

    # Save the results to a JSON file
    with open(args.output_file, "w") as output_file:
        json.dump(results, output_file, indent=4, ensure_ascii=False)  # Set ensure_ascii=False to preserve Unicode characters

if __name__ == "__main__":
    main()