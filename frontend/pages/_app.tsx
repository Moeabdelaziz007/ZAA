/**
 * Component: App
 * المؤلف: محمد عبدالعزيز (Amrikyy)
 * 
 * Description (EN): Root application component with theme provider and page transitions.
 * الوصف (ع): مكون التطبيق الرئيسي مع مزود الثيم وانتقالات الصفحات.
 * 
 * Props:
 * - Component: NextComponentType   // مكون الصفحة الحالية
 * - pageProps: any                 // خصائص الصفحة
 */
import type { AppProps } from 'next/app';
import { AnimatePresence } from 'framer-motion';
import { ThemeProvider } from '../contexts/ThemeContext';
import '../styles/globals.css';

export default function App({ Component, pageProps, router }: AppProps) {
  return (
    <ThemeProvider>
      <AnimatePresence mode="wait">
        <Component key={router.route} {...pageProps} />
      </AnimatePresence>
    </ThemeProvider>
  );
} 