from persiantools.jdatetime import JalaliDate
import pandas as pd
import math
from openpyxl import load_workbook


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


# api for user input
def question_Box(message, q1:list=['y'], q2:list=['n']):
    flag = True
    while(flag):      
        q = input(f"{message}").lower()
        try:
            if q in q1:
                flag = False
                return 1
            elif q in q2:
                flag = False
                return 2
            else :
                continue
        except:
            continue
        
# cell 4
  
# get input from user
res = question_Box('save or cost? (save/cost) ', q1=['s','save'], q2=['c','cost'])

if res == 1 :
    money = input("enter amount of money ? ")
    query = ((df['save']['month_id'] == get_month_id) & (df['save']['day'] == date_now.day))
    # check if row exist in db or not
    if(query.any()):
        # todo
        print("yes")
    else:
        data = {
                'month_id':get_month_id,
                'week_id':week_of_month,
                'day_id':get_day_id,
                'day':date_now.day,
                'sum':money
                }
        data = pd.DataFrame([data])
        
        print(df['save'])
        # join new row to existing table
        new_save = pd.concat([df['save'],data], ignore_index=True)
        # confirm add money or not
        confirm = question_Box(f"Are You sure add {money} toman to save at {get_day} {date_now.day} {get_month}? (yes/no) ", q1=['yes','y'], q2=['no','n'])
        if confirm == 1:
            with pd.ExcelWriter(FILE_PATH, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer :
            # write data to the excel sheet
                new_save.to_excel(writer, sheet_name='save', index=False)
        else:
            print("operation stopped !")
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