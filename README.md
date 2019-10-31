# MineiroBot

Bot de telegram para ajudar a organizar pedidos de almoço em grupo

### Como criar um token de acesso?

Há um bot para isso. Basta conversar com o [BotFather][botfather] e seguir alguns passos simples. Depois de criar um bot e receber seu token de autorização.

### Configuração

Criar arquivo `.env` com variáveis de ambiente e setar a variáveis

```
TELEGRAM_TOKEN="<INSER_API_KEY>"
ALLOWED_CHATS="<ALLOWED_CHAT_ID>,<ALLOWED_CHAT_ID>,..."
```

### Comandos

Para executar, basta chamar o arquivo principal

```
python mineirobot.py
```

[botfather]: https://telegram.me/botfather