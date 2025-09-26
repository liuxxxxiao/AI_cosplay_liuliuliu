export default function Message({ role, content }) {
  const isUser = role === "user";
  return (
    <div className={`mb-2 ${isUser ? "text-blue-600" : "text-green-600"}`}>
      <b>{isUser ? "你" : "角色"}:</b> {content}
    </div>
  );
}


