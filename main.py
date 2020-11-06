import telebot
import psycopg2

bot = telebot.TeleBot('1428721851:AAH4QMlY1grNmYuSbuY6Ef5e8uobQtFP1wQ')
conn = psycopg2.connect(dbname="fuelprice", user="pyParser", password="qwerty123", host="localhost", port="5432")
cursor = conn.cursor()


@bot.message_handler(commands=['start'])

def start_message(message):
    msg=bot.send_message(message.chat.id, 'Чтобы узнать среднюю стоимость топлива укажите город')
    bot.register_next_step_handler(msg, lvl2)

def lvl2(message):
    a = message.text
    cursor.execute("select * from cities where city_name in ('{}')".format(a))

    try:
        b=cursor.fetchone()[0]
        cursor.execute("""select city_id, to_char(avg(ph.price),'FM999999999.00')
                         from price_histories ph where 1=1 
                         and date_time >= (select max(date_time) 
                         from price_histories) 
                         and ph.price <> (0) 
                         and ph.city_id in ('{}') 
                         and ph.brand like ('95%')
                       group by city_id """.format(b))
        avg=cursor.fetchone()[1]
        bot.send_message(message.chat.id,"Средняя стоимость топлива в {}: {}".format(a,avg))
    except TypeError:
        msg=bot.send_message(message.chat.id,'Город не найден, введите название корректно')
        bot.register_next_step_handler(msg, lvl2)

bot.polling()
