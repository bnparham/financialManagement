from api_module import *


def create_db(db, log, db_sheet_name, log_sheet_name, query, *args, **kwargs):
    # there is not any save data yet for today
    db_id = len(db)
    log_id = len(log)
    # new save db
    new_save = new_df_api(
        obj={
            'id': db_id,
            'month_id':kwargs['get_month_id'],
            'week_id':kwargs['week_of_month'],
            'day_id':kwargs['get_day_id'],
            'day':kwargs['today'],
            'sum':kwargs['money'],
            'date':kwargs['jalali_date']
            },
        pd=kwargs['pd'],
        dataFrame=db
    )
    # new log db
    new_log = new_df_api(
        obj={
        'id':log_id,
        f'{db_sheet_name}_id' : db_id, 
        'desc':kwargs['log_decs'], 
        'amount':kwargs['money'],
        'time':kwargs['time']
        }, 
        pd=kwargs['pd'], 
        dataFrame=log
    )
    # confirm add money or not
    confirm_save_db(
        message=f"Are You sure add {kwargs['money']} toman to {db_sheet_name} at {kwargs['get_day']} {kwargs['today']} {kwargs['get_month']}? (yes/no) ", q1=['yes','y'], q2=['no','n'],
        pd= kwargs['pd'],
        FILE_PATH= kwargs['FILE_PATH'],
        db = new_save,
        log = new_log,
        db_sheet= db_sheet_name,
        log_sheet= log_sheet_name
    )

def update_db(db, log, db_sheet_name, log_sheet_name, query, *args, **kwargs):
    # find exist row in table
    row = db[query]
    # find save_id
    id = row['id'][0]
    # find sum and plus to money input
    row['sum'] += kwargs['money']
    # updare save data frame
    db[query] = row
    
    # new log db  
    new_log = new_df_api(
        obj={
        f'{db_sheet_name}_id' : id, 
        'desc':kwargs['log_decs'], 
        'amount':kwargs['money'],
        'time':kwargs['time']
        }, 
        pd=kwargs['pd'], 
        dataFrame=log
    )
    # confirm add money or not
    confirm_save_db(
        message=f"Are You sure add {kwargs['money']} toman to {db_sheet_name} at {kwargs['get_day']} {kwargs['today']} {kwargs['get_month']}? (yes/no) ", q1=['yes','y'], q2=['no','n'],
        pd= kwargs['pd'],
        FILE_PATH= kwargs['FILE_PATH'],
        db= db,
        log= new_log,
        db_sheet= db_sheet_name,
        log_sheet= log_sheet_name
    )