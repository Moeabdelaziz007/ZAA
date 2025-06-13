/**
 * @component MessagesPage
 * @author محمد عبدالعزيز (Amrikyy)
 * @description Messages and notifications center for user communications
 * @description_ar مركز الرسائل والإشعارات للتواصل بين المستخدمين
 * @props None
 */

import { motion } from "framer-motion";

const MessagesPage = () => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="container mx-auto px-4 py-8"
    >
      <h1 className="text-3xl font-bold mb-6">الرسائل</h1>
      <p className="text-gray-600">هذه الصفحة قيد التطوير</p>
    </motion.div>
  );
};

export default MessagesPage;