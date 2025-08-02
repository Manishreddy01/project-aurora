import { useState, useEffect } from "react";
import Navbar from "./components/Navbar";
import ChatWindow from "./components/ChatWindow";
import NewChatSidebar from "./components/NewChatSidebar";

const LOCAL_STORAGE_KEY = "auroraChatHistory";

export default function App() {
  const defaultMessage = [
    { type: "bot", text: "I'm an AI chatbot. How can I help you today?" }
  ];

  const [messages, setMessages] = useState(defaultMessage);
  const [chatList, setChatList] = useState([]);

  // Load from storage
  useEffect(() => {
    const saved = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY));
    if (saved?.length) {
      setChatList(saved);
      setMessages(saved[saved.length - 1]); // Load last chat by default
    }
  }, []);

  // Save current messages to storage when they change
  useEffect(() => {
    if (messages.length) {
      const updated = [...chatList.slice(0, -1), messages];
      setChatList(updated);
      localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(updated));
    }
  }, [messages]);

  const handleNewChat = () => {
    const newChat = defaultMessage;
    const updated = [...chatList, newChat];
    setChatList(updated);
    setMessages(newChat);
    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(updated));
  };

  const handleSelectChat = (index) => {
    setMessages(chatList[index]);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0f172a] via-[#1a365d] to-[#27496d] text-white">
      <Navbar />
      <div className="flex pt-16 h-full">
        <NewChatSidebar
          onNewChat={handleNewChat}
          chatList={chatList}
          onSelectChat={handleSelectChat}
        />
        <div className="flex-1 flex items-center justify-center px-4">
          <ChatWindow messages={messages} setMessages={setMessages} />
        </div>
      </div>
    </div>
  );
}
