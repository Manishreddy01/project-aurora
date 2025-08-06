import { useState } from "react";
import ChatFeed from "./ChatFeed";
import ChatInput from "./ChatInput";
import FileUpload from "./FileUpload";

export default function ChatWindow({ messages, setMessages }) {
  const [files, setFiles] = useState([]); // store uploaded files temporarily

  const handleSend = (inputText) => {
    if (!inputText.trim() && files.length === 0) return;

    const newMessages = [];

    // Add text message (if any)
    if (inputText.trim()) {
      newMessages.push({ role: "user", content: inputText });
    }

    // Add uploaded file messages
    if (files.length > 0) {
      const fileMessages = files.map((file) => ({
        role: "user",
        content: `📄 Uploaded: ${file.name}`,
      }));
      newMessages.push(...fileMessages);
    }

    // Push all messages to chat
    setMessages((prev = []) => [...prev, ...newMessages]);

    // ✅ Reset file upload and input box
    setFiles([]);
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto space-y-5 px-4">
        <ChatFeed messages={messages} />
      </div>

      <div className="mt-4 p-4 bg-white space-y-4">
        {/* Drag & drop stays visible until user clicks send */}
        <ChatInput onSend={handleSend} />
        <FileUpload files={files} setFiles={setFiles} />
        
      </div>
    </div>
  );
}
