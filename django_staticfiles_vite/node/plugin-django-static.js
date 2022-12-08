const vite = require('vite');
const { resolveId, extensions, STATIC_TOKEN } = require('./utils');

function djangoStatic({
  addDependicies,
  base,
  command,
  paths,
}) {
  const findStaticAliasBuild = new RegExp(`^${STATIC_TOKEN}(?!.*\.(${extensions.join('|')}))`)
  const findStaticAliasServe = new RegExp(`^${STATIC_TOKEN}(.*)`);
  const findStaticBaseServe = new RegExp(`^${base}(.*)`);

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
            find: command === 'build' ? findStaticAliasBuild : findStaticAliasServe,
            replacement: '/$1',
            async customResolver(id, importer) {
              const match = await resolveId.call(this, id, paths);

              if (match) {
                addDependicies?.([match.id.split('?')[0]]);
                return match;
              }
            },
          },
          command === 'serve' ? {
            find: findStaticBaseServe,
            replacement: '/$1',
            async customResolver(id, importer) {
              if (!importer.endsWith('.html')) {
                return null;
              }

              return await resolveId.call(this, id, paths);
            },
          } : null,
        ].filter(Boolean),
      }
    }),
    handleHotUpdate(ctx) {
      if (ctx.file.endsWith('.html')) {
        ctx.server.ws.send({ type: 'full-reload' });
        return []
      }
    },
    buildEnd() {
      addDependicies?.(Array.from(this.getModuleIds())
        .filter((path) => {
          return (
            !path.includes('node_modules')
              && path[0] === '/'
          )
        })
        .map((path) => {
          return path.split('?')[0].replace('\x00', '')
        }));
    },
  }
}

module.exports = djangoStatic;
