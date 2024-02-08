import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('survey.db')
cursor = conn.cursor()

# Update all rows, setting specified columns to -1 and Isdone to 0
cursor.execute('''
    UPDATE survey_check
    SET
        users_headline_score = -1,
        llama2_chat13b_headline_score_usp2shothist = -1,
        llama2_chat13b_headline_score_usp2shotnothist = -1,
        llama2_chat13b_headline_score_uspzeroshothist = -1,
        Mistralv2_headline_score_usp2shothist = -1,
        Mistralv2_headline_score_usp2shotnothist = -1,
        Mistralv2_headline_score_uspzeroshothist = -1,
        Tulu7b_headline_score_usp2shothist = -1,
        Tulu7b_headline_score_usp2shotnothist = -1,
        Tulu7b_headline_score_uspzeroshothist = -1,
        Isdone = 0
''')

# Commit the changes
conn.commit()

# Close the connection
conn.close()
