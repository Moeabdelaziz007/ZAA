/**
 * Component: SkipToContent
 * المؤلف: محمد عبدالعزيز (Amrikyy)
 * 
 * Description (EN): Accessibility component that allows keyboard users to skip navigation and jump directly to main content.
 * الوصف (ع): مكون للوصول يسمح لمستخدمي لوحة المفاتيح بتخطي التنقل والانتقال مباشرة إلى المحتوى الرئيسي.
 * 
 * Props:
 * - None
 */
import React from 'react';

const SkipToContent: React.FC = () => (
  <a
    href="#main-content"
    className="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-[var(--accent)] focus:text-white focus:rounded-lg focus:shadow-lg"
  >
    تخطي إلى المحتوى الرئيسي | Skip to main content
  </a>
);

export default SkipToContent; 