import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router";
import { Login } from "./auth/login.tsx";
import { Register } from "./auth/register.tsx";
import { Dashboard } from "./dashboard/dashboard.tsx";
import { Error } from "./error/error.tsx";
import { Board } from "./board/board.tsx";
import "./index.css";
import App from "./App.tsx";
import { AuthProvider } from "./context/AuthContext.tsx";

createRoot(document.getElementById("root")!).render(
  <AuthProvider>
    <BrowserRouter>
      <Routes>
        {/* Landing Page */}
        <Route path="/" element={<App />} />

        {/* Auth Pages */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* 404 */}
        <Route path="*" element={<Error />} />

        {/* Protected Board Routes */}
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/board/:boardId" element={<Board />} />
      </Routes>
    </BrowserRouter>

  </AuthProvider>
);
