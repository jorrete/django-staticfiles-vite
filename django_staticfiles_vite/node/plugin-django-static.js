const { readFileSync } = require('fs');
const { resolveId } = require('./utils');

function djangoStatic({ base, paths, extensions, addDependicies }) {
  const find = (
    base.slice(-1) === '/'
      ? base.slice(0, -1)
      : base
  );

  return {
    name: 'django-static',
    config: () => ({
      appType: 'custom',
      resolve: {
        alias: [
          {
            find,
            replacement: '',
            customResolver: (id) => {
              return resolveId(id, paths, extensions)
            },
          }
        ],
      }
    }),
    resolveId(id) {
      return resolveId(id, paths, extensions);
    },
    handleHotUpdate(ctx) {
      if (ctx.file.endsWith('.html')) {
        ctx.server.ws.send({ type: 'full-reload' });
        return []
      }
    },
    configureServer(server) {
      // return a post hook that is called after internal middlewares are
      // installed
      return () => {
        server.middlewares.use((req, res, next) => {
          if (req.originalUrl === base) {
            next();
          } else {
            const path = resolveId(req.url, paths);

            if (!path) {
              next();
            } else {
              res.end(readFileSync(path));
            }
          }
        });
      };
    },
    buildEnd(foo, bar) {
      if (addDependicies) {
        addDependicies(Array.from(this.getModuleIds())
          .filter((path) => {
            return (
              !path.includes('node_modules')
                && path[0] === '/'
            )
          })
          .map((path) => {
            return path.split('?')[0].replace('\x00', '')
          }));
      }
    },
  }
}

module.exports = djangoStatic;
