/// <reference types="node" />
import type { IncomingMessage, OutgoingHttpHeaders, ServerResponse } from 'http';
import type { SourceMap } from 'rollup';
export interface SendOptions {
    etag?: string;
    cacheControl?: string;
    headers?: OutgoingHttpHeaders;
    map?: SourceMap | null;
}
export declare function send(req: IncomingMessage, res: ServerResponse, content: string | Buffer, type: string, options: SendOptions): void;
