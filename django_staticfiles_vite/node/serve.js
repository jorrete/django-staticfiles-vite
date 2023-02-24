/* eslint-disable node/no-missing-require */
const { resolve } = require('path');
const { createServer } = require('vite');
const djangoStatic = require('./plugin-django-static');
const replace = require('postcss-replace');

const {
  paths,
  testPaths,
  base,
  port,
  context,
} = JSON.parse(process.argv[2] || '{}');

(async () => {
  console.log(context);
  const server = await createServer({
    envFile: false,
    css: {
      postcss: {
        plugins: [
          replace({
            pattern: /(url\(["']?)/,
            data: {
              replaceAll: `$1http://localhost:${port}`
            }
          })
        ]
      }
    },
    plugins: [
      {
        ...djangoStatic({
          context,
          base,
          paths,
          testPaths,
          command: 'serve'
        }),
        enforce: 'pre'
      }
    ],
    server: {
      cors: true,
      host: true,
      port,
      hmr: {
        host: 'localhost',
        port
      },
      fs: {
        strict: true,
        allow: [
          ...[].concat(testPaths, paths).map(([, path]) => path),
          resolve(process.cwd(), 'node_modules')
        ]
      }
    }
  });

  await server.listen();
  server.printUrls();
})();
