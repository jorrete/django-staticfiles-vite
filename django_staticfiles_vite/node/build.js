import djangoStatic from './plugin-django-static.js';
import replace from 'postcss-replace';
import { STATIC_TOKEN, normalizeJS, isCSS } from './utils.js';
import { build } from 'vite';
import { join, dirname } from 'path';
import { mkdirSync } from 'fs';

const {
  base,
  entry,
  format,
  outDir,
  paths,
  testPaths,
  buildCSS = false,
  context = {},
} = JSON.parse(process.argv[2] || '{}');

(async () => {
  Object.keys(entry).forEach((name) => {
    mkdirSync(dirname(join(outDir, name)), { recursive: true });
  });

  await build({
    envFile: false,
    // logLevel: 'silent', // since the assets management to avoid inlining is it a hack supress warnings
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
          context,
          base,
          paths,
          testPaths,
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

            if (name === 'qunit.css') {
              return name;
            }

            if (buildCSS) {
              return name;
            }

            if (!buildCSS && isCSS(name)) {
              const relativePath = dirname(Object.keys(entry)[0]);
              return join(relativePath, name.replace('.css', '.js.css'));
            }

            return name;
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

  // process.stdout.write(JSON.stringify(Array.from(new Set(dependencies))));
})();
