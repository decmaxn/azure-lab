# Deploy the whole stack manually from Azure Portal
Following [Deploy DeepSeek R1 using Azure AI Foundry and Build a Web Chatbot | No Charges for API Use](https://youtu.be/pj2knBX4S1w?si=I2_7MniDn0Us9bl0), I checked [DeepSeek models availability](https://learn.microsoft.com/en-us/azure/ai-studio/how-to/deploy-models-serverless-availability#deepseek-models-from-microsoft) and found a few regions are available. 

After deployment, I have also tested the playground, works fine.

# Test using the API
Prepare the pythong environment. Also copy the code from playground after a working test, replace the API key.
```bash
python3 -m venv venv
source venv/bin/activate
```
The error for DeepSeekR1 model is 500, which everyone says it is a temporary server error. I wil retry later.
```bash
pip install AzureOpenAI

$ python deepseekr1-chat.py 
... ...
openai.InternalServerError: Error code: 500 - {'error': {'code': 'InternalServerError', 'message': 'Backend returned unexpected response. Please contact Microsoft for help.'}}
```
After creating the same stack in other regions and the tests still failed, I created gpt-4o-mini model manually. This time there are different errors.
```bash
python gpt-4o-mini-chat.py
```
The problems are due to the default "copy code" button on portal doesn't give accurate script for now. Modifeed the gpt-4o-mini-chat.py fixed the problems.

Improve the script by taking the API key from environment variable, and print the response in a more readable format.
```bash
cp example.env .env  # Then update the .env file with the API key manually 
pip install -r requirements.txt 
python gpt-4o-mini-chat.py
```

## Test using the API with Azure AI model inference
There are 3 types of end points for the project. "Azure AI inference" is the one we need to use with azure.ai.inference libraries, as in azure--inference-chat.py.

An other one is for "Azure OpenAI Service", use it with AzureOpenAI library, as in gpt-4o-mini-chat.py.

Using wrong endpoint will result in error like this:
```bash
azure.core.exceptions.ResourceNotFoundError: (404) Resource not found
```

And "Azure AI Services" endpoint to call Computer Vision, Content Safety, Document Intelligence, Language, Translation, and Token services. There are also 2 Speech service's endpoints, one for Speech to Text and the other for Text to Speech.

There is another endpoint for the specific model, it's longer including api version, and maybe deployment name.

But no matter which endpoints, They all share the same API key. 
