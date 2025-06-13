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

if (process.env.NODE_ENV === 'production' && !process.env.NEXT_PUBLIC_API_URL) {
  throw new Error('NEXT_PUBLIC_API_URL is required for production builds');
}

module.exports = nextConfig;
