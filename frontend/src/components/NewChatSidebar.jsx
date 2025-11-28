export default function NewChatSidebar({ onNewChat, chatList, onSelectChat, activeConversationId}) {
  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      <div className="p-4 pb-2 border-b border-gray-200 bg-gray-100">
        <h2 className="text-xl font-semibold text-gray-800">Project Aurora</h2>
        <button
          onClick={onNewChat}
          className="mt-4 w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg shadow transition-colors"
        >
          New Chat
        </button>
      </div>

      <div className="flex-1 overflow-y-auto bg-gray-100">
        <div className="p-2">
          <h3 className="text-sm font-medium text-gray-500 px-2 mb-2 sticky top-0 bg-gray-100 z-10">
            Conversations
          </h3>
          <div className="space-y-1">
            {chatList.map((chat, index) => {
            const isActive = chat.conversationId === activeConversationId;

            return (
                <button
                key={chat.conversationId || index}
                onClick={() => onSelectChat(index)}
                className={`w-full text-left p-2 rounded-lg transition-colors text-sm truncate ${
                    isActive ? "bg-blue-100 text-blue-800 font-medium" : "hover:bg-gray-200 text-gray-700"
                }`}
                >
                {chat.messages?.[1]?.content || "New Chat"}
                </button>
            );
            })}

          </div>
        </div>
      </div>
    </div>
  );
}
