# LogSense AI with MCP – CI/CD Log Analyzer

This project demonstrates an AI agent built with Google ADK that uses the Model Context Protocol (MCP) to fetch logs from Google Cloud Build and analyze them. The agent separates reasoning from tool execution, following the MCP pattern.

## Architecture

- **ADK Agent** (deployed on Cloud Run) – uses Gemini 2.5 Flash to analyze logs.
- **MCP Server** (deployed on Cloud Run) – exposes a `get_cloud_build_log` tool that fetches logs from Cloud Build via the Cloud Logging API.
- **External Data Source** – Google Cloud Build logs.

## Prerequisites

- Google Cloud project with billing enabled.
- Enabled APIs: Cloud Run, Cloud Build, Vertex AI, Cloud Logging.
- IAM roles: `roles/cloudbuild.builds.viewer` for the service account used by the MCP server.
- `gcloud` CLI configured.

## Deployment

### 1. Deploy the MCP Server

```bash
cd mcp-server
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/mcp-cb-server
gcloud run deploy mcp-cb-server \
  --image gcr.io/YOUR_PROJECT_ID/mcp-cb-server \
  --platform managed \
  --region asia-south1 \
  --allow-unauthenticated
