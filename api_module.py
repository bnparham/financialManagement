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
        
def confirm_save_db(*args, **kwargs):
    confirm = question_Box(f"Are You sure add {kwargs['money']} toman to save at {kwargs['get_day']} {kwargs['now_day']} {kwargs['get_month']}? (yes/no) ", q1=['yes','y'], q2=['no','n'])
    if confirm == 1:
        with kwargs['pd'].ExcelWriter(kwargs['FILE_PATH'], engine='openpyxl', mode='a', if_sheet_exists='replace') as writer :
            # write data to the excel 'save' sheet
            kwargs['db'].to_excel(writer, sheet_name=kwargs['db_sheet'], index=False)
            # save log to the excel 'save_log' sheet
            kwargs['log'].to_excel(writer, sheet_name=kwargs['log_sheet'], index=False)
    else:
        print("operation stopped !")
        
        
def new_df_api(obj ,*args, **kwargs):
    obj = kwargs['pd'].DataFrame([obj])
    df = kwargs['pd'].concat([kwargs['dataFrame'],obj], ignore_index=True)
    return df