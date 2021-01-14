import os, random

from config import save_dir, number_of_card, number_of_images, number_of_moneybox, number_of_textbox, \
    font_size_range, number_of_players
from utility import drop_blanks, dummy
from statistic import get_statistic
from cards import create_card
from textbox import create_textbox
from moneybox import create_moneybox
from players import create_players, create_fill_players


def playground_wrapper(card_number, text_font_size, textbox_number,
                       money_font_size, moneybox_number, number_of_players):
    """ Аргументы:
        card_number - int, колличество карт на одном фоне;
        text_font_size, int , размер шрифта текстбоксов in px,
        textbox_number, int, коллличество текстбоксов на одном фоне,
        money_font_size, int, размер шрифта текстбоксов in px,
        moneybox_number, int, колличество манибоксов на одном фоне.

        При нулевом значении одного из аргументов колличества объектов,
        в последующую функцию переходити фон-заглушка, пустой список перекртий
        (overlap) и пустая строка-аннотация

    """
    if card_number == 0:
        card = [dummy, [], '']  # аргументы - заглушки
    else:
        card = create_card(card_number)
    if textbox_number == 0:
        if card_number == 0:
            textbox = [dummy, [], '']  # аргументы - заглушки
        else:
            textbox = card
    else:
        textbox = create_textbox(card[0], card[1], card[2], text_font_size, textbox_number)
    moneybox = create_moneybox(textbox[0], textbox[1], textbox[2], money_font_size, moneybox_number)
    players = create_fill_players(moneybox[0], moneybox[1], moneybox[2], money_font_size, number_of_players)
    playground = players[0]  # изображение в формате PIL.Image
    annotation = players[2]  # аннотация в формате str
    return playground, annotation


'''
Генерация изображений в колличестве number_of_images,
сохранение изображений в "номер"+jpg, аннотаций в "номер"+txt, статистики по колличеству
используемых символов в statistic.md в save_dir.
'''
for i in range(number_of_images):
    try:
        font_size = random.randint(font_size_range[0], font_size_range[1])
        test = playground_wrapper(number_of_card, font_size, number_of_textbox,
                                  font_size, number_of_moneybox, number_of_players)
        test[0].save(os.path.join(save_dir, str(i) + str('.jpg')))
        with open(os.path.join(save_dir, str(i) + '.txt'), 'w') as output_file:
            output_file.write(drop_blanks(test[1]))
        print(str(i) + ' is complete. Font size is ' + str(font_size))
    except:
        print('generation error')
    continue
print('collecting statistic...')
get_statistic(save_dir)
print('done')
