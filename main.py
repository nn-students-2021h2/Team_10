import logging
from typing import Dict

from pdf_operations import *
from PIL import Image, ImageDraw, ImageFont

TOKEN = ''
import random

from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

message_list = []
user_score_dict = {}

# U+1F3E0	\xF0\x9F\x8F\xA0
#house=\xF0\x9F\x8F\xA0

arrow = '⬅'
house = '🏠'
apply = '✅'
reset ='🔃'

#house='🔝'
#arrow='🔙'
#🔝
#🔙

def ob(str):
    return '^'+str+'$'


main_keyboard = [
    ['Convert'], ['Edit'],
]
convert_keyboard = [
    ['PDF to JPG'], ['JPG to PDF'], [arrow]
]
edit_keyboard = [
    ['Split'], ['Merge'], [arrow]
]

reset_apply_keyboard = [
    [arrow], [house], [reset], [apply]
]


back_keyboard = [[arrow], [house]]


markup_main = ReplyKeyboardMarkup(main_keyboard, one_time_keyboard=True)
markup_convert = ReplyKeyboardMarkup(convert_keyboard, one_time_keyboard=True)
markup_edit = ReplyKeyboardMarkup(edit_keyboard, one_time_keyboard=True)
markup_back = ReplyKeyboardMarkup(back_keyboard, one_time_keyboard=True)
markup_res_app = ReplyKeyboardMarkup(reset_apply_keyboard, one_time_keyboard=True)
IN_MAIN_MENU, IN_CONVERT_MENU, IN_EDIT_MENU, IN_SPLIT_FRS, IN_SPLIT_SEC, IN_MERGE, IN_PDF2JPG, IN_JPG2PDF = range(8)


#CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)



def made_photo(caption):
    import textwrap

    #caption = "Obama warns far-left candidates says average American does not want to tear down the system"

    wrapper = textwrap.TextWrapper(width=30)
    word_list = wrapper.wrap(text=caption)
    caption_new = ''
    for ii in word_list[:-1]:
        caption_new = caption_new + ii + '\n'
    caption_new += word_list[-1]

    image = Image.open(r"C:\PythonCode\NastyaBot/template.png")
    draw = ImageDraw.Draw(image)

    # Download the Font and Replace the font with the font file.
    font = ImageFont.truetype(r"C:\PythonCode\NastyaBot\ofont.ru_Kobzar KS.ttf", size=40)
    w, h = draw.textsize(caption_new, font=font)
    print(w,h)
    W, H = image.size
    print(W, H)
    x, y = 0.07 * (W), 0.15 * (H)

    draw.multiline_text((x, y), caption_new,(0,0,0), font=font)
    #image.show()
    image.save('output.png')
    photo = open(r"C:\PythonCode\NastyaBot/output.png", 'rb')
    return  photo
    #update.message.reply_photo(photo)





def start(update: Update, context: CallbackContext) -> int:
    """Start the conversation and ask user for input."""
    user_id=update.message.chat.id
    user_score_dict[user_id] = 0
    update.message.reply_text(
        "Hola! Welcome to a PDF_bot",
        reply_markup=markup_main,
    )
    return IN_MAIN_MENU

#REWRITE
def help(update: Update, context: CallbackContext) -> int:
    """Start the conversation and ask user for input."""
    update.message.reply_text(
        "Hola! Welcome to random message bot"
        "You can get a random message or send your message to random person",
        reply_markup=markup_main,
    )
    return IN_MAIN_MENU

def incorrect_input(update: Update, context: CallbackContext):
    update.message.reply_text('Incorrect input, try again', reply_markup = markup_main)


def incorrect_text_input(update: Update, context: CallbackContext):
    update.message.reply_text('Incorrect input, try again')

def done(update: Update, context: CallbackContext):
    update.message.reply_text('Ok')
    return IN_MAIN_MENU


def to_convert_menu(update: Update, context: CallbackContext):
    update.message.reply_text('Welcome to convert menu! \n What you want to do?', reply_markup=markup_convert)
    return IN_CONVERT_MENU
    pass

def to_edit_menu(update: Update, context: CallbackContext):
    update.message.reply_text('Welcome to edit menu! \n What you want to do?', reply_markup=markup_edit)
    return IN_EDIT_MENU
    pass


def to_pdf2jpg_menu(update: Update, context: CallbackContext):
    update.message.reply_text('Send files, that you want to convert', reply_markup=markup_back)
    return IN_PDF2JPG
    pass

def to_jpg2pdf_menu(update: Update, context: CallbackContext):
    update.message.reply_text('Send files, that you want to convert', reply_markup=markup_res_app)
    return IN_JPG2PDF
    pass

def to_split_menu(update: Update, context: CallbackContext):
    update.message.reply_text('Send files and a description of where to make a split', reply_markup=markup_back)
    return IN_SPLIT_FRS
    pass

def to_merge_menu(update: Update, context: CallbackContext):
    update.message.reply_text('Send files to merge', reply_markup=markup_res_app)
    return IN_MERGE
    pass

def to_main_menu(update: Update, context: CallbackContext):
    update.message.reply_text("I'm back!", reply_markup=markup_main)
    return IN_MAIN_MENU
    pass

def merge_fun(update: Update, context: CallbackContext):
    print('in_merge_fun')
    print(update.message)
    print(update.message.document)
    #update.message.reply_text('Send files to merge', reply_markup=markup_back)
    #return IN_MERGE
    pass


#def to_edit_menu(update: Update, context: CallbackContext):
 #   pass

#def to_edit_menu(update: Update, context: CallbackContext):
 #   pass

photo_dict={}
def jpg2pdf_fun_add1(update: Update, context: CallbackContext):#Add to dictionary

    file = context.bot.getFile(update.message.document.file_id)
    print('jpg get', file)
    chat_id=update.message.chat_id

    list_j = photo_dict.get(chat_id)
    if list_j is None:
        list_j=[]
    list_j.append(file)
    photo_dict[chat_id]=list_j
    #update.message.reply_text('', reply_markup=markup_res_app)


def jpg2pdf_fun_add2(update: Update, context: CallbackContext):
    file = context.bot.getFile(update.message.photo[-1].file_id)
    print('photo get', file)
    chat_id=update.message.chat_id

    list_j = photo_dict.get(chat_id)
    if list_j is None:
        list_j=[]
    list_j.append(file)
    photo_dict[chat_id]=list_j
    #update.message.reply_text('', reply_markup=markup_res_app)



def jpg2pdf_fun_app(update: Update, context: CallbackContext):#WorkWithFiles
    print(photo_dict)
    chat_id=update.message.chat_id

    file_list=photo_dict.get(chat_id)
    jpg_files=[]

    if file_list is not None:
        count=0
        for item in file_list:
            file_name=str(chat_id)+'_jpg2pdf_'+str(count)+'.jpg'
            count=count+1
            item.download(file_name)
            jpg_file = Image.open(file_name)
            jpg_files.append(jpg_file)
        print(jpg_files)
        pdf_file=jpg_to_pdf(jpg_files,A4=True,chat_id=chat_id)

        #Удаляем из словаря
        photo_dict.pop(chat_id)
        #Отправляем
        update.message.reply_document(pdf_file,reply_markup=markup_res_app)


    else:
        update.message.reply_text('Ты же ничего не залил')

    pass

def jpg2pdf_fun_res(update: Update, context: CallbackContext):#WorkWithFiles
    #print(photo_dict
    chat_id = update.message.chat_id
    photo_dict.pop(chat_id),
    update.message.reply_text('reset', reply_markup=markup_res_app)
    pass



def pdf2jpg_fun(update: Update, context: CallbackContext):
    file = context.bot.getFile(update.message.document.file_id)
    print(file)
    file.download('gettted.pdf')
    jgp_files = pdf_to_jpg('gettted.pdf', '')
    for photo in jgp_files:
        update.message.reply_document(photo, reply_markup=markup_back)

#####
#####MERGE
#####
pdf_dict={}
def merge_fun_add(update: Update, context: CallbackContext):
    file = context.bot.getFile(update.message.document.file_id)
    print('pdf get', file)
    chat_id=update.message.chat_id

    list_j = pdf_dict.get(chat_id)
    if list_j is None:
        list_j = []
    list_j.append(file)
    pdf_dict[chat_id] = list_j
    #update.message.reply_text('', reply_markup=markup_res_app)
    pass

def merge_fun_app(update: Update, context: CallbackContext):
    from PyPDF2 import PdfFileReader, PdfFileMerger
    print(pdf_dict)
    chat_id = update.message.chat_id

    file_list = pdf_dict.get(chat_id)

    pdf_files = PdfFileMerger()

    if file_list is not None:
        count = 0
        for item in file_list:
            file_name = str(chat_id) + 'to_merge_pdf_' + str(count) + '.pdf'
            count = count + 1
            item.download(file_name)
            pdf_file = PdfFileReader(file_name)
            print(file_name)
            pdf_files.append(pdf_file, import_bookmarks=False)
        print(pdf_files)
        out_name=str(chat_id) + 'to_merge_pdf_out.pdf'
        with open(out_name, "wb") as output_stream:
            pdf_files.write(output_stream)
        to_send=open(out_name,'rb')

        # Удаляем из словаря
        pdf_dict.pop(chat_id)
        # Отправляем
        update.message.reply_document(to_send, reply_markup=markup_res_app)

def merge_fun_res(update: Update, context: CallbackContext):#WorkWithFiles
    #print(photo_dict)
    chat_id = update.message.chat_id
    pdf_dict.pop(chat_id),
    update.message.reply_text('reset', reply_markup=markup_res_app)
#####
#####
#####

f_split_pdf_dict={}
def split_fun_frs(update: Update, context: CallbackContext):
    file = context.bot.getFile(update.message.document.file_id)
    print('pdf get', file)

    chat_id = update.message.chat_id
    f_split_pdf_dict[chat_id]=file

    update.message.reply_text('Напиши на что хочешь разделить, желательно в таком формате:\n [a b],[c d]', reply_markup= markup_back)
    return IN_SPLIT_SEC

def split_fun_sec(update: Update, context: CallbackContext):
    text=update.message.text
    print(text)
    text=text.strip(',').split(',')
    print(text)
    command_list=[]
    #.strip('/').split('/')
    begin='b'
    end='e'
    for item in text:
        print(item)
        item=item.strip(' ').split(' ')
        print(item)
        if len(item)==1:

            #Это доп обработай
            if item[0]!='e' and item[0]!='b':
                item[0]=int(item[0])
            command1=[begin, item[0]]
            command2=[item[0]+1,end]
            command_list.append(command1)
            command_list.append(command2)
        elif len(item)==2:
            if item[0]!='e' and item[0]!='b':
                item[0]=int(item[0])
            if item[1]!='e' and item[1]!='b':
                item[1]=int(item[1])


            command=[item[0], item[1]]
            command_list.append(command)
        else:
            update.message.reply_text('incorrect command', reply_markup=markup_back)
    print(command_list)

    chat_id = update.message.chat_id
    file_to_split=f_split_pdf_dict[chat_id]

    file_name=str(chat_id)+'_to_split.pdf'
    file_to_split.download(file_name)

    pdf_files=split_pdf(file_name, command_list)
    for pdf_file in pdf_files:
        update.message.reply_document(pdf_file, reply_markup=markup_back)




def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            #LEVEL I
            IN_MAIN_MENU: [
                MessageHandler(Filters.regex('^Convert$'), to_convert_menu),
                MessageHandler(Filters.regex('^Edit$'), to_edit_menu),
                #Поставь фильтр на текст
            ],

            #LEVEL II
            IN_CONVERT_MENU: [
                MessageHandler(Filters.regex('^PDF to JPG$'), to_pdf2jpg_menu),
                MessageHandler(Filters.regex('^JPG to PDF$'), to_jpg2pdf_menu),
                MessageHandler(Filters.regex(ob(arrow)), to_main_menu),
            ],
            IN_EDIT_MENU: [
                MessageHandler(Filters.regex('^Split$'), to_split_menu),
                MessageHandler(Filters.regex('^Merge$'), to_merge_menu),
                MessageHandler(Filters.regex(ob(arrow)), to_main_menu),
            ],
            IN_MERGE: [

                MessageHandler(Filters.document.pdf, merge_fun_add),
                MessageHandler(Filters.regex(ob(apply)), merge_fun_app),
                MessageHandler(Filters.regex(ob(arrow)), to_edit_menu),
                MessageHandler(Filters.regex(ob(house)), to_main_menu),
            ],
            IN_SPLIT_FRS: [
                MessageHandler(Filters.document.pdf, split_fun_frs),
                MessageHandler(Filters.regex(ob(arrow)), to_edit_menu),
                MessageHandler(Filters.regex(ob(house)), to_main_menu),
            ],
            IN_SPLIT_SEC:[
                MessageHandler(Filters.text, split_fun_sec),
                MessageHandler(Filters.regex(ob(arrow)), to_edit_menu),
                MessageHandler(Filters.regex(ob(house)), to_main_menu),
            ],


            IN_JPG2PDF: [
                MessageHandler(Filters.document.jpg, jpg2pdf_fun_add1),
                MessageHandler(Filters.photo, jpg2pdf_fun_add2),
                MessageHandler(Filters.regex(ob(apply)), jpg2pdf_fun_app),
                MessageHandler(Filters.regex(ob(arrow)), to_convert_menu),
                MessageHandler(Filters.regex(ob(house)), to_main_menu),
                MessageHandler(Filters.regex(ob(reset)), jpg2pdf_fun_res),
            ],
            IN_PDF2JPG: [
                MessageHandler(Filters.document.pdf, pdf2jpg_fun),
                MessageHandler(Filters.regex(ob(arrow)), to_convert_menu),
                MessageHandler(Filters.regex(ob(house)), to_main_menu),

            ],




            #LEVEL III








        },
        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()









