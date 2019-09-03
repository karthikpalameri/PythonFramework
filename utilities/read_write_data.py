import csv
import logging

def getCsvData(filename):
    """
    method to get csv data
    :param filename: filename
    :return: csvdata list
    """
    return_rows = []

    with open(file=filename, mode='r') as fileData:
        # create a CSV Reader from the CSV file
        rowData = csv.reader(fileData)

        # skip the headers
        row_data_iter = iter(rowData)
        next(row_data_iter)

        # add rows from rowData to list
        for row in rowData:
            return_rows.append(row)
        return return_rows


def putCsvData(filepath, row_to_write):
    """
    Appends the data to the csv file, if the file is not present it will create as it is opened in 'a' mode
    :param filepath:
    :param row_to_write:
    :return:
    """
    with open(filepath, mode='a') as fileDataReferenceVariable:
        writer = csv.writer(fileDataReferenceVariable)
        writer.writerow(row_to_write)
