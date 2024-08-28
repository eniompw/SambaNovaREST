import requests
import json
import os

API_URL = "https://fast-api.snova.ai/v1/chat/completions"
API_KEY = os.environ.get("SN_API_KEY")

def get_chat_completion(query, model="llama3-405b"):
    headers = {"Authorization": f"Basic {API_KEY}"}
    data = {
        "messages": [{"role": "user", "content": query}],
        "model": model,
        "stream": True
    }

    response = requests.post(API_URL, headers=headers, json=data)
    return response

def process_streamed_response(response):
    full_response = ""
    for line in response.iter_lines():
        if not line:
            continue
        
        line = line.decode('utf-8')
        if line == "data: [DONE]":
            break
        
        if line.startswith("data: "):
            json_data = json.loads(line[6:])
            content = json_data['choices'][0]['delta'].get('content', '')
            if content:
                full_response += content
                print(content, end='', flush=True)
    
    return full_response

def main():
    query = "Which number is bigger: 9.11 or 9.9?"
    response = get_chat_completion(query)
    full_response = process_streamed_response(response)
    print()

if __name__ == "__main__":
    main()
