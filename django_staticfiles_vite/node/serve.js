#!/usr/bin/env node
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
  extraAllowedPaths,
} = JSON.parse(process.argv[2] || '{}');

const config = require(configPath);

(async () => {
  const server = await createServer(defineConfig({
    appType: 'custom',
    configFile: false,
    envFile: false,
    plugins: [
      {
        ...djangoStatic({
          baseUrl,
          paths,
          extensions,
        }),
        enforce: 'pre',
      },
      ...(config?.plugins || []),
    ],
    css: {
      postcss: {
        plugins: [
          ...(config?.css?.postcss?.plugins || []),
        ]
      }
    },
    esbuild: {
      logOverride: { 'this-is-undefined-in-esm': 'silent' }
    },
    clearScreen: false,
    base,
    root,
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
          nodeModulesPath,
          ...extraAllowedPaths,
        ]
      }
    },
  }));
  await server.listen()
  server.printUrls()
})()
