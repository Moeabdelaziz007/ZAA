/**
 * @component Footer
 * @author محمد عبدالعزيز (Amrikyy)
 * @description Global footer component that appears on all pages providing branding and copyright
 * @description_ar مكون التذييل العام الذي يظهر في جميع الصفحات لعرض العلامة التجارية وحقوق النشر
 * @props None
 */

import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-background border-t border-border text-center text-sm text-muted-foreground py-4">
      <p>© 2024 Zentix AI – Powered by ZAA Platform</p>
    </footer>
  );
};

export default Footer;
export { Footer };