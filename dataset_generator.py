import os
import tqdm
import random
from PIL import Image
from utility import random_backgrounds
from config import *
from utility import drop_blanks
from statistic import get_statistic
from cards import create_card
from moneybox import create_moneybox


def playground_wrapper(card_number, text_font_size, textbox_number,
                       money_font_size, moneybox_number):
    if card_number != 0:
        dummy = create_card(card_number, background_size[0],
                            background_size[1])
    else:
        dummy = (Image.open(random_backgrounds()).
                 resize((background_size[0], background_size[1]),
                        Image.ANTIALIAS), [], '')
    if textbox_number != 0:
        dummy = create_moneybox(dummy[0], dummy[1], dummy[2], text_font_size,
                                textbox_number, textmode=True)
    if moneybox_number != 0:
        dummy = create_moneybox(dummy[0], dummy[1], dummy[2], money_font_size,
                                moneybox_number, textmode=False)
    playground = dummy[0]  # изображение в формате PIL.Image
    annotation = dummy[2]  # аннотация в формате str

    return playground, annotation


print('image generation starting...')
for i in tqdm.tqdm(range(number_of_images)):
    font_size = random.randint(font_size_range[0], font_size_range[1])
    test = playground_wrapper(number_of_card, font_size, number_of_textbox,
                              font_size, number_of_moneybox)
    test[0].save(os.path.join(SAVE_PATH, str(i) + str('.webp')))
    with open(os.path.join(SAVE_PATH, str(i) + '.txt'), 'w') as output_file:
        output_file.write(drop_blanks(test[1]))

print('collecting statistic...')
get_statistic(SAVE_PATH)
print('done')
