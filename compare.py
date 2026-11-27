"""Build side-by-side images (left = no RAG, right = RAG) from eval_out/ into compare/."""
from pathlib import Path
from PIL import Image, ImageDraw

SRC, OUT, W = Path("eval_out"), Path("compare"), 640
OUT.mkdir(exist_ok=True)


def load(path):
    if not path.exists():
        img = Image.new("RGB", (W, 200), "white")
        ImageDraw.Draw(img).text((W // 2 - 90, 90), "FAILED TO COMPILE", fill="red")
        return img, True
    img = Image.open(path).convert("RGB")
    return img.resize((W, max(1, int(img.height * W / img.width)))), False


for i in range(1, 17):
    left, lfail = load(SRC / f"no_rag_{i:02d}.png")
    right, rfail = load(SRC / f"rag_{i:02d}.png")
    h = max(left.height, right.height)
    canvas = Image.new("RGB", (2 * W + 60, h + 50), "white")
    d = ImageDraw.Draw(canvas)
    d.text((10, 10), f"#{i}  LEFT: no RAG", fill="black")
    d.text((W + 50, 10), f"RIGHT: RAG", fill="black")
    canvas.paste(left, (10, 40))
    canvas.paste(right, (W + 50, 40))
    d.line([(W + 30, 0), (W + 30, h + 50)], fill="gray")
    canvas.save(OUT / f"compare_{i:02d}.png")
    note = "  <- no RAG failed" if lfail else ""
    note += "  <- RAG failed" if rfail else ""
    print(f"compare_{i:02d}.png{note}")
print("Done. Open the files in the compare folder.")
