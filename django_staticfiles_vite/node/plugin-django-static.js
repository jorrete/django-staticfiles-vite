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

function djangoStatic({ paths, extensions }) {
  return {
    name: 'django-static',
    config: () => ({
      resolve: {
        alias: [
          {
            find: '@static',
            replacement: '',
            customResolver: (id) => resolveId(id, paths, extensions),
          }
        ],
      }
    }),
    resolveId(id) {
      return resolveId(id, paths, extensions);
    },
  }
}

module.exports = djangoStatic;
