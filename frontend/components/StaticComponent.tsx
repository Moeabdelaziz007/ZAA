/**
 * Component: LoadingIndicator
 * المؤلف: محمد عبدالعزيز (Amrikyy)
 * 
 * Description (EN): Circular loading spinner with progress and accent color support. Used for global and local loading states.
 * الوصف (ع): مؤشر تحميل دائري يدعم تخصيص اللون ونسبة التقدم، يستخدم لحالات التحميل العامة والمحلية.
 * 
 * Props:
 * - size: 'small' | 'medium' | 'large'   // حجم المؤشر
 * - accentColor: string                  // لون التمييز (Tailwind أو Hex)
 */
import React from 'react';

type LoadingIndicatorProps = {
  size?: 'small' | 'medium' | 'large';
  accentColor?: string; // Tailwind color class, e.g., 'green-500'
};

export const LoadingIndicator: React.FC<LoadingIndicatorProps> = ({
  size = 'medium',
  accentColor = 'green-500'
}) => {
  const sizes: Record<'small' | 'medium' | 'large', string> = {
    small: 'h-4 w-4 sm:h-6 sm:w-6',
    medium: 'h-6 w-6 sm:h-8 sm:w-8',
    large: 'h-8 w-8 sm:h-12 sm:w-12'
  };

  return (
    <div className="flex justify-center items-center">
      <div
        className={`
        animate-spin
        rounded-full
          border-t-2 border-b-2
          border-${accentColor}
          bg-white/30 dark:bg-black/30
          backdrop-blur-md
          shadow-lg
        ${sizes[size]}
        `}
        aria-label="Loading"
        title="Loading..."
      />
    </div>
  );
}; 