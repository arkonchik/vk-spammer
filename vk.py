#!/usr/bin/python
# Author: https://vk.com/id181265169
# https://github.com/fgRuslan/vk-spammer
import argparse
import vk_api
import urllib.request
import urllib.error
import urllib.parse
import json
import random
import string
import time
import math
from requests.utils import requote_uri
from python3_anticaptcha import ImageToTextTask, errors

import threading
import sys
import os
import platform
import json
import codecs

HOME_PATH = os.path.expanduser("~")
SPAMMER_PATH = os.path.join(HOME_PATH + "/" + ".vk-spammer/")

SPAMMING_ONLINE_USERS = False
SPAMMING_FRIENDS = False
USE_TOKEN = False

# Данные из Kate mobile
API_ID = "2685278"
tmp = "hHbJug59sKJie78wjrH8"

API_VERSION = 5.132

ANTICAPTCHA_KEY = ''

username = None
password = None

# Если директории с настройками спамера нет, создать её
if not os.path.exists(SPAMMER_PATH):
    os.mkdir(SPAMMER_PATH)

DELAY = 4  # Количество секунд задержки

auth_data = {}

# -------------------------------------------
# Сообщения, которые будет отправлять спаммер
messages = []

if os.path.exists(SPAMMER_PATH + "messages.txt"):
    with codecs.open(SPAMMER_PATH + "messages.txt", 'r') as f:
        for line in f:
            messages.append(line)
else:
    messages = [
        "hi",
        "2",
        "3",
        "fuck",
        "5"
    ]
    # Создаём пустой файл messages.txt
    codecs.open(SPAMMER_PATH + "messages.txt", 'a').close()


# -------------------------------------------
# Сохраняем введённые данные авторизации в файл auth.dat


def do_save_auth_data():
    with open(SPAMMER_PATH + "auth.dat", "w+") as f:
        json.dump(auth_data, f)
    f.close()


# Загружаем данные авторизации из файла auth.dat


def load_auth_data():
    global auth_data
    if os.path.exists(SPAMMER_PATH + "auth.dat"):
        f = open(SPAMMER_PATH + "auth.dat", 'r')
        obj = json.load(f)
        auth_data = obj
        f.close()
        return True
    return False


def remove_auth_data():
    print("Удаляю текущие данные авторизации...")
    os.remove(SPAMMER_PATH + "auth.dat")


# -------------------------------------------


keys_nearby = {
    'а': ['е', 'у'],
    'б': ['ь', 'л', 'д', 'ъ'],
    'в': ['к', 'а', 'с', 'ы', 'ч'],
    'г': ['р', 'н', 'л', 'о', 'с'],
    'д': ['л', 'б', 'ж', 'з'],
    'е': ['а', 'о', 'ё'],
    'ж': ['э', 'х', 'з', 'д', 'ю'],
    'з': ['х', '3', 'д', 'ж'],
    'и': ['й', 'м', 'т', 'п'],
    'й': ['и', 'ц', 'ы'],
    'к': ['в', 'k', 'е'],
    'л': ['д', 'n'],
    'м': ['m', 'п'],
    'н': ['р', 'г', 'е', 'п'],
    'о': ['0', 'л'],
    'п': ['n', 'н', 'р', 'а'],
    'р': ['п', 'т', 'н', 'г'],
    'с': ['ч', 'в'],
    'т': ['р', 'ь'],
    'у': ['к', 'в', 'ц', 'y'],
    'ф': ['у', 'ц'],
    'ч': ['ы', 'в', '4'],
    'щ': ['ш', 'ж'],
    'ш': ['щ', 'ж'],
    'ы': ['ь', 'и', 'ь1', 'ъ', 'b1'],
    'ь': ['ъ', 'b', 'ы'],
    'ъ': ['ь', 'b'],
    'э': ['з'],
    'ю': ['б', 'ь', ],
    'я': ['ч', 'ы'],
}


def get_nearby_letter(letter):
    if letter not in keys_nearby:
        return ""

    key_options = keys_nearby[letter]
    return key_options[random.randint(1, len(key_options)) - 1]


def string_length(word: str):
    return len(word)


def make_typo(sentence: str, percent: float):
    result = sentence
    words_list = sentence.split()
    words_count = len(words_list)

    count_words_with_typo = math.ceil(words_count * percent)

    words_list.sort(key=string_length, reverse=True)

    i = 0
    for word in words_list:
        word_with_typo = make_typo_in_word(word)
        if word_with_typo != word:
            result = result.replace(word, word_with_typo, 1)
            i += 1
            if i == count_words_with_typo:
                break

    return result


def make_typo_in_word(word: str):
    word_without_punctuation = word
    for character in string.punctuation:
        word_without_punctuation = word_without_punctuation.replace(character, '')

    count_letters_in_word = len(word_without_punctuation)

    letters_from_begging_end = [3, 2]  # we start to replace symbols from 2 or 3 from beginning
    for startIndex in letters_from_begging_end:
        count_letter_that_could_changed = count_letters_in_word - (2 * startIndex)
        if count_letter_that_could_changed > 0:
            end_index = count_letters_in_word - startIndex
            letter_index = random.randint(startIndex, end_index)
            #print(startIndex, end_index, letter_index)
            letter_to_change = word[letter_index - 1:letter_index]
            changed_letter = get_nearby_letter(letter_to_change)
            if changed_letter != "":
                word = word[:letter_index] + changed_letter + word[letter_index + 1:]
                break

    return word


class MainThread(threading.Thread):
    def run(self):

        # print("-" * 4)
        # print("Задержка: ", args.delay)
        # print("-" * 4)
        print("Нажмите Ctrl+C чтобы остановить")

        DELAY = args.delay
        if SPAMMING_ONLINE_USERS:
            friend_list = vk_session.method('friends.search', {"is_closed": "false",
                                                               "can_access_closed": "true",
                                                               'can_write_private_message': 1, 'count': 1000,
                                                               'fields': 'online'})['items']
            while (True):
                try:
                    msg = random.choice(messages)
                    for friend in friend_list:
                        if friend['online'] == 0:
                            continue
                        victim_id = int(friend['id'])
                        r = vk.messages.send(
                            user_id=victim_id, message=msg, v=API_VERSION, random_id=random.randint(0, 10000))
                        print("Відправили ", text, " to ", victim_id)
                    time.sleep(DELAY)
                except vk_api.exceptions.ApiError as e:
                    print("Помилка!")
                    print(e)
                except Exception as e:
                    print(e)

        elif SPAMMING_FRIENDS:

            try:
                user = vk.users.get()[0]
                print("Авторизувалися в :", user.get('first_name'), " ", user.get('last_name'))
            except:
                print("Помилка авторизації , перевірте дані, або візьміть інший аккаунт")
                input("Натисніть Ентер для виходу")
                return

            acc_file = open("Accounts.txt", "r", encoding='utf-8')

            lista = []

            for s in acc_file:
                s = s.rstrip()
                lista = lista + [s]

            count_sms = input("Номер повiдомлення: ")
            text_file = open(f"text{count_sms}.txt", "r", encoding="utf-8")

            text = text_file.read()
            text_file.close()
            print(text)
            i = 0

            while (True):
                for friend in lista:
                    try:

                        with open("Accounts.txt", "w") as file:
                            for line in lista:
                                file.write(line + '\n')

                        try:
                            acc = lista.pop(0)
                            print(acc + "\n")
                            acc = acc.replace("https://vk.com/", "")

                        except:
                            print("список аккаунтiв закiнчився")
                            sys.exit(1)

                        acc = acc.replace("https://vk.com/public", "")

                        man_id = -147845620  # id группа, с которой будем брать посты и комментарии
                        postidlist = vk.wall.get(owner_id=man_id, count=1, offset=0)  # получаем последний пост со стены
                        a = str(postidlist['items'][0]['id'])
                        vk.wall.createComment(owner_id="-147845620", post_id=a, message="добрый вечер")

                        i = i + 1
                        print("Відправили користувачу", acc)

                        if (i > 18):
                            break

                        time.sleep(DELAY)
                    except vk_api.exceptions.ApiError as e:
                        print("Помилка відправлення!")
                        # print(e)
                        ()

                print("Всі контакти оброблені")

                input("Завдання завершено, натисніть Enter для виходу")

                return False


        elif SPAMMING_Groups:

            try:
                user = vk.users.get()[0]
                print("Авторизувалися в :", user.get('first_name'), " ", user.get('last_name'))
            except:
                print("Помилка авторизації , перевірте дані, або візьміть інший аккаунт")
                input("Натисніть Ентер для виходу")
                return

            group_text = []
            group_text_f = open("Group_Text.txt", "r", encoding='utf-8')
            for gr in group_text_f:
                gr = gr.rstrip()
                if gr.strip():
                    group_text = group_text + [gr]

            acc_file = open("Groups.txt", "r", encoding='utf-8')

            lista = []

            for s in acc_file:
                s = s.rstrip()
                lista = lista + [s]

            i = 0

            while (True):
                for friend in lista:
                    try:
                        acc = lista.pop(0)
                        with open("Groups.txt", "w") as file:
                            for line in lista:
                                file.write(line + '\n')
                        print(acc + "\n")
                        acc = acc.replace("https://vk.com/public", "")

                        man_id = "-" + acc  # id группа, с которой будем брать посты и комментарии
                        postidlist = vk.wall.get(owner_id=man_id, count=3, sort='desc',
                                                 offset=0)  # получаем последний пост со стены

                        listt = postidlist['items']

                        for post in listt:
                            a = str(post['id'])
                            mes = random.choice(group_text)
                            mes = make_typo(mes, mistake_percent)
                            vk.wall.createComment(owner_id=man_id, post_id=a, message=mes)
                            print("Группа " + man_id + ", пост " + a + "\n")

                            time.sleep(5)


                    except vk_api.exceptions.ApiError as e:
                        print("Помилка відправлення!")
                        print(e)
                        ()

                print("Всі контакти оброблені")

                input("Завдання завершено, натисніть Enter для виходу")

                return False


        else:
            while (True):
                try:
                    msg = random.choice(messages)

                    print(victim)
                    r = vk.messages.send(
                        peer_id=victim, message=msg, v=API_VERSION, random_id=random.randint(0, 10000))
                    print("Sent ", msg)
                    time.sleep(DELAY)
                except vk_api.exceptions.ApiError as e:
                    print("ОШИБКА!")
                    print(e)
                except Exception as e:
                    print(e)

        input("Завдання завершено, натисніть Enter для виходу")


def main():
    try:
        thread = MainThread()
        thread.daemon = True
        thread.start()

        while thread.is_alive():
            thread.join(1)
    except KeyboardInterrupt:
        print("Ctrl+C pressed...")

        sys.exit(1)


# -------------------------------------------
# Парсер аргументов
parser = argparse.ArgumentParser(description='Spam settings:')
parser.add_argument(
    '-d',
    '--delay',
    type=int,
    default=4,
    help='Delay (default: 4)'
)
parser.add_argument('-e', '--editmessages', action='store_true',
                    help='Use this argument to edit the message list')

parser.add_argument('-m', '--mistakespercent',
                    type=int,
                    default=5,
                    help='Mistake percent(while sending comments in group) from 0 to 100, better to use from 5 to 7')

parser.add_argument('-dm', '--debugmistakes',
                    type=bool,
                    default=False,
                    )

parser.add_argument('-r', '--removedata', action='store_true',
                    help='Use this argument to delete auth data (login, password)')
args = parser.parse_args()
# -------------------------------------------

if (args.editmessages):
    if platform.system() == "Windows":
        os.system("notepad.exe " + SPAMMER_PATH + "messages.txt")
    if platform.system() == "Linux":
        os.system("nano " + SPAMMER_PATH + "messages.txt")
    print("Перезапустите спамер, чтобы обновить список сообщений")
    exit(0)

if (args.removedata):
    remove_auth_data()

mistake_percent = 0
if args.mistakespercent >= 0 and args.mistakespercent <= 100:
    mistake_percent = args.mistakespercent/100
else:
    print("mistakespercent(m) должно быть в диапозоне от 0 до 100")
    exit(0)

if args.debugmistakes:
    group_text_f = open("Group_Text.txt", "r", encoding='utf-8')
    for gr in group_text_f:
        gr = gr.rstrip()
        if gr.strip():
            print(gr.strip() + "\n")
            print(make_typo(gr.strip(), mistake_percent) + "\n")
    exit(1)

# Пытаемся загрузить данные авторизации из файла
# Если не удалось, просим их ввести
load_result = load_auth_data()
if (load_result == False):
    username = input("Login : ")
    if len(username) == 85:
        USE_TOKEN = True
    if not USE_TOKEN:
        password = input("Пароль: ")
    else:
        password = ''
    # save_auth_data = input("Сохранить эти данные авторизации? (Y/n): ")

    save_auth_data = "Y"
    if (save_auth_data == "Y" or save_auth_data == "y" or save_auth_data == ""):
        auth_data['username'] = username
        auth_data['password'] = password
        do_save_auth_data()
else:
    print("Данные авторизации получены из настроек")
    username = auth_data['username']
    password = auth_data['password']
    if len(username) == 85:
        USE_TOKEN = True


def captcha_handler(captcha):
    if ANTICAPTCHA_KEY == '':
        solution = input("Решите капчу ({0}): ".format(captcha.get_url()))
        return captcha.try_again(solution)
    key = ImageToTextTask.ImageToTextTask(
        anticaptcha_key=ANTICAPTCHA_KEY, save_format='const').captcha_handler(captcha_link=captcha.get_url())

    # s = captcha.try_again(key['solution']['text'])

    s = (key['solution']['text'])
    print(s)
    return s


def auth_handler():
    key = input("Введите код подтверждения: ")
    remember_device = True
    return key, remember_device


# -------------------------------------------
# Логинимся и получаем токен
vk_session = None

anticaptcha_api_key = '60fe494e48e83c06a26da2e2d3e8d78b'
# anticaptcha_api_key = input(     "API ключ от anti-captcha.com (оставьте пустым если он не нужен): ")
if anticaptcha_api_key == '':
    if USE_TOKEN:
        vk_session = vk_api.VkApi(
            token=username, auth_handler=auth_handler, app_id=API_ID, client_secret=tmp)
    else:
        vk_session = vk_api.VkApi(
            username, password, auth_handler=auth_handler, app_id=API_ID, client_secret=tmp)
else:
    ANTICAPTCHA_KEY = anticaptcha_api_key
    if USE_TOKEN:
        vk_session = vk_api.VkApi(token=username, captcha_handler=captcha_handler,
                                  auth_handler=auth_handler, app_id=API_ID, client_secret=tmp)
    else:
        vk_session = vk_api.VkApi(username, password, captcha_handler=captcha_handler,
                                  auth_handler=auth_handler, app_id=API_ID, client_secret=tmp)

try:
    vk_session.auth(token_only=True)
except vk_api.AuthError as error_msg:
    print(error_msg)

vk = vk_session.get_api()

# -------------------------------------------
#Преобразовываем введённый id пользователя в цифровой формат


victim = input("Введіть 1 для розсилання по особистим повідомленням, 2 для розсилання по группам: ")

if victim == "#online":
    SPAMMING_ONLINE_USERS = True
elif victim == "1":
    SPAMMING_FRIENDS = True
elif victim == "2":
    SPAMMING_Groups = True

elif victim.startswith("#c"):
    victim = victim.replace("#c", "")
    victim = int(victim) + 2000000000
else:

    victim = victim.split("/")
    victim = victim[len(victim) - 1]

    if victim.isdigit():
        victim = victim
    else:
        print("Resolving screen name...")
        r = vk.utils.resolveScreenName(screen_name=victim, v=API_VERSION)
        victim = r["object_id"]
        print("It is: " + str(victim))

    r = vk.users.get(user_id=victim, fields="id", v=API_VERSION)
    r = r[0]["id"]

    victim = r
# -------------------------------------------
# Запускатор главного потока
main()
