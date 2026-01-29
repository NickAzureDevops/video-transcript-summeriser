var sites_asp_func_agentcon_vienna_name = 'asp-func-agentcon-vienna'
var appServicePlanName = 'agentcon-vienna-asp'
@description('Name of the Function App')


resource asp 'Microsoft.Web/serverfarms@2024-11-01' = {
  name: appServicePlanName
  location: 'East US'
  sku: {
    name: 'B1'
    tier: 'Basic'
    size: 'B1'
    family: 'B'
    capacity: 1
  }
  kind: 'linux'
  properties: {
    perSiteScaling: false
    elasticScaleEnabled: false
    maximumElasticWorkerCount: 1
    isSpot: false
    reserved: true
    isXenon: false
    hyperV: false
    targetWorkerCount: 0
    targetWorkerSizeId: 0
    zoneRedundant: false
    asyncScalingEnabled: false
  }
}

targetScope = 'resourceGroup'

@minLength(1)
@maxLength(64)
@description('Name of the environment')
param environmentName string

@minLength(1)
@description('Primary location for all resources')
param location string = 'eastus2'

@description('Name of the AI Foundry account (must be globally unique)')
param aiFoundryName string = 'agentcon-vienna-${uniqueString(subscription().id, environmentName)}'


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
