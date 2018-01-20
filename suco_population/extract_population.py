# coding: utf-8

from xlrd import open_workbook
import csv

def extract_municipality(sheet, municipality_name):
    row = 11 if municipality_name == 'Viqueque' else 10

    while True:
        subdistrict_cell = sheet.cell(row, 0)
        subdistrict = subdistrict_cell.value
        subdistrict_sum = int(sheet.cell(row, 1).value)
        suco_sum = 0

        # record next subdistrict
        while suco_sum < subdistrict_sum:
            row += 4
            suco_name = sheet.cell(row, 0).value
            suco_value = sheet.cell(row, 1).value
            suco_sum += suco_value
            writer.writerow([municipality_name, subdistrict, suco_name, suco_value,
                             sheet.cell(row + 1, 1).value, sheet.cell(row + 2, 1).value, sheet.cell(row, 18).value])

        row += 4
        try:
            subdistrict_cell = sheet.cell(row, 0)
        except IndexError:
            break
        subdistrict = subdistrict_cell.value
        subdistrict_sum = sheet.cell(row, 1).value
        if not subdistrict_sum:
            break

with open('suco_population.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['district', 'subdistrict', 'suco', 'population', 'male', 'female', 'households'])

    wb = open_workbook('/Users/raphaelmerx/Downloads/2015 Census Timor/1_2015 V4 Households & Population by 5 year age group.xls')

    for sheet in wb.sheets()[2:]:
        municipality_name = sheet.cell(0, 0).value.split(' ')[-1]
        extract_municipality(sheet, municipality_name)
