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
    // use instead of plugins
    // resolve: {
    //   alias: {
    //     'my_app': '/home/jorro/tmp/css/my_app',
    //     'modules': resolve(__dirname, 'src/modules'),
    //   },
    // },
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
