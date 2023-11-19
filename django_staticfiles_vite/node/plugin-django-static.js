import {
  STATIC_TOKEN,
  excludeExtCSS,
  hasExtension,
  isCSS,
  resolveId,
  resolveStatic,
} from './utils.js';

export default function djangoStatic ({
  base,
  command,
  paths,
  testPaths = [],
  context = {},
}) {
  let config;

  return {
    context,
    name: 'django-static',
    config: () => ({
      publicDir: false,
      clearScreen: false,
      appType: 'custom', // don't include html middlewares
      resolve: {
        alias: [
          {
            find: new RegExp('^(?:/[\\w_-]+/tests/)(.*)'),
            replacement: '$1',
            async customResolver (id) {
              const match = await resolveId.call(this, id, testPaths);

              if (match) {
                return match;
              }
            }
          },
          {
            find: new RegExp(`^(?:${STATIC_TOKEN}|${base})(.*)`),
            replacement: '$1',
            async customResolver (id, importer) {
              if (id.startsWith('/')) {
                return null;
              }

              if (command === 'build') {
                if (isCSS(importer)) {
                  if (hasExtension(id, excludeExtCSS)) {
                    return null;
                  }
                }
              }

              const match = await resolveId.call(this, id, paths);

              if (match) {
                return match;
              }
            }
          }
        ]
      }
    }),
    configResolved(resolvedConfig) {
      config = resolvedConfig;
    },
    configureServer(server) {
      const check = new RegExp(`^(?:${STATIC_TOKEN}|${base})(.*)`);

      return () => {
        server.middlewares.use((req, res, next) => {
          if (check.test(req.url)) {
            res.end(
              resolveStatic(
                req.url.replace(STATIC_TOKEN, '').replace(base, ''),
                paths,
              ),
            );
          }

          return next();
        });
      };
    },
    resolveId(id) {
      if (id === 'qunit') {
        return id;
      }

      if (id === '@context') {
        return id;
      }
    },
    load(id) {
      if (id === 'qunit') {
        return `
          import '/node_modules/qunit/qunit/qunit.js'

          window.QUnit.done((result) => {
            window.qunitResult = result;
            if (window._qunitDone) {
              window._qunitDone(result);
            }
          });

          window.qunitDone = (callback) => {
            if (window.qunitResult) {
              callback(window.qunitResult);
              return;
            }

            window._qunitDone = callback;
          };

          export default window.QUnit;
        `;
      }

      if (id === '@context') {
        const name = 'context';
        return `
        const ${name} = Object.freeze(${JSON.stringify(context)});
        ${config.command === 'serve' ? `console.log('[${name}]', ${name});` : ''}
        export default ${name};
        `;
      }
    },
    transform(src, id) {
      if (id.endsWith('?qunit')) {
        return `
        import 'qunit/qunit/qunit.css';
        ${src}
        `;
      }

      return src.replace(new RegExp(`["']${STATIC_TOKEN}([\\w/.-]+)["']`, 'gm'), `"${base}$1"`);
    },
    handleHotUpdate (ctx) {
      if (ctx.file.endsWith('.html')) {
        ctx.server.ws.send({ type: 'full-reload' });
        return [];
      }
    },
  };
}
