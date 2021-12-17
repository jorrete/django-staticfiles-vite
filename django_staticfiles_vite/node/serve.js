const postcssImport = require('postcss-import');
const { createServer, defineConfig } = require('vite');
const djangoStatic = require('./plugin-django-static');

const {
  paths,
  base,
  root,
  nodeModulesPath,
  extensions,
  configPath,
  port,
} = JSON.parse(process.argv[2] || '{}');

const config = require(configPath);

(async () => {
  const server = await createServer(defineConfig({
    configFile: false,
    envFile: false,
    plugins: [
      djangoStatic({
        paths,
        extensions,
      }),
      ...(config?.plugins || []),
    ],
    css: {
      postcss: {
        plugins: [
          postcssImport({
            path: paths,
          }),
          ...(config?.css?.postcss?.plugins || []),
        ]
      }
    },
    clearScreen: false,
    base,
    root,
    server: {
      port,
      fs: {
        strict: true,
        allow: [
          ...paths,
          nodeModulesPath,
        ]
      }
    },
  }));
  await server.listen()
  server.printUrls()
})()

