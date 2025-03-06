#!/bin/bash

# Check if the resource ID is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <resource-id>"
    exit 1
fi

RESOURCE_ID="$1"

# Extract necessary details using 'awk' or 'cut'
LOCATION=$(echo "$RESOURCE_ID" | awk -F'/' '{print $(NF-4)}')
RESOURCE_GROUP=$(echo "$RESOURCE_ID" | awk -F'/' '{print $(NF-2)}')
ACCOUNT_NAME=$(echo "$RESOURCE_ID" | awk -F'/' '{print $(NF)}')

# Validate extracted values
if [ -z "$LOCATION" ] || [ -z "$RESOURCE_GROUP" ] || [ -z "$ACCOUNT_NAME" ]; then
    echo "Error extracting details from resource ID."
    exit 1
fi

echo "Purging Cognitive Services account: $ACCOUNT_NAME in resource group: $RESOURCE_GROUP and location: $LOCATION"

# Execute the purge command
az cognitiveservices account purge --location "$LOCATION" --resource-group "$RESOURCE_GROUP" --name "$ACCOUNT_NAME"
