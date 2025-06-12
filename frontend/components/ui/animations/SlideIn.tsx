"use client";
import { motion } from "framer-motion";
import React from "react";

interface SlideInProps {
  children: React.ReactNode;
  from?: "left" | "right" | "top" | "bottom";
  duration?: number;
}

export const SlideIn = ({ children, from = "left", duration = 0.5 }: SlideInProps) => {
  const variants: Record<string, any> = {
    left: { x: -50, opacity: 0 },
    right: { x: 50, opacity: 0 },
    top: { y: -50, opacity: 0 },
    bottom: { y: 50, opacity: 0 },
  };
  return (
    <motion.div
      initial={variants[from]}
      animate={{ x: 0, y: 0, opacity: 1 }}
      transition={{ duration }}
    >
      {children}
    </motion.div>
  );
};

export default SlideIn;
