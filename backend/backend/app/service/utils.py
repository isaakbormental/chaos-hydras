from PIL import Image, ImageFont, ImageDraw
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline
import time
import numpy as np
import warnings
warnings.filterwarnings('ignore')

from app import data

# _the_cnum='0CCCGS'
return_na = True

def get_gender(_cnum,_cl):
    try:
        if(str(list(_cl[_cl['cnum_']==_cnum]['gender'])[0])=='F'):
            return 'Женщина'
        return 'Мужчина'
    except:
        if return_na:
            return 'N/A'
        return 'Мужчина'

def get_age(_cnum,_cl):
    try:
        return (int(list(_cl[_cl['cnum_']==_cnum]['age'])[0]))
    except:
        if return_na:
            return 0
        return 36

def get_marriage(_cnum,_cl):
    try:
        if (str(list(_cl[_cl['cnum_'] == _cnum]['married_'])[0]) == 'not_married'):
            return 'Не в браке'
        return 'В браке'
    except:
        if return_na:
            return 'N/A'
        return 'В браке'

def get_residence(_cnum,_cl):
    try:
        if (str(list(_cl[_cl['cnum_'] == _cnum]['residenttype'])[0]) == 'R'):
            return 'Резидент'
        return 'Приезжий'
    except:
        if return_na:
            return 'N/A'
        return 'Резидент'
    # return (str(list(_cl[_cl['cnum_']==_cnum]['residenttype'])[0]))

def get_premium(_cnum,_cl):
    try:
        _proto_premium=str(list(_cl[_cl['cnum_']==_cl]['description'])[0])
        if 'Affluent' in _proto_premium:
            return 'VIP'
        if 'High income' in _proto_premium:
            return 'Премиум'
        if 'Premium' in _proto_premium:
            return 'Премиум'
        return 'Без премиального статуса'
    except:
        if return_na:
            return 'N/A'
        return 'Премиум'

def get_tourism (_cnum,_f_c):
    _m =_f_c['Коэффициент_туризма'].mean()
    try:
        if (float(_f_c[_f_c['cnum_']==_cnum]['Коэффициент_туризма'])<_m):
            return 'Домосед'
        return 'Турист'
    except:
        if return_na:
            return 'N/A'
        return 'Склонный к путешествиям'

def get_interests (_item,_grouped_tr):
    try:
        return list(_grouped_tr.loc[_item].index)
    except:
        if return_na:
            return ['N/A']
        return ['Еда']

def get_impulsivity(_cnum,_grouped_tr2):

    try:
        if(np.std([x[1] for x in _grouped_tr2[_grouped_tr2['cnum'] == _cnum].index]) / np.mean(
    [x[1] for x in _grouped_tr2[_grouped_tr2['cnum'] == _cnum].index])>=2):
            return 'Импульсивный'
        else:
            return 'Рассудительный'
    except:
        if return_na:
            return 'N/A'
        return 'Осторожный'


def get_versatility (_cnum,_f_c):
    _m =_f_c['Коэффициент_туризма'].mean()
    try:
        if (float(_f_c[_f_c['cnum_']==_cnum]['Коэффициент_туризма'])<_m):
            return 'Однообразный'
        return 'Разносторонний'
    except:
        if return_na:
            return 'N/A'
        return 'Умеренно-разносторонний'

def get_wealth (_cnum,_f_c):
    _m =_f_c['Состоятельность'].mean()
    try:
        if (float(_f_c[_f_c['cnum_']==_cnum]['Состоятельность'])<_m):
            return 'Экономный'
        return 'Расточительный'
    except:
        if return_na:
            return 'N/A'
        return 'Умеренно-экономный'

class Colors:
    yellow = (254,230,0)
    white = (255, 255, 255)
    grey = (30, 47, 65)


def draw_text(image, text, position: tuple, font_type, color=Colors.white, font_size=16) -> None:
    draw = ImageDraw.Draw(image)
    # font = ImageFont.truetype(<font-file>, <font-size>)
    font = ImageFont.truetype(f"HelveticaNeueCyr-{font_type.capitalize()}.ttf", font_size)
    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text(position, text, color, font=font)


def draw_elliplse(image, position):
    draw = ImageDraw.Draw(image)
    draw.ellipse(position, fill = (255,255,255))


def draw_rect_w_gradient(im, pos=None):
    def interpolate(f_co, t_co, interval):
        det_co =[(t - f) / interval for f , t in zip(f_co, t_co)]
        for i in range(interval):
            yield [round(f + det * i) for f, det in zip(f_co, det_co)]

    gradient = Image.new('RGBA', im.size, color=0)
    draw = ImageDraw.Draw(gradient)

    f_co = (13, 255, 154)
    t_co = (4, 128, 30)
    for i, color in enumerate(interpolate(f_co, t_co, im.width * 2)):
        draw.line([(i, 0), (0, i)], tuple(color), width=1)

    return Image.alpha_composite(gradient, im)

def get_categories(_the_cnum: str):
    return_dict = {}

    # print(data)

    #1. Пол, возраст, брак, резидентство, премиальность
    print('Фичи')
    # print(data)
    try:
        full_clients = data['full_clients']
        grouped_tr = data['grouped_tr']
        mccs = data['mccs']
        grouped_tr2 = data['grouped_tr2']
        grouped_tr3 = data['grouped_tr3']

        _gender=get_gender(_the_cnum,full_clients)
        _age=get_age(_the_cnum,full_clients)
        _married=get_marriage(_the_cnum,full_clients)
        _residence_status=get_residence(_the_cnum,full_clients)
        _premium_status=get_premium(_the_cnum,full_clients)

                # print(_gender)
                # print(_age)
                # print(_married)
                # print(_residence_status)
                # print(_premium_status)

                #2. Туризм

                # print(get_tourism(_the_cnum,full_clients))
        tourism_status=get_tourism(_the_cnum,full_clients)

                #3. Интересы
                # print(get_interests('0CCCGS',grouped_tr))
        inters_mccs=get_interests(_the_cnum,grouped_tr)

        _list_of_interests=[]
        try:
            for item in inters_mccs:
                _list_of_interests.append(str(list(mccs[mccs['mcc']==item]['category'])[0]))
        except:
            _list_of_interests=['food', 'clothes', 'beauty']
                # print(_list_of_interests)

                #4.Импульсивность

        _impulsivity=get_impulsivity(_the_cnum,grouped_tr2)
                # print(_impulsivity)

                #5. Разносторонний/однообразный

                # print(get_versatility(_the_cnum,full_clients))
        versatlity_status=get_versatility(_the_cnum,full_clients)

        wealth_status=get_wealth(_the_cnum,full_clients)

        print(_gender)
        print(_age)
        print(_married)
        print(_residence_status)
        print(_premium_status)

        return_dict['versatlity_status'] = versatlity_status #
        return_dict['_impulsivity'] = _impulsivity #
        return_dict['tourism_status'] = tourism_status
        return_dict['_gender'] = _gender
        return_dict['_age'] = _age
        return_dict['_married'] = _married
        return_dict['_residence_status'] = _residence_status
        return_dict['_premium_status'] = _premium_status
        return_dict['wealth_status'] = wealth_status #
        return_dict['_list_of_interests'] = _list_of_interests
    except Exception as e:
        print(e)
        return_dict['versatlity_status'] = 'N/A'
        return_dict['_impulsivity'] = 'N/A'
        return_dict['tourism_status'] = 'N/A'
        return_dict['_gender'] = 'N/A'
        return_dict['_age'] = 'N/A'
        return_dict['_married'] = 'N/A'
        return_dict['_residence_status'] = 'N/A'
        return_dict['_premium_status'] = 'N/A'
        return_dict['_list_of_interests'] = []

    return return_dict