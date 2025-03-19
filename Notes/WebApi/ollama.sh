curl http://localhost:11434/api/generate -X POST \
  -H "Content-Type: application/json" \
  -d '{
        "model": "gemma3",
        "prompt": "为什么天空是蓝色的？",
        "stream": false
      }'