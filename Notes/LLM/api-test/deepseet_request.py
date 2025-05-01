import requests
import json

def deepseek_chat(api_key, prompt, model="deepseek-chat", stream=False):
    """
    与 DeepSeek 模型进行聊天。

    Args:
        api_key (str): DeepSeek API 的密钥。
        prompt (str):  要发送给 DeepSeek 模型的提示语。
        model (str, 可选): 使用的 DeepSeek 模型名称。默认为 "deepseek-chat"。
        stream (bool, 可选): 是否使用流式传输。默认为 False。

    Returns:
        str: DeepSeek 模型的响应文本。

    Raises:
        requests.exceptions.RequestException: 如果 API 请求失败。
        json.JSONDecodeError: 如果响应不是有效的 JSON。
        KeyError:  如果响应 JSON 中缺少预期的字段。
    """
    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": stream
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # 抛出 HTTP 错误状态

        # 尝试解析 JSON 响应
        try:
            json_response = response.json()
        except json.JSONDecodeError:
            raise json.JSONDecodeError(
                f"DeepSeek 返回了无效的 JSON 响应: {response.text}",
                doc=response.text,
                pos=0,
            )

        # 检查响应中是否有 'choices'
        if 'choices' not in json_response:
            raise KeyError(f"DeepSeek 响应 JSON 中缺少 'choices' 字段: {json_response}")

        # 进一步检查 'choices' 列表是否为空
        if not json_response['choices']:
            raise ValueError(f"DeepSeek 响应 'choices' 列表为空: {json_response}")
            
        # 检查 'message' 是否在 choices[0] 中
        if 'message' not in json_response['choices'][0]:
            raise KeyError(f"DeepSeek 响应 JSON 中缺少 'message' 字段: {json_response}")

        # 检查 'content' 是否在 message 中
        if 'content' not in json_response['choices'][0]['message']:
            raise KeyError(f"DeepSeek 响应 JSON 中缺少 'content' 字段: {json_response}")
            
        return json_response["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        print(f"发生错误: {e}")
        print(f"请求 URL: {url}")
        print(f"请求 headers: {headers}")
        print(f"请求 payload: {payload}")
        if response is not None:
            print(f"响应状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
        raise  # 重新抛出异常，以便调用者可以处理它
    except json.JSONDecodeError as e:
        print(f"发生JSON解码错误: {e}")
        raise
    except KeyError as e:
        print(f"发生KeyError: {e}")
        raise
    except ValueError as e:
        print(f"发生ValueError: {e}")
        raise

if __name__ == "__main__":
    # 替换为你的 DeepSeek API 密钥
    api_key = "sk-a9ef18cba06e4742b824b7d42dab1cac"  
    prompt = "请用中文回答：什么是人工智能？"
    try:
        response = deepseek_chat(api_key, prompt)
        print(f"DeepSeek 响应: {response}")
    except Exception as e:
        print(f"程序遇到错误: {e}") # 打印更详细的错误
