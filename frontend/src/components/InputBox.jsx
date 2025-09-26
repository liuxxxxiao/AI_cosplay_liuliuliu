import { useState } from "react";
export default function InputBox({ onSend, role, setRole, replyType, setReplyType }) {
  const [input, setInput] = useState("");
  const handleSend = () => {
    if (!input) return;
    onSend(input);
    setInput("");
  };
  return (
    <div className="mt-4 flex">
      <div className="flex gap-2">
        <select value={role} onChange={e => setRole(e.target.value)} className="border rounded p-2">
          <option value="苏格拉底">苏格拉底</option>
          <option value="哈利波特">哈利波特</option>
        </select>
        <select value={replyType} onChange={e => setReplyType(e.target.value)} className="border rounded p-2">
          <option value="文本回复">文本回复</option>
          <option value="语音回复">语音回复</option>
        </select>
      </div>
      <input
        className="flex-1 border rounded p-2"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="输入你的话..."
      />
      <button
        onClick={handleSend}
        className="ml-2 px-4 py-2 bg-blue-500 text-white rounded"
      >
        发送
      </button>
    </div>
  );
}

