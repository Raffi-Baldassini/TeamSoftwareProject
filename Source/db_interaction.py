#first two imports for string generation
from random import randint
import string
#for wpm timing
from time import time
#for db interaction
import pymysql
#for printing db information
import prettytable
#for historical records
from datetime import datetime
#import db_setup
from Source import db_setup

class DB:
    #returns a cursor object
    def get_cursor():
        con = DB.connect_db()
        return con.cursor()
    
    #returns a connection object
    def connect_db():
        return pymysql.connect(host = db_setup.server,
                    user= db_setup.username,
                    port=3306,
                    passwd=db_setup.password,
                    db= db_setup.db_name)

    
    def upload_game(game_stats):
        #retrieves stats from a game object as specified above
        user = int(game_stats[0])
        words = int(game_stats[1])
        chars = int(game_stats[2])
        wpm = int(game_stats[3])
        acc = int(game_stats[4])
        
        connection = DB.connect_db()
        cursor = connection.cursor()
        
        #checks for user existence and adds game data into both 'user' and 'stats' tables if id is not in 'user'
        cursor.execute("SELECT id FROM stats WHERE id = %s;", (user))
        if len(cursor.fetchall()) == 0:
            cursor.execute("""INSERT INTO stats(id, solo_games, online_games,
                                    words, chars, wpm, accuracy, acc_best, acc_worst,
                                    wpm_best,wpm_worst)
                                    VALUES(%s,1,0,%s,%s,%s,%s,%s,%s,%s,%s);
                                    """, (user,words,chars,acc,acc,wpm,wpm,wpm,acc))
        else:
            cursor.execute("SELECT * FROM stats WHERE id = %s;", (user))
            stats = list(cursor.fetchall()[0])
            #weighting for current acc/wpm
            weight = stats[1]
            #increment games, words, chars
            stats[1] += 1
            stats[3] += words
            stats[4] += chars
            #best/worst just max/min comparison with game value and value in 'stats' table
            stats[5] = max(stats[5], acc)
            stats[6] = min(stats[6], acc)
            stats[7] = max(stats[7], wpm)
            stats[8] = min(stats[8], wpm)
            #acc/wpm calc'd as average of current value weighted by number of games + game value
            stats[9] = (stats[9] * weight + wpm) / stats[1]
            stats[10] = (stats[10] * weight + acc) / stats[1]

            cursor.execute("""UPDATE stats SET solo_games = %s, words = %s, chars = %s,
                        acc_best = %s, acc_worst = %s, wpm_best = %s, wpm_worst = %s, 
                        wpm = %s, accuracy = %s WHERE id = %s""",
                       (stats[1],stats[3],stats[4],stats[5],stats[6],stats[7],
                        stats[8],stats[9],stats[10],stats[0]))

        today = datetime.utcnow().strftime('%Y-%m-%d')
            
        cursor.execute("SELECT * FROM records WHERE id = %s AND score_date = %s",
                           (user, today))
        if len(cursor.fetchall()) == 0:
                cursor.execute("""INSERT INTO records(id, score_date, wpm, acc)
                                VALUES (%s, %s, %s,%s);""",
                                (user, today, wpm, acc))
        else:
            cursor.execute("SELECT wpm,acc FROM records WHERE id = %s AND score_date = %s", (user, today))
            (current_wpm, current_acc) = cursor.fetchall()[0]
            if current_wpm > wpm:
                day_best = (current_wpm, current_acc)
            elif wpm > current_wpm:
                day_best = (wpm, acc)
            else:
                if current_acc > acc:
                    day_best = (current_wpm, current_acc)
                else:
                    day_best = (wpm, acc)
            cursor.execute("""UPDATE records SET wpm = %s, acc = %s WHERE id = %s AND score_date = %s""",
                           (day_best[0], day_best[1], user, today))
        connection.commit()
        connection.close()

    def getBestWPM(user):
        today = datetime.utcnow().strftime('%Y-%m-%d')
        cursor = DB.get_cursor()
        cursor.execute("SELECT wpm FROM records WHERE id=%s AND score_date=%s", (user, today))
        ans = cursor.fetchall()
        if len(ans) != 0:
            wpm_day = ans[0][0]
        else:
            wpm_day = 0
        cursor.execute("SELECT wpm_best FROM stats WHERE id=%s", (user))
        ans = cursor.fetchall()
        if len(ans) != 0:
            wpm_all = ans[0][0]
        else:
            wpm_all = 0
        return wpm_day, wpm_all

    #these two functions are the only reason for the prettytables import and can be removed if not being used for testing purposes
    def print_table(name):
        cursor = DB.get_cursor()
        cursor.execute(f"DESCRIBE {name};")
        field_names = []
        for field in cursor.fetchall():
            field_names += [field[0]]
        table = prettytable.PrettyTable(field_names)
        cursor.execute(f"select * from {name};")
        for row in cursor.fetchall():
            table.add_row(list(row))
        print(table)

    def print_all():
        DB.print_table("user")
        DB.print_table("stats")
        DB.print_table("records")
        DB.print_table("friends")
        
#test of db interaction
if __name__ == "__main__":
    print("##### Database Test #####")
    print("current user and stats tables:\n")
    DB.print_all()
