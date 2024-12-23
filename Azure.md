Login
```bash
$ az login
$ az account set --subscription "Free Trial" 
$ az account show --query name
$ az account show --query id # Later use this id shown: 83cb1fd7-2152-4b72-b3c8-5970858ef674
$ az ad signed-in-user show 
```
Storage commands
```bash
$ az group list --subscription 83cb1fd7-2152-4b72-b3c8-5970858ef674 # Assume you have manually created resource group trg
$ az storage account list --subscription 83cb1fd7-2152-4b72-b3c8-5970858ef674 --query [].name
# Assume you have manually created this storage account and Later use the name storeibrzj7ov3bnpo

$ az ad signed-in-user show --query id -o tsv | az role assignment create \
    --role "Storage Blob Data Contributor" \
    --assignee @- \
    --scope "/subscriptions/83cb1fd7-2152-4b72-b3c8-5970858ef674/resourceGroups/trg/providers/Microsoft.Storage/storageAccounts/storeibrzj7ov3bnpo"

$ az storage container create --account-name storeibrzj7ov3bnpo --name victoronto --auth-mode login
$ az storage blob upload --account-name storeibrzj7ov3bnpo --container-name victoronto --name test --file test --auth-mode login
```