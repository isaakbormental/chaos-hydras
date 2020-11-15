import os
from flask import Flask
import pandas as pd
# from flask_redis import FlaskRedis
# from config import Config, TestConfig


# redis_store = FlaskRedis()
data = dict()

# N_ROWS_TRANSACTIONS = 1000000
# N_ROWS_CLIENTS = 10000

N_ROWS_TRANSACTIONS = 1000
N_ROWS_CLIENTS = 1000


def init():
    print('Initializing')
    client_categories=pd.read_csv('data/client_categories.csv',sep=';')
    clients=pd.read_csv('data/clients_last_2_fixed.csv', sep=';',nrows=N_ROWS_CLIENTS)
    full_clients=pd.merge(clients,client_categories,how='left',left_on='categorycode',right_on='category')
    stores=pd.read_csv('data/store_last_2.csv', error_bad_lines=False,encoding= 'windows-1251',sep=';')
    transactions=pd.read_csv('data/transactions_last_2.csv',encoding= 'windows-1251',sep=';',nrows=N_ROWS_TRANSACTIONS)
    print('Transactions Loaded')
    mccs=pd.read_excel('data/MCC_last.xlsx')

    #для туризма
    transactions['Строка']=1
    clients_unique_cities=transactions.groupby('cnum')['mrchcity'].nunique()
    clients_number_of_transactions=transactions.groupby('cnum')['Строка'].sum()
    tourism=pd.concat([clients_unique_cities, clients_number_of_transactions], axis=1)
    tourism['Коэффициент_туризма']=tourism['mrchcity']/tourism['Строка']
    print('Check 1')

    #для разносторонности поведения
    clients_unique_stores=transactions.groupby('cnum')['mrchname'].nunique()
    customer_behavior=pd.concat([clients_unique_stores, clients_number_of_transactions], axis=1)
    tourism['Коэффициент_разносторонности']=customer_behavior['mrchname']/tourism['Строка']
    full_clients=pd.merge(full_clients,tourism[['Коэффициент_туризма','Коэффициент_разносторонности']],how='left',left_on='cnum_',right_index=True)
    print('Check 2')
    #для интересов
    grouped_tr=transactions[['cnum','mcc','amount']].groupby(['cnum','mcc']).sum()
    grouped_tr.sort_values(by='amount',ascending=False,inplace=True)

    #для импульсивности
    grouped_tr2=transactions[['cnum','purchdate','amount']].groupby(['purchdate','amount']).sum()

    transactions['строка']=1
    grouped_tr3=transactions[['cnum','amount','строка']].groupby(['cnum']).sum()
    grouped_tr3['Состоятельность']=grouped_tr3['amount']/grouped_tr3['строка']
    print('Check 3')
    full_clients=pd.merge(full_clients,grouped_tr3[['Состоятельность']],how='left',left_on='cnum_',right_index=True)
    
    data['client_categories'] = client_categories
    data['clients'] = clients
    data['full_clients'] = full_clients
    data['stores'] = stores
    data['transactions'] = transactions
    data['mccs'] = mccs
    data['clients_unique_cities'] = clients_unique_cities

    data['clients_number_of_transactions'] = clients_number_of_transactions
    data['tourism'] = tourism
    data['clients_unique_stores'] = clients_unique_stores
    data['customer_behavior'] = customer_behavior
    data['full_clients'] = full_clients
    data['grouped_tr'] = grouped_tr
    data['grouped_tr2'] = grouped_tr2
    data['grouped_tr3'] = grouped_tr3

    # transactions['строка']=1
    # grouped_tr4=transactions[['cnum','строка']].groupby(['cnum']).sum()
    # grouped_tr4.sort_values(by=['строка'],ascending=False,inplace=True)
    # print(list(grouped_tr4.index)[:20])

    print(clients.head())

    print('Init done')


def create_app():
    init()
    app = Flask(__name__)
    from .service import bp
    app.register_blueprint(bp)
    return app
