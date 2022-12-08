import qrcode
import pandas as pd
import sqlite3
import os
import json
import string
import random

# data = pd.read_excel('DS_KHACH_MOI.xlsx')
# df = pd.DataFrame(data)

# for i in range(len(df)):
#     url = 'http://127.0.0.1:88/?name='+str(df.iloc[i]['name'])+'&call='+str(df.iloc[i]['call'])+'&time='+str(df.iloc[i]['time'])
#     qr = qrcode.QRCode(
#         version=1,
#         box_size=10,
#         border=5)
#     qr.add_data(url)
#     qr.make(fit=True)
#     img = qr.make_image(fill='black', back_color='white')
#     img.save('qrcode{}.png'.format(i))

class CreateDatabase:
    def __init__(self) -> None:
        # Connect to SQLite database
        self.database = 'database.db'
        self.connection_db = sqlite3.connect(self.database, check_same_thread=False)
        self.cursor = self.connection_db.cursor()
        # URL path
        self.url = 'http://10.91.13.88:88/?id='
        # Path to QR folder
        self.qr_folder = os.path.join('statics', 'images', 'qr')
        if not os.path.exists(self.qr_folder):
            os.makedirs(self.qr_folder)

    def create_random_id(self):
        '''
        CREATE RANDOM ID
        ------------
        Tạo ID ngẫu nhiên cho URL
        '''
        number_of_string = 10
        ID = ''.join(random.choices(string.ascii_uppercase + string.digits, k = number_of_string))  
        result = self.cursor.execute('SELECT COUNT(ID) FROM data WHERE ID = ?', (ID,))
        if(int(result.fetchone()[0])==0):
            return ID
        else:
            return self.create_random_id()


    def create_qr_code(self, file_name):
        '''
        CREATE QR CODE
        ------
        Tạo mã QR và URL, save vào Database
        '''
        f = pd.read_excel(file_name)
        df = pd.DataFrame(f)

        for i in range(len(df)):
            ID = self.create_random_id()
            try:
                self.cursor.execute('INSERT INTO data (NAME, CALL, TIME, DATE, ID) VALUES (?, ?, ?, ?, ?)', (str(df.iloc[i]['name']), str(df.iloc[i]['call']), str(df.iloc[i]['time']), str(df.iloc[i]['date']), ID))
                self.connection_db.commit()
                # Tạo mã QR
                qr = qrcode.QRCode(
                    version=1,
                    box_size=10,
                    border=5)
                qr.add_data(self.url + str(ID))
                qr.make(fit=True)
                img = qr.make_image(fill='black', back_color='white')
                img.save('{}\qrcode_{}_{}.png'.format(self.qr_folder, str(df.iloc[i]['name']), str(ID)))
            except Exception:
                print("Error when trying to insert into database")

if __name__=="__main__":
    create = CreateDatabase()
    create.create_qr_code('DS_KHACH_MOI.xlsx')