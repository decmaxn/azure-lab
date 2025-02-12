# Deploy the whole stack manually from Azure Portal
Following [Deploy DeepSeek R1 using Azure AI Foundry and Build a Web Chatbot | No Charges for API Use](https://youtu.be/pj2knBX4S1w?si=I2_7MniDn0Us9bl0), I checked [DeepSeek models availability](https://learn.microsoft.com/en-us/azure/ai-studio/how-to/deploy-models-serverless-availability#deepseek-models-from-microsoft) and found a few regions are available. 

After deployment, I have also tested the playground, works fine.

## Manually test the model
After deployed the model as DeepSeek-R1, create a ds-model.env file with the target Uri and Key, test the API simplly with curl:
```bash
export $(grep -v '^#' ds-model.env | xargs)
curl -X POST \
     -H "Content-Type: application/json" \
     -H "api-key: $AZURE_OPENAI_API_KEY" \
     -d '{
           "messages": [{"role": "user", "content": "who are you"}],
           "model": "DeepSeek-R1"
         }' \
     "$ENDPOINT_URL"
```
# Deploy the whole stack using ARM
Copy the ARM template from the portal, and modify the parameters. The deployment is successful.
```bash
ResourceGroupName=infra-rg
az group create --name $ResourceGroupName --location eastus

SubID=$(az account show --query id --output tsv)
sed s/\$SubID/$SubID/g azure-serverlessai-parameters.json  > parameters.json 

az deployment group create \
    --resource-group $ResourceGroupName \
    --template-file azure-serverlessai-template.json \
    --parameters @parameters.json
```
After that, login to portal and manually deploy a model, you will have to created a project if it's not already there. This time I deployed gtp-4o-mini model.
## Clean up
Only the "Azure AI hub" and "Azure AI services" are created by the ARM template. Just delete them instead of deleting the whole resource group. 
```bash
az ml workspace delete --name iaihub \
    --resource-group $ResourceGroupName
az cognitiveservices account delete --name ai-iaihub \
    --resource-group $ResourceGroupName

# The cognitiveservices is only "Soft deleted", need to purge it before create it again.
for ID in $(az cognitiveservices account list-deleted | jq -r .[].id); do \
    ./purge-congnitive-service-acct-with-id.sh $ID
done

# Same for the key vault, it is only "Soft deleted", need to purge it before create it again.
for NAME in $(az keyvault list-deleted |  jq -r '.[].name'); do \
    az keyvault purge --name $NAME
done
```
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

<del>After creating the same stack in other regions and the tests still failed, I found the problem is I used the wrong endpoint. Use the endpoint for the model itself works. Refer to "Test using the API with Azure AI model inference" section below for more details.</del>

Also, I created gpt-4o-mini model manually. This time there are different errors.
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

<del>At this point, I found the gpt-4o-mini-chat.py works for deepseekr1 model as well. The only difference is the endpoint/modelname defined in the .env file. So deleted both gpt-4o-mini-chat.py and deepseekr1-chat.py, and created azure-openai-chat.py. This script will read the .env file, and send the chat request.</del>

## Test using the API with Azure AI model inference
Note: the endpoint for the model is not the same as the one for the project. The endpoint for the model is the one you can find in the "API" tab of the model. The endpoint for the project is the one you can find in the "Overview" tab of the project. The model API endpoint is longer, including the version and deployment name, works with the curl command. 

There are 3 projects endpoints, "Azure AI inference", "Azure OpenAI Service", and "Azure AI Services". Using wrong endpoint will result in error like this:
```bash
azure.core.exceptions.ResourceNotFoundError: (404) Resource not found
```

The "Azure AI inference" is the one we need to use with azure.ai.inference libraries, as in azure--inference-chat.py. 

An other one is for "Azure OpenAI Service", use it with AzureOpenAI library, as in gpt-4o-mini-chat.py. 

And "Azure AI Services" endpoint to call Computer Vision, Content Safety, Document Intelligence, Language, Translation, and Token services. There are also 2 Speech service's endpoints, one for Speech to Text and the other for Text to Speech.

But no matter which endpoints, They all share the same API key. 
