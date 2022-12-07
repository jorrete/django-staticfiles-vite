#!/usr/bin/env node
const djangoStatic = require('./plugin-django-static');
const { build, defineConfig, mergeConfig, loadConfigFromFile } = require('vite');
const { resolveId } = require('./utils');
const { mkdirSync, writeFileSync, readFileSync, readFile, unlinkSync } = require('fs');
const { join, dirname } = require('path');
const replace = require("postcss-replace");
const { deprecate } = require('util');

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
  const entry = '/home/jorro/Development/python/django-staticfiles-vite/test_app/django/www/static/' + cleanName;

  function addDependicies(deps) {
    dependencies.push(...deps);
  }

  console.log(name, entry);

  const finalConfig = mergeConfig(
    (await loadConfigFromFile())?.config,
    {
      publicDir: false,
      root: process.cwd(),
      clearScreen: false,
      appType: 'custom', // don't include html middlewares
      configFile: false,
      envFile: false,
      css: {
        postcss: {
          plugins: [
            replace({
              pattern: '/static/',
              data: {
                replaceAll: 'http://foo.com/static/',
              },
            }),
            replace({
              pattern: 'static@',
              data: {
                replaceAll: 'http://foo.com/static/',
              },
            }),
          ],
        },
      },
      plugins: [
        {
          ...djangoStatic({
            base,
            paths,
            addDependicies,
          }),
          enforce: 'pre',
        },
      ],
      build: {
        assetsInlineLimit: 10,
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
    unlinkSync(join(outDir, cleanName + '.js'));
  }

  process.stdout.write(JSON.stringify(Array.from(new Set(dependencies))));
})()
