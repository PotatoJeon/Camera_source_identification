from PIL import Image
from PIL.ExifTags import TAGS

def get_image_exif(image):
    img = Image.open(image)

    exif_info = {}
    img_info = img._getexif()
    #print(img_info)
    for tag_id in img_info:
        tag = TAGS.get(tag_id, tag_id)
        data = img_info.get(tag_id)

        owner_identificaion = ['Make', 
                               'Model', 
                               'DateTime', 
                               'CameraOwnerName', 
                               'BodySerialNumber', 
                               'LensModel',
                               'LensSerialNumber']

        if tag in owner_identificaion:
            exif_info[f'{tag}'] = f'{data}'

    img.close()

    return exif_info

