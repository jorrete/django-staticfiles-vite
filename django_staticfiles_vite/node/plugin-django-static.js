const vite = require('vite');

function djangoStatic({ base, paths, command, addDependicies }) {
  async function djangoResolver(id) {
    for (let index = 0; index < paths.length; index++) {
      const path = paths[index];
      const match = await this.resolve(`${path}${id}`);
      if (match) {
        addDependicies?.([match.id.split('?')[0]]);
        return match;
      }
    }
  }

  const extensions = [
    // images
    'png',
    'jpe?g',
    'jfif',
    'pjpeg',
    'pjp',
    'gif',
    'svg',
    'ico',
    'webp',
    'avif',

    // media
    'mp4',
    'webm',
    'ogg',
    'mp3',
    'wav',
    'flac',
    'aac',

    // fonts
    'woff2?',
    'eot',
    'ttf',
    'otf',

    // other
    'webmanifest',
    'pdf',
    'txt',
  ];
  const findStaticAliasBuild = new RegExp(`^static@(?!.*\.(${extensions.join('|')}))`)
  const findStaticAliasServe = new RegExp('^static@(.*)');
  const findStaticBaseBuild = new RegExp(`^${base}(?!.*\.(${extensions.join('|')}))`)
  const findStaticBaseServe = new RegExp(`^${base}(.*)`);

  return {
    name: 'django-static',
    config: () => ({
      resolve: {
        alias: [
          {
            find: command === 'build' ? findStaticAliasBuild : findStaticAliasServe,
            replacement: '/$1',
            customResolver: djangoResolver,
          },
          {
            find: command === 'build' ? findStaticBaseBuild : findStaticBaseServe,
            replacement: '/$1',
            customResolver: djangoResolver,
          },
        ],
      }
    }),
    handleHotUpdate(ctx) {
      if (ctx.file.endsWith('.html')) {
        ctx.server.ws.send({ type: 'full-reload' });
        return []
      }
    },
    buildEnd(foo, bar) {
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
