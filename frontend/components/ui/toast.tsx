/**
 * Component: Toast
 * المؤلف: محمد عبدالعزيز (Amrikyy)
 * 
 * Description (EN): Animated toast notification component with support for different types and auto-dismiss.
 * الوصف (ع): مكون تنبيه متحرك يدعم أنواع مختلفة من الرسائل وإغلاق تلقائي.
 * 
 * Props:
 * - message: string           // رسالة التنبيه
 * - type: 'success' | 'error' | 'info' | 'warning'   // نوع التنبيه
 * - duration?: number         // مدة العرض (بالميلي ثانية)
 * - onClose?: () => void     // دالة الإغلاق
 */
import React, { useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FiCheck, FiAlertCircle, FiInfo, FiX } from 'react-icons/fi';

interface ToastProps {
  message: string;
  type: 'success' | 'error' | 'info' | 'warning';
  duration?: number;
  onClose?: () => void;
}

const Toast: React.FC<ToastProps> = ({
  message,
  type = 'info',
  duration = 3000,
  onClose,
}) => {
  useEffect(() => {
    if (duration && onClose) {
      const timer = setTimeout(onClose, duration);
      return () => clearTimeout(timer);
    }
  }, [duration, onClose]);

  const icons = {
    success: <FiCheck className="w-5 h-5" />,
    error: <FiAlertCircle className="w-5 h-5" />,
    info: <FiInfo className="w-5 h-5" />,
    warning: <FiAlertCircle className="w-5 h-5" />,
  };

  const colors = {
    success: 'bg-green-500',
    error: 'bg-red-500',
    info: 'bg-blue-500',
    warning: 'bg-yellow-500',
  };

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: 20 }}
        className={`fixed bottom-4 right-4 ${colors[type]} text-white px-4 py-3 rounded-lg shadow-lg flex items-center gap-2`}
      >
        {icons[type]}
        <span>{message}</span>
        {onClose && (
          <button
            onClick={onClose}
            className="ml-2 hover:opacity-80 transition-opacity"
            aria-label="إغلاق التنبيه"
          >
            <FiX className="w-4 h-4" />
          </button>
        )}
      </motion.div>
    </AnimatePresence>
  );
};

export default Toast;
