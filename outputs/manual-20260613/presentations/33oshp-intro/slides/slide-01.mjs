import fs from "node:fs/promises";
import path from "node:path";

export async function slide01(presentation, ctx) {
  const slide = presentation.slides.add();
  slide.background.fill = "#010302";

  const gifPath = path.join(ctx.workspaceDir, "assets", "33oshp-soft-reveal.gif");
  const gifBytes = await fs.readFile(gifPath);
  slide.images.add({
    blob: gifBytes,
    contentType: "image/gif",
    position: { left: 0, top: 0, width: 720, height: 1280 },
    name: "33ОШП — плавна поява",
  });

  return slide;
}
