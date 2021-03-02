import os, glob, random
from PIL import Image

rang_suit = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'k', 'q', 'j', 'a',
             '♦', '♣', '♥', '♠']


def count_files(some_dir):
    jpg = len(glob.glob(some_dir + '/*jpg'))
    pbm = len(glob.glob(some_dir + '/*pbm'))
    return min(jpg, pbm)


def extend_folder(some_folder, delta):
    def random_basename(some_dir):
        list_dir = os.listdir(some_dir)
        index = len(list_dir) - 1
        random_val = random.randint(0, index)
        return list_dir[random_val].split('.')[-2]

    for i in range(delta):
        basename = random_basename(some_folder)
        img = basename + '.jpg'
        mask = basename + '.pbm'
        img = os.path.join(some_folder, img)
        mask = os.path.join(some_folder, mask)
        img = Image.open(img)
        mask = Image.open(mask)
        save_img_path = os.path.join(some_folder, basename + '_' + str(i) + '.jpg')
        save_mask_path = os.path.join(some_folder, basename + '_' + str(i) + '.pbm')
        img.save(save_img_path)
        mask.save(save_mask_path)
