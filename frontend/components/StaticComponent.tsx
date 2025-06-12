/**
 * LoadingIndicator
 * Spinner component with customizable size and accent color, supporting dark mode and glassmorphism.
 * 
 * مؤشر تحميل دائري مع إمكانية تخصيص الحجم واللون، يدعم الوضع الداكن وتأثير الزجاج.
 * 
 * @param size - حجم المؤشر: صغير | متوسط | كبير
 * @param accentColor - لون التمييز (افتراضي: أخضر نيون)
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
    small: 'h-6 w-6',
    medium: 'h-8 w-8',
    large: 'h-12 w-12'
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