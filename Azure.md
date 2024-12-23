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
    --parameters vmName=tvm adminUsername=victoronto adminPassword=Victoront012
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
What is wrong with the VM creation?
```bash
az vm create \
    --resource-group trg \
    --name tvm \
    --image Ubuntu2404 \
    --size Standard_B1s \
    --admin-username victoronto \
    --admin-password Victoront012 \
    --zone 3 
{
  "fqdns": "",
  "id": "/subscriptions/d1df09aa-4d86-4495-88f0-eaff2c7106c1/resourceGroups/trg/providers/Microsoft.Compute/virtualMachines/tvm",
  "location": "eastus",
  "macAddress": "7C-1E-52-0B-74-66",
  "powerState": "VM running",
  "privateIpAddress": "10.0.0.5",
  "publicIpAddress": "172.190.115.29",
  "resourceGroup": "trg",
  "zones": "3"
}
 # It also work without the option zones 3, meaning it's not a zone problem as suggested by the error message

az vm delete --resource-group trg --name tvm --yes
disks=$(az disk list --resource-group trg --query "[?contains(name, 'tvm_disk')].{name:name}" -o tsv)
for disk in $disks; do
    az disk delete --resource-group trg --name $disk --yes
done
az network nic delete --resource-group trg --name tvmVMNic
az network public-ip delete --resource-group trg --name tvmPublicIP
az network nsg delete --resource-group trg --name tvmNSG


az vm create \
    --resource-group trg \
    --name tvm \
    --image Ubuntu2404 \
    --size Standard_B1s \
    --admin-username victoronto \
    --admin-password Victoront012 \
    --priority Spot \
    --max-price -1
inner errors for details.","details":[{"code":"SkuNotAvailable","message":"The requested VM size for resource 'Following SKUs have failed for Capacity Restrictions: Standard_B1s' is currently not available in location 'eastus'. Please try another size or deploy to a different location or different zone. See https://aka.ms/azureskunotavailable for details."}]}}
```
So the problem is the spot request. The error message is not so clear.