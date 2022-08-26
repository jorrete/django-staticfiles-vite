const djangoStatic = require('./plugin-django-static');
const { build, defineConfig } = require('vite');

const {
  entry,
  filename,
  format,
  name,
  outDir,
  paths,
  extensions,
  configPath,
  baseUrl,
} = JSON.parse(process.argv[2] || '{}');

const config = require(configPath);

(async () => {
  await build(defineConfig({
    configFile: false,
    envFile: false,
    root: process.cwd(),
    css: {
      postcss: {
        plugins: [
          ...(config?.css?.postcss?.plugins || []),
        ]
      }
    },
    plugins: [
      djangoStatic({
        baseUrl,
        paths,
        extensions,
      }),
      ...(config?.plugins || []),
    ],
    // TODO mangling
    build: {
      emptyOutDir: false,
      outDir,
      rollupOptions: {
        output: {
          assetFileNames: () => `${name}.js.css`,
        },
      },
      lib: {
        entry,
        formats: [format],
        name,
        fileName: () => filename,
      },
    },
    minify: true,
    esbuild: {
      drop: ['console', 'debugger'],
    },
  }));
})()
