from pathlib import Path
from PIL import Image, UnidentifiedImageError

### Quick docs:
# make_thumbnails will iterate over files in a given directory and make thumnails out of them
# kwargs:
# path_gallery          - path to original images
# path_thumb            - directory to which thumbnails are saved
# thumb_size            - size of the thumbnail
# pattern               - function that takes original filename and changed it to the thumbnail name
# verbose               - will stop the program with an input() before the end in case you want to check the files that weren't identified as images
# format                - see PIL.format

def make_thumbnails(
        path_gallery = "static\\gallery",
        path_thumb = "static\\gallery_thumb",
        thumb_size = (400, 400),
        pattern = None,
        verbose = False, 
        format = "JPEG"):
    gallery_dir = Path(path_gallery)
    thumbnail_dir = Path(path_thumb)
    if not thumbnail_dir.exists():
        thumbnail_dir.mkdir(parents=True, exist_ok=True)

    new_width, new_height = thumb_size

    for file in gallery_dir.iterdir():
        try:
            with Image.open(gallery_dir.joinpath(file.name)) as img:
                width, height = img.size                            # get original sizes
                
                if height >= width:                                 # img is portrait
                    resized_height = int(height * new_width/width)  # calc height of resized img
                    img = img.resize((new_width, resized_height))   # resize the image
                    width, height = img.size                        # get new sizes
                    top = (height - new_height)//2                  # get center vertical values
                    bottom = (height + new_height)//2               # ^
                    img = img.crop((0, top, new_width, bottom))     # crop image to center

                else:                                               # img is landscape
                    resized_width = int(width * new_height/height)  # calc height of resized img
                    img = img.resize((resized_width, new_height))   # resize the image
                    width, height = img.size                        # get new sizes
                    left = (width - new_width)//2                   # get center horizontal values
                    right = (width + new_width)//2                  # ^
                    img = img.crop((left, 0, right, new_height))    # crop image to center
                
                if pattern:
                    img.save(thumbnail_dir.joinpath(pattern(file.name)), format)
                else:
                    img.save(thumbnail_dir.joinpath(f"{file.name[0:file.name.find('.')]}_thumb.{format.lower()}"), format if format else None)
        except UnidentifiedImageError as error:
            if verbose: print(error)

    if verbose: input("Done! Press enter to terminate...\n")

if __name__ == "__main__":
    make_thumbnails(verbose=True)
