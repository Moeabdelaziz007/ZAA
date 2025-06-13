/**
 * @component PointsPage
 * @author محمد عبدالعزيز (Amrikyy)
 * @description User points and rewards management page
 * @description_ar صفحة إدارة نقاط المستخدم والمكافآت
 * @props None
 */

import { motion } from "framer-motion";

const PointsPage = () => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="container mx-auto px-4 py-8"
    >
      <h1 className="text-3xl font-bold mb-6">النقاط والمكافآت</h1>
      <p className="text-gray-600">هذه الصفحة قيد التطوير</p>
    </motion.div>
  );
};

export default PointsPage; 