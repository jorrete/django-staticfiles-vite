import { defineConfig } from 'vite';
import preact from '@preact/preset-vite';

export default defineConfig({
  plugins: [
    preact(),
  ],
  build: {
    minify: false,
  },
  esbuild: {
    drop: ['console', 'debugger'],
  },
});
