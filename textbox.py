import random, cv2, string
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from utility import extend_coordinate, overlap, random_fonts, rgb_color, create_bb


def synttext(font_size, background_image, h, w, x_start, y_start):
    """

    :param font_size: размер шрифта, px, int
    :param background_image: фон, PIL.Image
    :param h: высота ректа с текстом, int
    :param w: ширина ректа с текстом, int
    :param x_start: начальная координата x, int
    :param y_start: начальная координта y, int
    :return:
    pil_img - фон с наложением ректа с текстом, PIL.Image
    str_answer - символы текста и соответствующие им координтаы bounding boxes, dict

    """
    symb = string.ascii_letters + string.digits + '$%./'

    def random_symb():
        """
        :return: произвольный единичный символ, str
        """
        index = random.randint(0, len(symb) - 1)
        return symb[index]

    def split_sentence(sentence_len):
        """
        :param sentence_len: длинна предложения, int
        :return: возвращает предложение заданой длинны из рандомных символов, str
        """
        permissible_numbers = [1, 2, 3, 4, 5, 6]
        a = str('')
        while len(a) < sentence_len:
            word_len = random.choice(permissible_numbers)
            for i in range(word_len):
                a += random_symb()
            a += ' '
        return a

    def sentence_coord(some_sentence, start_point_x, start_point_y, font):
        """
        :param some_sentence: предложение, str
        :param start_point_x: начальная координта х, int
        :param start_point_y: начальная координта у, int
        :param font: шрифт, ImageFont
        :return: answer - список списков с координатами всех букв предложения, list
        """
        start_x = start_point_x
        start_y = start_point_y
        answer = []
        for i in some_sentence:
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
    symb_size = (font.getsize(symb))
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
        for i in c:
            text_part = [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]]
            for j in text_part:
                str_answer += str(j).lower() + str(' ')
            str_answer += '\n'
        str_answer += '\n'
        area = (x, y, x + h, y + symb_size[1])
        crop_back = background_image.crop(area)
        crop_arr = np.asarray(crop_back)
        r = rgb_color(crop_arr, 0)
        g = rgb_color(crop_arr, 1)
        b = rgb_color(crop_arr, 2)
        draw.text((x, y), words, font=font, fill=(255 - r, 255 - g, 255 - b))
        y += int(font.getsize(symb)[1])

    return pil_im, str_answer


def create_textbox(background, list_to_overlap, string_annotate, font_size, textbox_number):
    """

    :param background:  фон, PIL.Image
    :param list_to_overlap: список координта всех объектов, расположенных на фоне
    :param string_annotate: список всех объектов и соответствующих им координат bounding boxes,
                                        уже расположенных на фоне, str
    :param font_size: размер шрифта в px, int
    :param textbox_number: требуемое колличество текстбоксов
    :return:
    background - фон с наложением текстбоксов, PIL.Image
    list_to_overlap - список координат всех ректов, расположенных на фоне, list
    string_answer - список всех объектов и соответствующих им координат bounding boxes, str
    """
    TEXTBOX_NUMBER = textbox_number
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
            for i in list_to_overlap:
                answer += [overlap(i, text_box)]
            if True not in answer:
                text_box_list += [text_box]
                list_to_overlap += [text_box]
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
        return back_add[0], list_to_overlap, string_answer
    except UnboundLocalError:
        'maximum attempts is reached'
        return background, list_to_overlap, string_answer
