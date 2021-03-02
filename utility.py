import numpy as np
import string, math
import cv2
import glob
import random
import os
from PIL import ImageFont, ImageDraw, Image
from config import *

RANGS = os.path.join(PIPELINE_FOLDER, 'Rangs')  # dir with crop rang / suits for big card
BIG_SUITS = os.path.join(PIPELINE_FOLDER, 'SuitsBig')  # dir with big suits
SMALL_SUITS = os.path.join(PIPELINE_FOLDER, 'SuitsSmall')  # dir with small suits
backgrounds = glob.glob(BACKGROUNDS + '/*')
all_fonts = glob.glob(FONTS + '/*ttf')


def list_dir(some_dir):
    return [os.path.join(some_dir, i) for i in sorted(os.listdir(some_dir))]


rangs = list_dir(RANGS)
big_list = list_dir(BIG_SUITS)
small_list = list_dir(SMALL_SUITS)


# RANDOM VALUES TO GEN

def random_int():
    return str(round(random.randint(0, 500), 2))


def random_float():
    return str(round(random.uniform(0.0, 500.00), 2))


def random_money_float():
    return '$' + str(round(random.uniform(0.0, 500.00), 2))


def random_money_int():
    return '$' + str(round(random.randint(0, 500), 2))


def all_money_position():
    all_money = [random_int(), random_float(),
                 random_money_int(), random_money_float()]
    return random.choice(all_money)


def random_white():
    unique_white = [[221, 255, 235], [222, 226, 225],
                    [255, 255, 255], [251, 228, 236], [252, 252, 252]]
    index = random.randint(0, len(unique_white) - 1)
    return tuple(unique_white[index])


def random_fonts():
    index = random.randint(0, len(all_fonts) - 1)
    return all_fonts[index]


def random_backgrounds():
    index = random.randint(0, len(backgrounds) - 1)
    return backgrounds[index]


def random_file(folder_list):
    idx = random.randint(0, len(folder_list) - 1)
    folder_name = folder_list[idx]
    all_files = [os.path.join(folder_name, i) for i in os.listdir(folder_name) if i.endswith('.jpg')]
    index = random.randint(0, len(all_files) - 1)
    return all_files[index]


symb = string.ascii_letters + '%/'


def random_symb():
    index = random.randint(0, len(symb) - 1)
    return symb[index].lower()


def random_text():
    permissible_numbers = [4, 5, 6, 7]
    a = str('')
    word_len = random.choice(permissible_numbers)
    for i in range(word_len):
        a += random_symb()
    a = a[0].capitalize() + a[1::]
    return a


def random_sentence():
    index = random.randint(5, 8)
    answ = ''
    for i in range(index):
        answ += random_symb()
    return answ


random_sentence()

dummy = Image.open(random_backgrounds()).resize((640, 640), Image.ANTIALIAS)


# COMMON DEF


def rgb_color(array, dim):
    color = 0
    size = array.shape[0]
    for j in range(size):
        color += np.mean((np.asarray([i[dim] for i in array[j]])))
    return int(color / size)


def drop_blanks(a):
    answ = ''
    for i in a.split('\n'):
        el = (i.split(' '))
        if el == ['']:
            answ += ('#')
        elif el[-2] == '':
            answ += ('#')
        else:
            answ += (' '.join(el[:-1]))
            answ += ('#')
    answ = answ.replace('####', '\n\n')
    answ = answ.replace('###', '\n\n')
    answ = answ.replace('##', '\n\n')
    answ = answ.replace('#', '\n')
    return answ


def extend_coordinate(test):
    answer = [test[0], test[1],
              test[2], test[1],
              test[2], test[3],
              test[0], test[3]]
    return answer


def sentence_coord(sentence_letter, start_point_x, start_point_y, font):
    start_x = start_point_x
    start_y = start_point_y
    answer = []
    for i in sentence_letter:
        coord = (font.getsize(i))
        x1 = start_x
        y1 = start_y
        x2 = start_x + coord[0]
        y2 = start_y + coord[1]
        c = extend_coordinate([x1, y1, x2, y2])
        c.append(i)
        answer += [c]
        start_x += coord[0]
    return answer


def draw_border(img, pt1, pt2, color, thickness, r, d):
    x1, y1 = pt1
    x2, y2 = pt2
    len_x = x2 - x1
    len_y = y2 - y1
    # Top left
    cv2.line(img, (x1 + r, y1), (x1 + len_x // 2, y1), color, thickness)
    cv2.line(img, (x1, y1 + r), (x1, y1 + len_y // 2), color, thickness)
    cv2.ellipse(img, (x1 + r, y1 + r), (r, r), 180, 0, 90, color, thickness)
    # Top right
    cv2.line(img, (x2 - r, y1), (x2 - len_x // 2, y1), color, thickness)
    cv2.line(img, (x2, y1 + r), (x2, y1 + len_y // 2), color, thickness)
    cv2.ellipse(img, (x2 - r, y1 + r), (r, r), 270, 0, 90, color, thickness)
    # Bottom left
    cv2.line(img, (x1 + r, y2), (x1 + len_x // 2, y2), color, thickness)
    cv2.line(img, (x1, y2 - r), (x1, y2 - len_y // 2), color, thickness)
    cv2.ellipse(img, (x1 + r, y2 - r), (r, r), 90, 0, 90, color, thickness)
    # Bottom right
    cv2.line(img, (x2 - r, y2), (x2 - len_x // 2, y2), color, thickness)
    cv2.line(img, (x2, y2 - r), (x2, y2 - len_y // 2), color, thickness)
    cv2.ellipse(img, (x2 - r, y2 - r), (r, r), 0, 0, 90, color, thickness)
    return img


def resize_to_basesize(img, basewidth):
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    return img.resize((basewidth, hsize), Image.ANTIALIAS)


def create_bb(one, two, three, four):
    return {'xmax': one, 'ymax': two, 'xmin': three, 'ymin': four}


def overlap(a, b):
    DELTA = 20
    dx = min(a['xmax'], b['xmax']) - max(a['xmin'], b['xmin']) + DELTA
    dy = min(a['ymax'], b['ymax']) - max(a['ymin'], b['ymin']) + DELTA
    if (dx >= 0) and (dy >= 0):
        return True
    else:
        return False


def change_symb(suit_name):
    suit_dict = {'kresti': '♣',
                 'chervi': '♥',
                 'piki': '♠',
                 'bubi': '♦'}
    return suit_dict[suit_name]
