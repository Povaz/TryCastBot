from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from category import *
from timer_utils import *
import datetime
from pytz import UTC

categories = []


def command(update, context):
    """Command Description."""
    try:
        return 0
    except Exception:
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')
        raise Exception


def newcategory(update, context):
    """Add a new note Category"""
    global categories
    try:
        categories.append(Category(context.args[0]))
        update.message.reply_text('Category created successfully', parse_mode='Markdown')
    except Exception:
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')
        raise Exception


def delcategory(update, context):
    """Delete Category"""
    global categories
    try:
        cat_name = context.args[0]
        categories = [cat for cat in categories if cat.name != cat_name]
        update.message.reply_text('Category deleted successfully', parse_mode='Markdown')
    except Exception:
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')
        raise Exception


def newnote(update, context):
    """Add a Note to the Category"""
    global categories
    try:
        cat_name = context.args[0]
        note_text = ''
        for arg in context.args[1:]:
            note_text += arg + ' '
        cat = [cat for cat in categories if cat.name == cat_name][0]
        cat.add_note(note_text)
        update.message.reply_text('Note added!', parse_mode='Markdown')
    except Exception:
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')
        raise Exception


def delnote(update, context):
    """Add a Note to the Category"""
    global categories
    try:
        cat_name = context.args[0]
        note_id = context.args[1]
        print(note_id)
        cat = [cat for cat in categories if cat.name == cat_name][0]
        cat.del_note(note_id)
        update.message.reply_text('Note deleted!', parse_mode='Markdown')
    except Exception:
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')
        raise Exception


def notelist(update, context):
    """Get the list of all Notes"""
    global categories
    try:
        msg = ''
        for cat in categories:
            msg += cat.get_text() + '\n'
        update.message.reply_text(msg, parse_mode='Markdown')
    except Exception:
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')
        raise Exception


def notelist_timed(context):
    """Timed function to return the list of Notes."""
    global categories
    msg = ''
    for cat in categories:
        msg += cat.get_text() + '\n'
    job = context.job
    sent = context.bot.send_message(job.context, text=msg, parse_mode='Markdown')
    context.bot.pin_chat_message(chat_id=job.name, message_id=sent.message_id)


def help(update, context):
    """Get the list of all Notes"""
    global categories
    try:
        msg = '/newcategory _categoryname_: Add a new note Category.\n' \
              '/delcategory _categoryname_: Delete a note Category. \n' \
              '/newnote _categoryname note_: Add a new Note for the Category. \n' \
              '/delnote _categoryname noteid_: Delete a Note for the Category. \n' \
              '/notelist: Return all notes. \n' \
              '/help: Return all commands. \n'
        update.message.reply_text(msg, parse_mode='Markdown')
    except Exception:
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')
        raise Exception


def set_timer(update, context):
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    try:
        hour = int(context.args[0] - 1)
        min = int(context.args[1])

        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_daily(notelist_timed, time=datetime.time(hour=hour, minute=min, second=0, microsecond=0,
                                                                       tzinfo=UTC), context=chat_id, name=str(chat_id))

        text = 'Timer successfully set!'
        if job_removed:
            text += ' Old one was removed.'
        update.message.reply_text(text)

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds>')


def unset_timer(update, context):
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Timer successfully cancelled!' if job_removed else 'You have no active timer.'
    update.message.reply_text(text)


# Unrecognized command
def notfound(update, context):
    """Command not recognized"""
    update.message.reply_text('This command does not exist. COJO, neanche scrivere.', parse_mode='Markdown')


def main():
    # Load Secret Token
    try:
        with open('files/token', 'r') as file:
            token = file.read()
    except FileNotFoundError:
        raise FileNotFoundError

    # Create Updater (and thus the bot)
    updater = Updater(token)
    dp = updater.dispatcher

    # Add Handlers for the Commands
    dp.add_handler(CommandHandler("newcategory", newcategory))
    dp.add_handler(CommandHandler("delcategory", delcategory))
    dp.add_handler(CommandHandler("newnote", newnote))
    dp.add_handler(CommandHandler("delnote", delnote))
    dp.add_handler(CommandHandler("notelist", notelist))
    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(CommandHandler("set", set_timer))
    dp.add_handler(CommandHandler("unset", unset_timer))

    # Start the Bot Polling
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
