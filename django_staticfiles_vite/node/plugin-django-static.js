const { existsSync, statSync} = require('fs');
const { resolve } = require('path');

function resolveId(id, paths, extensions) {
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

function djangoStatic({ baseUrl, paths, extensions }) {
  const find = (
    baseUrl.slice(-1) === '/'
      ? baseUrl.slice(0, -1)
      : baseUrl
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
    }
  }
}

module.exports = djangoStatic;
