import { motion, AnimatePresence } from 'framer-motion';
import { createContext, useContext, useState, useCallback } from 'react';
import { twMerge } from 'tailwind-merge';
import { XIcon, CheckCircleIcon, ExclamationIcon, InformationCircleIcon } from '@heroicons/react/outline';

type ToastType = 'success' | 'error' | 'info' | 'warning';

interface Toast {
  id: string;
  type: ToastType;
  message: string;
  duration?: number;
}

interface ToastContextType {
  showToast: (toast: Omit<Toast, 'id'>) => void;
  hideToast: (id: string) => void;
}

const ToastContext = createContext<ToastContextType | undefined>(undefined);

export const ToastProvider = ({ children }: { children: React.ReactNode }) => {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const showToast = useCallback(({ type, message, duration = 5000 }: Omit<Toast, 'id'>) => {
    const id = Math.random().toString(36).substr(2, 9);
    setToasts((prev) => [...prev, { id, type, message, duration }]);

    if (duration > 0) {
      setTimeout(() => {
        hideToast(id);
      }, duration);
    }
  }, []);

  const hideToast = useCallback((id: string) => {
    setToasts((prev) => prev.filter((toast) => toast.id !== id));
  }, []);

  return (
    <ToastContext.Provider value={{ showToast, hideToast }}>
      {children}
      <div className="fixed bottom-4 right-4 z-50 flex flex-col gap-2">
        <AnimatePresence>
          {toasts.map((toast) => (
            <motion.div
              key={toast.id}
              initial={{ opacity: 0, y: 50, scale: 0.3 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, scale: 0.5, transition: { duration: 0.2 } }}
              className={twMerge(
                'flex items-center gap-2 rounded-lg px-4 py-3 shadow-lg',
                {
                  'bg-green-50 text-green-800 dark:bg-green-900/20 dark:text-green-400': toast.type === 'success',
                  'bg-red-50 text-red-800 dark:bg-red-900/20 dark:text-red-400': toast.type === 'error',
                  'bg-blue-50 text-blue-800 dark:bg-blue-900/20 dark:text-blue-400': toast.type === 'info',
                  'bg-yellow-50 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400': toast.type === 'warning',
                }
              )}
            >
              {toast.type === 'success' && <CheckCircleIcon className="h-5 w-5" />}
              {toast.type === 'error' && <ExclamationIcon className="h-5 w-5" />}
              {toast.type === 'info' && <InformationCircleIcon className="h-5 w-5" />}
              {toast.type === 'warning' && <ExclamationIcon className="h-5 w-5" />}
              <p className="text-sm font-medium">{toast.message}</p>
              <button
                onClick={() => hideToast(toast.id)}
                className="ml-2 rounded-full p-1 hover:bg-black/5 dark:hover:bg-white/5"
              >
                <XIcon className="h-4 w-4" />
              </button>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </ToastContext.Provider>
  );
};

export const useToast = () => {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within a ToastProvider');
  }
  return context;
};
