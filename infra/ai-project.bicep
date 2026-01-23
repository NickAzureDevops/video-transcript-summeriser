param aiFoundryName string = 'video-summarise-agent'
param aiProjectName string = '${aiFoundryName}-proj'
param location string = 'eastus2'

// Unique suffix for globally unique resource names
var uniqueSuffix = uniqueString(resourceGroup().id)
var cosmosDBName = 'cosmos-${uniqueSuffix}'
var storageAccountName = 'st${uniqueSuffix}'
var aiSearchName = 'search-${uniqueSuffix}'

/*
  An AI Foundry resources is a variant of a CognitiveServices/account resource type
*/ 
resource aiFoundry 'Microsoft.CognitiveServices/accounts@2025-04-01-preview' = {
  name: aiFoundryName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  sku: {
    name: 'S0'
  }
  kind: 'AIServices'
  properties: {
    allowProjectManagement: true 
    customSubDomainName: aiFoundryName // Required - defines API endpoint subdomain
    disableLocalAuth: false // Required for agents
  }
}

/*
  Azure Cosmos DB - Thread/conversation storage for agents
*/
resource cosmosDB 'Microsoft.DocumentDB/databaseAccounts@2024-12-01-preview' = {
  name: cosmosDBName
  location: location
  kind: 'GlobalDocumentDB'
  properties: {
    databaseAccountOfferType: 'Standard'
    locations: [
      {
        locationName: location
        failoverPriority: 0
      }
    ]
    capabilities: [
      {
        name: 'EnableServerless'
      }
    ]
    disableLocalAuth: true
  }
}

/*
  Azure Storage Account - File storage for agents
*/
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
    allowSharedKeyAccess: false
    minimumTlsVersion: 'TLS1_2'
  }
}

/*
  Azure AI Search - Vector store for RAG/knowledge retrieval
*/
resource aiSearch 'Microsoft.Search/searchServices@2024-06-01-preview' = {
  name: aiSearchName
  location: location
  sku: {
    name: 'basic'
  }
  properties: {
    replicaCount: 1
    partitionCount: 1
    hostingMode: 'default'
    authOptions: {
      aadOrApiKey: {
        aadAuthFailureMode: 'http401WithBearerChallenge'
      }
    }
  }
}

/*
  Developer APIs are exposed via a project, which groups in- and outputs that relate to one use case, including files.
  Its advisable to create one project right away, so development teams can directly get started.
  Projects may be granted individual RBAC permissions and identities on top of what account provides.
*/ 
resource aiProject 'Microsoft.CognitiveServices/accounts/projects@2025-04-01-preview' = {
  name: aiProjectName
  parent: aiFoundry
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {}

  // Connection to Cosmos DB
  resource cosmosConnection 'connections@2025-04-01-preview' = {
    name: 'cosmosdb-connection'
    properties: {
      category: 'CosmosDB'
      target: cosmosDB.properties.documentEndpoint
      authType: 'AAD'
      metadata: {
        ApiType: 'Azure'
        ResourceId: cosmosDB.id
        location: cosmosDB.location
      }
    }
  }

  // Connection to Storage Account
  resource storageConnection 'connections@2025-04-01-preview' = {
    name: 'storage-connection'
    properties: {
      category: 'AzureStorageAccount'
      target: storageAccount.properties.primaryEndpoints.blob
      authType: 'AAD'
      metadata: {
        ApiType: 'Azure'
        ResourceId: storageAccount.id
        location: storageAccount.location
      }
    }
  }

  // Connection to AI Search
  resource searchConnection 'connections@2025-04-01-preview' = {
    name: 'search-connection'
    properties: {
      category: 'CognitiveSearch'
      target: 'https://${aiSearch.name}.search.windows.net'
      authType: 'AAD'
      metadata: {
        ApiType: 'Azure'
        ResourceId: aiSearch.id
        location: aiSearch.location
      }
    }
  }
}

/*
  Model deployments for agents and tools
*/
resource modelDeployment 'Microsoft.CognitiveServices/accounts/deployments@2024-10-01'= {
  parent: aiFoundry
  name: 'gpt-4o'
  sku : {
    capacity: 1
    name: 'GlobalStandard'
  }
  properties: {
    model:{
      name: 'gpt-4o'
      format: 'OpenAI'
    }
  }
}

// DALL-E 3 for episode artwork generation
resource dalleDeployment 'Microsoft.CognitiveServices/accounts/deployments@2024-10-01'= {
  parent: aiFoundry
  name: 'dall-e-3'
  sku : {
    capacity: 1
    name: 'Standard'
  }
  properties: {
    model:{
      name: 'dall-e-3'
      format: 'OpenAI'
    }
  }
  dependsOn: [modelDeployment]
}

/*
  Account-level Capability Host - enables Agents on the account
*/
resource accountCapabilityHost 'Microsoft.CognitiveServices/accounts/capabilityHosts@2025-04-01-preview' = {
  name: '${aiFoundryName}-caphost'
  parent: aiFoundry
  properties: {
    capabilityHostKind: 'Agents'
  }
  dependsOn: [
    aiProject
  ]
}

/*
  Project-level Capability Host - enables Agents on the project with connections
*/
resource projectCapabilityHost 'Microsoft.CognitiveServices/accounts/projects/capabilityHosts@2025-04-01-preview' = {
  name: '${aiProjectName}-caphost'
  parent: aiProject
  properties: {
    capabilityHostKind: 'Agents'
    aiServicesConnections: []
    storageConnections: ['storage-connection']
    vectorStoreConnections: ['search-connection']
    threadStorageConnections: ['cosmosdb-connection']
  }
  dependsOn: [
    accountCapabilityHost
    aiProject::cosmosConnection
    aiProject::storageConnection
    aiProject::searchConnection
  ]
}

/*
  RBAC Role Assignments - Grant project identity access to dependencies
*/


// Storage Blob Data Contributor for file storage
resource storageBlobRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(storageAccount.id, aiProject.id, 'ba92f5b4-2d11-453d-a403-e96b0029c9fe')
  scope: storageAccount
  properties: {
    principalId: aiProject.identity.principalId
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'ba92f5b4-2d11-453d-a403-e96b0029c9fe') // Storage Blob Data Contributor
    principalType: 'ServicePrincipal'
  }
}

// Search Index Data Contributor for vector store
resource searchRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(aiSearch.id, aiProject.id, '8ebe5a00-799e-43f5-93ac-243d3dce84a7')
  scope: aiSearch
  properties: {
    principalId: aiProject.identity.principalId
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '8ebe5a00-799e-43f5-93ac-243d3dce84a7') // Search Index Data Contributor
    principalType: 'ServicePrincipal'
  }
}

// Search Service Contributor for managing indexes
resource searchServiceRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(aiSearch.id, aiProject.id, '7ca78c08-252a-4471-8644-bb5ff32d4ba0')
  scope: aiSearch
  properties: {
    principalId: aiProject.identity.principalId
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '7ca78c08-252a-4471-8644-bb5ff32d4ba0') // Search Service Contributor
    principalType: 'ServicePrincipal'
  }
}

// Outputs
output aiFoundryName string = aiFoundry.name
output aiProjectName string = aiProject.name
output aiFoundryEndpoint string = aiFoundry.properties.endpoint
output aiProjectEndpoint string = 'https://${aiFoundry.name}.services.ai.azure.com/api/projects/${aiProject.name}'
output cosmosDBName string = cosmosDB.name
output storageAccountName string = storageAccount.name
output aiSearchName string = aiSearch.name
output modelDeploymentName string = modelDeployment.name
output dalleDeploymentName string = dalleDeployment.name
