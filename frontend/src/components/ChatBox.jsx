import Message from "./Message";
export default function ChatBox({ messages }) {
  return (
    <div className="border rounded p-4 h-80 overflow-y-auto bg-gray-50">
      {messages.map((msg, i) => (
        <Message key={i} role={msg.role} content={msg.content} />
      ))}
    </div>
  );
}




