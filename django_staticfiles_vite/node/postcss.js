#!/usr/bin/node
const fs = require('fs').promises;
const postcss = require('postcss')
const postcssImport = require('postcss-import');
const postcssMinify = require('postcss-minify');

const {
  filename,
  entry,
  paths,
  outDir,
  configPath,
  baseUrl,
} = JSON.parse(process.argv[2] || '{}');

const config = require(configPath);

(async () => {
  console.log(`[postCss] ${filename}`);

  const find = baseUrl;

  const src = entry;
  const dest = `${outDir}/${filename}`;
  const plugins = [
    postcssImport({
      resolve: (css) => css.replace(find, ''),
      path: paths,
    }),
    postcssMinify(),
    ...(config?.css?.postcss?.plugins || []),
  ];
  const css = await fs.readFile(src);
  const result = await postcss(plugins).process(css, { from: src, to: dest })
  await fs.writeFile(dest, result.css, () => true)
})()
