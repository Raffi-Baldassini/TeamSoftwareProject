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
import db_setup

#Simple mockup to generate data for the db
class Game:
    def __init__(self, user=None):
        self.wpm = 0
        self.acc = 0
        self.mistakes = 0
        self.user = user
        self.words = 0
        self.chars = 0
        self.play()

    #generates alphabet soup text to be typed
    def generate_string(self):
        mylist = list(string.ascii_lowercase)
        n = len(mylist)
        for i in range(len(mylist)):
            j = randint(0, n-1)
            mylist[i], mylist[j] = mylist[j], mylist[i]
        gibberish = ''.join(mylist)
        return gibberish[randint(0, len(gibberish)/2 - 1):randint(len(gibberish)/2, len(gibberish)-1)].strip()
    
    def play(self):
        self.words = int(input("how many words would you like to type?\n"))
        start = time()
        word_num = 0
        while word_num < self.words:
            substring = self.generate_string()
            if len(substring) == 0:
                continue
            self.chars += len(substring)
            print(substring)
            
            ans = None
            while True:
                ans = input("")
                #because I'm bad at typing
                if ans == "skip":
                    break
                if ans != substring:
                    self.mistakes+=1
                else:
                    break
            word_num += 1

        #calculating words per minute and accuracy during game
        self.wpm = int((self.words / (time() - start)) * 60)
        if self.mistakes == 0:
            self.acc = 100
        else:
            self.acc = int((self.words / (self.words + self.mistakes)) * 100)
        print(self)

    #information from db is tuple, using tuple for stats for uniformity
    def stats(self):
        return (self.user, self.words, self.chars, self.wpm,  self.acc)

    def __str__(self):
        return f"\nWords typed: {self.words}\nCharacters typed: {self.chars}\nMistakes: {self.mistakes}\nAccuracy: {self.acc}%\nWPM: {self.wpm}"
        

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

    
    def upload_game(game):
        #retrieves stats from a game object as specified above
        game_stats = game.stats()
        user = game_stats[0]
        words = game_stats[1]
        chars = game_stats[2]
        wpm = game_stats[3]
        acc = game_stats[4]
        
        connection = DB.connect_db()
        cursor = connection.cursor()
        
        #checks for user existence and adds game data into both 'user' and 'stats' tables if id is not in 'user'
        cursor.execute("SELECT id FROM user WHERE id = %s;", (user))
        if len(cursor.fetchall()) == 0:
            cursor.execute("""INSERT INTO user(id, uname, pword, email, dob)
                           VALUES (%s, 'test', 'test', 'test@test.com', '2021-02-04');
                           """, (user))
            cursor.execute("""INSERT INTO stats(id, solo_games, online_games,
                                    words, chars, wpm, accuracy, acc_best, acc_worst,
                                    wpm_best,wpm_worst)
                                    VALUES(%s,1,0,%s,%s,%s,%s,%s,%s,%s,%s);
                                    """, (user,words,chars,wpm,acc,acc,acc,wpm,wpm))
        else:
            cursor.execute("SELECT * FROM stats WHERE id = %s;", (user))
            stats = list(cursor.fetchall()[0])
            #weighting for current acc/wpm
            weight = stats[1]
            #increment games, words, chars
            stats[1] += 1
            stats[3] += words
            stats[4] += chars
            #acc/wpm calc'd as average of current value weighted by number of games + game value
            stats[5] = (stats[5] * weight + wpm) / stats[1]
            stats[6] = (stats[6] * weight + acc) / stats[1]
            #best/worst just max/min comparison with game value and value in 'stats' table
            stats[7] = max(stats[7], acc)
            stats[8] = min(stats[8], acc)
            stats[9] = max(stats[9], wpm)
            stats[10] = min(stats[10], wpm)

            cursor.execute("""UPDATE stats SET solo_games = %s, words = %s, chars = %s,
                        wpm = %s, accuracy = %s, acc_best = %s, acc_worst = %s,
                        wpm_best = %s, wpm_worst = %s WHERE id = %s""",
                       (stats[1],stats[3],stats[4],stats[5],stats[6],stats[7],
                        stats[8],stats[9],stats[10],stats[0]))

        today = datetime.utcnow().strftime('%Y-%m-%d')
            
        cursor.execute("SELECT * FROM records WHERE id = %s AND SCORE_DATE = %s",
                           (user, today))
        if len(cursor.fetchall()) == 0:
                cursor.execute("""INSERT INTO records(id, score_date, wpm, acc)
                                VALUES (%s, %s, %s,%s);""",
                                (user, today, wpm, acc))
        else:
            cursor.execute("SELECT wpm,accuracy FROM stats WHERE id = 1")
            (current_wpm, current_acc) = cursor.fetchall()[0]
            cursor.execute("""UPDATE records SET wpm = %s, acc = %s WHERE id = %s AND score_date = %s""",
                           (current_wpm, current_acc, user, today))
        connection.commit()
        connection.close()

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
    print("game begin")
    game = Game(input("input a new or old id: "))
    DB.upload_game(game)
    DB.print_all()
