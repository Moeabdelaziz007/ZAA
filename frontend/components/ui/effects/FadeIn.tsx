import { motion } from 'framer-motion';
import { HTMLAttributes } from 'react';
import { twMerge } from 'tailwind-merge';

interface FadeInProps extends HTMLAttributes<HTMLDivElement> {
  duration?: number;
}

export const FadeIn = ({ children, duration = 0.5, className, ...props }: FadeInProps) => (
  <motion.div
    initial={{ opacity: 0 }}
    animate={{ opacity: 1 }}
    transition={{ duration }}
    className={twMerge(className)}
    {...props}
  >
    {children}
  </motion.div>
);
