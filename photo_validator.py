# Проверка фотографий
import os
from PIL import Image, UnidentifiedImageError

content = os.listdir('img')
for dir_ in content:
    files = os.listdir(f'img/{dir_}')
    for f in files:
        try:
            im = Image.open(f"img/{dir_}/{f}")
        except Exception:
            print(f"{dir_}/{f}")
