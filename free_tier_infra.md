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
Teh above azure-infra-template.json creates network and a storage account, a file share. Technically I should put the Key Valut there too, but it's easier to create it separately. 

Because I got the template from portal by trying to create a Key Vault following [free for 12 monthes service](https://portal.azure.com/#view/Microsoft_Azure_Billing/FreeServicesBlade).

```bash
az deployment group create \
    --resource-group infra-rg \
    --template-file azure-infra-vault-template.json \
    --parameters @infra-vault-parameters.json
```