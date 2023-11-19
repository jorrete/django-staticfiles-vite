import { extname, join } from 'path';
import { existsSync, readFileSync } from 'fs';

const STATIC_TOKEN = 'static@';

async function resolveId (id, paths) {
  for (let index = 0; index < paths.length; index++) {
    const [alias, path] = paths[index];

    const name = (
      id.startsWith(`${alias}/`)
        ? id.replace(`${alias}/`, '')
        : id
    );

    const match = await this.resolve(join(path, name));

    if (match) {
      return match;
    }
  }

  return null;
}

function resolveStatic(id, paths) {
  for (let index = 0; index < paths.length; index++) {
    const [alias, path] = paths[index];

    const name = (
      id.startsWith(`${alias}/`)
        ? id.replace(`${alias}/`, '')
        : id
    );

    const filepath = join(path, name);

    if (existsSync(filepath)) {
      return readFileSync(filepath);
    }
  }

  return null;
}

function hasExtension (filename, extensions) {
  return extensions.some((ext) => (new RegExp(ext).test(extname(filename).slice(1))));
}

function isCSS (filename) {
  return hasExtension(filename, [
    'css',
    'scss',
    'sass'
  ]);
}

function isJS (filename) {
  return hasExtension(filename, [
    'js',
    'jsx',
    'ts',
    'ts,'
  ]);
}

function removeExtension (filename) {
  return filename.split('.').slice(0, -1).join('.');
}

function normalizeCSS (filename) {
  return removeExtension(filename) + '.css';
}

function normalizeJS (filename) {
  return removeExtension(filename) + '.js';
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
  'otf'
];

export {
  resolveStatic,
  resolveId,
  hasExtension,
  excludeExtCSS,
  isCSS,
  isJS,
  normalizeJS,
  normalizeCSS,
  STATIC_TOKEN
};
