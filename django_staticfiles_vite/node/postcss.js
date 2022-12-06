#!/usr/bin/env node
const fs = require('fs').promises;
const postcss = require('postcss')
const postcssImport = require('postcss-import');
const postcssMinify = require('postcss-minify');
const { loadConfigFromFile } = require('vite');

const {
  filename,
  entry,
  paths,
  outDir,
  base,
} = JSON.parse(process.argv[2] || '{}');

(async () => {
  console.log(`[postCss] ${filename}`);

  const config = (await loadConfigFromFile()).config || {};

  const find = base;

  const src = entry;
  const dest = `${outDir}/${filename}`;
  const plugins = [
    postcssImport({
      resolve: (css) => css.replace(find, ''),
      path: paths,
    }),
    ...(config?.build?.mifify ? [postcssMinify()] : []),
    ...(config?.css?.postcss?.plugins || []),
  ];
  const css = await fs.readFile(src);
  const result = await postcss(plugins).process(css, { from: src, to: dest })
  await fs.writeFile(dest, result.css, () => true)
})()
