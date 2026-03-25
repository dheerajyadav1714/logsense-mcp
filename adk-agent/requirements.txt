import os
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import MCPToolset

# Replace with your deployed MCP server URL
MCP_SERVER_URL = "https://mcp-cb-server-xxxx-uc.a.run.app"

mcp_toolset = MCPToolset(
    server_url=MCP_SERVER_URL,
    transport="sse",
    # auth="iam"  # uncomment if you secure with IAM
)

root_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="cloud_build_log_analyzer",
    description="Analyzes Cloud Build logs and provides insights.",
    instruction=(
        "You are a DevOps expert. When a user gives you a Cloud Build ID, use the "
        "get_cloud_build_log tool to fetch the logs. Then analyze them and provide:\n"
        "- **Summary**\n- **Root Cause**\n- **Fix Suggestions**\n- **Severity**\n\n"
        "Be concise and actionable."
    ),
    tools=[mcp_toolset],
)
