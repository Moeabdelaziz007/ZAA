import { Fragment } from 'react';
import { Menu, Transition } from '@headlessui/react';
import { motion } from 'framer-motion';
import {
  UserCircleIcon,
  CogIcon,
  MoonIcon,
  SunIcon,
  LogoutIcon,
} from '@heroicons/react/outline';
import { twMerge } from 'tailwind-merge';
import Image from 'next/image';
import { useTheme } from 'next-themes';

interface UserAvatarProps {
  user: {
    name: string;
    email: string;
    avatar?: string;
  };
  onLogout: () => void;
  className?: string;
}

export const UserAvatar = ({
  user,
  onLogout,
  className,
}: UserAvatarProps) => {
  const { theme, setTheme } = useTheme();

  const menuItems = [
    {
      label: 'الملف الشخصي',
      icon: UserCircleIcon,
      onClick: () => {},
    },
    {
      label: 'الإعدادات',
      icon: CogIcon,
      onClick: () => {},
    },
    {
      label: theme === 'dark' ? 'الوضع الفاتح' : 'الوضع الداكن',
      icon: theme === 'dark' ? SunIcon : MoonIcon,
      onClick: () => setTheme(theme === 'dark' ? 'light' : 'dark'),
    },
    {
      label: 'تسجيل الخروج',
      icon: LogoutIcon,
      onClick: onLogout,
    },
  ];

  return (
    <Menu as="div" className="relative">
      <Menu.Button
        className={twMerge(
          'flex items-center space-x-3 rounded-full focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800',
          className
        )}
      >
        {user.avatar ? (
          <Image
            src={user.avatar}
            alt={user.name}
            width={40}
            height={40}
            className="rounded-full"
          />
        ) : (
          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary-100 text-primary-600 dark:bg-primary-900 dark:text-primary-400">
            <UserCircleIcon className="h-6 w-6" />
          </div>
        )}
      </Menu.Button>

      <Transition
        as={Fragment}
        enter="transition ease-out duration-100"
        enterFrom="transform opacity-0 scale-95"
        enterTo="transform opacity-100 scale-100"
        leave="transition ease-in duration-75"
        leaveFrom="transform opacity-100 scale-100"
        leaveTo="transform opacity-0 scale-95"
      >
        <Menu.Items className="absolute left-0 mt-2 w-56 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none dark:bg-gray-800">
          <div className="px-4 py-2">
            <p className="text-sm font-medium text-gray-900 dark:text-white">
              {user.name}
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-400">
              {user.email}
            </p>
          </div>

          <div className="my-1 border-t border-gray-100 dark:border-gray-700" />

          {menuItems.map((item) => (
            <Menu.Item key={item.label}>
              {({ active }) => (
                <motion.button
                  whileHover={{ x: 5 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={item.onClick}
                  className={twMerge(
                    'flex w-full items-center px-4 py-2 text-sm',
                    active
                      ? 'bg-gray-100 text-gray-900 dark:bg-gray-700 dark:text-white'
                      : 'text-gray-700 dark:text-gray-300'
                  )}
                >
                  <item.icon className="ml-3 h-5 w-5" />
                  {item.label}
                </motion.button>
              )}
            </Menu.Item>
          ))}
        </Menu.Items>
      </Transition>
    </Menu>
  );
}; 