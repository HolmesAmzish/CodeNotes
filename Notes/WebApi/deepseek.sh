curl https://api.deepseek.com/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-9bab5ed6e8164eaf8dc500ac875e5129" \
  -d '{
    "model": "deepseek-chat",
    "messages": [
      {"role": "user", "content": "请用中文回答：什么是人工智能？"}
    ],
    "stream": false
  }'