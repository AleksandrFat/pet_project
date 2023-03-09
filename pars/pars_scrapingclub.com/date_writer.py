import xlsxwriter
from pars_scrapingclub import array


def writer(parametr):
    book = xlsxwriter.Workbook('data.xlsx')
    page = book.add_worksheet('Товар')
    row = 0
    column = 0

    page.set_column('A:A', 30)
    page.set_column('B:B', 20)
    page.set_column('C:C', 50)
    page.set_column('D:D', 50)
    page.set_column('E:E', 50)

    for item in parametr:
        page.write(row, column, item[0])
        page.write(row, column + 1, item[1])
        page.write(row, column + 2, item[2])
        page.write(row, column + 3, item[3])
        page.write(row, column + 4, item[4])
        row += 1
    book.close()


writer(array())
