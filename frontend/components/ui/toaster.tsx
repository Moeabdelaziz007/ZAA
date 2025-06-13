"use client";
import { useState, useEffect } from "react";

interface ToastProps {
  message: string;
  type?: "success" | "error" | "info" | "warning";
  duration?: number;
  onClose?: () => void;
}

export const Toaster = ({
  message,
  type = "info",
  duration = 3500,
  onClose,
}: ToastProps) => {
  const [show, setShow] = useState(true);

  useEffect(() => {
    if (!show) return;
    const timer = setTimeout(() => {
      setShow(false);
      if (onClose) onClose();
    }, duration);
    return () => clearTimeout(timer);
  }, [show, duration, onClose]);

  if (!show) return null;

  const color =
    type === "success"
      ? "bg-green-600"
      : type === "error"
      ? "bg-red-600"
      : type === "warning"
      ? "bg-yellow-500"
      : "bg-blue-600";

  return (
    <div
      className={`fixed z-50 bottom-6 right-6 px-6 py-4 rounded-xl shadow-xl transition-all duration-300 flex items-center gap-2 text-white ${color} dark:bg-opacity-90`}
      role="alert"
    >
      {/* أيقونة ديناميكية حسب النوع */}
      {type === "success" && <span>✅</span>}
      {type === "error" && <span>❌</span>}
      {type === "warning" && <span>⚠️</span>}
      {type === "info" && <span>ℹ️</span>}
      <span>{message}</span>
      <button
        className="ml-4 text-white/70 hover:text-white text-lg"
        onClick={() => setShow(false)}
        aria-label="إغلاق"
      >
        ×
      </button>
    </div>
  );
}; 