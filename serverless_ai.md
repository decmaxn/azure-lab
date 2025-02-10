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


