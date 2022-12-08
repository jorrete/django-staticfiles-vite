#!/usr/bin/env node
const djangoStatic = require('./plugin-django-static');
const { build, defineConfig, mergeConfig, loadConfigFromFile } = require('vite');
const { resolveId, isCSS, STATIC_TOKEN } = require('./utils');
const { mkdirSync, writeFileSync, readFileSync, readFile, unlinkSync } = require('fs');
const { join, dirname } = require('path');
const replace = require("postcss-replace");
const { deprecate } = require('util');

const {
  base,
  entry,
  format,
  name,
  outDir,
  paths,
} = JSON.parse(process.argv[2] || '{}');

(async () => {
  mkdirSync(dirname(join(outDir, name)), { recursive: true });
  const dependencies = [];

  function addDependicies(deps) {
    dependencies.push(...deps);
  }

  const finalConfig = mergeConfig(
    (await loadConfigFromFile())?.config,
    {
      configFile: false,
      envFile: false,
      logLevel: 'silent', // since the assets management to avoid inlining is it a hack supress warnings
      css: {
        postcss: {
          plugins: [
            replace({
              pattern: STATIC_TOKEN,
              data: {
                replaceAll: base,
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
            command: 'build',
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
              if (isCSS(entry)) {
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
            if (isCSS(entry)) {
              return `${name}.css.js`
            }
            return `${name}.js`
          },
        },
      },
    },
  );

  await build(defineConfig(finalConfig));

  if (isCSS(entry)) {
    unlinkSync(join(outDir, `${name}.css.js`));
  }

  process.stdout.write(JSON.stringify(Array.from(new Set(dependencies))));
})()
