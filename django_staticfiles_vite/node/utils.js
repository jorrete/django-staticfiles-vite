async function resolveId(id, paths) {
  for (let index = 0; index < paths.length; index++) {
    const path = paths[index];
    const match = await this.resolve(`${path}${id}`);
    if (match) {
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

function isCSS(filename) {
  return [
    "css",
    "scss",
    "sass",
  ].some((ext) => filename.endsWith(ext));
}

module.exports = {
  resolveId,
  extensions,
  isCSS,
};
