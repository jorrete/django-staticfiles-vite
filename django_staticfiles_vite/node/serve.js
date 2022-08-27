const { resolve } = require('path');
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
  baseUrl,
} = JSON.parse(process.argv[2] || '{}');

const config = require(configPath);

(async () => {
  const server = await createServer(defineConfig({
    appType: 'custom',
    configFile: false,
    envFile: false,
    plugins: [
      djangoStatic({
        baseUrl,
        paths,
        extensions,
      }),
      ...(config?.plugins || []),
    ],
    css: {
      postcss: {
        plugins: [
          ...(config?.css?.postcss?.plugins || []),
        ]
      }
    },
    clearScreen: false,
    base,
    root,
    server: {
      port,
      hmr: {
        host: 'localhost',
        port,
      },
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
