// 主页
// src/pages/Home.jsx
import { useState } from "react";
import ChatBox from "../components/ChatBox";
import InputBox from "../components/InputBox";
import { sendMessage } from "../services/api";

export default function Home() {
  const [messages, setMessages] = useState([]);

  const handleSend = async (text) => {
    const newMessages = [...messages, { role: "user", content: text }];
    setMessages(newMessages);

    try {
      const data = await sendMessage(text, "Harry Potter"); // 默认角色
      setMessages([
        ...newMessages,
        { role: "assistant", content: data.reply },
      ]);
    } catch (error) {
      setMessages([
        ...newMessages,
        { role: "assistant", content: "出错了，请稍后再试。" },
      ]);
    }
  };

  return (
    <div className="p-6 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">AI 角色扮演</h1>
      <ChatBox messages={messages} />
      <InputBox onSend={handleSend} />
    </div>
  );
}

