/**
 * @component MobileNav
 * @author محمد عبدالعزيز (Amrikyy)
 * @description Mobile navigation component for handling sidebar or menu on small screens
 * @description_ar مكون التنقل للهواتف لإدارة الشريط الجانبي أو القائمة في الشاشات الصغيرة
 * @props {children: ReactNode} - Child elements to render inside the nav
 */

import React from 'react';
import { motion } from 'framer-motion';

const MobileNav = ({ children }: { children: React.ReactNode }) => {
  return (
    <motion.nav
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="fixed bottom-0 left-0 right-0 bg-background shadow-md md:hidden"
    >
      <div className="flex justify-around p-4">
        {children}
      </div>
    </motion.nav>
  );
};

export default MobileNav; 