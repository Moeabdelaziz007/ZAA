import { motion } from 'framer-motion';
import { HTMLAttributes } from 'react';
import { twMerge } from 'tailwind-merge';

interface SlideInProps extends HTMLAttributes<HTMLDivElement> {
  offset?: number;
  duration?: number;
}

export const SlideIn = ({
  children,
  offset = 20,
  duration = 0.5,
  className,
  ...props
}: SlideInProps) => (
  <motion.div
    initial={{ opacity: 0, y: offset }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration }}
    className={twMerge(className)}
    {...props}
  >
    {children}
  </motion.div>
);
