/**
 * WelcomePage
 * A modern, animated welcome page with neon green accent color, glassmorphism, and dark mode support.
 * 
 * صفحة ترحيب عصرية مع تأثيرات زجاجية ودعم الوضع الداكن ولون أخضر نيون.
 */
import React from 'react';
import { FaRocket } from 'react-icons/fa';

const WelcomePage: React.FC = () => (
  <div className="min-h-screen flex flex-col justify-center items-center bg-gradient-to-br from-green-100/60 via-green-300/60 to-green-500/60 dark:from-gray-900/80 dark:via-gray-800/80 dark:to-gray-700/80 backdrop-blur-lg">
    <div className="bg-white/40 dark:bg-gray-900/40 rounded-3xl shadow-2xl p-10 flex flex-col items-center backdrop-blur-md border border-white/20 dark:border-gray-700/40">
      <FaRocket className="text-5xl text-green-500 mb-4 animate-bounce" />
      <h1 className="text-4xl font-extrabold text-green-900 dark:text-green-200 mb-2">مرحبًا بك في Zentix 🚀</h1>
      <p className="text-lg text-gray-700 dark:text-gray-300 mb-6">
        منصة متقدمة لإدارة مشاريعك بسهولة واحترافية.<br />
        <span className="text-base text-gray-500 dark:text-gray-400">Welcome to Zentix, your advanced project management platform.</span>
      </p>
      <a
        href="/"
        className="px-6 py-3 bg-green-500 hover:bg-green-600 text-white rounded-full font-semibold shadow-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-green-400"
        title="ابدأ الآن"
      >
        ابدأ الآن 🚀
      </a>
    </div>
  </div>
);

export default WelcomePage;
