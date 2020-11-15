from flask import redirect, render_template, request, make_response, send_file
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw 
import base64
import numpy
import os
import warnings
import random

from .utils import Colors, draw_text, draw_elliplse, draw_rect_w_gradient, get_categories
from . import bp

scale = 0.3

interests = dict()
goods = dict()


@bp.route('/client-info/<client_id>')
def get_client_info(client_id):
    path = os.path.join('app', 'service', 'img4.png')
    print('Starting...')

    categories = get_categories(client_id)
    versatlity_status = categories['versatlity_status']
    _impulsivity = categories['_impulsivity']
    tourism_status = categories['tourism_status']
    _gender = categories['_gender']
    _age = str(categories['_age'])
    _married = categories['_married']
    _residence_status = categories['_residence_status']
    _premium_status = categories['_premium_status']
    _list_of_interests = categories['_list_of_interests']
    wealth_status = categories['wealth_status']

    versatlity_status = categories['versatlity_status']
    _impulsivity = categories['_impulsivity']

    im = Image.open(path)

    width, height = im.size

    im = im.resize((int(width*scale), int(height*scale)), Image.ANTIALIAS)

    data = []

    list_goods=['Мясные блюда','Музыка Верди','Книги Коэльо','Караоке','Золото','Полевые цветы','Раболовные снасти',
            'Гольф','Плавание','Крепкий кофе','Театр Кабуки','Чайные церемонии','Китайская культура','Андройд',
            'Северное сияние','Математический анализ','Зоопарк','Первый канал','Тикток','Предпринимательство']
    _r1=random.choice(list_goods)
    list_goods.remove(_r1)
    _r2=random.choice(list_goods)
    list_goods.remove(_r2)
    _r3=random.choice(list_goods)

    goodies = [_r1, _r2, _r3]
    cached_goods = goods.get(client_id)
    if cached_goods:
        goodies = cached_goods

    if not cached_goods:
        goods[client_id] = [_r1, _r2, _r3]


    # draw_elliplse(im, (31, 334, 51, 354))
    # draw_elliplse(im, (31, 370, 51, 390))

    # im = draw_rect_w_gradient(im)

    draw_text(im, client_id, (263, 65), 'bold', color=Colors.yellow, font_size=20)

    draw_text(im, _age, (120, 173), 'bold', color=Colors.yellow)
    draw_text(im, _gender[0], (264, 173), 'bold', color=Colors.yellow)
    draw_text(im, _married, (220, 215), 'bold', color=Colors.yellow)
    draw_text(im, _residence_status, (207, 258), 'bold', color=Colors.yellow)
    draw_text(im, _premium_status, (195, 299), 'bold', color=Colors.yellow, font_size=12)

    # draw_text(im, tourism_status, (225, 338), 'bold', color=Colors.yellow)
    # draw_text(im, "стабильность", (260, 374), 'light', font_size=13, color=Colors.yellow)

    # draw_text(im, "авиабилеты", (55, 497), 'light')
    # draw_text(im, "билеты в горнолыжный комплекс", (55, 522), 'light')
    # draw_text(im, "спортивное питание", (55, 547), 'light')
    # ''
    # draw_text(im, "умеренность", (55, 600), 'light')
    # draw_text(im, "планомерность", (55, 625), 'light')
    print(_list_of_interests)
    bot_block_x = 86
    # List of interests
    print(interests)
    cached = interests.get(client_id)
    if cached:
        _list_of_interests = cached
    if _list_of_interests:
        draw_text(im, _list_of_interests[0], (bot_block_x, 422), 'medium', color=Colors.yellow)
    # draw_text(im, goodies[1], (80, 488), 'light')
    draw_text(im, versatlity_status, (bot_block_x, 515), 'medium', color=Colors.yellow)
    draw_text(im, _impulsivity, (bot_block_x, 543), 'medium', color=Colors.yellow)
    draw_text(im, tourism_status, (bot_block_x, 573), 'medium', color=Colors.yellow)
    draw_text(im, wealth_status, (bot_block_x, 603), 'medium', color=Colors.yellow)
    # draw_text(im, goodies[2], (80, 552), 'light')
    # draw_text(im, goodies[3], (80, 580), 'light')

    if not cached:
        interests[client_id] = _list_of_interests

    print(_r1)
    rec_h = 604
    print(_residence_status)
    print([a == 'N/A' for a in [_premium_status, _residence_status, _married, _gender ]])
    if any([a == 'N/A' for a in [_premium_status, _residence_status, _married, _gender ]]):
         draw_text(im, 'N/A', (bot_block_x, rec_h+108), 'medium', color=Colors.yellow)
    else:
        draw_text(im, goodies[0], (bot_block_x, rec_h+108), 'medium', color=Colors.yellow)
        draw_text(im, goodies[1], (bot_block_x, rec_h+136), 'medium', color=Colors.yellow)
        draw_text(im, goodies[2], (bot_block_x, rec_h+166), 'medium', color=Colors.yellow)
    # draw_text(im, goodies[3], (80, 769), 'light')

    
    # draw = ImageDraw.Draw(im)
    # # font = ImageFont.truetype(<font-file>, <font-size>)
    # font = ImageFont.truetype("HelveticaNeueCyr-Bold.ttf", 16)
    # # draw.text((x, y),"Sample Text",(r,g,b))
    # draw.text((50, 50),"Wassup",(255,255,255), font=font)

    buffered = BytesIO()
    im.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())

    print('Done')

    return img_str
