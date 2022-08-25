const fs = require('fs').promises;
const postcss = require('postcss')
const postcssImport = require('postcss-import');

const {
  filename,
  entry,
  paths,
  outDir,
  configPath,
} = JSON.parse(process.argv[2] || '{}');

const config = require(configPath);

(async () => {
  console.log(`[postCss] ${filename}`);
  const src = entry;
  const dest = `${outDir}/${filename}`;
  const plugins = [
    postcssImport({
      resolve: (css) => css.replace('/static', ''),
      path: paths,
    }),
    ...(config?.css?.postcss?.plugins || []),
  ];
  const css = await fs.readFile(src);
  const result = await postcss(plugins).process(css, { from: src, to: dest })
  await fs.writeFile(dest, result.css, () => true)
})()
