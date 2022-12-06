const { existsSync, statSync, readFileSync } = require('fs');
const { resolve } = require('path');

function resolveId(id, paths, extensions = []) {
  // TODO check if is css and the return null
  const match = paths
    .map((path) => resolve(path, (id.startsWith('/') ? id.slice(1) : id)).split('?'))
    .map(([path, query = null]) =>  {
      if (existsSync(path)) {
        if (statSync(path).isDirectory()) {
          return extensions.map((ext) => {
            const finalPath = `${path}${path.endsWith('/') ? '' : '/'}index${ext}`;
            return (existsSync(finalPath) ? [finalPath, query] : null);
          }).filter(Boolean).find(Boolean);
        } else {
          return [path, query];
        }
      }
      
      return extensions.map((ext) => {
        const finalPath = `${path}${ext}`;
        return (existsSync(finalPath) ? [finalPath, query] : null);
      }).filter(Boolean).find(Boolean);
  }).filter(Boolean).find(Boolean);

  if (!match) {
    return null;
  }

  return match.filter(Boolean).join('?');
}

function djangoStatic({ base, paths, extensions }) {
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
  }
}

module.exports = djangoStatic;
