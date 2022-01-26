from PIL import Image


def jpg_to_pdf(im_list, A4=False, chat_id=0):
    a4im_list = []
    if A4 is True:
        for im in im_list:
            a4_w = 2480
            a4_h = 3508
            a4_coef = a4_h / a4_w
            a4im = Image.new('RGB',
                             (a4_w, a4_h),  # A4 at 72dpi
                             (255, 255, 255))  # White

            width_src, height_src = im.size
            im_coef = height_src / width_src
            print('input_size', im.size)

            # if(width_src>height_src):
            if im_coef < a4_coef:
                basewidth = 2480
                wpercent = (basewidth / float(width_src))
                hsize = int((float(height_src) * float(wpercent)))
                im = im.resize((basewidth, hsize), Image.ANTIALIAS)
                new_w, new_h = im.size
                print('bas_width', im.size)
            else:
                baseheight = 3508
                hpercent = (baseheight / float(height_src))
                wsize = int((float(width_src) * float(hpercent)))
                im = im.resize((wsize, baseheight), Image.ANTIALIAS)
                new_w, new_h = im.size
                print('bas_height', im.size)

            a4im.paste(im, (int(0.5 * (a4_w - new_w)), int(0.5 * (a4_h - new_h))))  # Not centered, top-left corner
            # a4im.paste(im, im.getbbox())  # Not centered, top-left corner
            a4im_list.append(a4im)
            # im = a4im
        im_list = a4im_list

    if im_list is not None:  # Если не пуст
        print(len(im_list))
        frst = im_list.pop(0)
        print(len(im_list))

        name_part = ''
        if A4 is True:
            name_part = 'A4'

        file_name = str(chat_id) + '/' + "jpg2pdf" + name_part + "_res.pdf"
        frst.save(file_name, "PDF", resolution=100.0, save_all=True, append_images=im_list)
        out = open(file_name, 'rb')
        return out
    else:
        print("error")


def jpg_to_pdf_old(path_to_folder, A4=False):
    import glob
    import os
    jpg_files_pathes = glob.glob(path_to_folder + "/*.jpg")
    print(jpg_files_pathes)
    jpeg_files_pathes = glob.glob(path_to_folder + "/*.jpeg")

    files_pathes = jpg_files_pathes + jpeg_files_pathes
    print('merged', files_pathes)
    files_pathes.sort(key=os.path.getmtime)
    print('sorted', files_pathes)

    im_list = []
    for path in files_pathes:
        im = Image.open(path)
        im_list.append(im)

    a4im_list = []
    if A4 is True:
        for im in im_list:
            a4_w = 2480
            a4_h = 3508
            a4im = Image.new('RGB',
                             (a4_w, a4_h),  # A4 at 72dpi
                             (255, 255, 255))  # White

            width_src, height_src = im.size
            new_w = 0
            new_h = 0
            print('input_size', im.size)
            # if(width_src>height_src):
            if True:
                basewidth = 2480
                wpercent = (basewidth / float(width_src))
                hsize = int((float(height_src) * float(wpercent)))
                im = im.resize((basewidth, hsize), Image.ANTIALIAS)
                new_w, new_h = im.size
                print('bas_width', im.size)
            else:
                baseheight = 3508
                hpercent = (baseheight / float(height_src))
                wsize = int((float(width_src) * float(hpercent)))
                im = im.resize((wsize, baseheight), Image.ANTIALIAS)
                print('bas_height', im.size)

            a4im.paste(im, (int(0.5 * (a4_w - new_w)), int(0.5 * (a4_h - new_h))))  # Not centered, top-left corner
            # a4im.paste(im, im.getbbox())  # Not centered, top-left corner
            a4im_list.append(a4im)
            # im = a4im
        im_list = a4im_list

    if im_list is not None:  # Если не пуст
        print(len(im_list))
        frst = im_list.pop(0)
        print(len(im_list))
        frst.save(path_to_folder + "/out4.pdf", "PDF", resolution=100.0, save_all=True, append_images=im_list)
        out = open(path_to_folder + "/out4.pdf", 'rb')
        return out
    else:
        print("error")


def pdf_to_jpg(path_to_file, path_to_save, name_file):
    from pdf2image import convert_from_path
    pages = convert_from_path(path_to_file, 100, poppler_path=r'C:\PythonCode\poppler-0.68.0\bin')
    i = 0

    jpg_files = []
    for page in pages:
        all_name = path_to_save + "/pdf2jpg_" + str(i) + "_" + name_file + '.jpg'
        page.save(all_name, 'JPEG')
        i = i + 1
        file = open(all_name, 'rb')
        jpg_files.append(file)

    return jpg_files


from PyPDF2 import PdfFileWriter, PdfFileReader


def split_pdf_to_two(filename, page_number):
    pdf_reader = PdfFileReader(open(filename, "rb"))
    try:
        assert page_number < pdf_reader.numPages
        pdf_writer1 = PdfFileWriter()
        pdf_writer2 = PdfFileWriter()

        for page in range(page_number):
            pdf_writer1.addPage(pdf_reader.getPage(page))

        for page in range(page_number, pdf_reader.getNumPages()):
            pdf_writer2.addPage(pdf_reader.getPage(page))

        with open("part1.pdf", 'wb') as file1:
            pdf_writer1.write(file1)

        with open("part2.pdf", 'wb') as file2:
            pdf_writer2.write(file2)

    except AssertionError as e:
        print("Error: The PDF you are cutting has less pages than you want to cut!")


def split_pdf(path_to_file, split_borders, folder_name):
    # split_border
    # [b,5], [6,e]
    # [3,7], [6,8], [7,e]
    input_pdf = PdfFileReader(path_to_file)
    split_count = 0
    max_pages = input_pdf.numPages

    split_pdfs = []

    for split_item in split_borders:
        split_item[:] = [1 if x == 'b' else x for x in split_item]
        split_item[:] = [max_pages if x == 'e' else x for x in split_item]
        split_item[:] = [max_pages if x > max_pages else x for x in split_item]
        b = split_item[0] - 1
        e = split_item[1] - 1
        if b >= 0 and b < max_pages and e >= 0 and e < max_pages:
            pdf_writer = PdfFileWriter()

            dt = 1
            if e < b:
                dt = -1

            for page in range(b, e + dt, dt):
                print(page)
                pdf_writer.addPage(input_pdf.getPage(page))

            save_name = folder_name + "/split_" + str(split_count) + '_[' + str(b) + '_' + str(e) + ']' + '.pdf'
            # save_name = path_to_file.replace('.pdf', '_split' + str(split_count) + '.pdf')
            split_count = split_count + 1
            with open(save_name, 'wb') as file:
                pdf_writer.write(file)
            # открой и добавь в список
            to_list = open(save_name, 'rb')
            split_pdfs.append(to_list)

    return split_pdfs


def merge_pdf(path_to_folder):
    from PyPDF2 import PdfFileReader, PdfFileMerger
    import glob
    import os

    pdf_files_pathes = glob.glob(path_to_folder + "/*.pdf")
    print(pdf_files_pathes)

    files_pathes = pdf_files_pathes
    print('merged', files_pathes)
    files_pathes.sort(key=os.path.getmtime)
    print('sorted', files_pathes)

    pdf_list = PdfFileMerger()
    for path in files_pathes:
        pdf_file = PdfFileReader(path)
        pdf_list.append(pdf_file)

    with open("output.pdf", "wb") as output_stream:
        pdf_list.write(output_stream)


def docx_to_pdf(path_to_file):
    from docx2pdf import convert

    convert(path_to_file, path_to_file.replace('docx', 'pdf'))


def main():
    pass


if __name__ == '__main__':
    main()
