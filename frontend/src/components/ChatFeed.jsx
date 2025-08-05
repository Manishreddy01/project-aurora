import MessageBubble from "./MessageBubble";

export default function ChatFeed({ messages = [] }) {
  return (
    <div className="space-y-4">
      {messages.map((msg, index) => (
        <MessageBubble key={index} role={msg.role} content={msg.content} />
      ))}
    </div>
  );
}
