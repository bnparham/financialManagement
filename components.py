from api_module import *

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