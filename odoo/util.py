
import csv
import pandas as pd
from xlsxwriter import utility as xlsutil

def generate_csv_file(file_name, records, header = ""):

    with open(file_name, 'w') as csv_file:

        writer = csv.writer(csv_file, quoting = csv.QUOTE_ALL)

        if header:
          writer.writerow(header.split(","))

        writer.writerows(records)

        rec_count = len(records)
        print("\n{:0,} rows written to {}\n".format(rec_count, file_name))


def generate_xlsx_file(file_name, df, column_list, sheet_name = "SUMMARY"):

    # put df into Excel  sheet
    xls_writer = pd.ExcelWriter(file_name)
    df.to_excel(xls_writer, sheet_name, index = True)
    worksheet = xls_writer.sheets[sheet_name]
    workbook = xls_writer.book

    # format header - must use conditional format here since we don't want to format the entire column (which worksheet.set_column does)
    # so we pass some trivial conditional test that is always true for the header (no_blanks)

    header_rng = "{}:{}".format(xlsutil.xl_rowcol_to_cell(0, 0), xlsutil.xl_rowcol_to_cell(0, len(column_list)))
    header_fmt_dict = {
        'bold': True
        , 'font_color': '#FFFFFF'  ## white
        , 'bg_color': '#376283'  ## dark blue
    }
    header_format_wb = workbook.add_format(header_fmt_dict)
    worksheet.conditional_format(header_rng, {'type': 'no_blanks', 'format': header_format_wb})

    # format columns
    for i in range(len(column_list)):

        #print("processing column '{}' ...".format(column_list[i][0]))

        col_width = column_list[i][1]
        col_num_fmt =  column_list[i][2]
        col_align =  column_list[i][3]
        xls_cell = xlsutil.xl_rowcol_to_cell(0, i)  # returns header Excel position e.g. A1
        xls_col = '{col}:{col}'.format(col = xls_cell[:-1])  # convert to column notation e.g. A:A

        # format columns
        col_align = 'left' if col_align is None else col_align
        col_fmt_dict = {
            'font_name': 'Roboto'
            , 'font_size': 9
            , 'align': col_align
        }

        # add numeric fmt to dict if passed
        if col_num_fmt is not None:
            col_fmt_dict['num_format'] = col_num_fmt
        xls_col_format = workbook.add_format(col_fmt_dict)

        # set format in wb
        worksheet.set_column(xls_col, col_width, xls_col_format)

    xls_writer.save()

    print("\ndata saved in xlsx : {}\n".format(file_name))
