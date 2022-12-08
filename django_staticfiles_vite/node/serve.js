#!/usr/bin/env node
const { resolve } = require('path');
const { defineConfig, createServer, mergeConfig, loadConfigFromFile } = require('vite');
const djangoStatic = require('./plugin-django-static');
const replace = require("postcss-replace");
const { STATIC_TOKEN } = require('./utils');

const {
  paths,
  base,
  port,
} = JSON.parse(process.argv[2] || '{}');

(async () => {
  const finalConfig = mergeConfig(
    (await loadConfigFromFile())?.config,
    {
      configFile: false,
      envFile: false,
      css: {
        postcss: {
          plugins: [
            replace({
              pattern: /(url\(["\']?)/,
              data: {
                replaceAll: `$1http://localhost:${port}`,
              },
            }),
          ],
        },
      },
      plugins: [
        {
          ...djangoStatic({
            base,
            paths,
            command: 'serve',
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
            ...paths.map(([alias, path]) => path),
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
