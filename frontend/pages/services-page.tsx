/**
 * @component ServicesPage
 * @author محمد عبدالعزيز (Amrikyy)
 * @description Available services and features page
 * @description_ar صفحة الخدمات والميزات المتاحة
 * @props None
 */

import { motion } from "framer-motion";

const ServicesPage = () => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="container mx-auto px-4 py-8"
    >
      <h1 className="text-3xl font-bold mb-6">الخدمات</h1>
      <p className="text-gray-600">هذه الصفحة قيد التطوير</p>
    </motion.div>
  );
};

export default ServicesPage; 