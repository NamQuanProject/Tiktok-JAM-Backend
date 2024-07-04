from openai import OpenAI

def get_rec(prompt):
    client = OpenAI(
    api_key = "LL-3is84tAdyYhd4IwXiz47pJpPDkF6kYTxij4GEJuNMc9ktJqrZpaGTiyljTButnVY",
    base_url = "https://api.llama-api.com")
    response = client.chat.completions.create(
        model="llama3-70b",
        messages=[
            {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
            {"role": "user", "content": f"{prompt}"}
        ]
    )
    text_response = response.choices[0].message.content
    return text_response

def process_response(answer):
    start_index = answer.find('{')
    end_index = answer.rfind('}')
    
    if start_index != -1 and end_index != -1 and start_index < end_index:
        inside = answer[start_index:end_index + 1]
        return inside
    return ""

