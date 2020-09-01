import pandas as pd
import datetime
from flask import Flask, render_template
import os
import time

app = Flask(__name__)

##pathがどこにあるか確認
#path=os.getcwd()
#print(path)

##日付取得
os.environ["TZ"] = "Asia/Tokyo"
time.tzset()
tday=datetime.date.today()
yday= tday - datetime.timedelta(days=1)
d_tday=tday.strftime('20%y%m%d')
d_yday=yday.strftime('20%y%m%d')

##本日のレース予測
#d_tday= '20200612' #特別に設定したいとき 
df_pred = pd.read_csv('mysite/static/report/predict_'+d_tday+'.csv')
pred_num_tday = len(df_pred)
header = df_pred.columns
record = df_pred.values.tolist()

##昨日の予測結果
#d_yday= '20200612' #特別に設定したいとき
df_ans = pd.read_csv('mysite/static/report/result_'+d_yday+'.csv')
df_ans = df_ans.fillna("")
header_ans = df_ans.columns
record_ans = df_ans.values.tolist()
pred_num = len(df_ans)-len(df_ans[df_ans["Result"]=="Cancel"])
hit_num = len(df_ans[df_ans["Result"]=="Hit"])
hit_ratio = round(hit_num/pred_num*100,1)
pay = 100*pred_num
getmoney = df_ans["Payoff"].sum()
pay_return = round(getmoney/pay*100,1)

if hit_ratio >= 10:
    msg = "的中率10%超えるなんて..昨日は良い日でしたね"
elif hit_ratio > 6:
    msg = "なんともネタにもしにくい的中率.."
else:
    msg = "こういう日もあるよね。前を向いて歩こう"

if pay_return > 100:
    msg2 = "今日はちょっと良いビールでも買いましょうか"
elif pay_return > 75:
    msg2 = "お金を稼ぐって大変ですね"
else:
    msg2 = "涙の数だけ強くなれるよ"


##各ページへのレンダリング
@app.route('/')
def top_page():
    return render_template('top_page.html')

@app.route('/thissite')
def this_site():
    return render_template('this_site.html')

@app.route('/disclaimer')
def disclaimer():
    return render_template('disclaimer.html')

@app.route('/prediction')
def prediction():
    return render_template('prediction.html', tday=tday,header=header,record=record,pred_num=pred_num_tday)

@app.route('/result')
def result():
    return render_template('result.html', yday=yday,header=header_ans,record=record_ans,msg=msg,msg2=msg2,\
                          pred_num=pred_num,hit_num=hit_num,\
                           hit_ratio=hit_ratio,pay=pay,getmoney=getmoney,\
                          pay_return=pay_return)

#テスト用のページ
@app.route('/hello_earth')
def hello_earth():
    name = 'Universe'
    return render_template('hello_earth.html', name=name)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
