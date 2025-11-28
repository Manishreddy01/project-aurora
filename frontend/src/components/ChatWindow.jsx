import { useState } from "react";
import ChatFeed from "./ChatFeed";
import ChatInput from "./ChatInput";
import FileUpload from "./FileUpload";

// Set backend URL via .env or fallback to localhost
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000";

export default function ChatWindow({ messages, setMessages, conversationId }) {
  const [files, setFiles] = useState([]); // store uploaded files temporarily

  const handleSend = async (inputText) => {
    if (!inputText.trim() && files.length === 0) return;

    const newMessages = [];

    // Add text message (if any)
    if (inputText.trim()) {
      newMessages.push({ role: "user", content: inputText });
    }

    // Add uploaded file names
    if (files.length > 0) {
      const fileMessages = files.map((file) => ({
        role: "user",
        content: `📄 Uploaded: ${file.name}`,
      }));
      newMessages.push(...fileMessages);
    }

    // Show user message(s) in UI
    setMessages((prev) => [...prev, ...newMessages]);

    // Prepare upload form
    const formData = new FormData();
    formData.append("conversationId", conversationId);
    if (inputText.trim()) formData.append("text", inputText);
    files.forEach((file) => formData.append("file", file));

    // Upload files + text to backend
    try {
      await fetch(`${BACKEND_URL}/upload/`, {
        method: "POST",
        body: formData,
      });
    } catch (error) {
      console.error("Upload failed:", error);
    }

    // Query backend for response
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

    setFiles([]); // reset file input after send
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto space-y-5 px-4">
        <ChatFeed messages={messages} />
      </div>

      <div className="mt-4 p-4 bg-white space-y-4">
        <ChatInput onSend={handleSend} />
        <FileUpload files={files} setFiles={setFiles} />
      </div>
    </div>
  );
}
