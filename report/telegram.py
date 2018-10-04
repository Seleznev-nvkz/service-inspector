from pprint import pformat
from telegram.ext import Updater, CommandHandler
from telegram.parsemode import ParseMode

# TELEGRAM_TOKEN = 'token'
# TELEGRAM_CHANNEL = 'channel'
CHECKER_URL = ''


def formatting_text(data: dict) -> str:
    result = ''
    s = ' '
    for project, check in data.items():
        result += f'\n<code>{project}</code>\n'
        for check_name, details in check.items():
            ok, detail = details
            if not ok:  # alarm
                result += f'{s*4}<b>{check_name}</b>\n'
                if detail:
                    for detail_name, status in detail.items():
                        result += f'{s*8}<i>{detail_name} - {status}</i>\n'
    return result


class Bot:
    _client = None
    url = CHECKER_URL
    commands = ['help', 'status', 'mute', 'unmute', 'details']
    muted = False

    def __init__(self):
        self.TOKEN = TELEGRAM_TOKEN
        self.channel = TELEGRAM_CHANNEL

    @property
    def client(self):
        if self._client is None:
            self._client = Updater(token=self.TOKEN)
        return self._client

    @classmethod
    def send(cls, bot, msg):
        bot.send_message(cls.channel, msg, parse_mode=ParseMode.HTML)

    def status(self, bot, update):
        """ show status of hawkeye and url to site """
        self.send(bot, f'Running - <a href="{self.url}">link</a>')

    def details(self, bot, update):
        """ all current states """
        from app import keeper

        if keeper.is_launched:
            self.send(bot, pformat(keeper.data, depth=4))
            print(keeper.data)
        else:
            keeper.run()
            self.send(bot, 'Was not launched.\nRunning...')

    def mute(self, bot, update):
        """ mute all commands """
        self.muted = True
        self.send(bot, 'Muted')

    def unmute(self, bot, update):
        """ unmute all commands """
        self.muted = False
        self.send(bot, 'Unmuted')

    def help(self, bot, update):
        """ show available commands """
        msg = ''
        for command in self.commands:
            msg += f'/{command} -{getattr(self, command).__doc__}\n'
        self.send(bot, msg)

    def start_polling(self):
        """ mb on future """
        for command in self.commands:
            self.client.dispatcher.add_handler(CommandHandler(command, getattr(self, command)))
        self.client.start_polling()


class TelegramReporter:
    bot = None

    def __init__(self):
        try:
            self.bot = Bot()
            self.bot.start_polling()
        except NameError:
            print('Telegram bot disabled')

    def send_alarm(self, data: dict):
        if self.bot and not self.bot.muted:
            self.bot.send(self.bot.client.bot, formatting_text(data))
