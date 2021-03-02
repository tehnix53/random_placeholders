import glob
import os
from config import *

reference_files = sorted(['10', '2', '3', '4', '5',
                          '6', '7', '8', '9', 'a',
                          'bubi', 'chervi', 'j', 'k',
                          'kresti', 'piki', 'q'])

reference_folders = sorted(['♦', '♣', '♥', '♠'])


def test_config_exist():
    list_dirs = [SAVE_PATH, BACKGROUNDS,
                 FONTS, PIPELINE_FOLDER]
    non_false_list = []
    for i in list_dirs:
        non_false_list += [os.path.exists(i)]
    assert False not in non_false_list


def test_backgrounds():
    types = ('*.webp', '*.jpg', '*.png')
    volume = 0
    for i in types:
        files = glob.glob(os.path.join(BACKGROUNDS, i))
        volume += len(files)
    assert volume > 0


def test_fonts():
    types = "*.ttf"
    volume = 0
    for i in types:
        files = glob.glob(os.path.join(FONTS, i))
        volume += len(files)
    assert volume > 0










