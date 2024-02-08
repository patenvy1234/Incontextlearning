from flask import Flask, render_template, request, url_for, redirect
from db_util import get_summ_pairs, store_res, create_connection
from datetime import datetime, timedelta
# from apscheduler.schedulers.background import BackgroundScheduler
# from sqlitepool import ConnectionPool
app = Flask(__name__,
            static_url_path='/surveys/static',
            static_folder='static',
            template_folder='templates')

# Dictionary to store form submission timestamps
form_timestamps = {}
@app.route('/')
def index():
    return redirect(url_for('incontext_learning'))

@app.route('/surveys/incontext_learning', methods=['GET', 'POST'])
def incontext_learning():
    surv_conn = create_connection('survey.db')
    surv_cursor = surv_conn.cursor()
    main_con = create_connection('maindata.db')

    #
    # scheduler = BackgroundScheduler()
    # def my_background_job():
    #     surv_cnn = sqlite3.connect('survey.db')
    #     surv_curor = surv_conn.cursor()
    #     surv_curor.execute('''
    #         UPDATE survey_check
    #         SET Isdone = 0
    #         WHERE
    #             llama2_chat13b_headline_score_usp2shothist = -1
    #             AND llama2_chat13b_headline_score_usp2shotnothist = -1
    #             AND llama2_chat13b_headline_score_uspzeroshothist = -1
    #             AND Mistralv2_headline_score_usp2shothist = -1
    #             AND Mistralv2_headline_score_usp2shotnothist = -1
    #             AND Mistralv2_headline_score_uspzeroshothist = -1
    #             AND Tulu7b_headline_score_usp2shothist = -1
    #             AND Tulu7b_headline_score_usp2shotnothist = -1
    #             AND Tulu7b_headline_score_uspzeroshothist = -1
    #             AND Isdone = 1
    #     ''')
    #     surv_cnn.commit()
    #     print("Running task every 30 minutes")

    # Add the job to the scheduler to run every 30 minutes
    # scheduler.add_job(my_background_job, 'interval', seconds=10)
    #
    # # Start the scheduler when the app is started
    # scheduler.start()
    if request.method == 'GET':
        # Query the first row where Isdone is false
        surv_cursor.execute('''
            SELECT * FROM survey_check
            WHERE Isdone = 0
            LIMIT 1
        ''')
        result = surv_cursor.fetchone()
        doc_id = result[0]
        user1 = result[1]
        user2 = result[2]
        print(doc_id, user1, user2)

        # Store the timestamp for this form
        form_timestamps[(doc_id, user1, user2)] = datetime.now()

        surv_cursor.execute('''
        UPDATE survey_check
        SET Isdone=1
        WHERE doc_id = ? AND user1 = ? AND user2 = ?
        ''', (result[0], result[1], result[2]))
        surv_conn.commit()

        userpair_2shothisto_lst, userpair_2shotnohisto, userpair_zeroshot_hist = get_summ_pairs(main_con, doc_id,
                                                                                                user1, user2)
        return render_template("main.html", userpair_2shothisto_lst=userpair_2shothisto_lst,
                               userpair_2shotnohisto_lst=userpair_2shotnohisto,
                               userpair_zeroshot_hist_lst=userpair_zeroshot_hist, doc_id=doc_id, user1=user1,
                               user2=user2)

    if request.method == 'POST':
        name = request.form.get('name')
        gender = request.form.get('gender')
        occupation = request.form.get('occupation')
        res1 = request.form.get("1")
        res2 = request.form.get("2")
        res3 = request.form.get("3")
        res4 = request.form.get("4")
        res5 = request.form.get("5")
        res6 = request.form.get("6")
        res7 = request.form.get("7")
        res8 = request.form.get("8")
        res9 = request.form.get("9")
        res10 = request.form.get("10")
        doc_id = request.form.get("doc_id")
        user1 = request.form.get("user1")
        user2 = request.form.get("user2")

        # Check if the form submission occurred within the last 5 minutes
        # timestamp = form_timestamps.get((doc_id, user1, user2))
        # if timestamp and datetime.now() - timestamp > timedelta(secons=10):
        #     # The form submission has exceeded the timeout
        #     raise Exception("Form submission timeout")

        res = [res1, res2, res3, res4, res5, res6, res7, res8, res9, res10]
        store_res(surv_conn, name, gender, occupation, res, doc_id, user1, user2)

        # Redirect to the index page after submitting the form
        return redirect(url_for('incontext_learning'))



app.run(host='0.0.0.0', port=5000, debug=True)
