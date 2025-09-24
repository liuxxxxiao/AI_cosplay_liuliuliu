# AI_cosplay_liuliuliu
开发一个利用AI来做角色扮演的网站

设计思路：整体框架：
[前端 Web]  -----------------> [后端服务] -----------------> [AI 能力层]
   |                               |                               |
   | (Vue/React + Three.js 可选)   | (Python/Node.js Flask/FastAPI)| (API 调用组合)
   |                               |                               |
   |---录音上传(STT)->              |                               |---> [STT 模型: Whisper / Azure STT]
   |                               |                               |
   |<--语音播放(TTS)---             |                               |<--- [TTS 模型: GPT-4o 内置 / ElevenLabs / Azure TTS]
   |                               |                               |
   |<--角色设定结果---              |<--- Prompt 管理 / 会话上下文-->|---> [LLM: GPT-4o / Claude / GLM]
   |                               |                               |
   |---角色搜索/切换-->             |---角色设定加载-->              |---> [角色设定库 / embedding 向量检索]
