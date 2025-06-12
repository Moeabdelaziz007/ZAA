import React from 'react';
import { LucideIcon } from 'lucide-react';

interface IconButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  icon: LucideIcon;
  label: string;
  variant?: 'primary' | 'secondary' | 'danger';
}

const variants: Record<string, string> = {
  primary: 'bg-purple-600 hover:bg-purple-700 text-white',
  secondary: 'bg-gray-700 hover:bg-gray-600 text-white',
  danger: 'bg-red-600 hover:bg-red-700 text-white',
};

export const IconButton = React.forwardRef<HTMLButtonElement, IconButtonProps>(
  ({ icon: Icon, label, variant = 'primary', className = '', ...props }, ref) => (
    <button
      ref={ref}
      className={`
        inline-flex items-center gap-2 px-4 py-2 rounded-lg shadow-lg
        transition-transform duration-200 hover:-translate-y-0.5 active:translate-y-0
        focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500
        ${variants[variant]} ${className}
      `}
      {...props}
    >
      <Icon className="w-4 h-4" />
      <span className="text-sm font-medium">{label}</span>
    </button>
  )
);

IconButton.displayName = 'IconButton'; 