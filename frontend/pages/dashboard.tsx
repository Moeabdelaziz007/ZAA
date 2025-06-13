/**
 * File: dashboard.tsx
 * المؤلف: محمد عبدالعزيز (Amrikyy)
 * 
 * Description (EN): Dashboard page with AI analytics and insights.
 * الوصف (ع): صفحة لوحة التحكم مع تحليلات الذكاء الاصطناعي والرؤى.
 */

import { motion } from 'framer-motion';
import { AnimatedButton } from '../components/ui/AnimatedButton';
import { LoadingIndicator } from '../components/StaticComponent';

export default function Dashboard() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="min-h-screen bg-gray-50 dark:bg-gray-900"
    >
      <main className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-8 text-gray-900 dark:text-white">
          لوحة التحكم | Dashboard
        </h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Analytics Cards */}
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-lg"
          >
            <h2 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">
              التحليلات | Analytics
            </h2>
            <LoadingIndicator size="medium" />
          </motion.div>

          {/* AI Insights */}
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 0.1 }}
            className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-lg"
          >
            <h2 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">
              رؤى الذكاء الاصطناعي | AI Insights
            </h2>
            <LoadingIndicator size="medium" />
          </motion.div>

          {/* Performance Metrics */}
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-lg"
          >
            <h2 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">
              مؤشرات الأداء | Performance
            </h2>
            <LoadingIndicator size="medium" />
          </motion.div>
        </div>
      </main>
    </motion.div>
  );
} 