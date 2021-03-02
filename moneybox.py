from PIL import ImageFont, ImageDraw
import random
import numpy as np
from utility import all_money_position, create_bb, overlap, random_fonts, \
    sentence_coord, rgb_color, random_text


def moneybox_placeholder(font, background, overlap_list, moneybox_number, textmode=False):
    """
    :param font: шрифт, ImageFont
    :param background: фон, PIL.Image
    :param overlap_list: список координат всех объектов, расположенных на фоне, list
    :param moneybox_number: колличество манибоксов, int
    :param textmode - generation mode - text or money
    :return: moneybox_dict - координаты ректов, в которые могут быть вписаны манибоксы

    """
    MONEYBOX_NUMBER = moneybox_number
    LIST_TO_OVERLAP = overlap_list
    size = np.asarray(background).shape
    AREA_X = size[1]
    AREA_Y = size[0]
    money_box_dict = {}
    max_attempts = 90000
    for i in range(MONEYBOX_NUMBER):
        if textmode == False:
            text = all_money_position()
        elif textmode == True:
            text = random_text()
        # text = moneyboxes[i]
        moneybox_size = font.getsize(text)
        side_a = moneybox_size[0]
        side_b = moneybox_size[1]
        answer = [True]
        attempt = 0
        while True in answer:
            try:
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
            except:
                pass
    return money_box_dict


def create_moneybox(background, overlap_list, string_annotate, font_size, moneybox_number,
                    textmode=False):
    """

    :param background:  фон, PIL.Image

    :param overlap_list: список координта всех объектов, расположенных на фоне
    :param string_annotate: список всех объектов и соответствующих им координат bounding boxes,
                                        уже расположенных на фоне, str
    :param font_size: размер шрифта в px, int
    :param moneybox_number: требуемое колличество манибоксов
    :param textmode - если True - добавляет текстовые поля, если False - добавляет 4 варианта цыфровых
    полей: инты с долларом, инты без доллара, флоты с долларом, флоты без доллара в диапазоне от
    0 до 500.
    :return:
    pil_im - фон с наложением манибоксов, PIL.Image
    list_to_overlap - список координат всех ректов, расположенных на фоне, list
    string_answer - список всех объектов и соответствующих им координат bounding boxes, str
    """
    FONT = ImageFont.truetype(random_fonts(), font_size)
    symb_size = (FONT.getsize('$'))
    max_letters = 7
    pil_im = background
    draw = ImageDraw.Draw(pil_im)
    placeholders = moneybox_placeholder(FONT, background, overlap_list, moneybox_number, textmode=textmode)
    str_answer = string_annotate
    for k, v in placeholders.items():
        text = k
        first_x = v[0]['xmin']
        first_y = v[0]['ymin']
        # print (text, first_x, first_y)
        c = sentence_coord(text, first_x, first_y, FONT)
        for i in c:
            money_part = [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]]
            for j in money_part:
                str_answer += str(j).lower() + str(' ')
            str_answer += ('\n')
        str_answer += ('\n')
        area = (first_x, first_y, first_x + symb_size[0] * max_letters, first_y + symb_size[1])
        # print(area)
        crop_back = background.crop(area)
        crop_arr = np.asarray(crop_back)
        r = rgb_color(crop_arr, 0)
        g = rgb_color(crop_arr, 1)
        b = rgb_color(crop_arr, 2)

        draw.text((first_x, first_y), text, font=FONT, fill=
        (255 - r, 255 - g, 255 - b))

    return pil_im, overlap_list, str_answer

