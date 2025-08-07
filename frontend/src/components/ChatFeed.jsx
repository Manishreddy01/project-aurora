import { useEffect, useRef } from "react";
import MessageBubble from "./MessageBubble";

export default function ChatFeed({ messages = [] }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    if (bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  return (
    <div className="space-y-4 px-4">
      {messages.map((msg, index) => (
        <MessageBubble
          key={index}
          role={msg.role}
          content={msg.content}
          sources={msg.sources}
          confidence={msg.confidence}
          type={msg.type}
        />
      ))}

      <div ref={bottomRef} />
    </div>
  );
}
