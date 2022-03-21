const { defineConfig } = require('vite');
const preact = require('@preact/preset-vite').default;

module.exports = defineConfig({
  plugins: [
    preact(),
  ],
});
