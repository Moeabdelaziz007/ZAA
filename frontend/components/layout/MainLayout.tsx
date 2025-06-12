import { ReactNode } from 'react';
import { ThemeProvider } from 'next-themes';
import { theme } from '../../styles/theme';
import { motion, AnimatePresence } from 'framer-motion';
import { ThemeToggle } from '../common/ThemeToggle';

interface MainLayoutProps {
  children: ReactNode;
}

export const MainLayout = ({ children }: MainLayoutProps) => {
  return (
    <ThemeProvider {...theme}>
      <div className="min-h-screen bg-white dark:bg-dark-bg text-gray-900 dark:text-dark-text transition-colors duration-200">
        <header className="sticky top-0 z-50 bg-white/80 dark:bg-dark-card/80 backdrop-blur-sm border-b border-gray-200 dark:border-gray-700">
          <nav className="container mx-auto px-4 py-4 flex items-center justify-between">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="text-2xl font-bold text-primary-600 dark:text-primary-400"
            >
              Zentix AI
            </motion.div>
            <div className="flex items-center space-x-4">
              <ThemeToggle />
            </div>
          </nav>
        </header>

        <main className="container mx-auto px-4 py-8">
          <AnimatePresence mode="wait">
            <motion.div
              key="page-content"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              {children}
            </motion.div>
          </AnimatePresence>
        </main>

        <footer className="bg-gray-50 dark:bg-dark-card border-t border-gray-200 dark:border-gray-700">
          <div className="container mx-auto px-4 py-8">
            <div className="text-center text-gray-600 dark:text-gray-400">
              © {new Date().getFullYear()} Zentix AI. All rights reserved.
            </div>
          </div>
        </footer>
      </div>
    </ThemeProvider>
  );
}; 