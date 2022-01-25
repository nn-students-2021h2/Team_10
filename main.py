from pdf_operations import *
from PIL import Image, ImageDraw, ImageFont

from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

TOKEN = ''

# U+1F3E0	\xF0\x9F\x8F\xA0
# house=\xF0\x9F\x8F\xA0

arrow = 'back ⬅'
house = 'home 🏠'
apply = 'apply ✅'
reset = 'reset 🔃'


# house='🔝'
# arrow='🔙'
# 🔝
# 🔙

def ob(str):
    return '^' + str + '$'


main_keyboard = [
    ['Convert'], ['Edit'],
]
convert_keyboard = [
    ['PDF to JPG'], ['JPG to PDF', 'JPG to PDF A4'], ['DOC to PDF'], [arrow]
]
edit_keyboard = [
    ['Split'], ['Merge'], ['Rename'], [arrow]
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
IN_MAIN_MENU, IN_CONVERT_MENU, IN_EDIT_MENU, IN_SPLIT_FRS, IN_SPLIT_SEC, IN_MERGE, IN_PDF2JPG, IN_JPG2PDF, IN_JPG2PDF_A4, IN_DOC2PDF, IN_RENAME_FRS, IN_RENAME_SEC = range(
    12)


def start(update: Update, context: CallbackContext) -> int:
    user_id = update.message.chat.id
    update.message.reply_text(
        "Hola! Welcome to a PDF_bot",
        reply_markup=markup_main,
    )
    return IN_MAIN_MENU


def help(update: Update, context: CallbackContext) -> int:
    """Start the conversation and ask user for input."""
    update.message.reply_text(
        "Hola! Welcome to a PDF_bot"
        "You can split, merge and convert pdf files",
        reply_markup=markup_main,
    )
    return IN_MAIN_MENU


def incorrect_input(update: Update, context: CallbackContext):
    update.message.reply_text('Incorrect input, try again', reply_markup=markup_main)


def incorrect_text_input(update: Update, context: CallbackContext):
    update.message.reply_text('Incorrect input, try again')


def done(update: Update, context: CallbackContext):
    update.message.reply_text('Ok')
    return IN_MAIN_MENU


def to_convert_menu(update: Update, context: CallbackContext):
    update.message.reply_text('Welcome to convert menu! \nWhat you want to do?', reply_markup=markup_convert)
    return IN_CONVERT_MENU
    pass


def to_edit_menu(update: Update, context: CallbackContext):
    update.message.reply_text('Welcome to edit menu! \nWhat you want to do?', reply_markup=markup_edit)
    return IN_EDIT_MENU
    pass


def to_pdf2jpg_menu(update: Update, context: CallbackContext):
    update.message.reply_text('Send PDF files, that you want convert to JPG', reply_markup=markup_back)
    return IN_PDF2JPG
    pass


def to_jpg2pdf_menu(update: Update, context: CallbackContext):
    update.message.reply_text('Send JPG files, that you want convert to PDF', reply_markup=markup_res_app)
    return IN_JPG2PDF
    pass


def to_jpg2pdfA4_menu(update: Update, context: CallbackContext):
    update.message.reply_text('Send JPG files, that you want convert to PDF with A4 format',
                              reply_markup=markup_res_app)
    return IN_JPG2PDF_A4
    pass


def to_doc2pdf_menu(update: Update, context: CallbackContext):
    update.message.reply_text('Send DOC/DOCX file, that you want convert to PDF', reply_markup=markup_back)
    return IN_DOC2PDF
    pass


def to_split_menu(update: Update, context: CallbackContext):
    update.message.reply_text('Send PDF file and a description of where to make a split', reply_markup=markup_back)
    return IN_SPLIT_FRS
    pass


def to_merge_menu(update: Update, context: CallbackContext):
    update.message.reply_text('Send PDF files to merge', reply_markup=markup_res_app)
    return IN_MERGE
    pass


def to_rename_menu(update: Update, context: CallbackContext):
    update.message.reply_text('Send PDF file to rename', reply_markup=markup_back)
    return IN_RENAME_FRS


def to_main_menu(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome home!", reply_markup=markup_main)
    return IN_MAIN_MENU
    pass


def merge_fun(update: Update, context: CallbackContext):
    print('in_merge_fun')
    print(update.message)
    print(update.message.document)
    # update.message.reply_text('Send files to merge', reply_markup=markup_back)
    # return IN_MERGE
    pass


# def to_edit_menu(update: Update, context: CallbackContext):
#   pass

# def to_edit_menu(update: Update, context: CallbackContext):
#   pass

photo_dict = {}


def jpg2pdf_fun_add1(update: Update, context: CallbackContext):  # Add to dictionary

    file = context.bot.getFile(update.message.document.file_id)
    print('jpg get', file)
    chat_id = update.message.chat_id

    list_j = photo_dict.get(chat_id)
    if list_j is None:
        list_j = []
    list_j.append(file)
    photo_dict[chat_id] = list_j
    # update.message.reply_text('', reply_markup=markup_res_app)


def jpg2pdf_fun_add2(update: Update, context: CallbackContext):
    file = context.bot.getFile(update.message.photo[-1].file_id)
    print('photo get', file)
    chat_id = update.message.chat_id

    list_j = photo_dict.get(chat_id)
    if list_j is None:
        list_j = []
    list_j.append(file)
    photo_dict[chat_id] = list_j
    # update.message.reply_text('', reply_markup=markup_res_app)


def jpg2pdf_fun_app(update: Update, context: CallbackContext):  # WorkWithFiles
    print(photo_dict)
    chat_id = update.message.chat_id

    file_list = photo_dict.get(chat_id)
    jpg_files = []

    if file_list is not None:
        count = 0
        for item in file_list:
            file_name = str(chat_id) + '_jpg2pdf_' + str(count) + '.jpg'
            count = count + 1
            item.download(file_name)
            jpg_file = Image.open(file_name)
            jpg_files.append(jpg_file)
        print(jpg_files)
        pdf_file = jpg_to_pdf(jpg_files, A4=False, chat_id=chat_id)

        # Удаляем из словаря
        photo_dict.pop(chat_id)
        # Отправляем
        update.message.reply_document(pdf_file, reply_markup=markup_res_app)


    else:
        update.message.reply_text('Ты же ничего не залил')

    pass


def jpg2pdfA4_fun_app(update: Update, context: CallbackContext):  # WorkWithFiles
    print(photo_dict)
    chat_id = update.message.chat_id

    file_list = photo_dict.get(chat_id)
    jpg_files = []

    if file_list is not None:
        count = 0
        for item in file_list:
            file_name = str(chat_id) + '_jpg2pdf_' + str(count) + '.jpg'
            count = count + 1
            item.download(file_name)
            jpg_file = Image.open(file_name)
            jpg_files.append(jpg_file)
        print(jpg_files)
        pdf_file = jpg_to_pdf(jpg_files, A4=True, chat_id=chat_id)

        # Удаляем из словаря
        photo_dict.pop(chat_id)
        # Отправляем
        update.message.reply_document(pdf_file, reply_markup=markup_res_app)


    else:
        update.message.reply_text('Ты же ничего не залил')

    pass


def jpg2pdf_fun_res(update: Update, context: CallbackContext):  # WorkWithFiles
    # print(photo_dict
    chat_id = update.message.chat_id
    photo_dict.pop(chat_id),
    update.message.reply_text('reset', reply_markup=markup_res_app)
    pass


# from docx2pdf import convert


# convertapi.api_secret = 'your-api-secret'
# convert("input.docx")
# convert("input.docx", "output.pdf")
def doc2pdf_fun(update: Update, context: CallbackContext):
    file = context.bot.getFile(update.message.document.file_id)
    print(file)
    file_name = update.message.document.file_name
    print(file_name)
    file.download(file_name)
    new_f_n = file_name.replace('.docx', '.pdf')
    new_f_n = new_f_n.replace('.doc', '.pdf')
    print(new_f_n)

    import convertapi
    convertapi.api_secret = 'vpw15ysXvqQ0cXxm'
    result = convertapi.convert('pdf', {'File': file_name})
    result.file.save(new_f_n)

    # convert("C:\PythonCode\PDF_bot/"+file_name, "C:\PythonCode\PDF_bot/"+new_f_n)
    to_sent = open(new_f_n, 'rb')
    update.message.reply_document(to_sent, reply_markup=markup_back)
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
pdf_dict = {}


def merge_fun_add(update: Update, context: CallbackContext):
    file = context.bot.getFile(update.message.document.file_id)
    print('pdf get', file)
    chat_id = update.message.chat_id

    list_j = pdf_dict.get(chat_id)
    if list_j is None:
        list_j = []
    list_j.append(file)
    pdf_dict[chat_id] = list_j
    # update.message.reply_text('', reply_markup=markup_res_app)
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
        out_name = str(chat_id) + 'to_merge_pdf_out.pdf'
        with open(out_name, "wb") as output_stream:
            pdf_files.write(output_stream)
        to_send = open(out_name, 'rb')

        # Удаляем из словаря
        pdf_dict.pop(chat_id)
        # Отправляем
        update.message.reply_document(to_send, reply_markup=markup_res_app)


def merge_fun_res(update: Update, context: CallbackContext):  # WorkWithFiles
    # print(photo_dict)
    chat_id = update.message.chat_id
    pdf_dict.pop(chat_id),
    update.message.reply_text('reset', reply_markup=markup_res_app)


f_split_pdf_dict = {}


def split_fun_frs(update: Update, context: CallbackContext):
    file = context.bot.getFile(update.message.document.file_id)
    print('pdf get', file)

    chat_id = update.message.chat_id
    f_split_pdf_dict[chat_id] = file

    update.message.reply_text('Напиши на что хочешь разделить, желательно в таком формате:\n [a b],[c d]',
                              reply_markup=markup_back)
    return IN_SPLIT_SEC


def split_fun_frs_text(update: Update, context: CallbackContext):
    update.message.reply_text('Please send PDF file to split firstly!', reply_markup=markup_back)
    return IN_SPLIT_FRS


# Добавить try except для нормальной работы
def split_fun_sec(update: Update, context: CallbackContext):
    text = update.message.text
    print(text)
    text = text.replace('[', '')
    text = text.replace(']', ',')
    text = text.strip(',').split(',')
    print(text)
    command_list = []
    # .strip('/').split('/')
    begin = 'b'
    end = 'e'
    for item in text:
        print(item)
        item = item.strip(' ').split(' ')
        print(item)
        if len(item) == 1:
            if item[0] == 'e' or item[0] == 'b' or item[0].isdigit():
                # Это доп обработай
                if item[0] != 'e' and item[0] != 'b':
                    item[0] = int(item[0])
                command1 = [begin, item[0]]
                command2 = [item[0] + 1, end]
                command_list.append(command1)
                command_list.append(command2)
            else:
                update.message.reply_text('incorrect command', reply_markup=markup_back)
        elif len(item) == 2:
            if (item[0] == 'e' or item[0] == 'b' or item[0].isdigit()) and (
                    item[1] == 'e' or item[1] == 'b' or item[1].isdigit()):
                if item[0] != 'e' and item[0] != 'b':
                    item[0] = int(item[0])

                if item[1] != 'e' and item[1] != 'b':
                    item[1] = int(item[1])

                command = [item[0], item[1]]
                command_list.append(command)
            else:
                update.message.reply_text('incorrect command', reply_markup=markup_back)
        else:
            update.message.reply_text('incorrect command', reply_markup=markup_back)
    print(command_list)

    chat_id = update.message.chat_id
    file_to_split = f_split_pdf_dict[chat_id]

    file_name = str(chat_id) + '_to_split.pdf'
    file_to_split.download(file_name)

    pdf_files = split_pdf(file_name, command_list)
    for pdf_file in pdf_files:
        update.message.reply_document(pdf_file, reply_markup=markup_back)
    return IN_SPLIT_SEC


f_rrename_pdf_dict = {}


def rename_fun_frs(update: Update, context: CallbackContext):
    file = context.bot.getFile(update.message.document.file_id)
    print('pdf get', file)

    chat_id = update.message.chat_id
    f_split_pdf_dict[chat_id] = file

    update.message.reply_text('Write new name', reply_markup=markup_back)
    return IN_RENAME_SEC


def rename_fun_frs_text(update: Update, context: CallbackContext):
    update.message.reply_text('Please send PDF file to rename firstly!', reply_markup=markup_back)
    return IN_RENAME_FRS


def rename_fun_sec(update: Update, context: CallbackContext):
    text = update.message.text
    # По другому
    text.replace('.pdf', '')
    text = text + '.pdf'
    chat_id = update.message.chat_id
    file_to_split = f_split_pdf_dict[chat_id]

    file_name = str(chat_id) + '_to_split.pdf'
    file_to_split.download(text)
    pdf_file = open(text, 'rb')
    update.message.reply_document(pdf_file, reply_markup=markup_back)
    return IN_RENAME_SEC


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
            # LEVEL I
            IN_MAIN_MENU: [
                MessageHandler(Filters.regex('^Convert$'), to_convert_menu),
                MessageHandler(Filters.regex('^Edit$'), to_edit_menu),

                MessageHandler(Filters.text, to_main_menu),
                # Поставь фильтр на текст
            ],

            # LEVEL II
            IN_CONVERT_MENU: [
                MessageHandler(Filters.regex('^PDF to JPG$'), to_pdf2jpg_menu),
                MessageHandler(Filters.regex('^JPG to PDF$'), to_jpg2pdf_menu),
                MessageHandler(Filters.regex('^JPG to PDF A4$'), to_jpg2pdfA4_menu),
                MessageHandler(Filters.regex('^DOC to PDF$'), to_doc2pdf_menu),
                MessageHandler(Filters.regex(ob(arrow)), to_main_menu),

                MessageHandler(Filters.text, to_convert_menu),

            ],
            IN_EDIT_MENU: [
                MessageHandler(Filters.regex('^Split$'), to_split_menu),
                MessageHandler(Filters.regex('^Merge$'), to_merge_menu),
                MessageHandler(Filters.regex('^Rename$'), to_rename_menu),
                MessageHandler(Filters.regex(ob(arrow)), to_main_menu),

                MessageHandler(Filters.text, to_edit_menu),
            ],
            IN_MERGE: [

                MessageHandler(Filters.document.pdf, merge_fun_add),
                MessageHandler(Filters.regex(ob(apply)), merge_fun_app),
                MessageHandler(Filters.regex(ob(arrow)), to_edit_menu),
                MessageHandler(Filters.regex(ob(house)), to_main_menu),

                MessageHandler(Filters.text, to_merge_menu),
            ],
            IN_SPLIT_FRS: [
                MessageHandler(Filters.document.pdf, split_fun_frs),
                MessageHandler(Filters.regex(ob(arrow)), to_edit_menu),
                MessageHandler(Filters.regex(ob(house)), to_main_menu),
                MessageHandler(Filters.text, split_fun_frs_text),
            ],
            IN_SPLIT_SEC: [
                MessageHandler(Filters.document.pdf, split_fun_frs),
                MessageHandler(Filters.regex(ob(arrow)), to_edit_menu),
                MessageHandler(Filters.regex(ob(house)), to_main_menu),
                MessageHandler(Filters.text, split_fun_sec),
            ],
            IN_RENAME_FRS: [
                MessageHandler(Filters.document.pdf, rename_fun_frs),
                MessageHandler(Filters.regex(ob(arrow)), to_edit_menu),
                MessageHandler(Filters.regex(ob(house)), to_main_menu),
                MessageHandler(Filters.text, rename_fun_frs_text),
            ],
            IN_RENAME_SEC: [
                MessageHandler(Filters.document.pdf, rename_fun_frs),
                MessageHandler(Filters.regex(ob(arrow)), to_edit_menu),
                MessageHandler(Filters.regex(ob(house)), to_main_menu),
                MessageHandler(Filters.text, rename_fun_sec),
            ],

            IN_JPG2PDF: [
                MessageHandler(Filters.document.jpg, jpg2pdf_fun_add1),
                MessageHandler(Filters.photo, jpg2pdf_fun_add2),
                MessageHandler(Filters.regex(ob(apply)), jpg2pdf_fun_app),
                MessageHandler(Filters.regex(ob(arrow)), to_convert_menu),
                MessageHandler(Filters.regex(ob(house)), to_main_menu),
                MessageHandler(Filters.regex(ob(reset)), jpg2pdf_fun_res),

                MessageHandler(Filters.text, to_jpg2pdf_menu),
            ],

            IN_JPG2PDF_A4: [
                MessageHandler(Filters.document.jpg, jpg2pdf_fun_add1),
                MessageHandler(Filters.photo, jpg2pdf_fun_add2),
                MessageHandler(Filters.regex(ob(apply)), jpg2pdfA4_fun_app),
                MessageHandler(Filters.regex(ob(arrow)), to_convert_menu),
                MessageHandler(Filters.regex(ob(house)), to_main_menu),
                MessageHandler(Filters.regex(ob(reset)), jpg2pdf_fun_res),

                MessageHandler(Filters.text, to_jpg2pdfA4_menu),
            ],

            IN_PDF2JPG: [
                MessageHandler(Filters.document.pdf, pdf2jpg_fun),
                MessageHandler(Filters.regex(ob(arrow)), to_convert_menu),
                MessageHandler(Filters.regex(ob(house)), to_main_menu),

                MessageHandler(Filters.text, to_pdf2jpg_menu),
            ],

            IN_DOC2PDF: [
                MessageHandler(Filters.document.doc, doc2pdf_fun),
                MessageHandler(Filters.document.docx, doc2pdf_fun),
                MessageHandler(Filters.regex(ob(arrow)), to_convert_menu),
                MessageHandler(Filters.regex(ob(house)), to_main_menu),

                MessageHandler(Filters.text, to_doc2pdf_menu),
            ]
        },
        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
