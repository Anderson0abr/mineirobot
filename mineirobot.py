# Python Imports
import datetime
import os
import telebot

from collections import OrderedDict

# Thirt Party Imports
from dotenv import load_dotenv

load_dotenv()

# Constants
ALLOWED_CHATS = os.getenv("ALLOWED_CHATS").split(',')
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

bot = telebot.TeleBot(TELEGRAM_TOKEN, threaded=False)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if check(message):
        text = "Comandos\n\n" + \
                "Adicionar pedido: /add seu_pedido\n" + \
                "Remover pedido: /remove\n" + \
                "Editar lista: /edit nova_lista\n" + \
                "Informações de pagamento: /pay\n" + \
                "Imprimir lista: /list\n" + \
                "Apagar lista: /reset\n" + \
                "Cardápio: /menu"
        bot.reply_to(message, text)


@bot.message_handler(commands=['list'])
def list_orders(message):
    if check(message):
        global header, orders, total_pessoas
        update_things()
        bot.reply_to(message, header + "\n".join(orders) + "\nTotal: {} pessoa(s)".format(total_pessoas))


@bot.message_handler(commands=['add'])
def add_order(message):
    if check(message):
        global header, orders, total_pessoas
        if message.text == "/add":
            bot.reply_to(message, "Insira o pedido")
        elif (len("\n".join(orders)) + len(message.text) - 4) > 2900:
            bot.reply_to(message, "A lista está muito longa. Ignorando..")
        else:
            if len(message.text) > 100:
                bot.reply_to(message, "Pedido muito longo..Truncando")
            text = message.text[5:105]
            orders.append("{} {}: {}".format(message.from_user.first_name, message.from_user.last_name or "", text))
            update_things()
            bot.reply_to(message, header + "\n".join(orders) + "\nTotal: {} pessoa(s)".format(total_pessoas))


@bot.message_handler(commands=['edit'])
def edit_order(message):
    if check(message):
        global header, orders, total_pessoas
        if message.text == "/edit":
            bot.reply_to(message, "Copie a lista atual, edite e cole depois do /edit")
        elif len(message.text) > 2900:
            bot.reply_to(message, "A lista está muito longa. Ignorando..")
        else:
            orders = [x[:100] for x in message.text[6:].split("\n") if not x.startswith(("Total: ", "+-----", "/edit")) and x]
            update_things()
            bot.reply_to(message, header + "\n".join(orders) + "\nTotal: {} pessoas".format(total_pessoas))


@bot.message_handler(commands=['remove'])
def remove_order(message):
    if check(message):
        global header, orders, total_pessoas
        orders = [x for x in orders if not x.startswith("{} {}".format(message.from_user.first_name, message.from_user.last_name or ""))]
        update_things()
        bot.reply_to(message, header + "\n".join(orders) + "\nTotal: {} pessoa(s)".format(total_pessoas))


@bot.message_handler(commands=['reset'])
def reset_order(message):
    if check(message):
        global orders
        orders = []
        update_things()
        bot.reply_to(message, "Lista zerada")


@bot.message_handler(commands=['pay'])
def close_order(message):
    if check(message):
        global header, orders, total_pedidos, total_pessoas
        if not orders:
            bot.reply_to(message, "A lista está vazia")
        else:
            frete = 3
            price = frete / total_pessoas
            text = "Taxa para {} pessoas: {:.2f}\n\n".format(total_pessoas, price)
            for item, valor in get_cardapio().items():
                text += "{}: {:.2f}\n".format(item, valor + price)
            text += "Refrigerante lata: 5.00\n\n*Caso tenha pedido mais de um prato, adicione o valor do mesmo desconsiderando a taxa de entrega"
            bot.reply_to(message, text)


@bot.message_handler(commands=['menu'])
def print_menu(message):
    if check(message):
        bot.reply_to(message, "https://www.ifood.com.br/delivery/fortaleza-ce/mineiro-delivery---aldeota-aldeota")


def check(message):
    if message.chat.id in ALLOWED_CHATS:
        return True
    else:
        bot.send_message(message.chat.id, "Chat não cadastrado")
        return False


def update_things():
    global path, header, orders, total_pessoas, total_pedidos
    date = datetime.datetime.now().strftime("%d/%m")
    header = "+----- Almoço Mineiro {} -----+\n".format(date)
    total_pedidos = len(orders)
    total_pessoas = len(set([order.split(':')[0] for order in orders]))
    with open(path, "w") as f:
        f.write("\n".join(orders))


def get_cardapio():
    cardapio = OrderedDict()
    cardapio["Do dia"] = 13.90
    cardapio["Do dia (carbonara)"] = 14.90
    cardapio["Do dia, com refri"] = 16.90
    cardapio["Do dia 700"] = 19.90
    cardapio["Do mato"] = 12.90
    cardapio["Do mato com frango"] = 14.90
    cardapio["Paella Mineira"] = 19.90
    cardapio["Pratos comuns"] = 17.90
    return cardapio


root_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(root_dir, "orders.txt")
header = ""
total_pedidos = 0
total_pessoas = 0
try:
    with open(path) as f:
        orders = [x.strip() for x in f.readlines() if not x.startswith(("Total: ", "+-----"))]
except:
    orders = []
update_things()
bot.infinity_polling()
