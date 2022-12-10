#!/usr/bin/env node
const { resolve } = require('path');
const { createServer } = require('vite');
const djangoStatic = require('./plugin-django-static');
const { STATIC_TOKEN } = require('./utils');
const replace = require("postcss-replace");

const {
  paths,
  base,
  port,
} = JSON.parse(process.argv[2] || '{}');

(async () => {
  const server = await createServer({
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
  });

  await server.listen();
  server.printUrls();
})()
