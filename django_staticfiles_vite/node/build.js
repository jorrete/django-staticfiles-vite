#!/usr/bin/env node
const djangoStatic = require('./plugin-django-static');
const { build, defineConfig, mergeConfig, loadConfigFromFile } = require('vite');

const {
  entry,
  filename,
  format,
  name,
  outDir,
  paths,
  cssExtensions,
  jsExtensions,
  base,
} = JSON.parse(process.argv[2] || '{}');

(async () => {
  const finalConfig = mergeConfig(
    (await loadConfigFromFile())?.config,
    {
      appType: 'custom',
      configFile: false,
      envFile: false,
      root: process.cwd(),
      resolve: {
        extensions: jsExtensions,
      },
      plugins: [
        {
          ...djangoStatic({
            base,
            paths,
            extensions: [].concat(jsExtensions, cssExtensions),
          }),
          enforce: 'pre',
        },
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
    },
  );

  await build(defineConfig(finalConfig));
})()
