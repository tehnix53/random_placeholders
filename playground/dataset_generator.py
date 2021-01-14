import os, random
from config import save_dir, number_of_card, number_of_images, number_of_moneybox, number_of_textbox, \
    font_size_range, base_card_size
from utility import drop_blanks, create_card, create_moneybox, create_textbox


def playground_wrapper(card_base_size, card_number, text_font_size, textbox_number,
                       money_font_size, moneybox_number):
    card = create_card(card_base_size, card_number)
    textbox = create_textbox(card[0], card[1], card[2], text_font_size, textbox_number)
    moneybox = create_moneybox(textbox[0], textbox[1], textbox[2], money_font_size, moneybox_number)
    playground = moneybox[0]
    annotation = moneybox[2]
    return playground, annotation


for i in range(number_of_images):
    try:
        font_size = random.randint(font_size_range[0],font_size_range[1])
        test = playground_wrapper(base_card_size, number_of_card, font_size, number_of_textbox,
                                  font_size, number_of_moneybox)
        test[0].save(os.path.join(save_dir, str(i) + str('.jpg')))
        with open(os.path.join(save_dir, str(i) + '.txt'), 'w') as output_file:
            output_file.write(drop_blanks(test[1]))
        print(str(i) + ' is complete. Font size is ' + str(font_size))
    except:
        print('generation error')
    continue
