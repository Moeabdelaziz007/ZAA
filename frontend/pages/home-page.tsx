/**
 * @component HomePage
 * @author محمد عبدالعزيز (Amrikyy)
 * @description Main landing page component that displays the home screen with featured properties and services
 * @description_ar مكون الصفحة الرئيسية الذي يعرض الشاشة الرئيسية مع العقارات والخدمات المميزة
 * @props None
 */

import { motion } from "framer-motion";

const HomePage = () => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="container mx-auto px-4 py-8"
    >
      <h1 className="text-3xl font-bold mb-6">الصفحة الرئيسية</h1>
      <p className="text-gray-600">هذه الصفحة قيد التطوير</p>
    </motion.div>
  );
};

export default HomePage; 