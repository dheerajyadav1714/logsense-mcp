import os
import json
import asyncio
from google.cloud import logging_v2
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

server = Server("cloudbuild-log-fetcher")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="get_cloud_build_log",
            description="Retrieve the logs of a Google Cloud Build job given its build ID.",
            inputSchema={
                "type": "object",
                "properties": {
                    "build_id": {"type": "string", "description": "The Cloud Build ID (e.g., abc-123)."}
                },
                "required": ["build_id"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "get_cloud_build_log":
        build_id = arguments["build_id"]
        project_id = os.environ.get("PROJECT_ID")
        if not project_id:
            raise ValueError("PROJECT_ID environment variable not set")

        filter_str = f'resource.type="build" AND resource.labels.build_id="{build_id}"'
        client = logging_v2.LoggingServiceV2Client()
        entries = client.list_log_entries(
            resource_names=[f"projects/{project_id}"],
            filter=filter_str,
            order_by="timestamp asc"
        )

        log_lines = []
        for entry in entries:
            if hasattr(entry, "text_payload") and entry.text_payload:
                log_lines.append(entry.text_payload)
            elif hasattr(entry, "json_payload"):
                log_lines.append(json.dumps(entry.json_payload))

        if not log_lines:
            return [types.TextContent(type="text", text=f"No logs found for build ID {build_id}")]

        return [types.TextContent(type="text", text="\n".join(log_lines))]

    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="cloudbuild-log-fetcher",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
