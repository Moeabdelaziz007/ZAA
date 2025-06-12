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
        serverComponentsExternalPackages: ['sharp'],
    },

    // Webpack optimization
    webpack: (config, { dev, isServer }) => {
        if (!dev && !isServer) {
            config.optimization.splitChunks = {
                chunks: 'all',
                minSize: 15000,
                maxSize: 200000,
                minChunks: 1,
                maxAsyncRequests: 50,
                maxInitialRequests: 30,
                cacheGroups: {
                    vendors: {
                        test: /[\\/]node_modules[\\/]/,
                        name(module) {
                            const packageName = module.context.match(/[\\/]node_modules[\\/](.*?)([\\/]|$)/)[1];
                            return `vendor.${packageName.replace('@', '')}`;
                        },
                        priority: 20,
                    },
                    common: {
                        minChunks: 2,
                        priority: 10,
                        reuseExistingChunk: true,
                    },
                    styles: {
                        name: 'styles',
                        test: /\.(css|scss)$/,
                        chunks: 'all',
                        enforce: true,
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
                destination: 'http://localhost:8000/ws',
            },
        ];
    },

    // AI request optimization
    async redirects() {
        return [
            {
                source: '/api/ai/:path*',
                destination: 'http://localhost:8000/api/ai/:path*',
                permanent: true,
            },
        ];
    },
};

