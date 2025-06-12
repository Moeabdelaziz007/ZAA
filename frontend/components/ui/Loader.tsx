import { motion } from 'framer-motion';
import { twMerge } from 'tailwind-merge';

interface LoaderProps {
  size?: 'sm' | 'md' | 'lg';
  color?: 'primary' | 'white';
  className?: string;
  text?: string;
}

const sizeClasses = {
  sm: 'h-4 w-4',
  md: 'h-8 w-8',
  lg: 'h-12 w-12',
};

const colorClasses = {
  primary: 'text-primary-600 dark:text-primary-400',
  white: 'text-white',
};

export const Loader = ({
  size = 'md',
  color = 'primary',
  className,
  text,
}: LoaderProps) => {
  return (
    <div className="flex flex-col items-center justify-center">
      <motion.div
        animate={{
          rotate: 360,
        }}
        transition={{
          duration: 1,
          repeat: Infinity,
          ease: 'linear',
        }}
        className={twMerge(
          'relative',
          sizeClasses[size],
          className
        )}
      >
        <div
          className={twMerge(
            'absolute inset-0 rounded-full border-2 border-current border-t-transparent',
            colorClasses[color]
          )}
        />
      </motion.div>
      {text && (
        <motion.p
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-2 text-sm text-gray-600 dark:text-gray-400"
        >
          {text}
        </motion.p>
      )}
    </div>
  );
};

export const PageLoader = () => {
  return (
    <div className="flex min-h-screen items-center justify-center">
      <Loader size="lg" text="جاري التحميل..." />
    </div>
  );
};

export const ButtonLoader = () => {
  return (
    <div className="flex items-center justify-center">
      <Loader size="sm" color="white" />
    </div>
  );
}; 