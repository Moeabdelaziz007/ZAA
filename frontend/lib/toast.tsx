import React, { createContext, useContext, useState, useCallback } from 'react';
import { X, CheckCircle, AlertCircle, Info, AlertTriangle } from 'lucide-react';

// Toast Types
export type ToastType = 'success' | 'error' | 'warning' | 'info';

export interface Toast {
  id: string;
  type: ToastType;
  title: string;
  message?: string;
  duration?: number;
  action?: {
    label: string;
    onClick: () => void;
  };
}

interface ToastContextType {
  toasts: Toast[];
  addToast: (toast: Omit<Toast, 'id'>) => void;
  removeToast: (id: string) => void;
  success: (title: string, message?: string) => void;
  error: (title: string, message?: string) => void;
  warning: (title: string, message?: string) => void;
  info: (title: string, message?: string) => void;
}

const ToastContext = createContext<ToastContextType | undefined>(undefined);

// Hook to use toast
export const useToast = () => {
  const context = useContext(ToastContext);
  if (context === undefined) {
    throw new Error('useToast must be used within a ToastProvider');
  }
  return context;
};

// Toast Provider Component
export const ToastProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const addToast = useCallback((toast: Omit<Toast, 'id'>) => {
    const id = Math.random().toString(36).substr(2, 9);
    const newToast: Toast = {
      id,
      duration: 5000,
      ...toast,
    };

    setToasts((prev) => [...prev, newToast]);

    // Auto remove toast after duration
    if (newToast.duration && newToast.duration > 0) {
      setTimeout(() => {
        removeToast(id);
      }, newToast.duration);
    }
  }, []);

  const removeToast = useCallback((id: string) => {
    setToasts((prev) => prev.filter((toast) => toast.id !== id));
  }, []);

  const success = useCallback((title: string, message?: string) => {
    addToast({ type: 'success', title, message });
  }, [addToast]);

  const error = useCallback((title: string, message?: string) => {
    addToast({ type: 'error', title, message, duration: 8000 });
  }, [addToast]);

  const warning = useCallback((title: string, message?: string) => {
    addToast({ type: 'warning', title, message });
  }, [addToast]);

  const info = useCallback((title: string, message?: string) => {
    addToast({ type: 'info', title, message });
  }, [addToast]);

  return (
    <ToastContext.Provider
      value={{
        toasts,
        addToast,
        removeToast,
        success,
        error,
        warning,
        info,
      }}
    >
      {children}
      <ToastContainer toasts={toasts} onRemove={removeToast} />
    </ToastContext.Provider>
  );
};

// Toast Container Component
const ToastContainer: React.FC<{
  toasts: Toast[];
  onRemove: (id: string) => void;
}> = ({ toasts, onRemove }) => {
  if (toasts.length === 0) return null;

  return (
    <div className="fixed top-4 right-4 z-50 flex flex-col gap-2 max-w-sm">
      {toasts.map((toast) => (
        <ToastItem key={toast.id} toast={toast} onRemove={onRemove} />
      ))}
    </div>
  );
};

// Individual Toast Item Component
const ToastItem: React.FC<{
  toast: Toast;
  onRemove: (id: string) => void;
}> = ({ toast, onRemove }) => {
  const getToastStyles = (type: ToastType) => {
    switch (type) {
      case 'success':
        return 'bg-green-500/10 border-green-500/20 text-green-400';
      case 'error':
        return 'bg-red-500/10 border-red-500/20 text-red-400';
      case 'warning':
        return 'bg-yellow-500/10 border-yellow-500/20 text-yellow-400';
      case 'info':
        return 'bg-blue-500/10 border-blue-500/20 text-blue-400';
      default:
        return 'bg-gray-500/10 border-gray-500/20 text-gray-400';
    }
  };

  const getIcon = (type: ToastType) => {
    const iconProps = { className: 'w-5 h-5 flex-shrink-0' };
    switch (type) {
      case 'success':
        return <CheckCircle {...iconProps} className="w-5 h-5 flex-shrink-0 text-green-400" />;
      case 'error':
        return <AlertCircle {...iconProps} className="w-5 h-5 flex-shrink-0 text-red-400" />;
      case 'warning':
        return <AlertTriangle {...iconProps} className="w-5 h-5 flex-shrink-0 text-yellow-400" />;
      case 'info':
        return <Info {...iconProps} className="w-5 h-5 flex-shrink-0 text-blue-400" />;
      default:
        return <Info {...iconProps} />;
    }
  };

  return (
    <div
      className={`
        relative p-4 rounded-lg border backdrop-blur-sm animate-in slide-in-from-right-full
        ${getToastStyles(toast.type)}
      `}
    >
      <div className="flex items-start gap-3">
        {getIcon(toast.type)}
        <div className="flex-1 min-w-0">
          <h4 className="font-medium text-white">{toast.title}</h4>
          {toast.message && (
            <p className="mt-1 text-sm opacity-90">{toast.message}</p>
          )}
          {toast.action && (
            <button
              onClick={toast.action.onClick}
              className="mt-2 text-sm font-medium underline hover:no-underline"
            >
              {toast.action.label}
            </button>
          )}
        </div>
        <button
          onClick={() => onRemove(toast.id)}
          className="flex-shrink-0 p-1 rounded-md hover:bg-white/10 transition-colors"
        >
          <X className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};

// Utility functions for common toast patterns
export const toastUtils = {
  apiError: (error: string) => {
    const context = useContext(ToastContext);
    if (context) {
      context.error('خطأ في API', error);
    }
  },

  loginSuccess: (userName: string) => {
    const context = useContext(ToastContext);
    if (context) {
      context.success('تم تسجيل الدخول بنجاح', `مرحباً ${userName}!`);
    }
  },

  saveSuccess: () => {
    const context = useContext(ToastContext);
    if (context) {
      context.success('تم الحفظ', 'تم حفظ التغييرات بنجاح');
    }
  },

  connectionError: () => {
    const context = useContext(ToastContext);
    if (context) {
      context.error('خطأ في الاتصال', 'تعذر الاتصال بالخادم');
    }
  },

  unauthorizedError: () => {
    const context = useContext(ToastContext);
    if (context) {
      context.error('انتهت الجلسة', 'يرجى تسجيل الدخول مرة أخرى');
    }
  },
};

export default ToastProvider; 