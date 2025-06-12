/**
 * Component: Footer
 * المؤلف: محمد عبدالعزيز (Amrikyy)
 * 
 * Description (EN): A simple footer component displaying the branding 'Powered by Zentix.AI' at the bottom of every page.
 * الوصف (ع): مكون تذييل بسيط يعرض العلامة التجارية 'Powered by Zentix.AI' في أسفل كل صفحة.
 * 
 * Props:
 * - None
 */
import React from 'react';

const Footer: React.FC = () => (
  <footer className="w-full py-4 text-center bg-transparent">
    <span className="text-sm font-bold" style={{ color: 'var(--accent)' }}>
      Powered by Zentix.AI 🚀
    </span>
  </footer>
);

export default Footer; 