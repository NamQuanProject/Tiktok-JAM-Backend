from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from openai import OpenAI
import uuid
# Create your models here.



class User(AbstractUser):
    id = models.CharField(max_length=255, default= uuid.uuid4 ,primary_key=True)
    full_name = models.CharField(max_length=225, blank=False)
    bio = models.CharField(max_length=255, blank=True)
    shopping_history = []
    
    def __str__(self):
        return self.username
    


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




