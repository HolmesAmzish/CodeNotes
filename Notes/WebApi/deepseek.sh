curl https://api.deepseek.com/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-c6c11ae0a25a4e1ea64ff97e98d4057a" \
  -d '{
    "model": "deepseek-chat",
    "messages": [
      {
        "role": "user",
        "content": "请用中文回答：什么是人工智能？"
      }
    ],
    "stream": false
  }'