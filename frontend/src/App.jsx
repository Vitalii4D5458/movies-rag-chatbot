import React, { useState } from "react";
import ChatBox from "./components/ChatBox.jsx";

export default function App() {
  const [messages, setMessages] = useState([
    { role: "bot", text: "Hi! How can I help you? :)" },
  ]);
  const [userInput, setUserInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);

  const sendMessage = async (text) => {
    if (!text.trim()) return;
    const newMessages = [...messages, { role: "user", text }];
    setMessages(newMessages);
    setUserInput("");
    setIsTyping(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: text, top_k: 3 }),
      });
      const data = await response.json();
      setMessages([...newMessages, { role: "bot", text: data.answer }]);
    } catch (err) {
      setMessages([
        ...newMessages,
        { role: "bot", text: "Sorry, just a minute." },
      ]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-900 text-gray-100 p-4">
      <div className="w-full max-w-3xl border border-gray-700 rounded-2xl shadow-xl bg-gray-800 flex flex-col">
        <ChatBox messages={messages} isTyping={isTyping} />
        <div className="p-4 flex">
          <input
            type="text"
            className="flex-1 p-3 rounded-l-2xl bg-gray-700 text-gray-100 focus:outline-none"
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            placeholder="Type your message..."
            onKeyDown={(e) => e.key === "Enter" && sendMessage(userInput)}
          />
          <button
            className="bg-blue-600 px-6 py-3 rounded-r-2xl hover:bg-blue-500 transition-colors"
            onClick={() => sendMessage(userInput)}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
