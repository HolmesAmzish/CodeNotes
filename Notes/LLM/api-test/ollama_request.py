import requests
import json

def get_ollama_response(prompt, model="gemma3:1b", ollama_url="http://localhost:11434/api/generate"):
    """
    向 Ollama 发送一个请求并获取响应。

    Args:
        prompt (str): 要发送给 Ollama 的提示文本。
        model (str, 可选): 使用的 Ollama 模型名称。默认为 "llama2"。
        ollama_url (str, 可选): Ollama API 的基本 URL。
            默认为 "http://localhost:11434/api/generate"。

    Returns:
        str: Ollama 生成的响应文本。

    Raises:
        requests.exceptions.RequestException: 如果请求失败。
        json.JSONDecodeError: 如果响应不是有效的 JSON。
        KeyError: 如果响应 JSON 中缺少 "response" 字段。
    """
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False  # 设置为 False 以获取完整响应
    }

    try:
        response = requests.post(ollama_url, json=payload)
        response.raise_for_status()  # 抛出 HTTP 错误状态

        # 尝试解析 JSON 响应
        try:
            json_response = response.json()
        except json.JSONDecodeError:
            raise json.JSONDecodeError(
                f"Ollama 返回了无效的 JSON 响应: {response.text}",
                doc=response.text,
                pos=0,
            )

        # 检查 "response" 字段是否存在
        if "response" not in json_response:
            raise KeyError(
                f"Ollama 响应 JSON 中缺少 'response' 字段: {json_response}"
            )
        return json_response["response"]

    except requests.exceptions.RequestException as e:
        print(f"发生错误: {e}")
        print(f"请求 URL: {ollama_url}")
        print(f"请求 payload: {payload}")
        if response is not None:
            print(f"响应状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
        raise  # 重新抛出异常，以便调用者可以处理它
    except KeyError as e:
        print(f"发生错误: {e}")
        if response is not None:
            print(f"响应内容: {response.text}")
        raise
    except json.JSONDecodeError as e:
        print(f"发生JSON解码错误: {e}")
        raise

if __name__ == "__main__":
    prompt = "介绍一下你自己。"
    try:
        response = get_ollama_response(prompt, model="gemma3:1b")  # 替换为你想要使用的模型
        print(f"Ollama 响应: {response}")
    except Exception as e:
        print(f"程序遇到错误: {e}") #更详细的报错
