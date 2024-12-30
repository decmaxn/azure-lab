# Installation

I have avoided the one command installation, and followed the step-by-step on my ubuntu client. Refer to [Official Reference](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli). 

```bash
# Get packages needed for the install process:
sudo apt-get update
sudo apt-get install ca-certificates curl apt-transport-https lsb-release gnupg

#Download and install the Microsoft signing key:
sudo mkdir -p /etc/apt/keyrings
curl -sLS https://packages.microsoft.com/keys/microsoft.asc |
    gpg --dearmor |
    sudo tee /etc/apt/keyrings/microsoft.gpg > /dev/null
sudo chmod go+r /etc/apt/keyrings/microsoft.gpg

# Add the Azure CLI software repository:
AZ_REPO=$(lsb_release -cs)
echo "deb [arch=`dpkg --print-architecture` signed-by=/etc/apt/keyrings/microsoft.gpg] https://packages.microsoft.com/repos/azure-cli/ $AZ_REPO main" |
    sudo tee /etc/apt/sources.list.d/azure-cli.list

# Update repository information and install the azure-cli package:
sudo apt-get update
sudo apt-get install azure-cli
```

## Upgrade
The installation process above will update your Azure Cli, but it might not the latest. The following happens right after I updated it with apt command.
```bash
$ az upgrade
This command is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
Your current Azure CLI version is 2.47.0. Latest version available is 2.48.1.
Please check the release notes first: https://docs.microsoft.com/cli/azure/release-notes-azure-cli
Do you want to continue? (Y/n): y
```
## Uninstall
```bash
sudo apt-get remove -y azure-cli
# Remove it's data for security
rm -rf ~/.azure
```
# Login and look around
You will have to created your own tenant and subscription from the Azure Web Console before try to follow the commands below.
```bash
$ az login
# A web browser has been opened at https://login.microsoftonline.com/organizations/oauth2/v2.0/authorize. Please continue the login in the web browser. If no web browser is available or if the web browser fails to open, use device code flow with `az login --use-device-code`.
```
If you have multiple tenant and subscriptions, you will have to choose which one to use as part of login process above. Or, 
```bash
$ az account set --subscription "<Your subscription name>"
```
Now a lot of cli commands need subscription ID as a parameter, let's set it this way after you have set the subscription.
```bash
$ az account show --query name
$ SubID=$(az account show --query id --output tsv)
$ echo $SubID
```
Last, if you havn't create a resoruce group from web console, you can create one called trg as shown below.
```bash
$ az group create --name trg --location eastus
```