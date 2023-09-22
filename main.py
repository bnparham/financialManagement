from persiantools.jdatetime import JalaliDate
import pandas as pd
import math
from openpyxl import load_workbook
from datetime import datetime

# custom modules
from api_module import *

FILE_PATH = 'Financial-1402-1.xlsx'

# cell 2
sheet = {'cost':2, 'cost_log':3, 'save':0, 'save_log':1}
df = {}
for key in sheet:
    df[key] = pd.read_excel(FILE_PATH, sheet_name=sheet[key])


# cell 3
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

#todo: Example month id
# get_month_id = 10


        
# cell 4
  
# get input from user
res = question_Box('save or cost? (save/cost) ', q1=['s','save'], q2=['c','cost'])

if res == 1 :
    time = datetime.now().strftime("%H:%M")
    jalali_date = JalaliDate.today().strftime("%Y/%m/%d")
    money = int(input("enter amount of money ? "))
    log_decs = input("enter description : ")
    query = ((df['save']['month_id'] == get_month_id) & (df['save']['day'] == date_now.day))
    # check if row exist in db or not
    if(query.any()):
        # find exist row in table
        row = df['save'][query]
        # find save_id
        id = row['id'][0]
        # find sum and plus to money input
        row['sum'] += money
        # updare save data frame
        df['save'][query] = row
        
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
            money= money,
            get_day= get_day,
            now_day = date_now.day,
            get_month= get_month,
            pd= pd,
            FILE_PATH= FILE_PATH,
            db= df['save'],
            log= new_log,
            db_sheet= 'save',
            log_sheet= 'save_log'
        )
    else:
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
            money= money,
            get_day= get_day,
            now_day = date_now.day,
            get_month= get_month,
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
        pass
    else:
        money = input("enter amount of money ? ")
        data = {
                'month_id':get_month_id,
                'week_id':week_of_month,
                'day_id':get_day_id,
                'day':date_now.day,
                'sum':money
                }