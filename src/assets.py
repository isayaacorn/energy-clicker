from os.path import join

from wx import Bitmap, Image, BITMAP_TYPE_PNG


def get_asset(name: str, width: int = 128, height: int = 128):
    return Bitmap(Image(join('img', 'icons', f'{name}.png'), BITMAP_TYPE_PNG).Scale(width, height))
