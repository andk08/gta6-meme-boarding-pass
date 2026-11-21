// Boarding-pass entry for the GTA 6 meme bounty on make.fun.
//
// What this program does, and nothing more: it takes the POST.json file
// that sits at the root of this repository — the file that names the X
// post carrying the meme — and places an identical copy of it into the
// output directory the grader reads. The house then fetches the post
// from X itself and hands its first picture and its text to the judge.
//
// Two directories come from the environment so the same code runs both
// inside the grader's container and on a developer machine:
//   MAKEFUN_BOT_DIR     — where this repository is mounted (default /bot)
//   MAKEFUN_OUTPUT_DIR  — where the copied file must land (default /output)
//
// The output directory is created if it is missing, and it is never
// removed by this program: deleting it would break the grader's mount,
// so only the file inside it is written. No network, no clock, no files
// outside this repository are touched, and two runs write the same bytes.

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const sourceDir = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const targetDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const fileName = 'POST.json';

const sourcePath = join(sourceDir, fileName);
const targetPath = join(targetDir, fileName);

// Make sure the destination folder exists before writing into it.
mkdirSync(targetDir, { recursive: true });

// Read the post address, confirm it parses as JSON, then copy it over.
let postText: string;
try {
  postText = readFileSync(sourcePath, 'utf8');
  const parsed = JSON.parse(postText) as unknown;
  if (typeof parsed !== 'object' || parsed === null || !('url' in parsed)) {
    throw new Error('POST.json must be a JSON object with a url field');
  }
} catch (err) {
  console.error(`Could not read a valid ${fileName} from ${sourceDir}: ${(err as Error).message}`);
  process.exit(1);
}

try {
  copyFileSync(sourcePath, targetPath);
} catch (err) {
  console.error(`Could not write ${fileName} to ${targetDir}: ${(err as Error).message}`);
  process.exit(1);
}
