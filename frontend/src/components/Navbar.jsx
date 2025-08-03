import { motion } from "framer-motion";

export default function Navbar() {
  const reloadPage = () => {
    window.location.reload();
  };

  return (
    <motion.nav
      initial={{ y: -40, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
      className="fixed top-0 left-0 w-full z-50 bg-[#0b1d36] shadow-md border-b border-white/10 h-16"
    >
      <div className="max-w-6xl mx-auto px-4 h-full flex items-center">
        <h1
          className="text-xl sm:text-2xl font-bold tracking-wide text-white cursor-pointer"
          onClick={reloadPage}
        >
          Aurora AI
        </h1>
      </div>
    </motion.nav>
  );
}
