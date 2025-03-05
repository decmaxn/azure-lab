import os
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv, find_dotenv
from azure.ai.inference.models import SystemMessage, UserMessage


# Find and load the .env file
dotenv_path = find_dotenv()
print(f"Loading .env file from: {dotenv_path}")
load_dotenv(dotenv_path, override=True)

### ######################################################################## ###
# # Unset environment variables to ensure they are loaded from the .env file
# for key in ["ENDPOINT_URL", "AZURE_OPENAI_API_KEY", "DEPLOYMENT_NAME"]:
#     if key in os.environ:
#         del os.environ[key]

# # Print the contents of the .env file
# with open(dotenv_path, 'r') as file:
#     print("Contents of .env file:")
#     for line in file:
#         print(line.strip())

# # Print the environment variables loaded from the .env file
# print("Loaded environment variables:")
# for key in ["ENDPOINT_URL", "AZURE_OPENAI_API_KEY", "DEPLOYMENT_NAME"]:
#     print(f"{key}: {os.environ.get(key)}")
### ######################################################################## ###

client = ChatCompletionsClient(
    endpoint=os.environ["ENDPOINT_URL"],
    credential=AzureKeyCredential(os.environ["AZURE_OPENAI_API_KEY"]),
)

response = client.complete(
    messages=[
        SystemMessage(content="You are a helpful assistant."),
        UserMessage(content="who are you?"),
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