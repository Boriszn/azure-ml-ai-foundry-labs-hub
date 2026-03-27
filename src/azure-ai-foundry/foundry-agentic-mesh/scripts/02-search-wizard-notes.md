# Azure AI Search — Import data (new) wizard notes

Goal: create **data source → index → indexer** for documents stored in an existing Blob container.

## Inputs
- Existing Storage Account + container: `${BLOB_ACCOUNT_NAME}/${BLOB_CONTAINER_NAME}`
- Azure AI Search service: `${AZURE_SEARCH_ENDPOINT}`

## Steps (portal)
1. Open the Azure AI Search service in the Azure portal.
2. Select **Import data (new)**.
3. Choose **Azure Blob Storage** as the data source type.
4. Select the existing Storage Account and container.
5. Confirm authentication (managed identity or connection string) according to tenant policies.
6. Create the **Index**:
   - Keep default fields for a demo, or remove the full `content` field from the index schema if large PDFs cause token/term-size issues.
7. Create the **Indexer**:
   - Run once immediately.
   - Keep schedule disabled for the demo unless repeated re-indexing is required.
8. Verify indexer status:
   - Confirm at least one successful run.
   - Confirm documents appear in the index.

## Quick validation
Run a query in Search Explorer:
- Search term: “policy” (or another word known to exist in demo docs)
- Confirm results include blob metadata fields and any extracted text fields.
