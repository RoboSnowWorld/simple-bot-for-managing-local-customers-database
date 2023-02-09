import pymysql
import telebot
from telebot import types

#root:root@127.0.0.1:3306

state = ''
bot = telebot.TeleBot('5583426666:AAGULzrXho3AgHvo-Qv-hZadur2HjP8D0NQ')

general_markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
generalbtn_1 = types.KeyboardButton('Поиск покупателя 🔍')
generalbtn_2 = types.KeyboardButton('Редактирование данных 📝')
generalbtn_3 = types.KeyboardButton('Добавление покупателя ✅')
generalbtn_4 = types.KeyboardButton('Удалить покупателя ❌')
general_markup.add(generalbtn_1, generalbtn_2, generalbtn_3, generalbtn_4)

def establish_connetion():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='root',
                                 database='customers',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

def create_record(connection, id, name, balance, address, contact_number, orders):
    with connection:
        with connection.cursor() as cursor:
            # Create a new record
            sql = f"INSERT INTO customers(`ID`, `Name`, `Balance`, `Delivery_address`, `Contact_number`, `Orders`) VALUES({id}, '{name}', {balance}, '{address}', '{contact_number}', {orders});"
            cursor.execute(sql)
            cursor.close()
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

def remove_record(connection, id):
    with connection:
        with connection.cursor() as cursor:
            # Create a new record
            sql = f'DELETE FROM customers WHERE ID={id};'
            cursor.execute(sql)
            cursor.close()
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

def get_last_id(connection):
    with connection:
        with connection.cursor() as cursor:
            # Create a new record
            sql = f'SELECT max(id) FROM customers'
            cursor.execute(sql)
            result = cursor.fetchone()
            cursor.close()
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        return result['max(id)'] + 1


def read_record(connection, id):
    with connection:
        with connection.cursor() as cursor:
            # Create a new record
            sql = f'SELECT * FROM customers WHERE ID={id};'
            cursor.execute(sql)
            result = cursor.fetchone()
            cursor.close()
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        return result

@bot.message_handler(content_types=['text'])
def incoming_message(message):
    global state
    if 'Поиск покупателя' in message.text:
        bot.send_message(message.chat.id, 'Введите id покупателя')
        state = 'find_customer'
    elif 'Редактирование данных' in message.text:
        bot.send_message(message.chat.id, 'Введите id покупателя, затем имя, баланс, адрес, номер телефона, и количество заказов через двоеточие')
        state = 'edit_data'
    elif 'Добавление покупателя' in message.text:
        bot.send_message(message.chat.id, 'Введите имя, адрес и номер телефона через двоеточие\nПример: Зинаида:г.Москва, ул Тверская, 6, кв 30:79163904209')
        state = 'add_customer'
    elif 'Удалить покупателя' in message.text:
        state = 'remove_customer'
        bot.send_message(message.chat.id, 'Введите id покупателя')
    elif state == 'add_customer':
        name, address, phone_number = message.text.split(':')
        balance = 0
        orders = 0
        create_record(establish_connetion(), get_last_id(establish_connetion()), name, balance, address, phone_number,orders)
        bot.send_message(message.chat.id, 'Успешно ✅')
    elif state == 'find_customer':
        id = message.text
        information = read_record(establish_connetion(), id)
        bot.send_message(message.chat.id, f'Имя: {information["Name"]}\nНомер телефона: {information["Contact_number"]}\nАдрес доставки: {information["Delivery_address"]}')
    elif state == 'edit_data':
        id, name, balance, address, phone_number, orders = message.text.split(':')
        remove_record(establish_connetion(), id)
        create_record(establish_connetion(), id, name, balance, address, phone_number, orders)
        bot.send_message(message.chat.id, 'Успешно ✅')
    elif state == 'remove_customer':
        id = message.text
        remove_record(establish_connetion(), id)
        bot.send_message(message.chat.id, 'Успешно ✅')

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, 'Здравствуйте✋, \nЭтот бот позволяет искать покупателей в базе 🔍, \nа также добавлять и удалять записи 📝', reply_markup=general_markup)

bot.polling(none_stop=True, interval=1)

# create_record(establish_connetion(), 8, 'София', 0, 'большой пр в.о, 30', '+79516488449', 0)