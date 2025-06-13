/**
 * Sentry Configuration
 * المؤلف: محمد عبدالعزيز (Amrikyy)
 * 
 * Description (EN): Sentry configuration for error tracking and monitoring
 * الوصف (ع): تكوين Sentry لتتبع الأخطاء والمراقبة
 */

const { withSentryConfig } = require('@sentry/nextjs');

const sentryWebpackPluginOptions = {
  silent: true,
  org: 'zentix',
  project: 'frontend',
  authToken: process.env.SENTRY_AUTH_TOKEN,
};

const nextConfig = {
  sentry: {
    hideSourceMaps: true,
    widenClientFileUpload: true,
    transpileClientSDK: true,
    tunnelRoute: '/monitoring',
    hideSourceMaps: true,
    disableServerWebpackPlugin: false,
    disableClientWebpackPlugin: false,
  },
};

module.exports = withSentryConfig(nextConfig, sentryWebpackPluginOptions); 