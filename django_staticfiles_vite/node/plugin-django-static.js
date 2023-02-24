/* eslint-disable no-unexpected-multiline */
const { resolveId, excludeExtCSS, hasExtension, STATIC_TOKEN, isCSS } = require('./utils');

function djangoStatic ({
  addDependicies,
  base,
  command,
  paths,
  testPaths = [],
  context = {},
}) {
  return {
    name: 'django-static',
    config: () => ({
      publicDir: false,
      root: process.cwd(),
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
                addDependicies?.([match.id.split('?')[0]]);
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
                addDependicies?.([match.id.split('?')[0]]);
                return match;
              }
            }
          }
        ]
      }
    }),
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
        return `export default ${JSON.stringify(context)}`;
      }
      if (id === '@context') {
        const name = 'context';
        return `
        const ${name} = Object.freeze(${JSON.stringify(context)});
        console.log('[${name}]', ${name});
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
    },
    handleHotUpdate (ctx) {
      if (ctx.file.endsWith('.html')) {
        ctx.server.ws.send({ type: 'full-reload' });
        return [];
      }
    },
    buildEnd () {
      addDependicies?.(Array.from(this.getModuleIds())
        .filter((path) => {
          return (
            !path.includes('node_modules') &&
              path[0] === '/'
          );
        })
        .map((path) => {
          return path.split('?')[0].replace('\x00', '');
        }));
    }
  };
}

module.exports = djangoStatic;
