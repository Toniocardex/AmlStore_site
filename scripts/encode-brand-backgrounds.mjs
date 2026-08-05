import path from "node:path";
import process from "node:process";
import { stat } from "node:fs/promises";
import sharp from "sharp";

const root = process.cwd();
const mediaDir = path.join(root, "asset", "media");

const jobs = [
  {
    input: "aml_store_media_background.png",
    output: "aml_store_media_background.avif",
    maxSide: 1920,
  },
  {
    input: "aml_store_media_background_mobile.png",
    output: "aml_store_media_background_mobile.avif",
    maxSide: 1080,
  },
];

for (const job of jobs) {
  const inputPath = path.join(mediaDir, job.input);
  const outputPath = path.join(mediaDir, job.output);

  await sharp(inputPath)
    .rotate()
    .resize({
      width: job.maxSide,
      height: job.maxSide,
      fit: "inside",
      withoutEnlargement: true,
    })
    .avif({
      quality: 52,
      effort: 6,
    })
    .toFile(outputPath);

  const { size } = await stat(outputPath);
  console.log(`${job.output}: ${(size / 1024).toFixed(1)} KB`);
}
