/**
 * File: index.tsx
 * المؤلف: محمد عبدالعزيز (Amrikyy)
 * 
 * Description (EN): Home page component with welcome message and features overview.
 * الوصف (ع): مكون الصفحة الرئيسية مع رسالة ترحيب ونظرة عامة على الميزات.
 */

import { motion } from 'framer-motion';
import { AnimatedButton } from '../components/ui/AnimatedButton';

export default function Home() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="min-h-screen bg-gradient-to-br from-primary-50 to-primary-100 dark:from-gray-900 dark:to-gray-800"
    >
      <main className="container mx-auto px-4 py-16">
        <h1 className="text-4xl font-bold text-center mb-8 text-gray-900 dark:text-white">
          مرحباً بك في زينتكس | Welcome to Zentix
        </h1>
        <p className="text-lg text-center mb-12 text-gray-600 dark:text-gray-300">
          منصة ذكية للتحليلات والذكاء الاصطناعي | Smart Analytics & AI Platform
        </p>
        <div className="flex justify-center gap-4">
          <AnimatedButton
            onClick={() => window.location.href = '/dashboard'}
            className="bg-primary-500 text-white px-6 py-3 rounded-lg"
          >
            ابدأ الآن | Get Started
          </AnimatedButton>
        </div>
      </main>
    </motion.div>
  );
}
	
