import sqlite3

def print_first_5_rows(db_file):
    # Connect to the SQLite database
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    # Get the list of tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Print the first 5 rows of each table along with their column names
    for table in tables:
        table_name = table[0]
        print(f"\nTable: {table_name}")

        # Get the list of columns in the table
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        column_names = [column[1] for column in columns]

        # Fetch and print the first 5 rows
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 4;")
        rows = cursor.fetchall()

        # Print column names
        print("  ".join(column_names))

        # Print the first 5 rows
        for row in rows:
            print("  ".join(map(str, row)))

    # Close the database connection
    connection.close()

# Replace 'your_database_file.db' with the actual name of your SQLite database file
db_file = 'survey.db'
print_first_5_rows(db_file)
