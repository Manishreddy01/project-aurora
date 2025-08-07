# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.

# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.


# 🧠 AuroraAI Chatbot - Frontend

This is the **React + Tailwind** frontend for the AuroraAI chatbot. It handles:
- User input and responses
- File upload UI
- Connecting to backend API
- Displaying document/web-based chatbot replies

---

## 📦 Tech Stack

- React (Vite)
- Tailwind CSS (v4)
- PostCSS
- Framer Motion
- shadcn/ui (optional)

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/your-org/project-aurora.git
cd project-aurora/frontend


2. Install dependencies

npm install uuid

npm install

⚠️ Make sure you’re inside the frontend/ folder before running any commands.

3. Run the development server

npm run dev

Frontend will be available at:
🔗 http://localhost:5173


🟦 AuroraAI Chatbot – Frontend Setup Guide
This guide helps you set up and run the React + Tailwind frontend for AuroraAI locally.

🛠 Tech Stack
React (with Vite)

Tailwind CSS (v4)

PostCSS

Framer Motion

uuid (for generating conversation IDs)

shadcn/ui (optional UI library)

🚀 Getting Started
✅ 1. Clone the Repo

git clone https://github.com/your-org/project-aurora.git
cd project-aurora/frontend
✅ 2. Install Dependencies

npm install


✅ 3. (If Needed) Install Tailwind & Init Config (already done in repo)
Only needed if setting up from scratch

Follow the steps at this URL, do not create a new project as the project is already existing, just run the file installation.

https://tailwindcss.com/docs/installation/using-vite


npm install -D tailwindcss postcss autoprefixer

✅ 4. Start Development Server

npm run dev

By default, the app will be served at:


http://localhost:5173
If you see a blank screen, make sure the FastAPI backend is running on http://localhost:8000.

📦 Optional Additions
5. Install Framer Motion (already included)

npm install framer-motion
6. Install uuid (for unique conversation IDs)

npm install uuid
