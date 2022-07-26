import os
import re
from pathlib import Path
from pyrogram.errors.exceptions.flood_420 import FloodWait
from secrets import choice
from pyrogram import Client, filters, types
from pyrogram.errors import FloodWait
from pyrogram.types import Message, User
from pyrogram.types import ChatPermissions
import config
from PyroHelpers import ReplyCheck
import random
import calendar
import string
from speedtest import Speedtest
import pyshorteners
from datetime import date, datetime, timedelta
from pyrogram.raw import functions
from basic import edit_or_reply
import asyncio
from pyrogram.errors import PeerIdInvalid
import uuid
from countryinfo import CountryInfo
from httpx import AsyncClient
from pyrohelper import get_arg

api_id = config.api_id1
api_hash = config.api_hash1

app = Client('account', api_id, api_hash)

@app.on_message(filters.text & filters.incoming & filters.regex("^\-$") & filters.reply)
async def repDown(client, message):
    try:
        if message.reply_to_message.from_user.is_self:
            if Path(f"\\reputation.txt").is_file():
                with open("reputation.txt", "r") as f:
                    NowReputation = int(f.read())
                    f.close()
            else:
                NowReputation = 0
            with open("\\reputation.txt", "w") as f:
                reputation = str(NowReputation - 1)
                f.write(reputation)
                f.close()
            await message.reply_text(f"❎ Репутация понижена (-1)\n🌐 Моя репутация: {str(reputation)}")
    except:
        pass


@app.on_message(filters.text & filters.incoming & filters.regex("^\+$") & filters.reply)
async def repUp(client, message):
    try:
        if message.reply_to_message.from_user.is_self:
            if Path(f"\\reputation.txt").is_file():
                with open("\\reputation.txt", "r") as f:
                    NowReputation = int(f.read())
                    f.close()
            else:
                NowReputation = 0
            with open("\\reputation.txt", "w") as f:
                reputation = str(NowReputation + 1)
                f.write(reputation)
                f.close()
            await message.reply_text(f"✅ Репутация повышена (+1)\n🌐 Моя репутация: {str(reputation)}")
    except:
        pass


@app.on_message(filters.command(["rep"], ['.']) & filters.me)
async def repNakrutka(client, message):
    try:
        with open("\\reputation.txt", "w") as f:
            rep = str(int(message.command[1]))
            f.write(rep)
            f.close()
            text = f"Репутация изменена.\nРепутация: {str(rep)}"
            await message.edit(text)

    except Exception as error:
        await message.edit(f"Error! Reputation edited to '0'\n\nLog: {error}")
        with open("\\reputation.txt", "w") as f:
            f.write(str(int(0)))
            f.close()


@app.on_message(filters.command(["qr"], ['.']) & filters.me)
async def qr(client, message):
    texts = ""
    if message.reply_to_message:
        texts = message.reply_to_message.text
    elif len(message.text.split(maxsplit=1)) == 2:
        texts = message.text.split(maxsplit=1)[1]
    text = texts.replace(' ', '%20')
    QRcode = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={text}"
    await message.delete()
    await app.send_photo(message.chat.id, QRcode)

R = "❤️"
W = "🤍"

heart_list = [
    W * 9,
    W * 2 + R * 2 + W + R * 2 + W * 2,
    W + R * 7 + W,
    W + R * 7 + W,
    W + R * 7 + W,
    W * 2 + R * 5 + W * 2,
    W * 3 + R * 3 + W * 3,
    W * 4 + R + W * 4,
    W * 9,
]
joined_heart = "\n".join(heart_list)
heartlet_len = joined_heart.count(R)
SLEEP = 0.1


async def _wrap_edit(message, text: str):
    try:
        await message.edit(text)
    except FloodWait as fl:
        await asyncio.sleep(fl.x)


async def phase1(message):
    BIG_SCROLL = "🧡💛💚💙💜🖤🤎"
    await _wrap_edit(message, joined_heart)
    for heart in BIG_SCROLL:
        await _wrap_edit(message, joined_heart.replace(R, heart))
        await asyncio.sleep(SLEEP)


async def phase2(message):
    ALL = ["❤️"] + list("🧡💛💚💙💜🤎🖤")  # don't include white heart

    format_heart = joined_heart.replace(R, "{}")
    for _ in range(5):
        heart = format_heart.format(*random.choices(ALL, k=heartlet_len))
        await _wrap_edit(message, heart)
        await asyncio.sleep(SLEEP)


async def phase3(message):
    await _wrap_edit(message, joined_heart)
    await asyncio.sleep(SLEEP * 2)
    repl = joined_heart
    for _ in range(joined_heart.count(W)):
        repl = repl.replace(W, R, 1)
        await _wrap_edit(message, repl)
        await asyncio.sleep(SLEEP)


async def phase4(message):
    for i in range(7, 0, -1):
        heart_matrix = "\n".join([R * i] * i)
        await _wrap_edit(message, heart_matrix)
        await asyncio.sleep(SLEEP)


@app.on_message(filters.command(["hearts", "magic", "love"], ["."]) & filters.me)
async def hearts(client: Client, message: Message):
    await phase1(message)
    await asyncio.sleep(SLEEP * 3)
    await message.edit("**❤️ I**")
    await asyncio.sleep(0.5)
    await message.edit("**❤️ I love**")
    await asyncio.sleep(0.5)
    await message.edit("**❤️ I love you**")
    await asyncio.sleep(3)
    await message.edit("**❤️ I love you <3**")

class WWW:
    NearestDC = "Страна: `{}`\n" "Ближайший центр обработки данных: `{}`\n" "Этот центр обработки данных: `{}`"


@app.on_message(filters.command("dc", ".") & filters.me)
async def nearest_dc(client: Client, message: Message):
    dc = await app.send(functions.help.GetNearestDc())
    await message.edit(WWW.NearestDC.format(dc.country, dc.nearest_dc, dc.this_dc))

unmute_permissions = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False,
)

@app.on_message(filters.group & filters.command("unmute", ["."]) & filters.me)  
async def unmute(_, message: Message):
    if message.chat.type in ["group", "supergroup"]:
        me_m =await app.get_me()
        me_ = await message.chat.get_member(int(me_m.id))
        if not me_.can_restrict_members:
         await message.edit("Нет прав для анмута!")
         return
        can_mute= True
        if can_mute:
            try:
                if message.reply_to_message:
                    user_id = message.reply_to_message.from_user.id
                else:
                    usr = await app.get_users(message.command[1])
                    user_id = usr.id
            except IndexError:
                await message.edit_text("Неверно указано айди или юзернейм!")
                return
            try:
                await app.restrict_chat_member(
                    chat_id=message.chat.id,
                    user_id=user_id,
                    permissions=unmute_permissions,
                )
                await message.edit_text(f'Юзер: tg://user?id={user_id} был размучен.')
            except Exception as e:
                await message.edit_text("`Error!`\n" f"**Log:** `{e}`")
                return
        else:
            await message.edit_text("Отказано в доступе!")
    else:
        await message.delete()

mute_permission = ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False, 
    can_send_other_messages=False,
    can_send_polls=False,
    can_add_web_page_previews=False,
    can_change_info=False,
    can_pin_messages=False,
    can_invite_users=True,
)

@app.on_message(filters.command("mute", ["."]) & filters.me)  
async def mute(_, message: Message):
    if message.chat.type in ["group", "supergroup"]:
        me_m =await app.get_me()
        me_ = await message.chat.get_member(int(me_m.id))
        if not me_.can_restrict_members:
            await message.edit("Нет прав для мута!")
            return
        can_mute = True
        if can_mute:
            try:
                if message.reply_to_message:
                    user_id = message.reply_to_message.from_user.id
                else:
                    usr = await app.get_users(message.command[1])
                    user_id = usr.id
            except IndexError:
                await message.edit_text("Неверно указано айди или юзернейм!")
                return
            try:
                await app.restrict_chat_member(
                    chat_id=message.chat.id,
                    user_id=user_id,
                    permissions=mute_permission,
                )
                await message.edit_text(f'Юзер: tg://user?id={user_id} был замучен навсегда.')
            except Exception as e:
                await message.edit_text("`Error!`\n" f"**Log:** `{e}`")
                return
        else:
            await message.edit_text("Отказано в доступе!")
    else:
        await message.delete()

class PasteBins:
    def __init__(self) -> None:
        # API Urls
        self.nekobin_api = "https://nekobin.com/api/documents"
        self.spacebin_api = "https://spaceb.in/api/v1/documents"
        self.hastebin_api = "https://www.toptal.com/developers/hastebin/documents"
        # Paste Urls
        self.nekobin = "https://nekobin.com"
        self.spacebin = "https://spaceb.in"
        self.hastebin = "https://www.toptal.com/developers/hastebin"
    
    async def paste_text(self, paste_bin, text):
        if paste_bin == "spacebin":
            return await self.paste_to_spacebin(text)
        elif paste_bin == "hastebin":
            return await self.paste_to_hastebin(text)
        elif paste_bin == "nekobin":
            return await self.paste_to_nekobin(text)
        else:
            return "`Invalid pastebin service selected!`"
    
    async def __check_status(self, resp_status, status_code: int = 201):
        if int(resp_status) != status_code:
            return "real shit"
        else:
            return "ok"

    async def paste_to_nekobin(self, text):
        async with AsyncClient() as nekoc:
            resp = await nekoc.post(self.nekobin_api, json={"content": str(text)})
            chck = await self.__check_status(resp.status_code)
            if not chck == "ok":
                return None
            else:
                jsned = resp.json()
                return f"{self.nekobin}/{jsned['result']['key']}"
    
    async def paste_to_spacebin(self, text):
        async with AsyncClient() as spacbc:
            resp = await spacbc.post(self.spacebin_api, data={"content": str(text), "extension": "md"})
            chck = await self.__check_status(resp.status_code)
            if not chck == "ok":
                return None
            else:
                jsned = resp.json()
                return f"{self.spacebin}/{jsned['payload']['id']}"
    
    async def paste_to_hastebin(self, text):
        async with AsyncClient() as spacbc:
            resp = await spacbc.post(self.hastebin_api, data=str(text))
            chck = await self.__check_status(resp.status_code, 200)
            if not chck == "ok":
                return None
            else:
                jsned = resp.json()
                return f"{self.hastebin}/{jsned['key']}"


async def get_pastebin_service(text: str):
    if re.search(r'\bhastebin\b', text):
        pastebin = "hastebin"
    elif re.search(r'\bspacebin\b', text):
        pastebin = "spacebin"
    elif re.search(r'\bnekobin\b', text):
        pastebin = "nekobin"
    else:
        pastebin = "spacebin"
    return pastebin

@app.on_message(filters.command(["paste", "nekobin", "hastebin", "spacebin"], ["."]) & filters.me)
async def paste_dis_text(_, message: Message):
    pstbin_serv = await get_pastebin_service(message.text.split(" ")[0])
    paste_msg = await message.edit(f"`Загружаю {pstbin_serv.capitalize()}...`")
    replied_msg = message.reply_to_message
    tex_t = get_arg(message)
    message_s = tex_t
    if not tex_t:
        if not replied_msg:
            return await paste_msg.edit("Нужен реплай на файл или текст!")
        if not replied_msg.text:
            file = await replied_msg.download()
            m_list = open(file, "r").read()
            message_s = m_list
            os.remove(file)
        elif replied_msg.text:
            message_s = replied_msg.text
    paste_cls = PasteBins()
    pasted = await paste_cls.paste_text(pstbin_serv, message_s)
    if not pasted:
        return await paste_msg.edit("Произошла ошибка!")
    await paste_msg.edit(f"**Загружено на {pstbin_serv.capitalize()}!** \n\n**Url:** {pasted}", disable_web_page_preview=True)


moon = "🌖🌕🌔🌓🌒🌑🌘🌗"
clock = "🕛🕑🕒🕓🕔🕕🕖🕗🕘🕙🕚"
run = "🏃‍⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"
car = "🚗‍⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"


@app.on_message(filters.me & filters.command(['anim'], ['.', '/']))
async def spin(app, message):
    if len(message.text.split()) > 1:
        text = " ".join(message.text.split()[1:]).replace(" ", "")
        if text in ("moon", "clock", "run", "car"):
            a = ""
            if text == "moon": a = moon
            elif text == "clock": a = clock
            elif text == "run": a = run
            elif text == "car": a = car
            for i in range(1, 4):
                for i in range(1, len(a)):
                    await message.edit(a[i:] + a[:i])
                    await asyncio.sleep(0.4)
        else:
            for i in range(1,4):
                for i in range(1, len(text)):
                    await message.edit(text[i:] + text[:i])
                    await asyncio.sleep(0.4)


@app.on_message(filters.command("bomb", ["."]) & filters.me)
async def gahite(client: Client,message: Message):
    if message.forward_from:
        return
    await message.edit("▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n")
    await asyncio.sleep(0.5)
    await message.edit("💣💣💣💣 \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n")
    await asyncio.sleep(0.5)
    await message.edit("▪️▪️▪️▪️ \n💣💣💣💣 \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n")
    await asyncio.sleep(0.5)
    await message.edit("▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n💣💣💣💣 \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n")
    await asyncio.sleep(0.5)
    await message.edit("▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n💣💣💣💣 \n▪️▪️▪️▪️ \n")
    await asyncio.sleep(0.5)
    await message.edit("▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n💣💣💣💣 \n")
    await asyncio.sleep(1)
    await message.edit("▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n💥💥💥💥 \n")
    await asyncio.sleep(0.5)
    await message.edit("▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n💥💥💥💥 \n💥💥💥💥 \n")
    await asyncio.sleep(0.5)
    await message.edit("▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n😵😵😵😵 \n")
    await asyncio.sleep(0.5)
    await message.edit("`RIP......`")
    await asyncio.sleep(2)
    await message.delete()

@app.on_message(filters.command('neprivet', ["."]) & filters.me)
async def hello_world(client: Client, message: Message):
    await message.edit(f'||Сообщение удалится через 10 секунд.||\n\n<b>Пожалуйста, не пишите просто «Привет» в чате! neprivet.com</b>\n\n||Сообщение удалится через 10 секунд.||')
    await asyncio.sleep(10)
    await message.delete()

@app.on_message(filters.command("country", prefixes=".") & filters.me)
async def country_cmd(client: Client, message: Message):
    country1 = "".join(message.command[1])
    country = CountryInfo(country1)
    a = country.population() #Население
    b = country.languages() #Язык
    c = country.capital() #Столица
    c1 = country.capital_latlng() #Координаты столицы
    qwerty = country.latlng() #Приблизительные координаты страны
    e = country.area() #Площадь
    f = country.calling_codes() #Мжд-ный телефонный код
    d = country.currencies() #Валюты
    d2 = country.region() #Общий регион
    d3 = country.subregion() #Более конкретный регион
    d4 = country.timezones() #Часовой пояс
    d5 = country.borders() #Границы
    await message.edit(f'**ИНФОРМАЦИЯ О: [{country1}]\n\nНаселение: {a}\nЯзык: {b}\nСтолица: {c}\nКоординаты столицы: {c1}\nПлощадь: {e} `к²`\nПриблизительные координаты страны: {qwerty}\nМеждународный телефонный код: {f}\nВалюта: {d}\nОбщий регион: {d2}\nБолее конкретный регион: {d3}\nЧасовой пояс: {d4}\nГраницы: {d5}**')

@app.on_message(filters.command("link", prefixes=".") & filters.me)
async def slink(client: Client, message: Message):
    link_input = "".join(message.command[1:])
    pyshort = pyshorteners.Shortener()
    await message.edit('Сокращённая ссылка - ' + pyshort.tinyurl.short(link_input), disable_web_page_preview=True)

@app.on_message(filters.command("uid", prefixes=".") & filters.me)
async def audioss(client: Client, message: Message):
    id = uuid.uuid4()
    await message.edit(f"Сгенерированный уникальный uID:\n\n`{id}`")

@app.on_message(filters.command("day", prefixes=".") & filters.me)
async def calend(client: Client, message: Message):
    try:
        yy = int(message.command[1])
        mm = int(message.command[2])
        a = (calendar.month(yy, mm))
        q = date.today()
        await message.edit(f"`{a}`\n\n<b>||Сегодня: {q}||</b>")
    except ValueError:
        await message.edit('Неправильный ввод!')
        await asyncio.sleep(3)
        await message.delete()
    
    

@app.on_message(filters.command('password', ["."]) & filters.me)
async def password_cmd(_, message):
    command_text = "".join(message.command[1:])
    a = string.ascii_letters + str(string.digits) + string.punctuation
    a2 = string.ascii_letters + str(string.digits)
    b = 15
    password = ''.join(choice(a) for _ in range (b))
    password2 = ''.join(choice(a2) for _ in range (b))
    await message.edit(f"<b>Сгенерированый пароль:</b>\n\n<b> <code>{password}</code> </b>")
    if command_text == 'lite':
        await message.edit(f"<b>Сгенерированый пароль:</b>\n\n<b> <code>{password2}</code> </b>")


def speed_test():
    tester = Speedtest()
    tester.get_best_server()
    tester.download()
    tester.upload()
    return tester.results.dict()

@app.on_message(filters.command('speedtest', ["."]) & filters.me)
async def speedtest_cmd(_, message):
        await message.edit(f"<b>Запускаем тест...</b>")
 
        result = speed_test()
        text = (
            f"<b>Результаты теста:</b>\n\n"
            f"<b>Скачивание:</b> <code>{round(result['download'] / 2 ** 20 / 8, 2)}</code> <b>мб/с</b>\n"
            f"<b>Загрузка:</b> <code>{round(result['upload'] / 2 ** 20 / 8, 2)}</code> <b>мб/c</b>\n"
            f"<b>Задержка:</b> <code>{round(result['ping'], 2)}</code> <b>мc</b>"
        )
        return await message.edit(text)


@app.on_message(filters.command('nometa', ["."]) & filters.me)
async def hello_world(client: Client, message: Message):
    await message.edit(f'||Сообщение удалится через 10 секунд.||\n\n<b>Пожалуйста, не задавайте мета-вопросов в чате! nometa.xyz</b>\n\n||Сообщение удалится через 10 секунд.||')
    await asyncio.sleep(10)
    await message.delete()

@app.on_message(filters.command('hmm', ["."]) & filters.me)
async def hello_world(client: Client, message: Message):
    await edit_or_reply(message,f"┈┈╱▔▔▔▔▔╲┈┈┈HM┈HM\n┈╱┈┈╱▔╲╲╲▏┈┈┈HMMM\n╱┈┈╱━╱▔▔▔▔▔╲━╮┈┈\n▏┈▕┃▕╱▔╲╱▔╲▕╮┃┈┈\n▏┈▕╰━▏▊▕▕▋▕▕━╯┈┈\n╲┈┈╲╱▔╭╮▔▔┳╲╲┈┈┈\n┈╲┈┈▏╭━━━━╯▕▕┈┈┈\n┈┈╲┈╲▂▂▂▂▂▂╱╱┈┈┈\n┈┈┈┈▏┊┈┈┈┈┊┈┈┈╲\n┈┈┈┈▏┊┈┈┈┈┊▕╲┈┈╲\n┈╱▔╲▏┊┈┈┈┈┊▕╱▔╲▕\n┈▏┈┈┈╰┈┈┈┈╯┈┈┈▕▕\n┈╲┈┈┈╲┈┈┈┈╱┈┈┈╱┈╲\n┈┈╲┈┈▕▔▔▔▔▏┈┈╱╲╲╲▏\n┈╱▔┈┈▕┈┈┈┈▏┈┈▔╲▔▔\n┈╲▂▂▂╱┈┈┈┈╲▂▂▂╱┈ ")

@app.on_message(filters.command("help", prefixes=".") & filters.me)
async def help(_, message):
    await message.edit(
        f"""<b>КОМАНДЫ
        .help - помощь по командам.
        .plane - летящий самолётик.
        .id - узнать айди человека/чата.
        .hack - анимация взлома.
        .duck [text] - поиск в 🦆 DuckDuckGo.
        .f [text] - перевёрнутый текст.
        .s - фейковая надпись скриншота.
        .loveyou - надпись с признанием о любви.
        .eval [code]- выполнение простенького кода.
        .hmm - задумчевая обезьяна.
        .stats/.status - инфо моего аккаунта.
        .whois/.info - информация о пользователе.
        .nometa - мета вопрос nometa.xyz.
        .neprivet - непривет сообщение neprivet.com.
        .brain - анимация с мозгом.
        .speedtest - спидтест.
        .password/.password lite - генерирует пароль.
        .day [date, 2022 9] - выводит календарь на месяц.
        .uid - генерирует уникальный ID.
        .link [link] - сокращает ссылку.
        .country [country] - информация о указанной стране.
        .anim [moon, clock, run, car] - анимация.
        .paste/.nekobin/.hastebin/.spacebin - постит реплай/текст.
        .mute - мут реплай/айди.
        .unmute - анмут реплай/айди.
        .dc - инфа о DC
        .love - сердце.
        .qr - генерирует qr код.
        .rep - указать мою репутацию.</b>
    """)

@app.on_message(filters.command("plane", prefixes=".") & filters.me)
async def plane(client: Client, message: Message):
    await message.edit('🌬 ЛЕТИТ САМОЛЁТ ✈')
    await asyncio.sleep(2)
    await message.edit(".✈〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️.")
    await asyncio.sleep(0.20)
    await message.edit(".〰️✈〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️.")
    await asyncio.sleep(0.20)
    await message.edit(".〰️〰️✈〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️.")
    await asyncio.sleep(0.20)
    await message.edit(".〰️〰️〰️✈〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️.")
    await asyncio.sleep(0.20)
    await message.edit(".〰️〰️〰️〰️✈〰️〰️〰️〰️〰️〰️〰️〰️〰️.")
    await asyncio.sleep(0.20)
    await message.edit(".〰️〰️〰️〰️〰️✈〰️〰️〰️〰️〰️〰️〰️〰️.")
    await asyncio.sleep(0.20)
    await message.edit(".〰️〰️〰️〰️〰️〰️✈〰️〰️〰️〰️〰️〰️〰️.")
    await asyncio.sleep(0.20)
    await message.edit(".〰️〰️〰️〰️〰️〰️〰️✈〰️〰️〰️〰️〰️〰️.")
    await asyncio.sleep(0.20)
    await message.edit(".〰️〰️〰️〰️〰️〰️〰️〰️✈〰️〰️〰️〰️〰️.")
    await asyncio.sleep(0.20)
    await message.edit(".〰️〰️〰️〰️〰️〰️〰️〰️〰️✈〰️〰️〰️〰️.")
    await asyncio.sleep(0.20)
    await message.edit(".〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️✈〰️〰️〰️.")
    await asyncio.sleep(0.20)
    await message.edit(".〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️✈〰️〰️.")
    await asyncio.sleep(0.20)
    await message.edit(".〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️✈〰️.")
    await asyncio.sleep(0.20)
    await message.edit(".〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️✈.")
    await asyncio.sleep(1)
    await message.edit('✅ САМОЛЁТ ПРИЛЕТЕЛ ✈')
    await asyncio.sleep(3)
    await message.delete()

@app.on_message(filters.command('id', prefixes=".") & filters.me)
async def id(client: Client, message: Message):
    if message.reply_to_message is None:
        await message.edit(f"This chat ID is: <code>{message.chat.id}</code>")
    else:
        test = f"This user ID is: {message.reply_to_message.from_user.id}\n\nThis chat ID is: <code>{message.chat.id}</code>"
        await message.edit_text(test)
 
# Команда взлома пентагона
@app.on_message(filters.command("hack", prefixes=".") & filters.me)
async def hak(client: Client, message: Message):
    await message.edit_text("Looking for Telegram databases in targeted person...")
    await asyncio.sleep(2)
    await message.edit_text(" User online: True\nTelegram access: True\nRead Storage: True ")
    await asyncio.sleep(2)
    await message.edit_text("Hacking... 0%\n[░░░░░░░░░░░░░░░░░░░░]\n`Looking for Telegram...`\nETA: 0m, 20s")
    await asyncio.sleep(2)
    await message.edit_text("Hacking... 11.07%\n[██░░░░░░░░░░░░░░░░░░]\n`Looking for Telegram...`\nETA: 0m, 18s")
    await asyncio.sleep(2)
    await message.edit_text("Hacking... 20.63%\n[███░░░░░░░░░░░░░░░░░]\n`Found folder C:/Telegram`\nETA: 0m, 16s")  
    await asyncio.sleep(2)
    await message.edit_text("Hacking... 34.42%\n[█████░░░░░░░░░░░░░░░]\n`Found folder C:/Telegram`\nETA: 0m, 14s")
    await asyncio.sleep(2)
    await message.edit_text("Hacking... 42.17%\n[███████░░░░░░░░░░░░░]\n`Searching for databases`\nETA: 0m, 12s")
    await asyncio.sleep(2)
    await message.edit_text("Hacking... 55.30%\n[█████████░░░░░░░░░░░]\n`Found msgstore.db.crypt12`\nETA: 0m, 10s")
    await asyncio.sleep(2)
    await message.edit_text("Hacking... 64.86%\n[███████████░░░░░░░░░]\n`Found msgstore.db.crypt12`\nETA: 0m, 08s")
    await asyncio.sleep(2)
    await message.edit_text("Hacking... 74.02%\n[█████████████░░░░░░░]\n`Trying to Decrypt...`\nETA: 0m, 06s")
    await asyncio.sleep(2)
    await message.edit_text("Hacking... 86.21%\n[███████████████░░░░░]\n`Trying to Decrypt...`\nETA: 0m, 04s")
    await asyncio.sleep(2)
    await message.edit_text("Hacking... 93.50%\n[█████████████████░░░]\n`Decryption successful!`\nETA: 0m, 02s")
    await asyncio.sleep(2)
    await message.edit_text("Hacking... 100%\n[████████████████████]\n`Scanning file...`\nETA: 0m, 00s")
    await asyncio.sleep(2)
    await message.edit_text("Hacking complete!\nUploading file...")
    await asyncio.sleep(2)
    await message.edit_text("Targeted Account Hacked...!\n\n ✅ File has been successfully uploaded to server.\nTelegram Database:\n`./DOWNLOADS/msgstore.db.crypt12`")

@app.on_message(filters.command("brain", ".") & filters.me)
async def pijtau(client: Client, message: Message):
    if message.forward_from:
        return
    animation_interval = 1
    animation_ttl = range(0, 14)
    await message.edit("brain")
    animation_chars = [          
              "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n🧠         <(^_^ <)🗑",
              "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n🧠       <(^_^ <)  🗑",
              "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n🧠     <(^_^ <)    🗑",
              "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n🧠   <(^_^ <)      🗑",
              "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n🧠 <(^_^ <)        🗑",
              "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n🧠<(^_^ <)         🗑",
              "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n(> ^_^)>🧠         🗑",
              "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n  (> ^_^)>🧠       🗑",
              "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n    (> ^_^)>🧠     🗑",
              "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n      (> ^_^)>🧠   🗑",
              "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n        (> ^_^)>🧠 🗑",
              "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n          (> ^_^)>🧠🗑",
              "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n           (> ^_^)>🗑",
              "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n           <(^_^ <)🗑",
          ]
    for i in animation_ttl:
        	
            await asyncio.sleep(animation_interval)
            await message.edit(animation_chars[i %14 ])

@app.on_message(filters.command("duck", prefixes=".") & filters.me)
async def duckgo(client: Client, message: Message):
    input_str = " ".join(message.command[1:])
    sample_url = "https://duckduckgo.com/?q={}".format(input_str.replace(" ", "+"))
    if sample_url:
        link = sample_url.rstrip()
        await message.edit_text(
            "🦆 DuckDuckGo:\n🔎 [{}]({})".format(input_str, link), disable_web_page_preview=True)
    else:
        await message.edit_text("Пожалуйста, попробуйте позже...🐳")

REPLACEMENT_MAP = config.RWORDS

@app.on_message(filters.command("f", prefixes=".") & filters.me)
async def flip(_, msg):
    text = msg.text.split('.f', maxsplit=1)[1]
    final_str = ""
    for char in text:
        if char in REPLACEMENT_MAP.keys():
            new_char = REPLACEMENT_MAP[char]
        else:
            new_char = char
        final_str += new_char
    if text != final_str:
        await msg.edit(final_str)
    else:
        await msg.edit(text)

@app.on_message(filters.command(["s", "screenshot"], prefixes=".") & filters.me)
def take_a_screenshot(app, message):
    message.delete()
    app.send(
        functions.messages.SendScreenshotNotification(
            peer=app.resolve_peer(message.chat.id),
            reply_to_msg_id=0,
            random_id=app.rnd_id(),
        )
    )



RUNNING = "**Eval Expression:**\n```{}```\n**Running...**"
ERROR = "**Eval Expression:**\n```{}```\n**Error:**\n```{}```"
SUCCESS = "**Eval Expression:**\n```{}```\n**Success**"
RESULT = "**Eval Expression:**\n```{}```\n**Result:**\n```{}```"
NOBLE = [ "╲╲╲┏━━┓╭━━━╮╱╱╱\n╲╲╲┗┓┏┛┃╭━╮┃╱╱╱\n╲╲╲╲┃┃┏┫┃╭┻┻┓╱╱\n╱╱╱┏╯╰╯┃╰┫┏━╯╱╱\n╱╱┏┻━┳┳┻━┫┗┓╱╱╱\n╱╱╰━┓┃┃╲┏┫┏┛╲╲╲\n╱╱╱╱┃╰╯╲┃┃┗━╮╲╲\n╱╱╱╱╰━━━╯╰━━┛╲╲", "┏━╮\n┃▔┃▂▂┏━━┓┏━┳━━━┓\n┃▂┣━━┻━╮┃┃▂┃▂┏━╯\n┃▔┃▔╭╮▔┃┃┃▔┃▔┗━┓\n┃▂┃▂╰╯▂┃┗╯▂┃▂▂▂┃\n┃▔┗━━━╮┃▔▔▔┃▔┏━╯\n┃▂▂▂▂▂┣╯▂▂▂┃▂┗━╮\n┗━━━━━┻━━━━┻━━━┛", "┏┓┏━┳━┳━┳━┓\n┃┗┫╋┣┓┃┏┫┻┫\n┗━┻━┛┗━┛┗━┛\n────­­­­­­­­­YOU────", "╦──╔╗─╗╔─╔ ─\n║──║║─║║─╠ ─\n╚═─╚╝─╚╝─╚ ─\n╦─╦─╔╗─╦╦   \n╚╦╝─║║─║║ \n─╩──╚╝─╚╝" , "╔══╗....<3 \n╚╗╔╝..('\../') \n╔╝╚╗..( •.• ) \n╚══╝..(,,)(,,) \n╔╗╔═╦╦╦═╗ ╔╗╔╗ \n║╚╣║║║║╩╣ ║╚╝║ \n╚═╩═╩═╩═╝ ╚══╝", "░I░L░O░V░E░Y░O░U░", "┈┈╭━╱▔▔▔▔╲━╮┈┈┈\n┈┈╰╱╭▅╮╭▅╮╲╯┈┈┈\n╳┈┈▏╰┈▅▅┈╯▕┈┈┈┈\n┈┈┈╲┈╰━━╯┈╱┈┈╳┈\n┈┈┈╱╱▔╲╱▔╲╲┈┈┈┈\n┈╭━╮▔▏┊┊▕▔╭━╮┈╳\n┈┃┊┣▔╲┊┊╱▔┫┊┃┈┈\n┈╰━━━━╲╱━━━━╯┈╳", "╔ღ═╗╔╗\n╚╗╔╝║║ღ═╦╦╦═ღ\n╔╝╚╗ღ╚╣║║║║╠╣\n╚═ღ╝╚═╩═╩ღ╩═╝", "╔══╗ \n╚╗╔╝ \n╔╝(¯'v'¯) \n╚══'.¸./\n╔╗╔═╦╦╦═╗ ╔╗╔╗ \n║╚╣║║║║╩╣ ║╚╝║ \n╚═╩═╩═╩═╝ ╚══╝", "╔╗ \n║║╔═╦═╦═╦═╗ ╔╦╗ \n║╚╣╬╠╗║╔╣╩╣ ║║║ \n╚═╩═╝╚═╝╚═╝ ╚═╝ \n╔═╗ \n║═╬═╦╦╦═╦═╦═╦═╦═╗ \n║╔╣╬║╔╣╩╬╗║╔╣╩╣╔╝ \n╚╝╚═╩╝╚═╝╚═╝╚═╩╝", "╔══╗ \n╚╗╔╝ \n╔╝╚╗ \n╚══╝ \n╔╗ \n║║╔═╦╦╦═╗ \n║╚╣║║║║╚╣ \n╚═╩═╩═╩═╝ \n╔╗╔╗ ♥️ \n║╚╝╠═╦╦╗ \n╚╗╔╣║║║║ \n═╚╝╚═╩═╝", "╔══╗╔╗  ♡ \n╚╗╔╝║║╔═╦╦╦╔╗ \n╔╝╚╗║╚╣║║║║╔╣ \n╚══╝╚═╩═╩═╩═╝\n­­­─────­­­­­­­­­YOU─────", "╭╮╭╮╮╭╮╮╭╮╮╭╮╮ \n┃┃╰╮╯╰╮╯╰╮╯╰╮╯ \n┃┃╭┳━━┳━╮╭━┳━━╮ \n┃┃┃┃╭╮┣╮┃┃╭┫╭╮┃ \n┃╰╯┃╰╯┃┃╰╯┃┃╰┻┻╮ \n╰━━┻━━╯╰━━╯╰━━━╯", "┊┊╭━╮┊┊┊┊┊┊┊┊┊┊┊ \n━━╋━╯┊┊┊┊┊┊┊┊┊┊┊ \n┊┊┃┊╭━┳╮╭┓┊╭╮╭━╮ \n╭━╋━╋━╯┣╯┃┊┃╰╋━╯ \n╰━╯┊╰━━╯┊╰━┛┊╰━━"
]

@app.on_message(filters.me & (filters.command("loveyou", prefixes=".") | filters.regex("^loveyou ")))
async def _(client: Client, message: Message):
    noble = random.randint(1, len(NOBLE) - 2)
    reply_text = NOBLE[noble] 
    await edit_or_reply(message, reply_text)

@app.on_message(filters.command('eval', prefixes=".") & filters.me)
def eval_expression(client, message):
    expression = " ".join(message.command[1:])

    if expression:
        m = message.reply(RUNNING.format(expression))

        try:
            result = eval(expression)
        except Exception as error:
            client.edit_message_text(
                m.chat.id,
                m.message_id,
                ERROR.format(expression, error)
            )
        else:
            if result is None:
                client.edit_message_text(
                    m.chat.id,
                    m.message_id,
                    SUCCESS.format(expression)
                )
            else:
                client.edit_message_text(
                    m.chat.id,
                    m.message_id,
                    RESULT.format(expression, result)
                )

@app.on_message(filters.command(["stats", "status"], ".") & filters.me)
async def stats(client: Client, message: Message):
    await message.edit_text("Collecting stats...")
    start = datetime.now()
    u = 0
    g = 0
    sg = 0
    c = 0
    b = 0
    a_chat = 0
    Meh=await client.get_me()
    group = ["supergroup", "group"]
    async for dialog in client.iter_dialogs():
        if dialog.chat.type == "private":
            u += 1
        elif dialog.chat.type == "bot":
            b += 1
        elif dialog.chat.type == "group":
            g += 1
        elif dialog.chat.type == "supergroup":
            sg += 1
            user_s = await dialog.chat.get_member(int(Meh.id))
            if user_s.status in ("creator", "administrator"):
                a_chat += 1
        elif dialog.chat.type == "channel":
            c += 1

    end = datetime.now()
    ms = (end - start).seconds
    await message.edit_text(
        """**ʏᴏᴜʀ ꜱᴛᴀᴛꜱ ꜰᴇᴀᴛᴄʜᴇᴅ ɪɴ {} ꜱᴇᴄᴏɴᴅꜱ ⚡**

⚡**ʏᴏᴜ ʜᴀᴠᴇ {} ᴘʀɪᴠᴀᴛᴇ ᴍᴇꜱꜱᴀɢᴇꜱ.**
🏷️**ʏᴏᴜ ʜᴀᴠᴇ ᴊᴏɪɴᴇᴅ {} ɢʀᴏᴜᴘꜱ.**
🏷️**ʏᴏᴜ ʜᴀᴠᴇ ᴊᴏɪɴᴇᴅ {} ꜱᴜᴘᴇʀ ɢʀᴏᴜᴘꜱ.**
🏷️**ʏᴏᴜ ʜᴀᴠᴇ ᴊᴏɪɴᴇᴅ {} ᴄʜᴀɴɴᴇʟꜱ.**
🏷️**ʏᴏᴜ ᴀʀᴇ ᴀᴅᴍɪɴꜱ ɪɴ {} ᴄʜᴀᴛꜱ.**
🏷️**ʙᴏᴛꜱ ɪɴ ʏᴏᴜʀ ᴘʀɪᴠᴀᴛᴇ = {}**

⚠️**ꜰᴇᴀᴛᴄʜᴇᴅ ʙʏ ᴜꜱɪɴɢ @MrMozozavr**""".format(
            ms, u, g, sg, c, a_chat, b
        )
    )

WHOIS = (
    '**ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЕ: "{full_name}"**\n'
    "[Ссылка на профиль](tg://user?id={user_id})\n"
    "════════════════\n"
    "ID: `{user_id}`\n"
    "Имя: `{first_name}`\n"
    "Фамилия: `{last_name}`\n"
    "Юзернейм: `{username}`\n"
    "Последний раз в сети: `{last_online}`\n"
    "Общие группы: `{common_groups}`\n"
    "════════════════\n"
    "О себе:\n{bio}"
)

WHOIS_PIC = (
    '**ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЕ: "{full_name}"**\n'
    "[Ссылка на профиль](tg://user?id={user_id})\n"
    "════════════════\n"
    "ID: `{user_id}`\n"
    "Имя: `{first_name}`\n"
    "Фамилия: `{last_name}`\n"
    "Юзернейм: `{username}`\n"
    "Последний раз в сети: `{last_online}`\n"
    "Общие группы: `{common_groups}`\n"
    "════════════════\n"
    "Кол-во фото профиля: `{profile_pics}`\n"
    "Последнее обновление: `{profile_pic_update}`\n"
    "════════════════\n"
    "О себе:\n{bio}"
)


def LastOnline(user: User):
    if user.is_bot:
        return ""
    elif user.status == "recently":
        return "недавно"
    elif user.status == "within_week":
        return "на этой неделе"
    elif user.status == "within_month":
        return "в этом месяце"
    elif user.status == "long_time_ago":
        return "давно :("
    elif user.status == "online":
        return "в сети"
    elif user.status == "offline":
        return datetime.fromtimestamp(user.last_online_date).strftime(
            "%a, %d %b %Y, %H:%M:%S"
        )


async def GetCommon(bot: Client, get_user):
    common = await bot.send(
        functions.messages.GetCommonChats(
            user_id=await bot.resolve_peer(get_user), max_id=0, limit=0
        )
    )
    return common


def FullName(user: User):
    return user.first_name + " " + user.last_name if user.last_name else user.first_name


def ProfilePicUpdate(user_pic):
    return datetime.fromtimestamp(user_pic[0].date).strftime("%d.%m.%Y, %H:%M:%S")


@app.on_message(filters.command(["whois", "info"], ["."]) & filters.me)
async def who_is(bot: Client, message: Message):
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        get_user = message.from_user.id
    elif message.reply_to_message and len(cmd) == 1:
        get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
        try:
            get_user = int(cmd[1])
        except ValueError:
            pass
    try:
        user = await bot.get_users(get_user)
    except PeerIdInvalid:
        await message.edit("Я не знаю этого пользователя.")
        await asyncio.sleep(2)
        await message.delete()
        return

    user_details = await bot.get_chat(get_user)
    bio = user_details.bio
    user_pic = await bot.get_profile_photos(user.id)
    pic_count = await bot.get_profile_photos_count(user.id)
    common = await GetCommon(bot, user.id)

    if not user.photo:
        await message.edit(
            WHOIS.format(
                full_name=FullName(user),
                user_id=user.id,
                first_name=user.first_name,
                last_name=user.last_name if user.last_name else "",
                username=user.username if user.username else "",
                last_online=LastOnline(user),
                common_groups=len(common.chats),
                bio=bio if bio else "`No bio set up.`",
            ),
            disable_web_page_preview=True,
        )
    elif user.photo:
        await bot.send_photo(
            message.chat.id,
            user_pic[0].file_id,
            caption=WHOIS_PIC.format(
                full_name=FullName(user),
                user_id=user.id,
                first_name=user.first_name,
                last_name=user.last_name if user.last_name else "",
                username=user.username if user.username else "",
                last_online=LastOnline(user),
                profile_pics=pic_count,
                common_groups=len(common.chats),
                bio=bio if bio else "`No bio set up.`",
                profile_pic_update=ProfilePicUpdate(user_pic),
            ),
            reply_to_message_id=ReplyCheck(message),
        )

        await message.delete()



app.run()
