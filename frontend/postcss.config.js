// Skip PostCSS plugins in test environment
if (process.env.NODE_ENV === 'test' || process.env.VITEST) {
  module.exports = {
    plugins: {},
  }
} else {
  module.exports = {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  }
}
