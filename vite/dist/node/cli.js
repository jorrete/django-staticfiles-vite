'use strict';

var cac = require('cac');
var colors = require('picocolors');
var perf_hooks = require('perf_hooks');
var build = require('./chunks/dep-669d2ce2.js');
require('fs');
require('path');
require('connect');
require('cors');
require('chokidar');
require('debug');
require('os');
require('url');
require('resolve');
require('module');
require('@ampproject/remapping');
require('acorn');
require('magic-string');
require('strip-ansi');
require('http');
require('https');
require('ws');
require('http-proxy');
require('connect-history-api-fallback');
require('etag');
require('convert-source-map');
require('mrmime');
require('crypto');
require('periscopic');
require('estree-walker');
require('sirv');
require('fast-glob');
require('postcss-load-config');
require('@rollup/pluginutils');
require('esbuild');
require('es-module-lexer');
require('json5');
require('micromatch');
require('tsconfck');
require('resolve.exports');
require('open');
require('cross-spawn');
require('child_process');
require('launch-editor-middleware');
require('readline');
require('compression');
require('@rollup/plugin-alias');
require('dotenv');
require('dotenv-expand');
require('zlib');
require('util');
require('okie');
require('@rollup/plugin-commonjs');
require('@rollup/plugin-dynamic-import-vars');

function _interopDefaultLegacy (e) { return e && typeof e === 'object' && 'default' in e ? e["default"] : e; }

var colors__default = /*#__PURE__*/_interopDefaultLegacy(colors);

const cli = cac.cac('vite');
/**
 * removing global flags before passing as command specific sub-configs
 */
function cleanOptions(options) {
    const ret = { ...options };
    delete ret['--'];
    delete ret.c;
    delete ret.config;
    delete ret.base;
    delete ret.l;
    delete ret.logLevel;
    delete ret.clearScreen;
    delete ret.d;
    delete ret.debug;
    delete ret.f;
    delete ret.filter;
    delete ret.m;
    delete ret.mode;
    return ret;
}
cli
    .option('-c, --config <file>', `[string] use specified config file`)
    .option('--base <path>', `[string] public base path (default: /)`)
    .option('-l, --logLevel <level>', `[string] info | warn | error | silent`)
    .option('--clearScreen', `[boolean] allow/disable clear screen when logging`)
    .option('-d, --debug [feat]', `[string | boolean] show debug logs`)
    .option('-f, --filter <filter>', `[string] filter debug logs`)
    .option('-m, --mode <mode>', `[string] set env mode`);
// dev
cli
    .command('[root]') // default command
    .alias('serve') // the command is called 'serve' in Vite's API
    .alias('dev') // alias to align with the script name
    .option('--host [host]', `[string] specify hostname`)
    .option('--port <port>', `[number] specify port`)
    .option('--https', `[boolean] use TLS + HTTP/2`)
    .option('--open [path]', `[boolean | string] open browser on startup`)
    .option('--cors', `[boolean] enable CORS`)
    .option('--strictPort', `[boolean] exit if specified port is already in use`)
    .option('--force', `[boolean] force the optimizer to ignore the cache and re-bundle`)
    .action(async (root, options) => {
    // output structure is preserved even after bundling so require()
    // is ok here
    const { createServer } = await Promise.resolve().then(function () { return require('./chunks/dep-669d2ce2.js'); }).then(function (n) { return n.index$1; });
    try {
        const server = await createServer({
            root,
            base: options.base,
            mode: options.mode,
            configFile: options.config,
            logLevel: options.logLevel,
            clearScreen: options.clearScreen,
            server: cleanOptions(options)
        });
        if (!server.httpServer) {
            throw new Error('HTTP server not available');
        }
        await server.listen();
        const info = server.config.logger.info;
        info(colors__default.cyan(`\n  vite v${require('vite/package.json').version}`) +
            colors__default.green(` dev server running at:\n`), {
            clear: !server.config.logger.hasWarned
        });
        server.printUrls();
        // @ts-ignore
        if (global.__vite_start_time) {
            // @ts-ignore
            const startupDuration = perf_hooks.performance.now() - global.__vite_start_time;
            info(`\n  ${colors__default.cyan(`ready in ${Math.ceil(startupDuration)}ms.`)}\n`);
        }
    }
    catch (e) {
        build.createLogger(options.logLevel).error(colors__default.red(`error when starting dev server:\n${e.stack}`), { error: e });
        process.exit(1);
    }
});
// build
cli
    .command('build [root]')
    .option('--target <target>', `[string] transpile target (default: 'modules')`)
    .option('--outDir <dir>', `[string] output directory (default: dist)`)
    .option('--assetsDir <dir>', `[string] directory under outDir to place assets in (default: _assets)`)
    .option('--assetsInlineLimit <number>', `[number] static asset base64 inline threshold in bytes (default: 4096)`)
    .option('--ssr [entry]', `[string] build specified entry for server-side rendering`)
    .option('--sourcemap', `[boolean] output source maps for build (default: false)`)
    .option('--minify [minifier]', `[boolean | "terser" | "esbuild"] enable/disable minification, ` +
    `or specify minifier to use (default: esbuild)`)
    .option('--manifest', `[boolean] emit build manifest json`)
    .option('--ssrManifest', `[boolean] emit ssr manifest json`)
    .option('--emptyOutDir', `[boolean] force empty outDir when it's outside of root`)
    .option('-w, --watch', `[boolean] rebuilds when modules have changed on disk`)
    .action(async (root, options) => {
    const { build: build$1 } = await Promise.resolve().then(function () { return require('./chunks/dep-669d2ce2.js'); }).then(function (n) { return n.build$1; });
    const buildOptions = cleanOptions(options);
    try {
        await build$1({
            root,
            base: options.base,
            mode: options.mode,
            configFile: options.config,
            logLevel: options.logLevel,
            clearScreen: options.clearScreen,
            build: buildOptions
        });
    }
    catch (e) {
        build.createLogger(options.logLevel).error(colors__default.red(`error during build:\n${e.stack}`), { error: e });
        process.exit(1);
    }
});
// optimize
cli
    .command('optimize [root]')
    .option('--force', `[boolean] force the optimizer to ignore the cache and re-bundle`)
    .action(async (root, options) => {
    const { optimizeDeps } = await Promise.resolve().then(function () { return require('./chunks/dep-669d2ce2.js'); }).then(function (n) { return n.index; });
    try {
        const config = await build.resolveConfig({
            root,
            base: options.base,
            configFile: options.config,
            logLevel: options.logLevel
        }, 'build', 'development');
        await optimizeDeps(config, options.force, true);
    }
    catch (e) {
        build.createLogger(options.logLevel).error(colors__default.red(`error when optimizing deps:\n${e.stack}`), { error: e });
        process.exit(1);
    }
});
cli
    .command('preview [root]')
    .option('--host [host]', `[string] specify hostname`)
    .option('--port <port>', `[number] specify port`)
    .option('--strictPort', `[boolean] exit if specified port is already in use`)
    .option('--https', `[boolean] use TLS + HTTP/2`)
    .option('--open [path]', `[boolean | string] open browser on startup`)
    .action(async (root, options) => {
    try {
        const server = await build.preview({
            root,
            base: options.base,
            configFile: options.config,
            logLevel: options.logLevel,
            mode: options.mode,
            preview: {
                port: options.port,
                strictPort: options.strictPort,
                host: options.host,
                https: options.https,
                open: options.open
            }
        });
        server.printUrls();
    }
    catch (e) {
        build.createLogger(options.logLevel).error(colors__default.red(`error when starting preview server:\n${e.stack}`), { error: e });
        process.exit(1);
    }
});
cli.help();
cli.version(require('../../package.json').version);
cli.parse();
//# sourceMappingURL=cli.js.map
