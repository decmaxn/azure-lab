
# Pay as you go / Azure free account

According to this [FAQ](https://azure.microsoft.com/en-us/pricing/purchase-options/azure-account?icid=azurefaq), the only difference is "Spending protection—credit card won’t be charged" and the $200 credit. 

Even I have volunterrly converted to Pay as you go account, I still have free-tire as "Free monthly amounts of 20+ popular services for 12 months" and "Free monthly amounts of 65+ always-free services".

## How to Verify if You Still Have Free VM Hours?
Try creating a B1, B2ATS, or B2PTS VM.
If it's still eligible for free usage, it will indicate so before finalizing the deployment.

##  Check the Azure Cost Analysis 

Go to Azure Portal → Cost Management + Billing → Cost Analysis.
Use "Cost by resource" link and click on service. Select time period, and Look for charges related various services you have used.

Note, if you see a charge for a B-series VM, that means your free allocation has ended.

# Free Windows 
Using [free for 12 monthes service](https://portal.azure.com/#view/Microsoft_Azure_Billing/FreeServicesBlade), I created a free windows vm. 
Catpture the changes (not all necessary) and modified my ARM template - azure-template.json. 
```bash
az group create --name prg --location eastus

# Create a Key Vault
az keyvault create --name myKeyVault --resource-group prg --location eastus

# Set the Key Vault name
keyVaultName=myKeyVault

# Store the password in Azure Key Vault and retrieve it securely
az keyvault secret set --vault-name <YourKeyVaultName> --name MyPassword --value MyComplex123.password

# Retrieve the password from Azure Key Vault
export PW=$(az keyvault secret show --vault-name <YourKeyVaultName> --name MyPassword --query value -o tsv)
cat <<EOF > parameters.json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "vmName": { "value": "twvm" },
    "adminUsername": { "value": "vma" },
    "adminPassword": { "value": "$PW" }
  }
}
EOF

az deployment group create \
    --resource-group prg \
    --template-file azure-windows-template.json \
    --parameters @parameters.json

az group delete --name prg --yes
```
After remoted in using RDS, I saw the Windows core edition interface. It's nice to see Microsoft is pushing their core edition :-). 
```
================================================================================
              Welcome to Windows Server 2022 Datacenter Azure Edition
  ================================================================================

    1)  Domain/workgroup:                   Workgroup: WORKGROUP
    2)  Computer name:                      tvm
    3)  Add local administrator
    4)  Remote management:                  Enabled

    5)  Update setting:                     Manual
    6)  Install updates
    7)  Remote desktop:                     Enabled (more secure clients)

    8)  Network settings
    9)  Date and time
    10) Telemetry setting:                  Required
    11) Windows activation

    12) Log off user
    13) Restart server
    14) Shut down server
    15) Exit to command line (PowerShell)

  Enter number to select an option:
```
Exit to command line (PowerShell), and run taskmgr, there are your resources. 

Let's have some fun, I installed Choco and Google chrome, then ```start chrome```! It is slow, but hey, it's free. 

# Free linux
 Using [free for 12 monthes service](https://portal.azure.com/#view/Microsoft_Azure_Billing/FreeServicesBlade), I created a free Linux vm. 
Catpture the changes (not all necessary) and modified my ARM template - azure-linux-template.json. 

Replace id_rsa.pub with your public key file, which you have a private key and will use it to login to this VM. Of course replace vma with your user name, and vmName is you prefer to.

```bash
az group create --name prg --location eastus

export sshKey=$(cat ~/.ssh/id_rsa.pub)

cat <<EOF > parameters.json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "vmName": { "value": "tlvm" },
    "adminUsername": { "value": "vma" },
    "sshPublicKey": { "value": "$sshKey" }
  }
}
EOF

az deployment group create \
    --resource-group prg \
    --template-file azure-linux-template.json \
    --parameters @parameters.json

ssh -i ~/.ssh/id_rsa vma@tvm.eastus.cloudapp.azure.com

az group delete --name prg --yes
```

# Two VMS at the same time
Try to bring up 2 VMS at the same and expereienced conflict of names, etc. vmName, osDiskName. Modify the names and it works. 

One thing to be noticed is the myVnet resource are to be created in both ARM tempaltes, but there is no conflict. 
1. Not they can be created with the same name, but the later deployment will ignore this resource and use the existing one. 
1. Each VMs will get their own private IP and they can communicate with each other