import os
import importlib
from config import BASE_DIR
import tabula
from csv import writer


def main():
    for root, dirs, files in os.walk(os.path.join(BASE_DIR, "pdf")):
        lenth = len(files)
        print('[ INFO ] :: [ %s FILES DETECTED ]'% lenth)
        for file in files:
            if file.endswith(".pdf"):
                res = build_CSV(file, root)
                if res:
                    print("[ SUCCESS ] :: [ CREATED '%s' FILE. ]" % file)
                else:
                    print("[ WARNING ] :: [ ALREADY '%s' FILE CREATED IN CSV DIRECTORY. ]" % file)
            else:
                print('[ WARNING ] :: [ NOT PDF FORMATE ]')
    return '####################   Successfully Complete   ####################'


def build_CSV(PDF_NAME, root):
    path = root + '/' + PDF_NAME
    df = tabula.read_pdf(path, pages='all', output_format='json')
    CSV_NAME = 'csv/' + (PDF_NAME[:-4]) + '.csv'

    if exist_CSV(CSV_NAME):
        return False

    for page in range(0, len(df)):
        date = []
        transaction_details = []
        withdrawal = []
        deposit = []
        balance = []
        data = df[page].get('data')
        for index, content in enumerate(data):
            _date = content[0].get('text')
            if _date == 'Date':
                continue
            _transaction_details = content[1].get('text')
            if page == 0 and PDF_NAME == '20190630.pdf':
                if content[2].get('text'):
                    _transaction_details += " " + content[2].get('text')
                _withdrawal = (content[4].get('text')).replace(',', '')
                _deposit = (content[5].get('text')).replace(',', '')
                _balance = ((content[6].get('text')).replace(',', '')).replace('-', '')
            else:
                _withdrawal = (content[2].get('text')).replace(',', '')
                _deposit = (content[3].get('text')).replace(',', '')
                _balance = ((content[4].get('text')).replace(',', '')).replace('-', '')

            if _date:
                date.append(_date)
                withdrawal.append(_withdrawal)
                deposit.append(_deposit)
                balance.append(_balance)
                transaction_details.append(_transaction_details)
            elif len(transaction_details) > 0:
                details = transaction_details[-1]
                details += " " + _transaction_details
                transaction_details[-1] = details

        res = scraper_csv_write(date, transaction_details, withdrawal, deposit, balance, PDF_NAME, CSV_NAME)
        if res:
            file = page + 1
            print("[ SUCCESS ] :: [ PAGE %s's DATA INSERTED ON CSV FORMATE. ]" % file)
    return True


def exist_CSV(CSV_NAME):
    return os.path.exists(CSV_NAME)


def scraper_csv_write(date, transaction_details, withdrawal, deposit, balance, PDF_NAME, CSV_NAME):
    if not os.path.exists(CSV_NAME):
        header = ['Date', 'Transaction Details', 'Withdrawal', 'Deposit', 'Balance']
        with open(CSV_NAME, 'w+', newline='') as header_obj:
            header_writer = writer(header_obj)
            header_writer.writerow(header)
    else:
        for index, i in enumerate(date):
            msg = [date[index],
                   transaction_details[index],
                   withdrawal[index],
                   deposit[index],
                   balance[index]]
            with open(CSV_NAME, 'a+', newline='') as write_obj:
                csv_writer = writer(write_obj)
                csv_writer.writerow(msg)
    return True


if __name__ == "__main__":
    main()
