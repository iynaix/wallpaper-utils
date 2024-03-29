import cv2
from utils import (
    WALLPAPER_DIR,
    detect,
    Cropper,
    VERTICAL_ASPECT_RATIO,
    FRAMEWORK_ASPECT_RATIO,
    ULTRAWIDE_ASPECT_RATIO,
    HD_ASPECT_RATIO,
    WallpaperInfo,
)

WallpaperGeometries = dict[str, dict[str, str]]


def ratio_str(ratio: tuple[int, int]) -> str:
    return f"r{ratio[0]}x{ratio[1]}"


def swww(img: str, geometry: str, output: str) -> str:
    return f'convert "{img}" -crop "{geometry}" - | swww img --outputs "{output}" -;'


if __name__ == "__main__":
    ratios = [
        VERTICAL_ASPECT_RATIO,
        FRAMEWORK_ASPECT_RATIO,
        ULTRAWIDE_ASPECT_RATIO,
        HD_ASPECT_RATIO,
    ]

    IMAGE_DATA = WallpaperInfo()

    for img in sorted(WALLPAPER_DIR.iterdir()):
        fname = img.name

        if fname in IMAGE_DATA or fname.endswith(".json"):
            continue

        print(fname)
        image = cv2.imread(str(img))
        faces = detect(str(img))
        cropper = Cropper(image, faces)
        IMAGE_DATA[fname] = {
            "faces": cropper.faces_tuples(),
            **cropper.geometries(),
        }

    IMAGE_DATA.save()
