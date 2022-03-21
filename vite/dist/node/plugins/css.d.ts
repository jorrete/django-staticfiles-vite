import type { Plugin } from '../plugin';
import type { ResolvedConfig } from '../config';
import type { RenderedChunk, RollupError } from 'rollup';
import type { ResolveFn } from '../';
import type * as Postcss from 'postcss';
import type { Alias } from 'types/alias';
export interface CSSOptions {
    /**
     * https://github.com/css-modules/postcss-modules
     */
    modules?: CSSModulesOptions | false;
    preprocessorOptions?: Record<string, any>;
    postcss?: string | (Postcss.ProcessOptions & {
        plugins?: Postcss.Plugin[];
    });
}
export interface CSSModulesOptions {
    getJSON?: (cssFileName: string, json: Record<string, string>, outputFileName: string) => void;
    scopeBehaviour?: 'global' | 'local';
    globalModulePaths?: RegExp[];
    generateScopedName?: string | ((name: string, filename: string, css: string) => string);
    hashPrefix?: string;
    /**
     * default: null
     */
    localsConvention?: 'camelCase' | 'camelCaseOnly' | 'dashes' | 'dashesOnly' | null;
}
export declare const isCSSRequest: (request: string) => boolean;
export declare const isDirectCSSRequest: (request: string) => boolean;
export declare const isDirectRequest: (request: string) => boolean;
export declare const chunkToEmittedCssFileMap: WeakMap<RenderedChunk, Set<string>>;
export declare const removedPureCssFilesCache: WeakMap<Readonly<Omit<import("../config").UserConfig, "plugins" | "alias" | "dedupe" | "assetsInclude" | "optimizeDeps" | "worker"> & {
    configFile: string | undefined;
    configFileDependencies: string[];
    inlineConfig: import("../config").InlineConfig;
    root: string;
    base: string;
    publicDir: string;
    cacheDir: string;
    command: "build" | "serve";
    mode: string;
    isProduction: boolean;
    env: Record<string, any>;
    resolve: import("./resolve").ResolveOptions & {
        alias: Alias[];
    };
    plugins: readonly Plugin[];
    server: import("../server").ResolvedServerOptions;
    build: Required<Omit<import("../build").BuildOptions, "base" | "cleanCssOptions" | "polyfillDynamicImport" | "brotliSize">>;
    preview: import("../preview").ResolvedPreviewOptions;
    assetsInclude: (file: string) => boolean;
    logger: import("../logger").Logger;
    createResolver: (options?: Partial<import("./resolve").InternalResolveOptions> | undefined) => ResolveFn;
    optimizeDeps: Omit<import("../optimizer").DepOptimizationOptions, "keepNames">;
    packageCache: import("../packages").PackageCache;
    worker: import("../config").ResolveWorkerOptions;
}>, Map<string, RenderedChunk>>;
/**
 * Plugin applied before user plugins
 */
export declare function cssPlugin(config: ResolvedConfig): Plugin;
/**
 * Plugin applied after user plugins
 */
export declare function cssPostPlugin(config: ResolvedConfig): Plugin;
export declare const cssUrlRE: RegExp;
export interface StylePreprocessorResults {
    code: string;
    map?: object;
    errors: RollupError[];
    deps: string[];
}
