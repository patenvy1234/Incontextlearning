import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn


def get_summ_pairs(main_conn,doc_id,user1,user2):

    # print(f"offsets:{offsets}")
    with main_conn:
        main_cur = main_conn.cursor()
        main_cur.execute('''
            SELECT * FROM userpair_2shothisto
            WHERE doc_id = ? AND user1 = ? AND user2 = ?
        ''', (doc_id,user1,user2))
        userpair_2shothisto_lst = main_cur.fetchone()
        main_cur.execute('''
                   SELECT * FROM userpair_2shotnohisto
                   WHERE doc_id = ? AND user1 = ? AND user2 = ?
               ''', (doc_id, user1, user2))
        userpair_2shotnohisto = main_cur.fetchone()
        main_cur.execute('''
                   SELECT * FROM userpair_zeroshot_hist
                   WHERE doc_id = ? AND user1 = ? AND user2 = ?
               ''', (doc_id, user1, user2))
        userpair_zeroshot_hist = main_cur.fetchone()
        return userpair_2shothisto_lst,userpair_2shotnohisto,userpair_zeroshot_hist


# def _get_current_offsets(conn):
#     cur = conn.cursor()
#     cur.execute(
#         "SELECT var_name, curr_idx FROM metadata WHERE var_name in ('start_idx', 'survey_so_far', 'question_idx')")
#     res = cur.fetchall()
#     result = {k: int(v) for k, v in res}
#     return result

#
# def update_start_idx(conn):
#     # increment curr_index by 6 in metadata table
#     with conn:
#         offset_mapper = {(0, 0): (0, 6),
#                          (0, 6): (1, 0),
#                          (1, 0): (1, 6),
#                          (1, 6): (0, 0),
#                          }
#         res_dict = _get_current_offsets(conn)
#
#         if (res_dict["survey_so_far"], res_dict["question_idx"]) == (1, 6):
#             start_idx, (survey_so_far, question_idx) = res_dict["start_idx"] + 12, offset_mapper[
#                 (res_dict["survey_so_far"], res_dict["question_idx"])]
#         else:
#             start_idx, (survey_so_far, question_idx) = res_dict["start_idx"], offset_mapper[(
#                 res_dict["survey_so_far"], res_dict["question_idx"])]
#         print(
#             f"{res_dict['start_idx'], (res_dict['survey_so_far'], res_dict['question_idx'])}=>{start_idx, (survey_so_far, question_idx)}")
#         conn.execute(f"UPDATE metadata SET curr_idx = {start_idx} WHERE var_name = 'start_idx';")
#         conn.execute(f"UPDATE metadata SET curr_idx = {survey_so_far} WHERE var_name = 'survey_so_far';")
#         conn.execute(f"UPDATE metadata SET curr_idx = {question_idx} WHERE var_name = 'question_idx';")
#
#
def store_res(conn,  name, gender, occupation, res,doc_id,user1,user2):

     with conn:
         surv_cur = conn.cursor()
         print(doc_id, user1, user2)
         surv_cur.execute('''
         UPDATE survey_check
         SET
           users_headline_score = ?,
           llama2_chat13b_headline_score_usp2shothist = ?,
           llama2_chat13b_headline_score_usp2shotnothist = ?,
           llama2_chat13b_headline_score_uspzeroshothist = ?,
           Mistralv2_headline_score_usp2shothist = ?,
           Mistralv2_headline_score_usp2shotnothist = ?,
           Mistralv2_headline_score_uspzeroshothist = ?,
           Tulu7b_headline_score_usp2shothist = ?,
           Tulu7b_headline_score_usp2shotnothist = ?,
           Tulu7b_headline_score_uspzeroshothist = ?
         WHERE doc_id = ? AND user1 = ? AND user2 = ?
         ''',(res[0],res[1],res[2],res[3],res[4],res[5],res[6],res[7],res[8],res[9],doc_id,user1,user2))
         print(doc_id, user1, user2,"bye")




# if __name__ == '__main__':
#     db_file = "survey_db_v3.sqlite3"
#     conn = create_connection(db_file)
#     summ_pairs = update_start_idx(conn)
    # print(f"#summ_pairs: {len(summ_pairs)}")
    # for i, pair in enumerate(summ_pairs):
    #     print(f"pair#{i}: {pair}")
