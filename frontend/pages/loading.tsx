/**
 * @component LoadingPage
 * @author Amrikyy
 * @description A full-screen loading page with a neon green accent color and glassmorphism effect, displaying a spinner and loading text. | صفحة تحميل كاملة الشاشة مع لون أخضر نيون وتأثير زجاجي، تعرض مؤشر تحميل ونص تحميل.
 * @props
 *  - None
 */
import React from 'react';
import { LoadingIndicator } from '../components/StaticComponent';

const LoadingPage: React.FC = () => (
  <div className="min-h-screen flex flex-col justify-center items-center bg-gradient-to-br from-green-900/60 via-green-700/60 to-green-500/60 dark:from-gray-900/80 dark:via-gray-800/80 dark:to-gray-700/80 backdrop-blur-lg px-2 sm:px-4">
    <LoadingIndicator size="large" accentColor="green-500" />
    <h2 className="mt-4 sm:mt-8 text-lg sm:text-2xl font-bold text-green-900 dark:text-green-200 animate-pulse text-center">
      جاري التحميل...
      <span className="block text-xs sm:text-sm font-normal text-gray-500 dark:text-gray-300 mt-1 sm:mt-2">Loading...</span>
    </h2>
  </div>
);

export default LoadingPage;
