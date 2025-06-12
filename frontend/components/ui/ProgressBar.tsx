import { motion } from 'framer-motion';
import { twMerge } from 'tailwind-merge';

interface ProgressBarProps {
  value: number;
  max?: number;
  showLabel?: boolean;
  size?: 'sm' | 'md' | 'lg';
  color?: 'primary' | 'success' | 'warning' | 'error';
  className?: string;
}

export const ProgressBar = ({
  value,
  max = 100,
  showLabel = true,
  size = 'md',
  color = 'primary',
  className,
}: ProgressBarProps) => {
  const percentage = Math.min(100, Math.max(0, (value / max) * 100));

  const sizes = {
    sm: 'h-1',
    md: 'h-2',
    lg: 'h-3',
  };

  const colors = {
    primary: 'bg-primary-600 dark:bg-primary-500',
    success: 'bg-green-600 dark:bg-green-500',
    warning: 'bg-yellow-600 dark:bg-yellow-500',
    error: 'bg-red-600 dark:bg-red-500',
  };

  return (
    <div className={twMerge('w-full', className)}>
      {showLabel && (
        <div className="mb-1 flex items-center justify-between">
          <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
            التقدم
          </span>
          <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
            {percentage.toFixed(0)}%
          </span>
        </div>
      )}
      <div
        className={twMerge(
          'w-full overflow-hidden rounded-full bg-gray-200 dark:bg-gray-700',
          sizes[size]
        )}
      >
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
          className={twMerge(
            'h-full rounded-full transition-colors',
            colors[color]
          )}
        />
      </div>
    </div>
  );
}; 