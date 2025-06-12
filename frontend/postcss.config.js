/**
 * File: postcss.config.js
 * المؤلف: محمد عبدالعزيز (Amrikyy)
 * 
 * Description (EN): PostCSS configuration with optimizations for CSS processing.
 * الوصف (ع): إعدادات PostCSS مع تحسينات لمعالجة CSS.
 */

module.exports = {
  plugins: {
    'tailwindcss': {},
    'autoprefixer': {},
    'postcss-preset-env': {
      features: {
        'nesting-rules': true,
      },
    },
    'cssnano': process.env.NODE_ENV === 'production' ? {
      preset: ['default', {
        discardComments: {
          removeAll: true,
        },
        normalizeWhitespace: true,
        minifyFontValues: true,
        minifyGradients: true,
      }],
    } : false,
  },
}; 