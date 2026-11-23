// main.ts — Monday 23 November 2026 world-news broadsheet (news-image-20261123).
// Node 22 stdlib only. Copies entry.png byte-for-byte to $MAKEFUN_OUTPUT_DIR
// (default /output), verifies PNG magic bytes + byte count, exits 0.
// No network, no clock, no external dependencies.
import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const dst = join(outDir, "entry.png");

const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

const data = readFileSync(src);
if (data.length < 8 || !data.subarray(0, 8).equals(PNG_MAGIC)) {
  console.error("entry.png: bad PNG magic bytes");
  process.exit(1);
}
// IHDR: width and height are big-endian uint32 at bytes 16..24.
const width = data.readUInt32BE(16);
const height = data.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  console.error(`entry.png: expected 1024x1024, got ${width}x${height}`);
  process.exit(1);
}
mkdirSync(outDir, { recursive: true });
copyFileSync(src, dst);
const written = readFileSync(dst);
if (!written.equals(data)) {
  console.error("output bytes differ from entry.png");
  process.exit(1);
}
const size = statSync(dst).size;
console.log(`entry.png -> ${dst} (${size} bytes, PNG OK)`);
