from persiantools.jdatetime import JalaliDate
import pandas as pd
import math
from openpyxl import load_workbook
from datetime import datetime

# custom modules
from api_module import *
from components import *

FILE_PATH = 'Financial-1402-1.xlsx'


sheet = {'cost':2, 'cost_log':3, 'save':0, 'save_log':1}
df = {}
for key in sheet:
    df[key] = pd.read_excel(FILE_PATH, sheet_name=sheet[key])


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
    
  
# get inputs from user
res = question_Box('save or cost? (save/cost) ', q1=['s','save'], q2=['c','cost'])
money = int(input("enter amount of money ? "))
log_decs = input("enter description : ")



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
        )
    else:
        # there is not any save data yet for today
        id = len(df['save'])
        # new save db
        new_save = new_df_api(
            obj={
                'id': id,
                'month_id':get_month_id,
                'week_id':week_of_month,
                'day_id':get_day_id,
                'day':date_now.day,
                'sum':money,
                'date':jalali_date
                },
            pd=pd,
            dataFrame=df['save']
        )
        # new log db
        new_log = new_df_api(
            obj={
            'save_id' : id, 
            'desc':log_decs, 
            'amount':money,
            'time':time
            }, 
            pd=pd, 
            dataFrame=df['save_log']
        )
        # confirm add money or not
        confirm_save_db(
            message=f"Are You sure add {money} toman to save at {get_day} {date_now.day} {get_month}? (yes/no) ", q1=['yes','y'], q2=['no','n'],
            pd= pd,
            FILE_PATH= FILE_PATH,
            db = new_save,
            log = new_log,
            db_sheet= 'save',
            log_sheet= 'save_log'
        )
# todo
else :
    query = ((df['cost']['month_id'] == get_month_id) & (df['save']['day'] == date_now.day))
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
        )
    else:
        # there is not any cost data yet for today
        id = len(df['cost'])
        # new save db
        new_cost = new_df_api(
            obj={
                'id': id,
                'month_id':get_month_id,
                'week_id':week_of_month,
                'day_id':get_day_id,
                'day':date_now.day,
                'sum':money,
                'date':jalali_date
                },
            pd=pd,
            dataFrame=df['cost']
        )
        # new log db
        new_log = new_df_api(
            obj={
            'cost_id' : id, 
            'desc':log_decs, 
            'amount':money,
            'time':time
            }, 
            pd=pd, 
            dataFrame=df['cost_log']
        )
        # confirm add money or not
        confirm_save_db(
            message=f"Are You sure add {money} toman to cost at {get_day} {date_now.day} {get_month}? (yes/no) ", q1=['yes','y'], q2=['no','n'],
            pd= pd,
            FILE_PATH= FILE_PATH,
            db = new_cost,
            log = new_log,
            db_sheet= 'cost',
            log_sheet= 'cost_log'
        )