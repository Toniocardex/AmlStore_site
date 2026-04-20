/**
 * Rasterizza gli SVG delle sezioni M365 Solutions in WebP + PNG.
 * Uso: node scripts/build-m365-illustrations.cjs
 */
const path = require("path");
const sharp = require("sharp");

const WIDTH = 1120;
const HEIGHT = 720;
const WEBP_QUALITY = 86;

const NAMES = [
  "m365sol-illu-copilot",
  "m365sol-illu-onedrive",
  "m365sol-illu-defender",
  "m365sol-illu-outlook",
];

const OUT = path.join(__dirname, "..", "asset", "media");

(async () => {
  for (const base of NAMES) {
    const svgPath = path.join(OUT, `${base}.svg`);
    const resized = () =>
      sharp(svgPath).resize(WIDTH, HEIGHT, {
        fit: "fill",
        kernel: sharp.kernel.lanczos3,
      });
    await resized()
      .webp({ quality: WEBP_QUALITY, effort: 4 })
      .toFile(path.join(OUT, `${base}.webp`));
    await resized()
      .png({ compressionLevel: 9 })
      .toFile(path.join(OUT, `${base}.png`));
    console.log(base, "→ .webp, .png");
  }
  console.log("Done.");
})().catch((err) => {
  console.error(err);
  process.exit(1);
});
