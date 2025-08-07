import { useState } from "react";
import ChatFeed from "./ChatFeed";
import ChatInput from "./ChatInput";
import FileUpload from "./FileUpload";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000";

export default function ChatWindow({ messages, setMessages, conversationId }) {
  const [files, setFiles] = useState([]);

  const handleSend = async (inputText) => {
    if (!inputText.trim() && files.length === 0) return;

    const newMessages = [];

    if (inputText.trim()) {
      newMessages.push({ role: "user", content: inputText });
    }

    if (files.length > 0) {
      const fileMessages = files.map((file) => ({
        role: "user",
        content: `📄 Uploaded: ${file.name}`,
      }));
      newMessages.push(...fileMessages);
    }

    setMessages((prev) => [...prev, ...newMessages]);

    const formData = new FormData();
    formData.append("conversationId", conversationId);
    if (inputText.trim()) formData.append("text", inputText);
    files.forEach((file) => formData.append("files", file));

    try {
      await fetch(`${BACKEND_URL}/upload/`, {
        method: "POST",
        body: formData,
      });
    } catch (error) {
      console.error("Upload failed:", error);
    }

    try {
      const res = await fetch(`${BACKEND_URL}/query/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: inputText, conversationId }),
      });

      const data = await res.json();

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.answer,
          sources: data.sources,
          type: data.type,
          confidence: data.confidence,
        },
      ]);
    } catch (err) {
      console.error("Query failed:", err);
    }

    setFiles([]);
  };

  return (
    <div className="flex flex-col h-full">
      {/* 👇 Scrollable feed container is full width */}
      <div className="flex-1 overflow-y-auto">
        {/* 👇 ChatFeed centered inside */}
        <div className="w-full max-w-3xl mx-auto px-4 py-4">
          <ChatFeed messages={messages} />
        </div>
      </div>

      {/* 👇 Input bar also centered */}
      <div className="bg-white w-full max-w-3xl mx-auto px-4 py-4 space-y-4">
        <ChatInput onSend={handleSend} />
        <FileUpload files={files} setFiles={setFiles} />
      </div>
    </div>
  );
}
