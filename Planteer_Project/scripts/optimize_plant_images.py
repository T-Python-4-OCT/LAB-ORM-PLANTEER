import shutil
from pathlib import Path

from PIL import Image, ImageOps

BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_DIR = BASE_DIR / "media" / "plants"

BACKUP_DIR = Path.home() / "Planteer_Plant_Images_Backup"

MAX_DIMENSION = 1600

ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}


def optimize_image(path):

    original_size = path.stat().st_size

    relative_path = path.relative_to(MEDIA_DIR)

    backup_path = BACKUP_DIR / relative_path

    backup_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if not backup_path.exists():
        shutil.copy2(path, backup_path)

    temp_path = path.with_name(
        path.name + ".optimization_tmp"
    )

    try:

        with Image.open(path) as original:

            image = ImageOps.exif_transpose(original)

            image.thumbnail(
                (MAX_DIMENSION, MAX_DIMENSION),
                Image.Resampling.LANCZOS
            )

            extension = path.suffix.lower()

            if extension in {".jpg", ".jpeg"}:

                image = image.convert("RGB")

                image.save(
                    temp_path,
                    format="JPEG",
                    quality=82,
                    optimize=True,
                    progressive=True
                )

            elif extension == ".png":

                image.save(
                    temp_path,
                    format="PNG",
                    optimize=True,
                    compress_level=9
                )

            elif extension == ".webp":

                image.save(
                    temp_path,
                    format="WEBP",
                    quality=82,
                    method=6
                )

        optimized_size = temp_path.stat().st_size

        if optimized_size < original_size:

            temp_path.replace(path)

            print(
                f"Optimized: {path.name} "
                f"({original_size // 1024} KB → "
                f"{optimized_size // 1024} KB)"
            )

        else:

            temp_path.unlink()

            print(f"Already optimized: {path.name}")

    finally:

        if temp_path.exists():
            temp_path.unlink()


def main():

    if not MEDIA_DIR.exists():

        print("Plant image directory was not found.")
        return

    images = [
        path
        for path in MEDIA_DIR.rglob("*")
        if path.is_file()
        and path.suffix.lower() in ALLOWED_EXTENSIONS
    ]

    print(f"Found {len(images)} images.")

    for path in images:

        try:
            optimize_image(path)

        except Exception as error:
            print(f"Failed: {path.name}: {error}")

    print("Image optimization complete.")
    print(f"Backups: {BACKUP_DIR}")


if __name__ == "__main__":
    main()