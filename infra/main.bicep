targetScope = 'resourceGroup'

@minLength(1)
@maxLength(64)
@description('Name of the environment')
param environmentName string

@minLength(1)
@description('Primary location for all resources')
param location string = 'eastus2'

@description('Name of the AI Foundry account (must be globally unique)')
param aiFoundryName string = 'pizza-foundry-${uniqueString(subscription().id, environmentName)}'

var functionAppName = 'func-${uniqueString(subscription().id, environmentName)}'
var storageAccountName = 'stfunc${uniqueString(subscription().id, environmentName)}'
var appServicePlanName = 'planfunc${uniqueString(subscription().id, environmentName)}'

module aiProject 'ai-project.bicep' = {
  name: 'ai-project'
  params: {
    aiFoundryName: aiFoundryName
    aiProjectName: '${aiFoundryName}-proj'
    location: location
  }
}

// Outputs
output AZURE_LOCATION string = location
