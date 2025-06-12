/**
 * LoadingPage
 * Displays a full-screen loading indicator with neon green accent color and glassmorphism effect.
 * 
 * صفحة تحميل تعرض مؤشر تحميل دائري في منتصف الشاشة مع تأثير زجاجي ولون أخضر نيون.
 */
import React from 'react';
import { LoadingIndicator } from '../components/StaticComponent';

const LoadingPage: React.FC = () => (
  <div className="min-h-screen flex flex-col justify-center items-center bg-gradient-to-br from-green-900/60 via-green-700/60 to-green-500/60 dark:from-gray-900/80 dark:via-gray-800/80 dark:to-gray-700/80 backdrop-blur-lg">
    <LoadingIndicator size="large" accentColor="green-500" />
    <h2 className="mt-8 text-2xl font-bold text-green-900 dark:text-green-200 animate-pulse">
      جاري التحميل...
      <span className="block text-base font-normal text-gray-500 dark:text-gray-300 mt-2">Loading, please wait</span>
    </h2>
  </div>
);

export default LoadingPage;
