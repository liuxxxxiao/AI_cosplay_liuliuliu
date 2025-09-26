import { useState } from "react";
export default function InputBox({ onSend }) {
  const [input, setInput] = useState("");
  const handleSend = () => {
    if (!input) return;
    onSend(input);
    setInput("");
  };
  return (
    <div className="mt-4 flex">
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

