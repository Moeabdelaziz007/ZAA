import { motion } from 'framer-motion';
import { twMerge } from 'tailwind-merge';

type BadgeVariant = 'default' | 'success' | 'warning' | 'error' | 'info';
type BadgeSize = 'sm' | 'md' | 'lg';

interface BadgeProps {
  children: React.ReactNode;
  variant?: BadgeVariant;
  size?: BadgeSize;
  className?: string;
  animated?: boolean;
}

const variants = {
  default: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300',
  success: 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400',
  warning: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400',
  error: 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400',
  info: 'bg-blue-100 text-blue-800 dark:bg-blue-900/20 dark:text-blue-400',
};

const sizes = {
  sm: 'px-2 py-0.5 text-xs',
  md: 'px-2.5 py-0.5 text-sm',
  lg: 'px-3 py-1 text-base',
};

export const Badge = ({
  children,
  variant = 'default',
  size = 'md',
  className,
  animated = false,
}: BadgeProps) => {
  const Component = animated ? motion.span : 'span';

  return (
    <Component
      initial={animated ? { scale: 0.8, opacity: 0 } : undefined}
      animate={animated ? { scale: 1, opacity: 1 } : undefined}
      whileHover={animated ? { scale: 1.05 } : undefined}
      className={twMerge(
        'inline-flex items-center rounded-full font-medium',
        variants[variant],
        sizes[size],
        className
      )}
    >
      {children}
    </Component>
  );
};

// مكونات مساعدة للاستخدام السريع
export const NewBadge = (props: Omit<BadgeProps, 'variant'>) => (
  <Badge variant="info" {...props}>
    جديد
  </Badge>
);

export const RecommendedBadge = (props: Omit<BadgeProps, 'variant'>) => (
  <Badge variant="success" {...props}>
    موصى به
  </Badge>
);

export const TopRatedBadge = (props: Omit<BadgeProps, 'variant'>) => (
  <Badge variant="warning" {...props}>
    الأعلى تقييماً
  </Badge>
);

export const LimitedBadge = (props: Omit<BadgeProps, 'variant'>) => (
  <Badge variant="error" {...props}>
    محدود
  </Badge>
);
