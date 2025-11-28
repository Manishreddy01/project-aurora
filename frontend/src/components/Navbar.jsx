import { motion } from "framer-motion";
import logo from "../assets/AuroraLogo.png";

export default function Navbar() {
  const reloadPage = () => {
    window.location.reload();
  };

  return (
    <motion.nav
      initial={{ y: -40, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
      className="fixed top-0 left-0 w-full z-50 bg-[#0b1d36] shadow-md border-white/10 h-13"
    >
      <div className="w-full bg-white shadow-md px-4 py-2 text-slate-900">
        <div
          className="flex items-center gap-3 cursor-pointer"
          onClick={reloadPage}
        >
          <img
            src={logo}
            alt="Aurora AI Logo"
            className="w-8 h-8 object-contain"
          />
        <h1 className="text-xl sm:text-2xl font-bold tracking-wide text-transparent bg-clip-text bg-gradient-to-r from-yellow-600 via-orange-500 to-pink-500">
          Aurora AI
        </h1>
        </div>
      </div>
    </motion.nav>
  );
}
