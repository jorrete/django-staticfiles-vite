/// <reference types="node" />
import type { ResolvedConfig } from '../config';
import type { Plugin } from '../plugin';
export declare function bundleWorkerEntry(config: ResolvedConfig, id: string): Promise<Buffer>;
export declare function webWorkerPlugin(config: ResolvedConfig): Plugin;
