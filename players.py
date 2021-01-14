import random
import cv2
from PIL import ImageFont, ImageDraw, Image

import numpy as np
from utility import random_sentence, random_money, create_bb, overlap, random_fonts, \
    extend_coordinate, rgb_color


def playerbox_placeholder(font, background, overlap_list, moneybox_number):
    MONEYBOX_NUMBER = moneybox_number
    LIST_TO_OVERLAP = overlap_list
    size = np.asarray(background).shape
    AREA_X = size[0]
    AREA_Y = size[1]
    player_dict = {}
    max_attempts = 1000
    between_string = 0
    for i in range(MONEYBOX_NUMBER):

        text = random_sentence()
        text_size = font.getsize(text)

        money = random_money()
        moneybox_size = font.getsize(money)

        side_a = text_size[0]  # длинна текста
        side_b = text_size[1] + between_string + moneybox_size[1]  # ширина текста
        answer = [True]
        attempt = 0
        while True in answer:
            x = random.randint(0, AREA_X - 40 - 2 * side_a)
            y = random.randint(0, AREA_Y - 40 - 2 * side_b)
            outer_rect = create_bb(x + side_a, y + side_b, x, y)  # создаем гипотетический рект
            answer = []
            for i in LIST_TO_OVERLAP:  # прверяем на перекрытие
                answer += [overlap(i, outer_rect)]

            if True not in answer:
                # money_box_dict[text] = [money_box]
                LIST_TO_OVERLAP += [outer_rect]

                # text_bb for text
                text_bb = create_bb(outer_rect['xmax'], outer_rect['ymax'] - moneybox_size[1] - between_string, \
                                    outer_rect['xmin'], outer_rect['ymin'], )
                # money_bb for money
                money_bb = create_bb(outer_rect['xmax'], outer_rect['ymax'], \
                                     outer_rect['xmin'], outer_rect['ymin'] + between_string + text_size[1])

                player_dict[text] = [text_bb]

                player_dict[money] = [money_bb]

                break
            else:
                attempt += 1
            if attempt == max_attempts:
                print('max attempts is reached')
                break
    return (player_dict)


def create_players(background, overlap_list, string_annotate, font_size, moneybox_number):
    def sentence_coord(sentence_letter, start_point_x, end_point_y, FONT):
        start_x = start_point_x
        end_y = end_point_y
        answer = []
        for i in sentence_letter:
            coord = (FONT.getsize(i))
            x1 = start_x
            y1 = end_y - coord[1]
            x2 = start_x + coord[0]
            y2 = end_y
            c = [x1, y1, x2, y2]
            c = extend_coordinate([x1, y1, x2, y2])
            c.append(i)
            answer += [c]
            start_x += coord[0]
        return (answer)

    FONT = ImageFont.truetype(random_fonts(), font_size)
    draw = ImageDraw.Draw(background)
    placeholders = playerbox_placeholder(FONT, background, overlap_list, moneybox_number)

    for k, v in placeholders.items():
        text = k
        first_x = v[0]['xmin']
        low_y = v[0]['ymax']
        high_y = v[0]['ymin']
        c = sentence_coord(text, first_x, low_y, FONT)
        for i in c:
            money_part = [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]]
            for j in money_part:
                string_annotate += str(j).lower() + str(' ')
            string_annotate += ('\n')
        string_annotate += ('\n')
        size = FONT.getsize(text)
        area = (first_x, high_y, first_x + size[0], high_y + size[1])
        crop_back = background.crop(area)
        crop_arr = np.asarray(crop_back)
        r = rgb_color(crop_arr, 0)
        g = rgb_color(crop_arr, 1)
        b = rgb_color(crop_arr, 2)
        draw.text((first_x, high_y), text, font=FONT, fill= \
            (255 - r, 255 - g, 255 - b))

    return background, overlap_list, string_annotate


def create_fill_players(background, overlap_list, string_annotate, font_size, moneybox_number):
    # backgrounds
    green = (61, 167, 103)
    black = (21, 30, 29)
    # fonts
    white = (255, 255, 255)
    gold = (231, 231, 171)

    def sentence_coord(sentence_letter, start_point_x, end_point_y, FONT):
        start_x = start_point_x
        end_y = end_point_y
        answer = []
        for i in sentence_letter:
            coord = (FONT.getsize(i))
            x1 = start_x
            y1 = end_y - coord[1]
            x2 = start_x + coord[0]
            y2 = end_y
            c = [x1, y1, x2, y2]
            c = extend_coordinate([x1, y1, x2, y2])
            c.append(i)
            answer += [c]
            start_x += coord[0]
        return (answer)

    FONT = ImageFont.truetype(random_fonts(), font_size)

    placeholders = playerbox_placeholder(FONT, background, overlap_list, moneybox_number)

    for k, v in placeholders.items():
        text = k
        first_x = v[0]['xmin']
        low_y = v[0]['ymax']
        high_y = v[0]['ymin']
        size = FONT.getsize(text)
        color = random.choice([green, black])
        background = cv2.rectangle(np.asarray(background), (first_x, high_y), \
                                   (first_x + size[0], high_y + size[1]), color, -1)

    background = Image.fromarray(background)
    draw = ImageDraw.Draw(background)
    for k, v in placeholders.items():
        text = k
        first_x = v[0]['xmin']
        low_y = v[0]['ymax']
        high_y = v[0]['ymin']
        c = sentence_coord(text, first_x, low_y, FONT)
        for i in c:
            money_part = [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]]
            for j in money_part:
                string_annotate += str(j).lower() + str(' ')
            string_annotate += ('\n')
        string_annotate += ('\n')
        size = FONT.getsize(text)
        color = random.choice([white, gold])
        draw.text((first_x, high_y), text, font=FONT, fill=color)

    return background, overlap_list, string_annotate
