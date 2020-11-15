import pandas as pd
import matplotlib.pyplot as plt
import time
import numpy as np
import warnings
warnings.filterwarnings('ignore')

_the_cnum='0CCCGS'


def get_gender(_cnum,_cl):
    try:
        if(str(list(_cl[_cl['cnum_']==_cnum]['gender'])[0])=='F'):
            return 'Женщина'
        return 'Мужчина'
    except:
        return 'Мужчина'

def get_age(_cnum,_cl):
    try:
        return (int(list(_cl[_cl['cnum_']==_cnum]['age'])[0]))
    except:
        return 36

def get_marriage(_cnum,_cl):
    try:
        if (str(list(_cl[_cl['cnum_'] == _cnum]['married_'])[0]) == 'not_married'):
            return 'Не в браке'
        return 'В браке'
    except:
        'В браке'

def get_residence(_cnum,_cl):
    try:
        if (str(list(_cl[_cl['cnum_'] == _cnum]['residenttype'])[0]) == 'R'):
            return 'Резидент'
        return 'Приезжий'
    except:
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
        return 'Премиум'

def get_tourism (_cnum,_f_c):
    _m =_f_c['Коэффициент_туризма'].mean()
    try:
        if (float(_f_c[_f_c['cnum_']==_cnum]['Коэффициент_туризма'])<_m):
            return 'Домосед'
        return 'Турист'
    except:
        return 'Склонный к путешествиям'

def get_interests (_item,_grouped_tr):
    try:
        return list(_grouped_tr.loc[_item].index)
    except:
        return ['Еда']

def get_impulsivity(_cnum,_grouped_tr2):

    try:
        if(np.std([x[1] for x in _grouped_tr2[_grouped_tr2['cnum'] == _cnum].index]) / np.mean(
    [x[1] for x in _grouped_tr2[_grouped_tr2['cnum'] == _cnum].index])>=2):
            return 'Импульсивный'
        else:
            return 'Рассудительный'
    except:
        return 'Осторожный'


def get_versatility (_cnum,_f_c):
    _m =_f_c['Коэффициент_туризма'].mean()
    try:
        if (float(_f_c[_f_c['cnum_']==_cnum]['Коэффициент_туризма'])<_m):
            return 'Однообразный'
        return 'Разносторонний'
    except:
        return 'Умеренно-разносторонний'

def get_wealth (_cnum,_f_c):
    _m =_f_c['Состоятельность'].mean()
    try:
        if (float(_f_c[_f_c['cnum_']==_cnum]['Состоятельность'])<_m):
            return 'Экономный'
        return 'Расточительный'
    except:
        return 'Умеренно-экономный'


client_categories=pd.read_csv('docs/client_categories.csv',sep=';')
clients=pd.read_csv('docs/clients_last_2_fixed.csv', sep=';',nrows=10000)
full_clients=pd.merge(clients,client_categories,how='left',left_on='categorycode',right_on='category')
stores=pd.read_csv('docs/store_last_2.csv', error_bad_lines=False,encoding= 'windows-1251',sep=';')
transactions=pd.read_csv('docs/transactions_last_2.csv',encoding= 'windows-1251',sep=';',nrows=1000000)
mccs=pd.read_excel('docs/MCC_last.xlsx')

#для туризма
transactions['Строка']=1
clients_unique_cities=transactions.groupby('cnum')['mrchcity'].nunique()
clients_number_of_transactions=transactions.groupby('cnum')['Строка'].sum()
tourism=pd.concat([clients_unique_cities, clients_number_of_transactions], axis=1)
tourism['Коэффициент_туризма']=tourism['mrchcity']/tourism['Строка']

#для разносторонности поведения
clients_unique_stores=transactions.groupby('cnum')['mrchname'].nunique()
customer_behavior=pd.concat([clients_unique_stores, clients_number_of_transactions], axis=1)
tourism['Коэффициент_разносторонности']=customer_behavior['mrchname']/tourism['Строка']
full_clients=pd.merge(full_clients,tourism[['Коэффициент_туризма','Коэффициент_разносторонности']],how='left',left_on='cnum_',right_index=True)

#для интересов
grouped_tr=transactions[['cnum','mcc','amount']].groupby(['cnum','mcc']).sum()
grouped_tr.sort_values(by='amount',ascending=False,inplace=True)

#для импульсивности
grouped_tr2=transactions[['cnum','purchdate','amount']].groupby(['purchdate','amount']).sum()

transactions['строка']=1
grouped_tr3=transactions[['cnum','amount','строка']].groupby(['cnum']).sum()
grouped_tr3['Состоятельность']=grouped_tr3['amount']/grouped_tr3['строка']
full_clients=pd.merge(full_clients,grouped_tr3[['Состоятельность']],how='left',left_on='cnum_',right_index=True)

#1. Пол, возраст, брак, резидентство, премиальность
print('Фичи')

_gender=get_gender(_the_cnum,full_clients)
_age=get_age(_the_cnum,full_clients)
_married=get_marriage(_the_cnum,full_clients)
_residence_status=get_residence(_the_cnum,full_clients)
_premium_status=get_premium(_the_cnum,full_clients)

print(_gender)
print(_age)
print(_married)
print(_residence_status)
print(_premium_status)

#2. Туризм

print(get_tourism(_the_cnum,full_clients))
tourism_status=get_tourism(_the_cnum,full_clients)

#3. Интересы
# print(get_interests('0CCCGS',grouped_tr))
inters_mccs=get_interests(_the_cnum,grouped_tr)

_list_of_interests=[]
for item in inters_mccs:
    _list_of_interests.append(str(list(mccs[mccs['mcc']==item]['category'])[0]))

print(_list_of_interests)


#4.Импульсивность

_impulsivity=get_impulsivity(_the_cnum,grouped_tr2)
print(_impulsivity)

#5. Разносторонний/однообразный

print(get_versatility(_the_cnum,full_clients))
versatlity_status=get_versatility(_the_cnum,full_clients)

#6. Состоятельный
print(get_wealth(_the_cnum,full_clients))
wealth_status=get_versatility(_the_cnum,full_clients)

