import { createRoot } from "react-dom/client";
import { QueryClientProvider } from "@tanstack/react-query";
import App from "./App";
import "./index.css";
import "./i18n"; // Import i18n configuration
import { AuthProvider } from "./hooks/use-auth";
import { queryClient } from "./lib/queryClient";

// Check language and set direction
const savedLanguage = localStorage.getItem("i18nextLng");
document.documentElement.dir = savedLanguage === "ar" ? "rtl" : "ltr";

createRoot(document.getElementById("root")!).render(
  <QueryClientProvider client={queryClient}>
    <AuthProvider>
      <App />
    </AuthProvider>
  </QueryClientProvider>
);
