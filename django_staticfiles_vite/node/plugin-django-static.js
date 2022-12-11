const { resolveId, excludeExtCSS, hasExtension, STATIC_TOKEN, isCSS } = require('./utils');

function djangoStatic ({
  addDependicies,
  base,
  command,
  paths
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
