from persiantools.jdatetime import JalaliDate
import pandas as pd
import math
from openpyxl import load_workbook
from datetime import datetime

# custom modules
from api_module import *
from components import *

FILE_PATH = 'Financial-1402-1.xlsx'


def main():
    # get inputs from user
    res = question_Box('save or cost? (save/cost) ', q1=['s','save'], q2=['c','cost'])
    money = int(input("enter amount of money ? "))
    log_decs = input("enter description : ")
    program(res,money,log_decs)


def SELECT_TABLE():
    sheet = {'cost':2, 'cost_log':3, 'save':0, 'save_log':1, 'total':4}
    df = {}
    for key in sheet:
        df[key] = pd.read_excel(FILE_PATH, sheet_name=sheet[key])
    return df

  

def program(res,money,log_decs):
    # get date now
    date_now = JalaliDate.today()

    # week of month number
    week_of_month = math.ceil(date_now.day / 7)

    # day name
    get_day = date_now.strftime('%A')
    # day id
    get_day_id = date_now.weekday()
    # month name
    get_month = date_now.strftime('%B')
    # month id
    get_month_id = date_now.month
    # hour & minute
    time = datetime.now().strftime("%H:%M")
    # jalali date (1402/1/1)
    jalali_date = date_now.strftime("%Y/%m/%d")
    # year
    year = date_now.year
    
    df = SELECT_TABLE()
    
    if res == 1 :
        query = ((df['save']['month_id'] == get_month_id) & (df['save']['day'] == date_now.day))
        # check if row exist in db or not
        if(query.any()):
            update_db(
                db=df['save'],
                log=df['save_log'],
                query=query,
                db_sheet_name='save',
                log_sheet_name='save_log',
                money = money,
                time = time,
                log_decs = log_decs,
                FILE_PATH = FILE_PATH,
                get_day = get_day,
                get_month = get_month,
                today = date_now.day,
                pd = pd,
                df_total = df['total'],
                get_month_id = get_month_id,
                year = year,
                SELECT_TABLE_func = SELECT_TABLE
            )
        else:
            # there is not any save data yet for today
            create_db(
                db=df['save'],
                log=df['save_log'],
                query=query,
                db_sheet_name='save',
                log_sheet_name='save_log',
                money = money,
                time = time,
                log_decs = log_decs,
                FILE_PATH = FILE_PATH,
                get_day = get_day,
                get_month = get_month,
                today = date_now.day,
                pd = pd,
                get_month_id = get_month_id,
                week_of_month = week_of_month,
                get_day_id = get_day_id,
                jalali_date = jalali_date,
                df_total = df['total'],
                year = year,
                SELECT_TABLE_func = SELECT_TABLE
                
            )
    # todo
    else :
        query = ((df['cost']['month_id'] == get_month_id) & (df['cost']['day'] == date_now.day))
        # check if row exist in db or not
        if(query.any()):
            update_db(
                db=df['cost'],
                log=df['cost_log'],
                query=query,
                db_sheet_name='cost',
                log_sheet_name='cost_log',
                money = money,
                time = time,
                log_decs = log_decs,
                FILE_PATH = FILE_PATH,
                get_day = get_day,
                get_month = get_month,
                today = date_now.day,
                pd = pd,
                df_total = df['total'],
                get_month_id = get_month_id,
                year = year,
                SELECT_TABLE_func = SELECT_TABLE
                
            )
        else:
            # there is not any cost data yet for today
            create_db(
                db=df['cost'],
                log=df['cost_log'],
                query=query,
                db_sheet_name='cost',
                log_sheet_name='cost_log',
                money = money,
                time = time,
                log_decs = log_decs,
                FILE_PATH = FILE_PATH,
                get_day = get_day,
                get_month = get_month,
                today = date_now.day,
                pd = pd,
                get_month_id = get_month_id,
                week_of_month = week_of_month,
                get_day_id = get_day_id,
                jalali_date = jalali_date,
                df_total = df['total'],
                year = year,
                SELECT_TABLE_func = SELECT_TABLE
            )
            
if __name__ == '__main__':
    main()