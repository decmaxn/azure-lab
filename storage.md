
# Storage

Create storage account, pre-check and post-check. The StorageAccountToBeCreated has to be unique, so I set it to a random string.
```bash
SubID=$(az account show --query id --output tsv)
az group list --subscription $SubID --query [].name
az storage account list --subscription $SubID --query [].name
StorageAccountToBeCreated="jafijeofaewfjei"
az storage account create --name $StorageAccountToBeCreated \
    --resource-group trg \
    --location eastus \
    --sku Standard_RAGRS \
    --kind StorageV2 \
    --min-tls-version TLS1_2 \
    --allow-blob-public-access false
```
Give myself permission to create container and upload blob. It will take a few minutes to sync, you won't be able to do staff before that.
```bash
az ad signed-in-user show --query id -o tsv | az role assignment create \
    --role "Storage Blob Data Contributor" \
    --assignee @- \
    --scope "/subscriptions/$SubID/resourceGroups/trg"
```
Create container as tsc. pre-check and post-check.
```bash
az storage container list --account-name $StorageAccountToBeCreated --auth-mode login
az storage container create --account-name $StorageAccountToBeCreated --name tsc --auth-mode login
```
Now let's pre-check the container, upload a file, post-check and download it back.
```bash
az storage blob list --container-name tsc --account-name $StorageAccountToBeCreated --auth-mode login
az storage blob upload --account-name $StorageAccountToBeCreated --auth-mode login --container-name tsc --file README.md
az storage blob download --account-name $StorageAccountToBeCreated --container-name tsc --auth-mode login --name README.md --file DownloadedREADME.md
```
