#!/usr/bin/env node
const { resolve } = require('path');
const { defineConfig, createServer, mergeConfig, loadConfigFromFile } = require('vite');
const djangoStatic = require('./plugin-django-static');

const {
  paths,
  base,
  cssExtensions,
  jsExtensions,
  port,
} = JSON.parse(process.argv[2] || '{}');

(async () => {
  const finalConfig = mergeConfig(
    (await loadConfigFromFile())?.config,
    {
      base,
      publicDir: false,
      root: process.cwd(),
      clearScreen: false,
      appType: 'custom', // don't include html middlewares
      configFile: false,
      envFile: false,
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
      server: {
        cors: true,
        host: true,
        port,
        hmr: {
          host: 'localhost',
          port,
        },
        fs: {
          strict: true,
          allow: [
            ...paths,
            resolve(process.cwd(), 'node_modules'),
          ]
        }
      },
    },
  );

  const server = await createServer(defineConfig(finalConfig));
  await server.listen()
  server.printUrls()
})()
