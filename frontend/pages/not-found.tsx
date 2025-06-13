/**
 * Page: NotFound
 * Author: محمد عبدالعزيز (Amrikyy)
 * 
 * Description (EN): 404 Not Found page with a clean and modern design
 * الوصف (ع): صفحة 404 غير موجود مع تصميم عصري ونظيف
 */

import React from 'react';
import { motion } from 'framer-motion';
import { useLocation } from 'wouter';

export default function NotFound() {
  const [, setLocation] = useLocation();

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white flex items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center"
      >
        <h1 className="text-9xl font-bold bg-gradient-to-r from-white to-purple-200 bg-clip-text text-transparent">
          404
        </h1>
        <p className="text-2xl mt-4 text-gray-300">
          عذراً، الصفحة غير موجودة
        </p>
        <p className="text-gray-400 mt-2">
          يبدو أن الصفحة التي تبحث عنها غير موجودة أو تم نقلها
        </p>
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => setLocation('/')}
          className="mt-8 px-6 py-3 bg-purple-600 hover:bg-purple-700 rounded-lg text-white font-medium transition-colors"
        >
          العودة للرئيسية
        </motion.button>
      </motion.div>
    </div>
  );
} 