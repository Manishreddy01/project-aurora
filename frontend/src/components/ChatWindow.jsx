import { useState } from "react";
import ChatFeed from "./ChatFeed";
import ChatInput from "./ChatInput";
import FileUpload from "./FileUpload";

export default function ChatWindow() {
  const [messages, setMessages] = useState([
    { role: "user", content: "Hi, how are you?" },
    { role: "ai", content: "I'm an AI chatbot. How can I help you today?" },
  ]);
  const [files, setFiles] = useState([]);

  const handleSend = (newMessage) => {
    if (!newMessage.trim()) return;
    setMessages((prev) => [...prev, { role: "user", content: newMessage }]);
    setFiles([]);
  };

  return (
    <div className="w-full max-w-3xl h-[90vh] flex flex-col mx-auto rounded-xl overflow-hidden shadow-2xl border border-white/10 bg-white/10 backdrop-blur-lg backdrop-saturate-150 text-white">
      
      {/* Chat Feed Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        <ChatFeed messages={messages} />
      </div>

      {/* Input & Upload */}
      <div className="border-t border-white/10 bg-white/10 backdrop-blur-md px-4 py-3">
        <FileUpload files={files} setFiles={setFiles} />
        <ChatInput onSend={handleSend} />
      </div>
    </div>
  );
}
