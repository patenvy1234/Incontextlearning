from apscheduler.schedulers.blocking import BlockingScheduler
# from your_module import your_background_job_functionx
import sqlite3
# Create an instance of the BlockingScheduler
scheduler = BlockingScheduler()
def your_background_job_function():
    surv_conn = sqlite3.connect('survey.db')
    surv_curor = surv_conn.cursor()
    surv_curor.execute('''
        UPDATE survey_check
        SET Isdone = 0
        WHERE
            llama2_chat13b_headline_score_usp2shothist = -1
            AND llama2_chat13b_headline_score_usp2shotnothist = -1
            AND llama2_chat13b_headline_score_uspzeroshothist = -1
            AND Mistralv2_headline_score_usp2shothist = -1
            AND Mistralv2_headline_score_usp2shotnothist = -1
            AND Mistralv2_headline_score_uspzeroshothist = -1
            AND Tulu7b_headline_score_usp2shothist = -1
            AND Tulu7b_headline_score_usp2shotnothist = -1
            AND Tulu7b_headline_score_uspzeroshothist = -1
            AND Isdone = 1
    ''')
    surv_conn.commit()
    print("Running task every 30 minutes")
# Schedule your function to run every 30 minutes
scheduler.add_job(your_background_job_function, 'interval', minutes=15)

# Start the scheduler
scheduler.start()
