import { useState, useEffect } from "react";
import { v4 as uuidv4 } from "uuid";
import Navbar from "./components/Navbar";
import ChatWindow from "./components/ChatWindow";
import NewChatSidebar from "./components/NewChatSidebar";

const LOCAL_STORAGE_KEY = "auroraChatHistory";


export default function App() {
  const defaultMessage = [
    {
      role: "bot",
      content: "I'm an AI chatbot. How can I help you today?",
    },
  ];

  const [messages, setMessages] = useState(defaultMessage);
  const [chatList, setChatList] = useState([]);
  const [activeConversationId, setActiveConversationId] = useState(null);

  // Load from storage on mount
  useEffect(() => {
    const saved = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY));
    if (saved?.length) {
      setChatList(saved);
      const lastChat = saved[saved.length - 1];
      setMessages(lastChat.messages);
      setActiveConversationId(lastChat.conversationId);
    }
  }, []);

  // Save when messages change
useEffect(() => {
  if (!activeConversationId || !messages?.length) return;

  const updated = [...chatList];
  const index = updated.findIndex(chat => chat.conversationId === activeConversationId);

  if (index !== -1) {
    updated[index] = {
      ...updated[index],
      messages: messages,
    };

    setChatList(updated); // ✅ preserve order
    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(updated));
  }
}, [messages]);



  const handleNewChat = async () => {
    const newId = uuidv4();
    const newChat = {
      conversationId: newId,
      messages: defaultMessage,
    };

    try {
      await fetch("http://localhost:8000/conversations", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ conversationId: newId }),
      });
    } catch (error) {
      console.error("Error creating conversation:", error);
    }

    const updated = [newChat, ...chatList ];
    setChatList(updated);
    setMessages(defaultMessage);
    setActiveConversationId(newId);
    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(updated));
  };

  const handleSelectChat = (index) => {
    const selected = chatList[index];
    setMessages(selected.messages);
    setActiveConversationId(selected.conversationId);
  };

return (
  <div className="h-screen flex flex-col">
    <Navbar />

    <div className="flex flex-1 overflow-hidden pt-16">
      {/* Sidebar */}
      <div className="w-64 bg-gray-100 border-r border-gray-200">
        <NewChatSidebar
          onNewChat={handleNewChat}
          chatList={chatList}
          onSelectChat={handleSelectChat}
          activeConversationId={activeConversationId}
        />
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* 👇 Scrollable area spans full width */}
        <div className="flex-1 overflow-y-auto">
          <ChatWindow
            messages={messages}
            setMessages={setMessages}
            conversationId={activeConversationId}
          />
        </div>
      </div>
    </div>
  </div>
);

}
