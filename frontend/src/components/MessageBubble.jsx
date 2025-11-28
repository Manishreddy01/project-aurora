export default function MessageBubble({ role, content, sources = [], confidence, type }) {
  const isUser = role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-xl px-4 py-3 rounded-lg shadow-md whitespace-pre-wrap ${
          isUser
            ? "bg-blue-600 text-white rounded-br-none"
            : "bg-gray-100 text-gray-900 rounded-bl-none"
        }`}
      >
        <p>{content}</p>

        {!isUser && sources?.length > 0 && (
          <div className="mt-2 text-xs text-gray-500 border-t pt-2">
            <div>🔗 <strong>Sources</strong>: {sources.join(", ")}</div>
            <div>📄 <strong>Type</strong>: {type}</div>
            <div>🎯 <strong>Confidence</strong>: {Math.round(confidence * 100)}%</div>
          </div>
        )}
      </div>
    </div>
  );
}
