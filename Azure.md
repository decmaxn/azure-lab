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

VM commands
```bash
$ az deployment group create \
    --resource-group trg \
    --template-file azure-template.json \
    --parameters vmName=tvm adminUsername=victoronto adminPassword=victoronto
Inner Errors: 
{"code": "SkuNotAvailable", "message": "The requested VM size for resource 'Following SKUs have failed for Capacity Restrictions: Standard_B1s' is currently not available in location 'eastus'. Please try another size or deploy to a different location or different zone. See https://aka.ms/azureskunotavailable for details."}


$ az vm list-skus --location eastus --size Standard_B1s --output table
ResourceType     Locations    Name          Zones    Restrictions
---------------  -----------  ------------  -------  ----------------------------------------------------------------------
virtualMachines  eastus       Standard_B1s  1,2,3    NotAvailableForSubscription, type: Zone, locations: eastus, zones: 2,1
```
Comfirm the deployment is successful.
```bash
$ az deployment group show --resource-group trg --name azure-template
```