
import os  
import base64
from openai import AzureOpenAI  
from dotenv import load_dotenv

load_dotenv()

endpoint = os.getenv("ENDPOINT_URL", "https://taihub3485729352.openai.azure.com/")  
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o-mini")  
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "REPLACE_WITH_YOUR_KEY_VALUE_HERE")  

# Initialize Azure OpenAI Service client with key-based authentication    
client = AzureOpenAI(  
    azure_endpoint=endpoint,  
    api_key=subscription_key,  
    api_version="2024-05-01-preview",
)
    
    
# IMAGE_PATH = "YOUR_IMAGE_PATH"
# encoded_image = base64.b64encode(open(IMAGE_PATH, 'rb').read()).decode('ascii')

#Prepare the chat prompt 
chat_prompt = [
    {
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": "You are an AI assistant that helps people find information."
            }
        ]
    },
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "who are you"
            }
        ]
    },
    # {
    #     "role": "assistant",
    #     "content": [
    #         {
    #             "type": "text",
    #             "text": "I am an AI language model created by OpenAI, designed to assist with a variety of tasks, including answering questions, providing information, and engaging in conversation. How can I help you today?"
    #         }
    #     ]
    # }
] 
    
# Include speech result if speech is enabled  
messages = chat_prompt  
    
# Generate the completion  
completion = client.chat.completions.create(  
    model=deployment,
    messages=messages,
    max_tokens=800,  
    temperature=0.7,  
    top_p=0.95,  
    frequency_penalty=0,  
    presence_penalty=0,
    stop=None,  
    stream=False
).choices[0].message.content

print(completion)  
    