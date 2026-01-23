targetScope = 'subscription'

@minLength(1)
@maxLength(64)
@description('Name of the environment')
param environmentName string

@minLength(1)
@description('Primary location for all resources')
param location string = 'eastus2'

@description('Name of the AI Foundry account (must be globally unique)')
param aiFoundryName string = 'pizza-foundry-${uniqueString(subscription().id, environmentName)}'

resource rg 'Microsoft.Resources/resourceGroups@2022-09-01' = {
  name: 'rg-${environmentName}'
  location: location
}

module aiProject 'ai-project.bicep' = {
  name: 'ai-project'
  scope: rg
  params: {
    aiFoundryName: aiFoundryName
    aiProjectName: '${aiFoundryName}-proj'
    location: location
  }
}

// Outputs
output AZURE_LOCATION string = location
output AZURE_RESOURCE_GROUP string = rg.name
output AZURE_AI_FOUNDRY_NAME string = aiProject.outputs.aiFoundryName
output AZURE_AI_PROJECT_NAME string = aiProject.outputs.aiProjectName
output AZURE_AI_PROJECT_ENDPOINT string = aiProject.outputs.aiProjectEndpoint
output AZURE_COSMOS_DB_NAME string = aiProject.outputs.cosmosDBName
output AZURE_STORAGE_ACCOUNT_NAME string = aiProject.outputs.storageAccountName
output AZURE_AI_SEARCH_NAME string = aiProject.outputs.aiSearchName
output FOUNDRY_PROJECT_ENDPOINT string = aiProject.outputs.aiProjectEndpoint
output FOUNDRY_MODEL_DEPLOYMENT_NAME string = aiProject.outputs.modelDeploymentName
output AZURE_OPENAI_IMAGE_DEPLOYMENT string = aiProject.outputs.dalleDeploymentName
