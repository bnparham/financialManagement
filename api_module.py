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

# save to database with confirmation message, this method update 2 sheet. The table selected by the user and related log table   
def confirm_save_db(message, *args, **kwargs):
    confirm = question_Box(message)
    if confirm == 1:
        with kwargs['pd'].ExcelWriter(kwargs['FILE_PATH'], engine='openpyxl', mode='a', if_sheet_exists='replace') as writer :
            # write data to the excel 'save' sheet
            kwargs['db'].to_excel(writer, sheet_name=kwargs['db_sheet'], index=False)
            # save log to the excel 'save_log' sheet
            kwargs['log'].to_excel(writer, sheet_name=kwargs['log_sheet'], index=False)
            return True
    else:
        print("operation stopped !")
        return False

# this method dont need any confirmation for update table in database
def save_db_without_confirm(db, *args, **kwargs):
    with kwargs['pd'].ExcelWriter(kwargs['FILE_PATH'], engine='openpyxl', mode='a', if_sheet_exists='replace') as writer :
        # write data to the excel 'save' sheet
        db.to_excel(writer, sheet_name=kwargs['db_sheet'], index=False)
        

# use this method when want to add new record to table (Connecting the new data frame to the existing data frame in the database)
def new_df_api(obj ,*args, **kwargs):
    obj = kwargs['pd'].DataFrame([obj])
    df = kwargs['pd'].concat([kwargs['dataFrame'],obj], ignore_index=True)
    return df

# this method update total sheet in database
def update_total_table(db, db_sheet ,df_total, sum, *args, **kwargs):
    id = len(df_total)
    # query to find row
    query = df_total['month_id'] == kwargs['get_month_id']
    # find total value of save table or cost table (depend on user action)
    total_value = db[db['month_id'] == kwargs['get_month_id']]['sum'].sum()
    if(query.any()):
        # find row in total table with month id
        row = df_total[query]
        # update (save or cost) value
        row[db_sheet] = total_value + sum
        # upgdare data frame
        df_total[query] = row
        # save in database
        save_db_without_confirm(
            db = df_total,
            pd = kwargs['pd'],
            FILE_PATH = kwargs['FILE_PATH'],
            db_sheet = 'total',
        )
    else:
        new_total = new_df_api(
            obj = {
            'id':id,
             'month_id': kwargs['get_month_id'],
             'year': kwargs['year'],
             f'{db_sheet}':total_value + sum,
             },
            pd = kwargs['pd'],
            dataFrame = df_total,
        )
        save_db_without_confirm(
            db = new_total,
            pd = kwargs['pd'],
            FILE_PATH = kwargs['FILE_PATH'],
            db_sheet = 'total',
        )