import path from 'path';
/** @type {import('next').NextConfig} */
const nextConfig = {
    // Enable static optimization
    reactStrictMode: true,
    swcMinify: true,

    // Image optimization
    images: {
        domains: ['localhost'],
        formats: ['image/avif', 'image/webp'],
        deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
        imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
    },

    // Compression
    compress: true,

    // Cache control
    async headers() {
        return [
            {
                source: '/static/:path*',
                headers: [
                    {
                        key: 'Cache-Control',
                        value: 'public, max-age=31536000, immutable',
                    },
                ],
            },
            {
                source: '/api/:path*',
                headers: [
                    {
                        key: 'Cache-Control',
                        value: 'no-cache, no-store, must-revalidate',
                    },
                ],
            },
        ];
    },

    // Experimental features
    experimental: {
        optimizeCss: true,
        optimizePackageImports: ['@mui/material', '@mui/icons-material'],
        serverActions: true,
        serverComponentsExternalPackages: ['sharp'],
    },

    // Webpack optimization
    webpack: (config, { dev, isServer }) => {
        // Production optimizations
        if (!dev && !isServer) {
            config.optimization.splitChunks = {
                chunks: 'all',
                minSize: 20000,
                maxSize: 244000,
                minChunks: 1,
                maxAsyncRequests: 30,
                maxInitialRequests: 30,
                cacheGroups: {
                    defaultVendors: {
                        test: /[\\/]node_modules[\\/]/,
                        priority: -10,
                        reuseExistingChunk: true,
                    },
                    default: {
                        minChunks: 2,
                        priority: -20,
                        reuseExistingChunk: true,
                    },
                },
            };
        }
        return config;
    },

    // Environment variables
    env: {
        API_URL: process.env.API_URL,
        WS_URL: process.env.WS_URL,
    },

    // PWA support
    pwa: {
        dest: 'public',
        register: true,
        skipWaiting: true,
    },

    // Build optimization
    poweredByHeader: false,
    generateEtags: true,
    onDemandEntries: {
        maxInactiveAge: 25 * 1000,
        pagesBufferLength: 2,
    },

    // WebSocket configuration
    async rewrites() {
        return [
            {
                source: '/ws',
                destination: process.env.WS_URL,
            },
        ];
    },

    // AI request optimization
    async redirects() {
        return [
            {
                source: '/api/ai/:path*',
                destination: `${process.env.API_URL}/api/ai/:path*`,
                permanent: true,
            },
        ];
    },
};
export default nextConfig;
