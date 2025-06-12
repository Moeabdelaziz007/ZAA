import { motion } from 'framer-motion';
import { useState } from 'react';
import { twMerge } from 'tailwind-merge';
import {
  HomeIcon,
  ChartBarIcon,
  UserGroupIcon,
  CogIcon,
  MenuIcon,
  XIcon,
} from '@heroicons/react/outline';
import Link from 'next/link';
import { useRouter } from 'next/router';

interface SidebarItem {
  name: string;
  href: string;
  icon: React.ComponentType<{ className?: string }>;
}

const sidebarItems: SidebarItem[] = [
  { name: 'الرئيسية', href: '/', icon: HomeIcon },
  { name: 'نظرة عامة', href: '/dashboard/overview', icon: HomeIcon },
  { name: 'التحليلات', href: '/dashboard/analytics', icon: ChartBarIcon },
  { name: 'التوصيات', href: '/recommendations', icon: ChartBarIcon },
  { name: 'المستخدمين', href: '/users', icon: UserGroupIcon },
  { name: 'الإعدادات', href: '/settings', icon: CogIcon },
];

export const Sidebar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const router = useRouter();

  const toggleSidebar = () => setIsOpen(!isOpen);

  return (
    <>
      <button
        onClick={toggleSidebar}
        className="fixed top-4 right-4 z-50 rounded-lg bg-white p-2 shadow-lg dark:bg-gray-800 lg:hidden"
      >
        {isOpen ? (
          <XIcon className="h-6 w-6" />
        ) : (
          <MenuIcon className="h-6 w-6" />
        )}
      </button>

      <motion.div
        initial={false}
        animate={{
          width: isOpen ? '100%' : '0%',
          opacity: isOpen ? 1 : 0,
        }}
        className="fixed inset-y-0 right-0 z-40 w-64 bg-white shadow-lg dark:bg-gray-800 lg:w-64 lg:translate-x-0"
      >
        <div className="flex h-full flex-col">
          <div className="flex h-16 items-center justify-center border-b dark:border-gray-700">
            <h1 className="text-xl font-bold text-primary-600 dark:text-primary-400">
              Zentix AI
            </h1>
          </div>

          <nav className="flex-1 space-y-1 px-2 py-4">
            {sidebarItems.map((item) => {
              const isActive = router.pathname === item.href;
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={twMerge(
                    'group flex items-center rounded-lg px-2 py-2 text-sm font-medium transition-colors',
                    isActive
                      ? 'bg-primary-50 text-primary-600 dark:bg-primary-900/20 dark:text-primary-400'
                      : 'text-gray-600 hover:bg-gray-50 dark:text-gray-300 dark:hover:bg-gray-700/50'
                  )}
                >
                  <item.icon
                    className={twMerge(
                      'mr-3 h-5 w-5',
                      isActive
                        ? 'text-primary-600 dark:text-primary-400'
                        : 'text-gray-400 group-hover:text-gray-500 dark:text-gray-500 dark:group-hover:text-gray-400'
                    )}
                  />
                  {item.name}
                </Link>
              );
            })}
          </nav>

          <div className="border-t p-4 dark:border-gray-700">
            <div className="flex items-center space-x-3">
              <div className="h-8 w-8 rounded-full bg-primary-100 dark:bg-primary-900" />
              <div>
                <p className="text-sm font-medium text-gray-700 dark:text-gray-300">
                  اسم المستخدم
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-400">
                  user@example.com
                </p>
              </div>
            </div>
          </div>
        </div>
      </motion.div>

      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={toggleSidebar}
          className="fixed inset-0 z-30 bg-black/50 lg:hidden"
        />
      )}
    </>
  );
}; 