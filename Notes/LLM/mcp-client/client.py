import asyncio
from typing import Optional
from contextlib import AsyncExitStack
import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

import httpx
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env

class MCPClient:
    def __init__(self, ollama_base_url="http://localhost:11434"):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.ollama_base_url = ollama_base_url
        self.model_name = "gemma3:1b"  # Specify the Ollama model name

    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server

        Args:
            server_script_path: Path to the server script (.py or .js)
        """
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")

        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()

        # List available tools
        response = await self.session.list_tools()
        tools = response.tools
        print("\nConnected to server with tools:", [tool.name for tool in tools])

    async def _call_ollama(self, messages: list, tools: Optional[list] = None) -> dict:
        """Call the local Ollama API."""
        payload = {
            "model": self.model_name,
            "messages": messages,
            "stream": False,
        }
        if tools:
            payload["tools"] = tools

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(f"{self.ollama_base_url}/api/chat", json=payload, timeout=60)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                print(f"Error calling Ollama API: {e}")
                return None

    async def process_query(self, query: str) -> str:
        """Process a query using local Gemma and available tools"""
        messages = [
            {
                "role": "user",
                "content": query
            }
        ]

        response = await self.session.list_tools()
        available_tools = [{
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.inputSchema
        } for tool in response.tools]

        # Initial Ollama API call
        ollama_response = await self._call_ollama(messages, available_tools)

        if not ollama_response or not ollama_response.get("choices"):
            return "Error: Could not get initial response from local Gemma."

        assistant_response = ollama_response["choices"][0]["message"]
        final_text = []

        for content in assistant_response.get("content", "").split('\n'):
            if content:
                final_text.append(content)

        tool_calls = assistant_response.get("tool_calls", [])

        for tool_call in tool_calls:
            tool_name = tool_call["name"]
            tool_args = json.loads(tool_call["arguments"])

            # Execute tool call
            result = await self.session.call_tool(tool_name, tool_args)
            final_text.append(f"[Calling tool {tool_name} with args {tool_args}]")

            # Continue conversation with tool results
            messages.append({
                "role": "assistant",
                "content": assistant_response.get("content", ""),
                "tool_calls": [tool_call]
            })
            messages.append({
                "role": "user",
                "content": f"Tool call result: {result.content}"
            })

            # Get next response from Ollama
            ollama_response = await self._call_ollama(messages)
            if ollama_response and ollama_response.get("choices") and ollama_response["choices"][0].get("message"):
                final_text.append(ollama_response["choices"][0]["message"].get("content", ""))
            else:
                final_text.append("Error: Could not get next response from local Gemma after tool use.")
                break

        return "\n".join(final_text)

    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Client Started with local Gemma!")
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == 'quit':
                    break

                response = await self.process_query(query)
                print("\n" + response)

            except Exception as e:
                print(f"\nError: {str(e)}")

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()

async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)

    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    import sys
    asyncio.run(main())