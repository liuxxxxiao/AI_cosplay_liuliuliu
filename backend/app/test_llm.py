from backend.app.services.ollama_service import call_ollama

prompt = """
你是哈利波特，请用魔法师的语气。
用户问题如下：
test
请根据已有知识给出简洁清晰的回答。
"""

result = call_ollama(prompt, model="llama3")
print(result)
