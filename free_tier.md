
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
az deployment group create \
    --resource-group prg \
    --template-file azure-template.json \
    --parameters vmName=tvm adminUsername=victoronto adminPassword=Victoront012
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