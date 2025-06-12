"use client";
import { motion } from "framer-motion";
import React from "react";

interface FadeInProps {
  children: React.ReactNode;
  duration?: number;
}

export const FadeIn = ({ children, duration = 0.5 }: FadeInProps) => (
  <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration }}>
    {children}
  </motion.div>
);

export default FadeIn;
