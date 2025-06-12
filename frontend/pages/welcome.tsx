/**
 * @component WelcomePage
 * @author Amrikyy
 * @description A modern welcome page with neon green accent color, glassmorphism effects, animations, and dark mode support. | صفحة ترحيب عصرية مع لون أخضر نيون، تأثيرات زجاجية، رسوم متحركة، ودعم الوضع الداكن.
 * @props
 *  - None
 */
import React from "react";
import { FaRocket } from "react-icons/fa";

const WelcomePage: React.FC = () => (
  <div className="min-h-screen flex flex-col justify-center items-center bg-gradient-to-br from-green-100/60 via-green-300/60 to-green-500/60 dark:from-gray-900/80 dark:via-gray-800/80 dark:to-gray-700/80 backdrop-blur-lg px-2 sm:px-4">
    <div className="bg-white/40 dark:bg-gray-900/40 rounded-3xl shadow-2xl p-6 sm:p-10 flex flex-col items-center backdrop-blur-md border border-white/20 dark:border-gray-700/40 max-w-md w-full mx-2 sm:mx-0">
      <span className="text-5xl text-green-500 mb-4 animate-bounce"><FaRocket /></span>
      <h1 className="text-3xl sm:text-4xl font-extrabold text-green-900 dark:text-green-200 mb-2 text-center">
        مرحبًا بك في Zentix 🚀
      </h1>
      <p className="text-gray-600 dark:text-gray-300 text-center mb-6 sm:mb-8 text-sm sm:text-base">
        منصة ذكية لتحسين تجربتك الرقمية
      </p>
      <button 
        className="bg-green-500 hover:bg-green-600 dark:hover:bg-green-400 text-white font-bold py-2 px-4 rounded-xl transition duration-300 ease-in-out transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50"
        aria-label="ابدأ الآن في استكشاف Zentix"
      >
        ابدأ الآن
      </button>
    </div>
  </div>
);

export default WelcomePage;
