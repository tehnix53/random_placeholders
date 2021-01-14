import numpy as np
import cv2
import random
import os
from PIL import ImageFont, ImageDraw, Image

from config import *
from white_background import unique_white

# LISTS WITH MAIN FILES
backgrounds = [os.path.join(background_dir, i) for i in os.listdir(background_dir)]
rangs = [os.path.join(source_dir, i) for i in os.listdir(source_dir) if len(i) < 2]
suits = [os.path.join(source_dir, i) for i in os.listdir(source_dir) if len(i) > 2]

all_fonts = []
for root, dirs, files in os.walk(font_dir):
    for file in files:
        if file.endswith('.ttf'):
            path = os.path.join(root, file)
            all_fonts += [path]


# RANDOM VALUES TO GEN

def random_money():
    return '$' + str(round(random.uniform(0.0, 200.00), 2))


def random_white():
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


# COMMON DEF

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


def draw_border(img, pt1, pt2, color, thickness, r):
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


def set_suit(xmin, ymin, rang, suit, area, BASE_CARD_SIZE):
    coord = {}
    img1 = area
    mask = resize_to_basesize(Image.open(rang[:-3] + 'pbm'), int(BASE_CARD_SIZE / 4))
    img = resize_to_basesize(Image.open(rang), int(BASE_CARD_SIZE / 4))
    img = img.convert("RGBA")
    x1 = xmin + int(BASE_CARD_SIZE * 0.1)
    y1 = ymin + int(BASE_CARD_SIZE * 0.1)
    x2 = x1 + img.size[0]
    y2 = y1 + img.size[1]
    img1.paste(img, box=(x1, y1, x2, y2), mask=mask)
    coord['rang'] = [x1, y1, x2, y2]

    img2 = resize_to_basesize(Image.open(suit), int(BASE_CARD_SIZE / 4))
    mask = resize_to_basesize(Image.open(suit[:-3] + 'pbm'), int(BASE_CARD_SIZE / 4))
    img2 = img2.convert("RGBA")
    x1 = x1
    y1 = y2 + int(BASE_CARD_SIZE * 0.05)
    x2 = x1 + img2.size[0]
    y2 = y1 + img2.size[1]
    img1.paste(img2, box=(x1, y1, x2, y2), mask=mask)
    coord['small_suits'] = [x1, y1, x2, y2]

    diag = resize_to_basesize(Image.open(suit), int(2 * (BASE_CARD_SIZE / 4)))
    mask = resize_to_basesize(Image.open(suit[:-3] + 'pbm'), int(2 * BASE_CARD_SIZE / 4))
    diag = diag.convert('RGBA')
    x1 = x2
    y1 = y2 + int(BASE_CARD_SIZE * 0.05)
    x2 = x1 + diag.size[0]
    y2 = y1 + diag.size[1]
    img1.paste(diag, box=(x1, y1, x2, y2), mask=mask)
    coord['big_suits'] = [x1, y1, x2, y2]

    return img1, coord


def change_symb(suit_name):
    suit_dict = {'kresti': '♣',
                 'chervi': '♥',
                 'piki': '♠',
                 'bubi': '♦'}
    return suit_dict[suit_name]


# Create cards

def create_card(base_card_size, figure_numbers):
    max_attempts = 50
    background = Image.open(random_backgrounds())
    background = background.resize((640, 640), Image.ANTIALIAS)
    background = np.asarray(background)
    color = random_white()
    thickness = -1
    BASE_CARD_SIZE = base_card_size  # 60
    SIDE_X, SIDE_Y = (BASE_CARD_SIZE, int(BASE_CARD_SIZE * 3 / 2))
    AREA_X, AREA_Y = (background.shape[0], background.shape[1])
    FIGURE_NUMBERS = figure_numbers
    list_to_overlap = []

    for i in range(FIGURE_NUMBERS):
        attempts = 0
        answer = [True]
        while True in answer:
            x = random.randint(5, AREA_X - 2 * SIDE_X)
            y = random.randint(5, AREA_Y - 2 * SIDE_Y)
            start_point = (x, y)
            end_point = (x + SIDE_X, y + SIDE_Y)
            if len(list_to_overlap) == 0:
                list_to_overlap += [create_bb(end_point[0], end_point[1], start_point[0], start_point[1])]
                answer = [False]
            else:
                answer = []
                rect = create_bb(end_point[0], end_point[1], start_point[0], start_point[1])
                for i in list_to_overlap:
                    answer += [overlap(i, rect)]
                if True not in answer:
                    list_to_overlap += [rect]
                    break
                else:
                    attempts += 1
            if attempts == max_attempts:
                print('max attempts is reached')
                break

    if BASE_CARD_SIZE < 40:
        round_index = 5
    else:
        round_index = 10

    for a in (list_to_overlap):
        res = cv2.rectangle(background, (a['xmax'], a['ymax']), (a['xmin'], a['ymin']), color, thickness)

    back = Image.fromarray(res)
    string_answer = str('')
    for i in list_to_overlap:
        back = Image.fromarray(draw_border(np.asarray(back), (int(i['xmin'] - 3), int(i['ymin'] - 3)),
                                           (int(i['xmin'] + 3 + BASE_CARD_SIZE),
                                            int(i['ymin'] + 3 + int(BASE_CARD_SIZE * 3 / 2))),
                                           (color), 3, round_index))
        suit_file = random_file(suits)
        rang_file = random_file(rangs)

        midle = set_suit(i['xmin'], i['ymin'], rang_file, suit_file, back, \
                         BASE_CARD_SIZE=BASE_CARD_SIZE)
        back = midle[0]

        r_name = rang_file.split('/')[-2]
        r = extend_coordinate(midle[1]['rang'])

        rang_part = (r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r_name)

        for i in rang_part:
            string_answer += str(i) + str(' ')
        string_answer += '\n'

        s_name = change_symb(suit_file.split('/')[-2])
        s_s = extend_coordinate(midle[1]['small_suits'])
        small_suit_part = (s_s[0], s_s[1], s_s[2], s_s[3], s_s[4], s_s[5], s_s[6], s_s[7], s_name)

        for i in small_suit_part:
            string_answer += str(i) + str(' ')
        string_answer += '\n'

        b_s = extend_coordinate(midle[1]['big_suits'])
        big_suit_part = (b_s[0], b_s[1], b_s[2], b_s[3], b_s[4], b_s[5], b_s[6], b_s[7], s_name)
        for i in big_suit_part:
            string_answer += str(i) + str(' ')
        string_answer += 2 * '\n'

    return back, list_to_overlap, string_answer


# TEXTBOX

def synttext(font_size, background_image, h, w, x_start, y_start):
    symb = 'abcdefghijklmnopqrstuvwxyz1234567890$%./ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def random_symb():
        index = random.randint(0, len(symb) - 1)
        return symb[index]

    def split_sentence(sentence_len):
        permissible_numbers = [1, 2, 3, 4, 5, 6]
        a = str('')
        while len(a) < sentence_len:
            word_len = random.choice(permissible_numbers)
            for i in range(word_len):
                a += random_symb()
            a += ' '
        return a

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

    font = ImageFont.truetype(random_fonts(), font_size)
    zero_area = np.asarray(background_image)

    n = int(int(h - h * 0.20) / int(font.getsize(symb)[0] / len(symb)))
    m = int(w / int(font.getsize(symb)[1]))
    start_point = (x_start, y_start)
    all_colors = [0, 100, 200]
    end_point = (start_point[0] + h, start_point[1] + w)
    color = (random.choice(all_colors), random.choice(all_colors), random.choice(all_colors))
    thickness = 1
    res = cv2.rectangle(zero_area, start_point, end_point, color, thickness)
    pil_im = Image.fromarray(res)
    draw = ImageDraw.Draw(pil_im)
    y = start_point[1]
    str_answer = str('')

    for i in range(m):
        words = split_sentence(n)
        x = start_point[0]
        c = sentence_coord(words, x, y, font)
        for i in c:  # symbols in string
            # print (i)
            text_part = [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]]
            for j in text_part:
                # print (j)
                str_answer += str(j) + str(' ')
            str_answer += '\n'  # separate between blocks
        str_answer += '\n'
        draw.text((x, y), words, font=font, fill=
        (random.choice(all_colors), random.choice(all_colors),
         random.choice(all_colors), random.choice(all_colors)))
        y += int(font.getsize(symb)[1])

    cv2_im = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)
    return Image.fromarray(cv2_im), str_answer


def create_textbox(background, overlap_list, string_annotate, font_size, textbox_number):
    TEXTBOX_NUMBER = textbox_number
    LIST_TO_OVERLAP = overlap_list
    size = np.asarray(background).shape
    AREA_X = size[0]
    AREA_Y = size[1]
    max_attempts = 1000
    text_box_list = []
    for i in range(TEXTBOX_NUMBER):
        answer = [True]
        attempt = 0
        while True in answer:
            side_a = random.randint(50, 250)
            side_b = random.randint(100, 250)
            x = random.randint(0, AREA_X - 40 - side_a)
            y = random.randint(0, AREA_Y - 40 - side_b)
            text_box = create_bb(x + side_a, y + side_b, x, y)
            answer = []
            for i in LIST_TO_OVERLAP:
                answer += [overlap(i, text_box)]
            if True not in answer:
                text_box_list += [text_box]
                LIST_TO_OVERLAP += [text_box]
                break
            else:
                attempt += 1
            if attempt == max_attempts:
                print('max attempts is reached')
                break
    string_answer = string_annotate
    for s in text_box_list:
        back_add = synttext(font_size, background, (s['xmax'] - s['xmin']),
                            (s['ymax'] - s['ymin']), s['xmin'], s['ymin'])
        background = back_add[0]
        string_answer += back_add[1]
    try:
        return back_add[0], LIST_TO_OVERLAP, string_answer
    except UnboundLocalError:
        'maximum attempts is reached'
        return background, LIST_TO_OVERLAP, string_answer


# MONEYBOX


def moneybox_placeholder(font, background, overlap_list, moneybox_number):
    MONEYBOX_NUMBER = moneybox_number
    LIST_TO_OVERLAP = overlap_list
    size = np.asarray(background).shape
    AREA_X = size[0]
    AREA_Y = size[1]
    money_box_dict = {}
    max_attempts = 1000
    for i in range(MONEYBOX_NUMBER):
        text = random_money()
        moneybox_size = font.getsize(text)
        side_a = moneybox_size[0]
        side_b = moneybox_size[1]
        answer = [True]
        attempt = 0
        while True in answer:
            x = random.randint(0, AREA_X - 40 - 2 * side_a)
            y = random.randint(0, AREA_Y - 40 - 2 * side_b)
            money_box = create_bb(x + side_a, y + side_b, x, y)
            answer = []
            for i in LIST_TO_OVERLAP:
                answer += [overlap(i, money_box)]
            if True not in answer:
                money_box_dict[text] = [money_box]
                LIST_TO_OVERLAP += [money_box]
                break
            else:
                attempt += 1
            if attempt == max_attempts:
                print('max attempts is reached')
                break
    return money_box_dict


def create_moneybox(background, overlap_list, string_annotate, font_size, moneybox_number):
    FONT = ImageFont.truetype(random_fonts(), font_size)
    all_colors = [0, 100, 255]
    pil_im = background
    draw = ImageDraw.Draw(pil_im)
    placeholders = moneybox_placeholder(FONT, background, overlap_list, moneybox_number)
    str_answer = string_annotate
    for k, v in placeholders.items():
        text = k
        first_x = v[0]['xmin']
        first_y = v[0]['ymin']
        c = sentence_coord(text, first_x, first_y, FONT)
        for i in c:
            money_part = [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]]
            for j in money_part:
                str_answer += str(j) + str(' ')
            str_answer += '\n'
        str_answer += '\n'

        draw.text((first_x, first_y), text, font=FONT, fill=
        (random.choice(all_colors), random.choice(all_colors),
         random.choice(all_colors), random.choice(all_colors)))

    cv2_im = Image.fromarray(cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR))

    return cv2_im, overlap_list, str_answer
