@description('Location for all resources.')
param location string = resourceGroup().location

@description('Azure AI Search service name (must be globally unique).')
param searchServiceName string

@description('Log Analytics workspace name.')
param logAnalyticsName string

@description('Container Apps environment name.')
param containerAppEnvName string

@description('MCP Docs Server app name.')
param mcpAppName string

@description('Container image for MCP Docs Server.')
param mcpImage string

@description('SKU for Azure AI Search. Use basic for demos.')
@allowed([
  'basic'
  'standard'
  'standard2'
  'standard3'
])
param searchSku string = 'basic'

resource la 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: logAnalyticsName
  location: location
  properties: {
    retentionInDays: 30
  }
}

resource env 'Microsoft.App/managedEnvironments@2023-05-01' = {
  name: containerAppEnvName
  location: location
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: la.properties.customerId
        sharedKey: listKeys(la.id, la.apiVersion).primarySharedKey
      }
    }
  }
}

resource search 'Microsoft.Search/searchServices@2023-11-01' = {
  name: searchServiceName
  location: location
  sku: {
    name: searchSku
  }
  properties: {
    hostingMode: 'default'
    publicNetworkAccess: 'enabled'
  }
}

resource mcp 'Microsoft.App/containerApps@2023-05-01' = {
  name: mcpAppName
  location: location
  properties: {
    managedEnvironmentId: env.id
    configuration: {
      ingress: {
        external: true
        targetPort: 8080
        transport: 'auto'
      }
      activeRevisionsMode: 'Single'
    }
    template: {
      containers: [
        {
          name: 'mcp-docs-server'
          image: mcpImage
          env: [
            { name: 'AZURE_SEARCH_ENDPOINT', value: 'https://${searchServiceName}.search.windows.net' }
            { name: 'AZURE_SEARCH_INDEX_NAME', value: '' } // set after wizard creates index
            { name: 'AZURE_SEARCH_API_KEY', value: '' }    // set manually or via Key Vault for demos
            { name: 'AZURE_SEARCH_API_VERSION', value: '2024-07-01' }
            { name: 'CHANGE_REQUEST_OUTPUT_DIR', value: '/app/change_requests_out' }
          ]
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 1
      }
    }
  }
}

output searchEndpoint string = 'https://${searchServiceName}.search.windows.net'
output containerAppUrl string = 'https://${mcp.properties.configuration.ingress.fqdn}'
