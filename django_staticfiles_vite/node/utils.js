const { extname, join } = require('path');

const STATIC_TOKEN = 'static@';

async function resolveId(id, paths) {
  for (let index = 0; index < paths.length; index++) {
    const match = await this.resolve(join(paths[index], id));

    if (match) {
      return match;
    }
  }

  return null;
}

function hasExtension(filename, extensions) {
  return extensions.some((ext) => (new RegExp(ext).test(extname(filename).slice(1))));
}

function isCSS(filename) {
  return hasExtension(filename, [
    "css",
    "scss",
    "sass",
  ]);
}

const excludeExtCSS = [
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

  // fonts
  'woff2?',
  'eot',
  'ttf',
  'otf',
];

module.exports = {
  resolveId,
  hasExtension,
  excludeExtCSS,
  isCSS,
  STATIC_TOKEN,
};
