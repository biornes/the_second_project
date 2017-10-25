from sympy import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import telebot
#import cherrypy
from telebot import types
x = Symbol('x')
f = Symbol('f')
import misk_math
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations, implicit_multiplication_application)
token = misk_math.token
bot = telebot.TeleBot(token)
funcs = ['Интеграл', 'Производная', 'Предел']
FLAG = 0.0
ARG_LIM = ''
#bot.remove_webhook()
#функции обработки запроса:
#limit
#integral
#diff
#
#
#
bot.remove_webhook()


# WEBHOOK_HOST = '188.225.82.13'
# WEBHOOK_PORT = 443  # 443, 80, 88 или 8443 (порт должен быть открыт!)
# WEBHOOK_LISTEN = '188.225.82.13'  # На некоторых серверах придется указывать такой же IP, что и выше

# WEBHOOK_SSL_CERT = 'ssl/webhook_cert.pem'  # Путь к сертификату
# WEBHOOK_SSL_PRIV = 'ssl/webhook_pkey.pem'  # Путь к приватному ключу

# WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
# WEBHOOK_URL_PATH = "/%s/" % (misk_math.token)

# class WebhookServer(object):
#     @cherrypy.expose
#     def index(self):
#         if 'content-length' in cherrypy.request.headers and \
#                         'content-type' in cherrypy.request.headers and \
#                         cherrypy.request.headers['content-type'] == 'application/json':
#             length = int(cherrypy.request.headers['content-length'])
#             json_string = cherrypy.request.body.read(length).decode("utf-8")
#             update = telebot.types.Update.de_json(json_string)
#             # Эта функция обеспечивает проверку входящего сообщения
#             bot.process_new_updates([update])
#             return ''
#         else:
#             raise cherrypy.HTTPError(403)


def parse_req(request):
	print (request)
	request = parse_expr(request, transformations=(standard_transformations + (implicit_multiplication_application,)))
	request = str(request)
	return request

def make_png(answer):
	plt.close()
	plt.clf()
	plt.cla()
	fig = plt.figure()
	ax = fig.add_axes([0,0,1,1])
	ax.set_axis_off()
		### Отрисовка формулы
	t = ax.text(0.5, 0.5, answer,
	        horizontalalignment='center',
	        verticalalignment='center',
	        fontsize=20, color='black')
		        
		### Определение размеров формулы
	ax.figure.canvas.draw()
	bbox = t.get_window_extent()
		# Установка размеров области отрисовки
	fig.set_size_inches(bbox.width/80,bbox.height/80)
	plt.savefig('test.png', dpi=300)
	plt.close()
	plt.clf()
	plt.cla()

	#return menu()

def buttons ():
	keyboard = types.InlineKeyboardMarkup()
	butns = []
	for i in funcs:
		butns.append(types.InlineKeyboardButton(text = i, callback_data = i))
	keyboard.add(*butns)
	return keyboard

#@bot.
def button_cancel ():
	keyboard = types.InlineKeyboardMarkup()
	butns = []
	butns.append(types.InlineKeyboardButton(text = 'Отмена', callback_data = 'Отмена'))
	keyboard.add(*butns)
	return keyboard

def buttons_lim ():
	keyboard = types.InlineKeyboardMarkup()
	butns = []
	butns.append(types.InlineKeyboardButton(text = 'Бесконечность', callback_data = 'oo'))


@bot.message_handler(commands = ['start'])
def menu(text):
	bot.send_message(chat_id = text.chat.id,
			text = 'hello',
			parse_mode= 'Markdown',
			reply_markup= buttons())



@bot.callback_query_handler(func=lambda c: True)
def menu(obj):
	#print (obj)
	global FLAG
	if obj.data == 'Отмена':
		#keyboard = types.ReplyKeyboardRemove(selective = True)
		bot.edit_message_text(chat_id = obj.message.chat.id,
			 			message_id = obj.message.message_id,
						text = "Меню",
						parse_mode= 'Markdown',
						reply_markup= buttons())
	if obj.data == 'Интеграл':
		bot.edit_message_text(chat_id = obj.message.chat.id, message_id = obj.message.message_id, text = 'Введите ваш запрос')
		FLAG = 1
	if obj.data == 'Производная':
		bot.edit_message_text(chat_id = obj.message.chat.id, message_id = obj.message.message_id, text = 'Введите ваш запрос')
		FLAG = 2
	if obj.data == 'Предел':
		FLAG = 3
		bot.edit_message_text(chat_id = obj.message.chat.id, message_id = obj.message.message_id, text = 'Введите к чему стремится аргумент')

@bot.message_handler(content_types= 'text')
def main(text):
	quest = ''
	answer = ''
	request = text.text
	global ARG_LIM
	global FLAG
	flag = FLAG
	if flag == 1:
		make_png(integration(request))
	elif flag == 2:
		make_png(different(request))
	elif flag == 3:
		ARG_LIM = request
		bot.send_message(chat_id = text.chat.id, text = 'Введите функцию')
		FLAG = 3.1
		
	elif flag == 3.1:
		make_png(lim(request, ARG_LIM))
	if flag!=3.0:
		photo = open('test.png', 'rb')
		bot.send_photo(chat_id = text.chat.id,photo = photo)
		photo.close()
		bot.send_message(chat_id = text.chat.id, text = 'Меню', reply_markup= buttons())


def integration(request):
	request = parse_req(request)
	quest = latex(Integral(request, x))
	answer = latex(integrate(request, x))
	string = '$'+ quest+' = '+answer+'$'
	return string

def different(request):
	request = parse_req(request)
	quest = latex(request)
	answer = latex(diff(request, x))
	string = '$'+"("+ quest+")'"+' = '+answer+'$'
	return string

def lim(request, ARG_LIM):
	if ARG_LIM == 'oo':
		ARG_LIM = oo
	quest = latex(request)
	request = parse_req(request)
	if ARG_LIM == oo:
		answer = latex(limit(request, x, oo))
		#ARG_LIM = oo
		ARG_LIM = '\\infty'
	quest = latex("\lim_{x\\"+"to " +ARG_LIM+ "}" + "\\frac{"+ request+"}")
	string = '$'+ quest+' = '+answer+'$'
	return string

bot.polling()

# bot.remove_webhook()

#  # Ставим заново вебхук
# bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
#                 certificate=open(WEBHOOK_SSL_CERT, 'r'))
# cherrypy.config.update({
#     'server.socket_host': WEBHOOK_LISTEN,
#     'server.socket_port': WEBHOOK_PORT,
#     'server.ssl_module': 'builtin',
#     'server.ssl_certificate': WEBHOOK_SSL_CERT,
#     'server.ssl_private_key': WEBHOOK_SSL_PRIV
# })

#  # Собственно, запуск!
# cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})