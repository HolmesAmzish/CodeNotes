import ollama

try:
    # 1. 创建 Ollama 客户端
    client = ollama.Client()

    # 2. 调用模型生成文本 (使用 chat 接口进行对话)
    messages = [
        {
            'role': 'user',
            'content': 'what is the capital of Peru?',
        },
    ]

    chat_response = client.chat(
        model='gemma3:1b',
        messages=messages,
    )

    print("Chat Response:")
    print(chat_response.__dict__)
    print(chat_response.message.content)

    # print("\n--- 或使用 generate 接口进行单轮生成 ---")

    # # 3. 调用模型生成文本 (使用 generate 接口进行单轮生成)
    # generate_response = client.generate(
    #     model='gemma3:4b',  # 替换为您想要使用的模型名称
    #     prompt='what is the capital of Peru?',
    # )

    # print("Generate Response:")
    # print(generate_response.response)

except Exception as e:
    print(f"发生错误: {e}")