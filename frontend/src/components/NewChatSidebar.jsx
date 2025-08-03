export default function NewChatSidebar() {

  const handleNewChat = () => {
    window.location.reload(); // ✅ Refreshes the page
  };

  return (
    <div className="bg-[#0f172a] text-white w-64 p-4 flex flex-col gap-4 shadow-lg">
      <h2 className="text-xl font-semibold">Project Aurora</h2>
      <button
        onClick={handleNewChat}
        className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded shadow"
      >
        New Chat
      </button>
    </div>
  );
}
