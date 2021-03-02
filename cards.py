import random, os, cv2
from PIL import Image
import numpy as np
from utility import random_backgrounds, random_white, create_bb,\
    overlap,draw_border, random_file, small_list, BIG_SUITS, list_dir,\
    extend_coordinate, rangs




def set_suit(xmin, ymin, rang, small_suit, big_suit, area):
    '''
    :param xmin: координата начальной точки по оси х, int
    :param ymin: координтата начальной точки по оси y, int
    :param rang: путь до файла ранга, os.path
    :param small_suit: путь до файла с малой мастью, os.path
    :param big_suit: путь до файла с большой мастью, os.path
    :param area: фон, PIL.Image
    :return: area - фон с наложением мастей и рангов, PIL.Image
            coord - координаты ранга, большой и малой масти, dict
    '''

    def get_mask(path_to_file):
        pil_mask = Image.open(path_to_file[:-3] + 'pbm')
        pil_img = Image.open(path_to_file)
        pil_img = pil_img.convert("RGBA")
        return pil_mask, pil_img

    coord = {}
    overlap_between_suits = 10

    mask, rang_img = get_mask(rang)
    x1 = xmin
    y1 = ymin
    x2 = x1 + rang_img.size[0]
    y2 = y1 + rang_img.size[1]
    area.paste(rang_img, box=(x1, y1, x2, y2), mask=mask)
    coord['rang'] = [x1, y1, x2, y2]

    mask, small_img = get_mask(small_suit)
    x1 = x1 + int(rang_img.size[0] / 2) - int(small_img.size[0] / 2)
    y1 = y2
    x2 = x1 + small_img.size[0]
    y2 = y1 + small_img.size[1]
    area.paste(small_img, box=(x1, y1, x2, y2), mask=mask)
    coord['small_suits'] = [x1, y1, x2, y2]

    mask, big_img = get_mask(big_suit)
    x1 = x2
    y1 = y2 - overlap_between_suits
    x2 = x1 + big_img.size[0]
    y2 = y1 + big_img.size[1]
    area.paste(big_img, box=(x1, y1, x2, y2), mask=mask)
    coord['big_suits'] = [x1, y1, x2, y2]

    return area, coord


def create_card(figure_numbers, size_x, size_y):
    '''
    :param figure_numbers: число карт, int
    :return:
    pil_img - фон с наложением карт, PIL.Image
    list_to_overlap - список координат всех карт, расположенных на фоне, list
    string_answer - список всех мастей и рангов и соответствующих им координат bounding boxes, str
    '''

    max_attempts = 300
    background = Image.open(random_backgrounds())
    background = background.resize((size_x, size_y), Image.ANTIALIAS)
    background = np.asarray(background)
    color = random_white()
    thickness = -1
    round_index = 10
    BASE_CARD_SIZE = 60
    SIDE_X, SIDE_Y = (BASE_CARD_SIZE, int(BASE_CARD_SIZE * 5 / 4))
    AREA_X, AREA_Y = (background.shape[1], background.shape[0])
    FIGURE_NUMBERS = figure_numbers
    list_to_overlap = []
    # list_to_overlap+=[create_bb(1024,640,0,0)]
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

    for a in (list_to_overlap):
        res = cv2.rectangle(background, (a['xmax'], a['ymax']), (a['xmin'], a['ymin']), color, thickness)

    pil_img = Image.fromarray(res)
    string_answer = str('')
    for i in list_to_overlap:

        small_suit_file = random_file(small_list) # list
        suit = small_suit_file.split('/')[-2]
        big_pair_list = [i for i in list_dir(os.path.join(BIG_SUITS, suit)) if i.endswith('.jpg')] # big suit folder
        index = random.randint(0, len(big_pair_list) - 1)
        big_suit_file = big_pair_list[index]
        rang_file = random_file(rangs) # list with all tang files
        size = (np.asarray(Image.open(big_suit_file)).shape[0])
        # BASE_CARD_SIZE = size*2
        pil_img = Image.fromarray(draw_border(np.asarray(pil_img), (int(i['xmin'] - 3), int(i['ymin'] - 3)),
                                              (int(i['xmin'] + 3 + BASE_CARD_SIZE),
                                               int(i['ymin'] + 3 + int(BASE_CARD_SIZE * 5 / 4))),
                                              (color), 3, round_index, 0))


        midle = set_suit(i['xmin'], i['ymin'] - 5, rang_file, small_suit_file, big_suit_file, pil_img)
        pil_img = midle[0]

        r_name = rang_file.split('/')[-2]
        r = extend_coordinate(midle[1]['rang'])

        rang_part = (r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r_name)

        for i in rang_part:
            string_answer += str(i) + str(' ')
        string_answer += '\n'

        s_name = suit
        s_s = extend_coordinate(midle[1]['small_suits'])
        small_suit_part = (s_s[0], s_s[1], s_s[2], s_s[3], s_s[4], s_s[5], s_s[6], s_s[7], s_name)

        for i in small_suit_part:
            string_answer += str(i) + str(' ')
        string_answer += 2 * '\n'  # !!!!!!

        b_s = extend_coordinate(midle[1]['big_suits'])
        big_suit_part = (b_s[0], b_s[1], b_s[2], b_s[3], b_s[4], b_s[5], b_s[6], b_s[7], s_name)
        for i in big_suit_part:
            string_answer += str(i) + str(' ')
        string_answer += 2 * '\n'

    return pil_img, list_to_overlap, string_answer


