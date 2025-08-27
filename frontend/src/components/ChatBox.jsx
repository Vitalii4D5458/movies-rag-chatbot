import React, { useEffect, useRef } from "react";
import Message from "./Message.jsx";

export default function ChatBox({ messages, isTyping }) {
  const scrollRef = useRef();

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  return (
    <div className="flex-1 overflow-y-auto p-6 space-y-3 max-h-[80vh]">
      {messages.map((msg, idx) => (
        <Message key={idx} role={msg.role} text={msg.text} />
      ))}
      {isTyping && (
        <div className="flex justify-start text-gray-400 italic">
          Typing answer...
        </div>
      )}
      <div ref={scrollRef} />
    </div>
  );
}
