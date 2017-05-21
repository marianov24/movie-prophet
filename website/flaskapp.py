from flask import Flask, render_template, request, jsonify, json
import sys
import pymysql
import pickle
from datetime import datetime
app = Flask(__name__)

loaded_model = pickle.load(open('model\low_budget.mprophet', 'rb'))
print(loaded_model)
connection = pymysql.connect(host='localhost', user='root', password='toor', db='movies',charset='utf8')
cur = connection.cursor()

cur.execute("select * FROM scores_act")
act_sql = []
for row in cur: act_sql.append(list(row))

cur.execute("select * FROM scores_dir")
dir_sql = []
for row in cur: dir_sql.append(list(row))

cur.execute("select * FROM scores_pro")
pro_sql = []
for row in cur: pro_sql.append(list(row))

cur.execute("select * FROM scores_wri")
wri_sql = []
for row in cur: wri_sql.append(list(row))

cur.execute("select * FROM scores_cin")
cin_sql = []
for row in cur: cin_sql.append(list(row))

cur.execute("select * FROM scores_com")
com_sql = []
for row in cur: com_sql.append(list(row))

cur.execute("select * FROM scores_dis")
dis_sql = []
for row in cur: dis_sql.append(list(row))

cur.close()
connection.close()

k_act = [item[0] for item in act_sql]
v_act = [item[1] for item in act_sql]

k_dir = [item[0] for item in dir_sql]
v_dir = [item[1] for item in dir_sql]

k_pro = [item[0] for item in pro_sql]
v_pro = [item[1] for item in pro_sql]

k_wri = [item[0] for item in wri_sql]
v_wri = [item[1] for item in wri_sql]

k_cin = [item[0] for item in cin_sql]
v_cin = [item[1] for item in cin_sql]

k_com = [item[0] for item in com_sql]
v_com = [item[1] for item in com_sql]

k_dis = [item[0] for item in dis_sql]
v_dis = [item[1] for item in dis_sql]


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prediction/')
def prediction():
    data_act = []
    for i in range(len(k_act)):
        tmp={}
        tmp["id"] = v_act[i]
        tmp["text"] = k_act[i]
        data_act.append(tmp)
        # print(json.dumps(data_dir))

    data_dir = []
    for i in range(len(k_dir)):
        tmp={}
        tmp["id"] = v_dir[i]
        tmp["text"] = k_dir[i]
        data_dir.append(tmp)

    data_pro = []
    for i in range(len(k_pro)):
        tmp={}
        tmp["id"] = v_pro[i]
        tmp["text"] = k_pro[i]
        data_pro.append(tmp)

    data_wri = []
    for i in range(len(k_wri)):
        tmp={}
        tmp["id"] = v_wri[i]
        tmp["text"] = k_wri[i]
        data_wri.append(tmp)

    data_cin = []
    for i in range(len(k_cin)):
        tmp={}
        tmp["id"] = v_cin[i]
        tmp["text"] = k_cin[i]
        data_cin.append(tmp)

    data_com = []
    for i in range(len(k_com)):
        tmp={}
        tmp["id"] = v_com[i]
        tmp["text"] = k_com[i]
        data_com.append(tmp)

    data_dis = []
    for i in range(len(k_dis)):
        tmp={}
        tmp["id"] = v_dis[i]
        tmp["text"] = k_dis[i]
        data_dis.append(tmp)
	
    print('before return')	


    return render_template('prediction.html', data_act=json.dumps(data_act), data_dir=json.dumps(data_dir), 
        data_pro=json.dumps(data_pro), data_wri=json.dumps(data_wri), data_cin=json.dumps(data_cin),
        data_com=json.dumps(data_com), data_dis=json.dumps(data_dis))

    print('after return')

@app.route('/chart/')
def chart():
    return render_template('chart.html')

@app.route('/table/')
def table():
    return render_template('table.html')

@app.route('/_return_revenue')
def return_revenue():


    moviename = request.args.get('f_moviename', 'N/A')
    print("\nMovie Name:", moviename)

    bom_budget = request.args.get('f_budget', 0, type=int)
    print("Budget:", bom_budget)

    genre = request.args.getlist('f_gen[]')
    print('Genre:', sum(map(int,genre)))

    actor_score = request.args.getlist('f_act[]')
    actor_score = sum([float(i) for i in actor_score])
    print('Actor Score:', actor_score)

    director_score = request.args.getlist('f_dir[]')
    director_score = sum([float(i) for i in director_score])
    print('Director Score:', director_score)

    writer_score = request.args.getlist('f_wri[]')
    writer_score = sum([float(i) for i in writer_score])
    print('Writer Score:', writer_score)

    distributor_score = request.args.getlist('f_dis[]')
    distributor_score = sum([float(i) for i in distributor_score])
    print('Disctributor Score:', distributor_score)

    composer_score = request.args.getlist('f_com[]')
    composer_score = sum([float(i) for i in composer_score])
    print('Composer Score:', composer_score)

    cinematographer_score = request.args.getlist('f_cin[]')
    cinematographer_score = sum([float(i) for i in cinematographer_score])
    print('Cinematographer Score:', cinematographer_score)

    producer_score = request.args.getlist('f_pro[]')
    producer_score = sum([float(i) for i in producer_score])
    print('Producer Score:', producer_score)

    mpaa_rating = request.args.get('f_mpa', 'N/A')
    print('MPAA Rating:', mpaa_rating)

    date = request.args.get('f_dat')
    if date != '':
        date = datetime.strptime(date, '%Y-%m-%d')
        release_month = datetime.date(date).month
        release_week_of_the_year = datetime.date(date).isocalendar()[1]
        release_quarter = (release_month-1)//3 + 1
        release_day_of_the_year = datetime.date(date).timetuple().tm_yday
        print('Month, Week, Quarter, Day of the Year:', release_month, release_week_of_the_year, release_quarter, 
            release_day_of_the_year)
    else:
         release_month, release_week_of_the_year, release_quarter, release_day_of_the_year = '', '', '', '' 
         print('No valid date entered')

    holiday_season = True
    print('Holiday Season:', holiday_season, '\n')

    x = [bom_budget, release_month, release_week_of_the_year, release_quarter, mpaa_rating,
    holiday_season,release_day_of_the_year, actor_score,director_score,writer_score,
    distributor_score, composer_score, cinematographer_score, producer_score, genre]

    #roi = loaded_model.predict(x)

    rev = 0 
    if bom_budget < 1000: 
    	rev+=-2000
    else: rev+=710000000
    rev+=actor_score

    return jsonify(result=rev, mname=moviename, bdgt=bom_budget, act=actor_score)

if __name__ == "__main__":
    app.run(host="127.0.0.1",
        port=int("5000"),
        debug=True)
