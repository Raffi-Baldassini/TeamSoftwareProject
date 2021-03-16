from pychartjs import BaseChart, ChartType, Color, Options
import pymysql
#from db_interaction import DB
from Source.db_interaction import DB
from datetime import datetime, date
import time

"""
TO_DO:
    Format to style guide
"""

#gets a username from an id
def get_uname(user):
    cursor=DB.get_cursor()
    cursor.execute("SELECT uname FROM user WHERE id=%s;", (user))
    return cursor.fetchall()[0][0]


#creates a list of tuples (year, month) to be used for generating x-axis labels and for querying Db
def last_six_months():
    now = time.localtime()
    t = [time.localtime(time.mktime((now.tm_year, now.tm_mon - n, 1, 0, 0, 0, 0, 0, 0)))[:2] for n in range(6)]
    t.reverse()
    return t


#returns a list of a user's max 'stat' from each of the last 6 months (or 0 in place of no result)
def construct_data(user, stat):
    last_six = last_six_months()
    cursor = DB.get_cursor()
    data = []
    for n in range(6):
        #extracts the highest value achieved by a user in a stat for each of the last six months
        cursor.execute(f"SELECT max({stat}) FROM records WHERE MONTH(score_date) = {last_six[n][1]} AND YEAR(score_date) = {last_six[n][0]} AND id = {user};")
        wpm = cursor.fetchall()[0][0]
        #None value equates to a max stat of 0
        if wpm == None:
            data += [0]
        else:
            data += [wpm]
    return data


#returns a list of the last six months' string representation
def get_months():
    return [date(1900, i[1], 1).strftime('%B') for i in last_six_months()]
    


#obtains a list of the ids that are registered as friends of 'user'
def get_friends(user):
    cursor = DB.get_cursor()
    cursor.execute(f"SELECT friend_id FROM friends WHERE id = {user};")
    return [i[0] for i in cursor.fetchall()]
        
def get_charts(user_id):
    #Due to the limitations of pyChartJS, chart and Data classes have been hardcoded
    #A chart is created by creating a class inheriting from BaseChart, defining classes for data, labels and (optionally) options
    #Inside the data class data can be represented by creating classes that incldue their own labels, data and options
    #as these are identical, comments apply accross the charts and data
    class wpmChart(BaseChart):
        #Type of graph is determined by a constant from the ChartType class
        #using the 'type' keyword as the variable name is unfortunately unavoidable, to the best of my knowledge
        type = ChartType.Line

        class data:
            #classes here each represent a set on the graoh, a line in this case
            class user:
                #Using the username as their label
                label = get_uname(user_id)
                #data used is the maximum values for a user in each stat for each of the last six months
                data = construct_data(user_id, "wpm")
                #Sets the colour to a gradient from Olive to Green, values stored as constants in the Color class.
                #Single colours can also be used, I just prefer the gradient
                #You are not limited to the constants, however it is more readable than using the hex values
                _color = Color.JSLinearGradient('ctx', 0, 0, 1000, 0)
                _color.addColorStop(0, Color.Olive)
                _color.addColorStop(1, Color.Green)
                
                borderColor = _color.returnGradient()
                fill = False
                pointBorderWidth = 10
                pointRadius = 3

            class friend1:
                friends = get_friends(user_id)
                data = []
                if len(friends) > 0:
                    label = get_uname(friends[0])
                    data = construct_data(friends[0], "wpm")
                borderColor = Color.JSLinearGradient('ctx', 0, 0, 1000, 0,
                                                         (0, Color.Red), 
                                                         (1, Color.Magenta)
                                                         ).returnGradient()
                fill = False
                pointBorderWidth = 10
                pointRadius = 3

            class friend2:
                friends = get_friends(user_id)
                data = []
                if len(friends) > 1:
                    label = get_uname(friends[1])
                    data = construct_data(friends[1], "wpm")
                borderColor = Color.JSLinearGradient('ctx', 0, 0, 1000, 0,
                                                     (0, Color.Yellow), 
                                                     (1, Color.Orange)
                                                     ).returnGradient()
                fill = False
                pointBorderWidth = 10
                pointRadius = 3

            class friend3:
                friends = get_friends(user_id)
                data = []
                if len(friends) > 2:
                    label = get_uname(friends[2])
                    data = construct_data(friends[2], "wpm")
                _color = Color.JSLinearGradient('ctx', 0, 0, 1000, 0)
                _color.addColorStop(0, Color.Teal)
                _color.addColorStop(1, Color.Cyan)
                
                borderColor = _color.returnGradient()
                fill = False
                pointBorderWidth = 10
                pointRadius = 3

            class friend4:
                friends = get_friends(user_id)
                data = []
                if len(friends) > 3:
                    label = get_uname(friends[3])
                    data = construct_data(friends[3], "wpm")
                borderColor = Color.JSLinearGradient('ctx', 0, 0, 1000, 0,
                                                         (0, Color.Red), 
                                                         (1, Color.Magenta)
                                                         ).returnGradient()
                fill = False
                pointBorderWidth = 10
                pointRadius = 3

            class friend5:
                friends = get_friends(user_id)
                data = []
                if len(friends) > 4:
                    label = get_uname(friends[4])
                    data = construct_data(friends[4], "wpm")
                _color = Color.JSLinearGradient('ctx', 0, 0, 1000, 0)
                _color.addColorStop(0, Color.Beige)
                _color.addColorStop(1, Color.Maroon)
                fill = False
                pointBorderWidth = 10
                pointRadius = 3

        class labels:
            grouped = get_months()

        class options:
            title   = Options.Title(text="WPM Over Time", fontSize=18)
            _lables = Options.Legend_Labels(fontColor=Color.Gray, fullWidth=True)
            legend  = Options.Legend(position='Bottom', labels=_lables)
            _yAxes = [Options.General(ticks=Options.General(beginAtZero=True, padding=15, max=300))]
            scales = Options.General(yAxes=_yAxes)

    class accChart(BaseChart):
        type = ChartType.Line
        

        class data:
            class user:
                label = get_uname(user_id)
                data = construct_data(user_id, "acc")
                _color = Color.JSLinearGradient('ctx', 0, 0, 1000, 0)
                _color.addColorStop(0, Color.Olive)
                _color.addColorStop(1, Color.Green)
                
                borderColor = _color.returnGradient()
                fill = False
                pointBorderWidth = 10
                pointRadius = 3

            class friend1:
                friends = get_friends(user_id)
                data = []
                if len(friends) > 0:
                    label = get_uname(friends[0])
                    data = construct_data(friends[0], "acc")
                borderColor = Color.JSLinearGradient('ctx', 0, 0, 1000, 0,
                                                         (0, Color.Red), 
                                                         (1, Color.Magenta)
                                                         ).returnGradient()
                fill = False
                pointBorderWidth = 10
                pointRadius = 3

            class friend2:
                friends = get_friends(user_id)
                data = []
                if len(friends) > 1:
                    label = get_uname(friends[1])
                    data = construct_data(friends[1], "acc")
                borderColor = Color.JSLinearGradient('ctx', 0, 0, 1000, 0,
                                                     (0, Color.Yellow), 
                                                     (1, Color.Orange)
                                                     ).returnGradient()
                fill = False
                pointBorderWidth = 10
                pointRadius = 3

            class friend3:
                friends = get_friends(user_id)
                data = []
                if len(friends) > 2:
                    label = get_uname(friends[2])
                    data = construct_data(friends[2], "acc")
                _color = Color.JSLinearGradient('ctx', 0, 0, 1000, 0)
                _color.addColorStop(0, Color.Teal)
                _color.addColorStop(1, Color.Cyan)
                
                borderColor = _color.returnGradient()
                fill = False
                pointBorderWidth = 10
                pointRadius = 3

            class friend4:
                friends = get_friends(user_id)
                data = []
                if len(friends) > 3:
                    label = get_uname(friends[3])
                    data = construct_data(friends[3], "acc")
                borderColor = Color.JSLinearGradient('ctx', 0, 0, 1000, 0,
                                                         (0, Color.Red), 
                                                         (1, Color.Magenta)
                                                         ).returnGradient()
                fill = False
                pointBorderWidth = 10
                pointRadius = 3

            class friend5:
                friends = get_friends(user_id)
                data = []
                if len(friends) > 4:
                    label = get_uname(friends[4])
                    data = construct_data(friends[4], "acc")
                _color = Color.JSLinearGradient('ctx', 0, 0, 1000, 0)
                _color.addColorStop(0, Color.Beige)
                _color.addColorStop(1, Color.Maroon)
                fill = False
                pointBorderWidth = 10
                pointRadius = 3

        class labels:
            grouped = get_months()
            
        class options:
            title   = Options.Title(text="Accuracy Over Time", fontSize=18)
            _lables = Options.Legend_Labels(fontColor=Color.Gray, fullWidth=True)
            legend  = Options.Legend(position='Bottom', labels=_lables)
            _yAxes = [Options.General(ticks=Options.General(beginAtZero=True, padding=15, max=100))]
            scales = Options.General(yAxes=_yAxes)
    
    wpm = wpmChart()
    acc = accChart()
    return wpm.get(), acc.get()