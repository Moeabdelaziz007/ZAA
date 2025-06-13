/**
 * Next.js Configuration
 * المؤلف: محمد عبدالعزيز (Amrikyy)
 * 
 * Description (EN): Next.js configuration with performance optimizations
 * الوصف (ع): تكوين Next.js مع تحسينات الأداء
 */

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: ['images.unsplash.com'],
    formats: ['image/avif', 'image/webp'],
  },
  compress: true,
  swcMinify: true,
};

module.exports = nextConfig;