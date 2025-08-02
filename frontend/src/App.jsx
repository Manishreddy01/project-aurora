import './App.css'
import Navbar from "./components/Navbar";
import ChatWindow from "./components/ChatWindow";

export default function App() {
  return (
    <div className="min-h-screen w-full flex flex-col">
      <Navbar />
      <main className="flex-1 flex items-center justify-center px-4">
        <ChatWindow />

      </main>
    </div>
  );
}
