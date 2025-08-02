import { motion } from "framer-motion";

export default function Navbar() {
  return (
    <motion.nav
      initial={{ y: -40, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
      className="w-full fixed top-0 left-0 z-50 bg-[#0f172a] shadow-md border-b border-white/10"
    >
      <div className="max-w-6xl mx-auto px-4 py-4 flex justify-start items-center">
        <h1
          className="text-xl sm:text-2xl font-bold tracking-wide text-white drop-shadow-sm cursor-pointer"
          onClick={() => window.location.reload()}
        >
          Aurora AI
        </h1>
      </div>
    </motion.nav>
  );
}
