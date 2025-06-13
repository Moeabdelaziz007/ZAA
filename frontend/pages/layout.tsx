/**
 * File: layout.tsx
 * المؤلف: محمد عبدالعزيز (Amrikyy)
 * 
 * Description (EN): Root layout component that wraps all pages with theme provider and animations.
 * الوصف (ع): مكون التخطيط الرئيسي الذي يغلف جميع الصفحات مع مزود السمة والحركات.
 */

import { ThemeProvider } from '../contexts/ThemeContext';
import { AnimatePresence } from 'framer-motion';
import '../styles/animations.css';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ar" dir="rtl">
      <body>
        <ThemeProvider>
          <AnimatePresence mode="wait">
            {children}
          </AnimatePresence>
        </ThemeProvider>
      </body>
    </html>
  );
} 