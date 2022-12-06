#!/usr/bin/env node
const djangoStatic = require('./plugin-django-static');
const { build, defineConfig, mergeConfig, loadConfigFromFile } = require('vite');
const { resolveId } = require('./utils');
const { mkdirSync, writeFileSync, readFileSync, readFile, unlinkSync } = require('fs');
const { join, dirname } = require('path');

const {
  filename,
  format,
  name,
  outDir,
  paths,
  cssExtensions,
  jsExtensions,
  base,
} = JSON.parse(process.argv[2] || '{}');

function isCSS(filename) {
  return [
    "css",
    "scss",
    "sass",
  ].some((ext) => filename.endsWith(ext));
}

function getEntryPath(filename, paths, extensions) {
  let entry = resolveId(filename, paths, extensions);

  if (!isCSS(filename)) {
    return entry;
  }
  const cssEntry = join(outDir, filename + '.js');

  writeFileSync(cssEntry, `import '${filename}';`);

  return cssEntry;
}

(async () => {
  mkdirSync(dirname(join(outDir, name)), { recursive: true });

  const extensions = [].concat(jsExtensions, cssExtensions);
  const dependencies = [];
  const cleanName = filename.split('?')[0];
  const entry = getEntryPath(cleanName, paths, extensions);

  function addDependicies(deps) {
    dependencies.push(...deps);
  }

  console.log(dirname(join(outDir, name)));

  const finalConfig = mergeConfig(
    (await loadConfigFromFile())?.config,
    {
      appType: 'custom',
      configFile: false,
      envFile: false,
      root: process.cwd(),
      resolve: {
        extensions: jsExtensions,
      },
      plugins: [
        {
          ...djangoStatic({
            base,
            paths,
            extensions,
            addDependicies,
          }),
          enforce: 'pre',
        },
      ],
      build: {
        emptyOutDir: false,
        outDir,
        rollupOptions: {
          output: {
            assetFileNames: () => {
              if (isCSS(cleanName)) {
                return `${name}.css`
              }
              return `${name}.js.css`
            },
          },
        },
        lib: {
          entry,
          formats: [format],
          name,
          fileName: () => {
            if (isCSS(cleanName)) {
              return `${name}.css.js`
            }
            return `${name}.js`
          },
        },
      },
    },
  );

  await build(defineConfig(finalConfig));

  if (isCSS(cleanName)) {
    unlinkSync(entry);
  }

  process.stdout.write(JSON.stringify(dependencies));
})()
