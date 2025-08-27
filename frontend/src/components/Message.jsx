import React from "react";
import ReactMarkdown from "react-markdown";

export default function Message({ role, text }) {
  const isUser = role === "user";
  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} my-1`}>
      <div
        className={`p-3 rounded-2xl max-w-xl break-words
        ${
          isUser
            ? "bg-blue-600 text-white rounded-tr-none"
            : "bg-gray-700 text-gray-100 rounded-tl-none"
        }`}
      >
        <ReactMarkdown>{text}</ReactMarkdown>
      </div>
    </div>
  );
}
