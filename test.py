import telebot
import psycopg2

bot = telebot.TeleBot('1428721851:AAH4QMlY1grNmYuSbuY6Ef5e8uobQtFP1wQ')
conn = psycopg2.connect(dbname="fuelprice", user="pyParser", password="qwerty123", host="localhost", port="5432")
cursor = conn.cursor()
a='Екатеринбург'
cursor.execute("select * from cities where city_name in ('{}')".format(a))
b = cursor.fetchone()[0]
cursor.execute("""select city_id, avg(ph.price) as b 
                     from price_histories ph where 1=1 
                     and date_time >= (select max(date_time) 
                     from price_histories) 
                     and ph.price <> (0) 
                     and ph.city_id in ('{}') 
                     and ph.brand like ('95%')
                     group by city_id""".format(b))
avg = cursor.fetchone()[1]
print("средняя стоимость топлива в {} : {}".format(a, avg))