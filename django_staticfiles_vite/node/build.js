/* eslint-disable node/no-missing-require */
const djangoStatic = require('./plugin-django-static');
const { build } = require('vite');
const { STATIC_TOKEN, normalizeCSS, normalizeJS } = require('./utils');
const { mkdirSync } = require('fs');
const { join, dirname } = require('path');
const replace = require('postcss-replace');

const {
  base,
  entry,
  format,
  outDir,
  paths,
  testPaths,
  buildCSS = false
} = JSON.parse(process.argv[2] || '{}');

(async () => {
  Object.keys(entry).forEach((name) => {
    mkdirSync(dirname(join(outDir, name)), { recursive: true });
  });

  const dependencies = [];

  function addDependicies (deps) {
    dependencies.push(...deps);
  }

  await build({
    envFile: false,
    logLevel: 'silent', // since the assets management to avoid inlining is it a hack supress warnings
    css: {
      postcss: {
        plugins: [
          replace({
            pattern: STATIC_TOKEN,
            data: {
              replaceAll: base
            }
          })
        ]
      }
    },
    plugins: [
      {
        ...djangoStatic({
          base,
          paths,
          testPaths,
          addDependicies,
          command: 'build'
        }),
        enforce: 'pre'
      }
    ],
    build: {
      assetsInlineLimit: 10,
      emptyOutDir: false,
      cssCodeSplit: true,
      outDir,
      rollupOptions: {
        output: {
          chunkFileNames: 'chunk.[name].js',
          assetFileNames: ({ name, source }) => {
            if (source === '/* vite internal call, ignore */') {
              return name;
            }

            const [alias, path] = [].concat(paths, testPaths).find(([alias, path]) => {
              const relativePath = path.replace(process.cwd(), '').slice(1);

              if (name.startsWith(relativePath + '/')) {
                return [alias, relativePath];
              }

              return null;
            }) || [null, null];

            if (!path) {
              return name;
            }

            const finalName = join(
              alias,
              normalizeCSS(
                name.replace(path.replace(process.cwd(), '').slice(1), '').slice(1)
              )
            );

            if (buildCSS) {
              return finalName;
            }

            return (finalName.includes('/tests/') ? 'tests/' : '') + finalName.replace('.css', '.js.css');
          }
        }
      },
      lib: {
        entry,
        formats: [format],
        fileName: (_, name) => {
          return normalizeJS(name);
        }
      }
    }
  });

  process.stdout.write(JSON.stringify(Array.from(new Set(dependencies))));
})();
