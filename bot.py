import logging
from telegram import *
from telegram.ext import *
import requests
import os

TOKEN = os.environ["TOKEN"]
TENOR_KEY = os.environ["TENOR"]

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
    '''
    Here are the commands:
    /help - show all the commands
    /meow - random cat image
    /meme - random meme from reddit
    /meme [arg] - random post from a specific subreddit
    /gif [arg] - gif about the argument given
    /dad_joke - random dad joke
    /cat_fact - random cat fact
    /fake_advice - random advice
    /bored - idea when you're bored
    ''')
    
async def handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Get the user input
    user_input = update.message.text
    print(user_input)

async def meow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    message = await context.bot.send_message(chat_id=chat_id, text="Meowingg....")
    image_url = "https://cataas.com/cat"

    try:
        response = requests.get(image_url)
        await context.bot.send_photo(chat_id=chat_id, photo=response.content)
        await context.bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text="Meow🐱 Meow🐱 Meow🐱")
    except:
        await context.bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text='Oops! Something went wrong. Try again later.')

async def meme(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id

    if (len(context.args) == 0):
        meme_res = requests.get("https://meme-api.com/gimme")
        message = await context.bot.send_message(chat_id=chat_id, text='Cooking some fresh memes from <i>reddit</i>....', parse_mode='HTMl')
    else:
        meme_res = requests.get(f"https://meme-api.com/gimme/{context.args[0]}")
        message = await context.bot.send_message(chat_id=chat_id, text=f'Cooking some fresh memes from subreddit <b><i>{context.args[0]}</i></b>', parse_mode='HTMl')
    
    if meme_res.status_code == 200:
        image_url = meme_res.json()['url'] # url of the meme

        try:
            response = requests.get(image_url)
            await context.bot.send_photo(chat_id=chat_id, photo=response.content)

            if 'title' in meme_res.json():
                await context.bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text=meme_res.json()['title'])
            else:
                await context.bot.delete_message(chat_id=chat_id, message_id=message.message_id)

        except:
            await context.bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text='Oops! Something went wrong. Try again later.')
    else:
        await context.bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text=meme_res.json()['message'])       

async def gif(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    search_term = ' '.join(context.args)
    gif_response = requests.get("https://tenor.googleapis.com/v2/search?q=%s&key=%s&client_key=%s&limit=%s" % (search_term, TENOR_KEY, "eccentric bot telegram",  1))

    if gif_response.status_code == 200:
        gif_json = gif_response.json()
        gif_url = gif_json['results'][0]['media_formats']['gif']['url']

        await context.bot.send_animation(chat_id=update.message.chat_id, animation=gif_url)
    else:
        await update.message.reply_text("Oops! Something went wrong.")

async def dad_joke(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # chat id
    chat_id = update.message.chat_id
    message = await context.bot.send_message(chat_id=chat_id, text='Cooking some fresh dad jokes....')

    headers = { "Accept": "application/json" }
    joke_res = requests.get("https://icanhazdadjoke.com/", headers=headers)

    if joke_res.status_code == 200:
        await context.bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text=joke_res.json()["joke"])
    else:
        await context.bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text='Oops! Something went wrong. Try again later.')

async def cat_fact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # chat id
    chat_id = update.message.chat_id
    message = await context.bot.send_message(chat_id=chat_id, text='Cat fact, huh🙄..')

    headers = { "Accept": "application/json" }
    joke_res = requests.get("https://catfact.ninja/fact", headers=headers)

    if joke_res.status_code == 200:
        await context.bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text=joke_res.json()["fact"])
    else:
        await context.bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text='hehe 🙂, no fact for now.')
        
async def advice_quotes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # chat id
    chat_id = update.message.chat_id
    message = await context.bot.send_message(chat_id=chat_id, text='Lil kiddo need some advices huh 😏..')

    headers = { "Accept": "application/json" }
    joke_res = requests.get("https://api.adviceslip.com/advice", headers=headers)

    if joke_res.status_code == 200:
        await context.bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text=joke_res.json()["slip"]["advice"])
    else:
        await context.bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text='hehe 🙂, no advice for now.')

async def bored(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # chat id
    chat_id = update.message.chat_id
    message = await context.bot.send_message(chat_id=chat_id, text='Ok, lemme think..')

    headers = { "Accept": "application/json" }
    joke_res = requests.get("https://www.boredapi.com/api/activity", headers=headers)

    if joke_res.status_code == 200:
        await context.bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text=joke_res.json()["activity"])
    else:
        await context.bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text='Do whatever you want to do, lil kiddo')

async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # chat id
    chat_id = update.message.chat_id
    message = await context.bot.send_message(chat_id=chat_id, text='Humor on the way 🚗')

    categories = ['Programming', 'Misc', 'Dark' 'Pun', 'Spooky', 'Christmas']
    headers = { "Accept": "application/json" }
    
    if len(context.args) != 0:
        arg = context.args[0]
        if arg in categories:
            joke_res = requests.get(f"https://v2.jokeapi.dev/joke/{arg}", headers=headers)
        else:
            joke_res = requests.get("https://v2.jokeapi.dev/joke/Any", headers=headers)
    else:
        joke_res = requests.get("https://v2.jokeapi.dev/joke/Any", headers=headers)

    if joke_res.status_code == 200:
        json = joke_res.json()
        if json['type'] == 'single':
            await context.bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text=json["joke"])
        else:
            await context.bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text=f"{json['setup']}\n{json['delivery']}")
    else:
        await context.bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text='Oops! Humor crashed 😐')

async def number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # chat id
    chat_id = update.message.chat_id
    message = await context.bot.send_message(chat_id=chat_id, text='Numbers huh! lets see what I got 🙄..')

    headers = { "Accept": "application/json" }
    joke_res = requests.get("http://numbersapi.com/random/trivia?json", headers=headers)

    if joke_res.status_code == 200:
        await context.bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text=joke_res.json()["text"])
    else:
        await context.bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text='hehe 🙂, no number for now.')

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("meow", meow))
    application.add_handler(CommandHandler("meme", meme))
    application.add_handler(CommandHandler("gif", gif))
    application.add_handler(CommandHandler("dad_joke", dad_joke))
    application.add_handler(CommandHandler("cat_fact", cat_fact))
    application.add_handler(CommandHandler("fake_advice", advice_quotes))
    application.add_handler(CommandHandler("bored", bored))
    application.add_handler(CommandHandler("joke", joke))
    application.add_handler(CommandHandler("number", number))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_input))
    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
