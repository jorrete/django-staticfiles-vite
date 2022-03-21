const djangoStatic = require('./plugin-django-static');
const postcssImport = require('postcss-import');
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
} = JSON.parse(process.argv[2] || '{}');

const config = require(configPath);

(async () => {
  await build(defineConfig({
    configFile: false,
    envFile: false,
    root: process.cwd(),
    css: {
      postcss: {
        import: {
          path: paths,
        },
        plugins: [
          ...(config?.css?.postcss?.plugins || []),
        ]
      }
    },
    plugins: [
      djangoStatic({
        paths,
        extensions,
      }),
      ...(config?.plugins || []),
    ],
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
  }));
})()
