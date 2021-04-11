import sqlite3 as sl

path = path = "t:\\workspaces\\Atom\\Youless\\"

con = sl.connect(path + 'youless.db')


# # CREATE YEAR_DAY TABLE
# with con:
#     con.execute("""
#         CREATE TABLE yeardays_e (
#
#             date TEXT NOT NULL PRIMARY KEY,
#             year TEXT NOT NULL,
#             month TEXT NOT NULL,
#             monthname TEXT NOT NULL,
#             kwh TEXT NOT NULL
#         );
#     """)
#
#
# # CREATE DAY_HOUR TABLE
# with con:
#     con.execute("""
#         CREATE TABLE dayhours_e (
#             date TEXT NOT NULL PRIMARY KEY,
#             year TEXT NOT NULL,
#             week TEXT NOT NULL,
#             month TEXT NOT NULL,
#             monthname TEXT NOT NULL,
#             day TEXT NOT NULL,
#             yearday TEXT NOT NULL,
#             watt TEXT NOT NULL
#         );
#     """)
#
# CREATE DAY_HOUR TABLE
with con:
    con.execute("""
        CREATE TABLE dayminutes_e (
            date TEXT NOT NULL PRIMARY KEY,
            year INTEGER NOT NULL,
            week INTEGER NOT NULL,
            month INTEGER NOT NULL,
            monthname TEXT NOT NULL,
            day INTEGER NOT NULL,
            dayname TEXT NOT NULL,
            time TEXT NOT NULL,
            watt INTEGER NOT NULL
        );
    """)
