# Improvement of the temoprary VMs
So far we are creating the VM as well as the supporting resources, like network and security group every time we run the script, and deleting them after testing. It's good to clean up the VM since they cost money when not been used, but those supporting resources are not. Recreating them every time is not efficient.

Since we are deleting the resource group to clean up the temporary resources, we have to create another resource group to hold the permanent resources. Also to create some storage, let's first storage account.

```bash
az group create --name infra-rg --location eastus

az deployment group create \
    --resource-group infra-rg \
    --template-file azure-infra-template.json \
    --parameters @infra-parameters.json

# Don't need to clean it up, it suppose to be there all the time without been charged
az group delete --name infra-rg --yes
```
## Create a Key Vault
The above azure-infra-template.json creates network and a storage account, a file share and a blob container. Technically should put the Key Valut there too, but it's easier to create it separately, because I got the template and parameter files from portal by trying to create a Key Vault following [free for 12 monthes service](https://portal.azure.com/#view/Microsoft_Azure_Billing/FreeServicesBlade).

```bash
az deployment group create \
    --resource-group infra-rg \
    --template-file azure-infra-vault-template.json \
    --parameters @infra-vault-parameters.json
```
### create a secret and a key
```bash
# Variables
keyVaultName="infratkvault"
secretName="adminUserPassword"
secretValue="MyComplex123.password"
sshKeyName="vma_rsa"

# Get the Key Vault Resource ID and the my User Principal ID
keyVaultResourceId=$(az keyvault show --name $keyVaultName --query id --output tsv)
userPrincipalName=$(az ad signed-in-user show --query id -o tsv)

# Assign the Key Vault Secrets Officer role to the me
az role assignment create --role "Key Vault Secrets Officer" --assignee $userPrincipalName --scope $keyVaultResourceId

# Create a secret in Azure Key Vault
az keyvault secret set --vault-name $keyVaultName --name $secretName --value $secretValue

# Generate an SSH key pair if you don't have one: ssh-keygen -t rsa -b 2048 -f $sshKeyName

# Store the public key in Azure Key Vault
az keyvault secret set --vault-name $keyVaultName --name "admin-ssh-key-public" --file "~/.ssh/${sshKeyName}.pub"
```