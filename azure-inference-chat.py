import os
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
from azure.ai.inference.models import SystemMessage, UserMessage

load_dotenv()

client = ChatCompletionsClient(
    endpoint=os.environ["ENDPOINT_URL"],
    credential=AzureKeyCredential(os.environ["AZURE_OPENAI_API_KEY"]),
)

response = client.complete(
    messages=[
        SystemMessage(content="You are a helpful assistant."),
        UserMessage(content="Can you use python for creating a frontend app?"),
    ],
    max_tokens=2048,
    model=os.getenv("DEPLOYMENT_NAME")
)

print("Response:", response.choices[0].message.content)
print("Model:", response.model)
print("Usage:")
print("\tPrompt tokens:", response.usage.prompt_tokens)
print("\tTotal tokens:", response.usage.total_tokens)
print("\tCompletion tokens:", response.usage.completion_tokens)