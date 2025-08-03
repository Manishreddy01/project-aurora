import { useState } from "react";
import Navbar from "./components/Navbar";
import ChatWindow from "./components/ChatWindow";
import NewChatSidebar from "./components/NewChatSidebar";

export default function App() {
  const defaultMessage = [
    { type: "bot", text: "I'm an AI chatbot. How can I help you today?" }
  ];

  const [messages, setMessages] = useState(defaultMessage);

  const handleNewChat = () => {
    // Reset the chat to default message (like refreshing)
    setMessages(defaultMessage);
  };

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-[#0f172a] via-[#1a365d] to-[#27496d] text-white">
      <Navbar />

      <div className="flex flex-1 pt-16">
        {/* Sidebar */}
        <NewChatSidebar onNewChat={handleNewChat} />

        {/* Chat Window */}
        <div className="flex-1 flex items-center justify-center px-4">
          <ChatWindow messages={messages} setMessages={setMessages} />
        </div>
      </div>
    </div>
  );
}
