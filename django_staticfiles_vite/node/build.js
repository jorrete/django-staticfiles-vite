#!/usr/bin/env node
const djangoStatic = require('./plugin-django-static');
const { build, defineConfig, mergeConfig, loadConfigFromFile } = require('vite');
const {
  resolveId,
  isCSS,
  isJS,
  STATIC_TOKEN,
  normalizeCSS,
  normalizeJS,
} = require('./utils');
const {
  mkdirSync,
  writeFileSync,
  readFileSync,
  readFile,
  unlinkSync,
} = require('fs');
const { join, dirname, basename } = require('path');
const replace = require("postcss-replace");
const { deprecate } = require('util');

const {
  base,
  entry,
  format,
  outDir,
  paths,
  buildCSS = false,
} = JSON.parse(process.argv[2] || '{}');

(async () => {
  Object.keys(entry).forEach((name) => {
    mkdirSync(dirname(join(outDir, name)), { recursive: true });
  })

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
        cssCodeSplit: true,
        outDir,
        rollupOptions: {
          output: {
            chunkFileNames: 'chunk.[name].[hash].js',
            assetFileNames: ({ name, type, source }) => {
              if (source === '/* vite internal call, ignore */') {
                return name;
              }

              const [alias, path] = paths.find(([alias, path]) => {
                const relativePath = path.replace(process.cwd(), '').slice(1);

                if (name.startsWith(relativePath + '/')) {
                  return [alias, relativePath];
                }

                return null;
              });

              const finalName = join(
                alias,
                normalizeCSS(
                  name.replace(path.replace(process.cwd(), '').slice(1), '').slice(1),
                ),
              );

              if (buildCSS) {
                return finalName;
              }

              return finalName.replace('.css', '.js.css');
            },
          },
        },
        lib: {
          entry: entry,
          formats: [format],
          fileName: (_, name) => {
            return normalizeJS(name);
          },
        },
      },
    },
  );

  await build(defineConfig(finalConfig));

  process.stdout.write(JSON.stringify(Array.from(new Set(dependencies))));
})()
