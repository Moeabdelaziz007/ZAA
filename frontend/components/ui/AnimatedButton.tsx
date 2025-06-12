/**
 * Component: AnimatedButton
 * المؤلف: محمد عبدالعزيز (Amrikyy)
 * 
 * Description (EN): A button component with smooth animations using Framer Motion, supporting hover and tap effects.
 * الوصف (ع): مكون زر مع رسوم متحركة سلسة باستخدام Framer Motion، يدعم تأثيرات التحويم والضغط.
 * 
 * Props:
 * - children: React.ReactNode   // محتوى الزر
 * - onClick?: () => void       // دالة النقر
 * - className?: string         // كلاسات CSS إضافية
 * - disabled?: boolean         // حالة التعطيل
 */
import React from 'react';
import { motion } from 'framer-motion';

interface AnimatedButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  className?: string;
  disabled?: boolean;
}

const AnimatedButton: React.FC<AnimatedButtonProps> = ({
  children,
  onClick,
  className = '',
  disabled = false,
}) => {
  return (
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      className={`px-4 py-2 rounded-lg bg-[var(--accent)] text-white font-semibold 
        transition-colors duration-200 hover:bg-opacity-90 focus:outline-none 
        focus:ring-2 focus:ring-[var(--accent)] focus:ring-opacity-50 
        disabled:opacity-50 disabled:cursor-not-allowed ${className}`}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </motion.button>
  );
};

export default AnimatedButton; 