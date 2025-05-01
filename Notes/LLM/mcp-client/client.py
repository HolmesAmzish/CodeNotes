import asyncio
import sys
from typing import Optional
from contextlib import AsyncExitStack
import requests
from dotenv import load_dotenv

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()  # 加载环境变量

class MCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.ollama_url = "http://localhost:11434/api/chat"
        self.model = "gemma3:1b"  # 你可以换成你本地 Ollama 安装的其他模型

    async def connect_to_server(self, server_script_path: str):
        """连接到 MCP 工具服务器"""
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

        response = await self.session.list_tools()
        tools = response.tools
        print("\nConnected to server with tools:", [tool.name for tool in tools])

    async def query_ollama(self, messages: list) -> str:
        """调用本地 Ollama 模型"""
        try:
            response = requests.post(
                self.ollama_url,
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False
                }
            )
            response.raise_for_status()
            result = response.json()
            return result["message"]["content"]
        except Exception as e:
            return f"[Error calling Ollama] {str(e)}"

    async def process_query(self, query: str) -> str:
        """处理用户查询并与 Ollama 对话"""
        messages = [{"role": "user", "content": query}]
        final_text = []

        # 列出工具
        response = await self.session.list_tools()
        available_tools = [{
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.inputSchema
        } for tool in response.tools]

        # 向 Ollama 模型发送消息
        assistant_reply = await self.query_ollama(messages)
        final_text.append(assistant_reply)

        # 可在此解析模型生成内容，检查是否包含工具调用标记（TODO）
        # 示例占位：你可以用正则识别 [TOOL_CALL] tool_name {...}

        return "\n".join(final_text)

    async def chat_loop(self):
        """运行交互式聊天循环"""
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                query = input("\nPrompt: ").strip()
                if query.lower() == 'quit':
                    break

                response = await self.process_query(query)
                print("\nResponse:\n" + response)
            except Exception as e:
                print(f"\nError: {str(e)}")

    async def cleanup(self):
        """资源清理"""
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
    asyncio.run(main())
