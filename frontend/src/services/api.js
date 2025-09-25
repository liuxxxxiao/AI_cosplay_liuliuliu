// 调用后端 API
// src/services/api.js
export async function sendMessage(message, role = "Harry Potter") {
  const res = await fetch("http://localhost:8000/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, role }),
  });
  if (!res.ok) throw new Error("网络错误");
  return res.json();
}


