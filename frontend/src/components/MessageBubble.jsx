export default function MessageBubble({ role, content }) {
  const isUser = role === "user";

  return (
    <div className={`w-full flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[75%] px-5 py-3 rounded-2xl text-sm shadow-md whitespace-pre-line ${
          isUser
            ? "bg-blue-600 text-white rounded-br-none"
            : "bg-gray-100 text-gray-800 rounded-bl-none border border-gray-300"
        }`}
      >
        {content}
      </div>
    </div>
  );
}
