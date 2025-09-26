// 调用后端 API
export async function sendMessage({ question, isAudio }) {
  console.log(JSON.stringify({ data: { question, isAudio } }));
  const res = await fetch("http://127.0.0.1:8000/chat_v1", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      question, 
      isAudio
    })
  });
  if (!res.ok) throw new Error("网络错误");
  return res.json();
}





