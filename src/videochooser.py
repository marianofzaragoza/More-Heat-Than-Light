from config import DynamicConfigIni
import logging
import mhlog 
import numpy as np
import pathlib
import config
import gspread
import pandas as pd

class Videochooser():
    def __init__(self, enable_appqueue=False):
        logging.setLoggerClass(mhlog.Logger)
        self.log = mhlog.getLog("newplaylist", self)
        self.log.setLevel(logging.WARN)
        srcdir = pathlib.Path(__file__).parent.resolve()
 
        self.tempsfile = str(srcdir) + '/temperaturas.dataframe'
        self.videofile = str(srcdir) + '/finaledits.dataframe'

        self.config = DynamicConfigIni()
        self.nodename = self.config.DEFAULT.nodename  # Access the nodename

    def load_data_gsheet(self):
        try:
            gc = gspread.service_account()
            sheet = gc.open("Optic Lab Shooting schedule")
            #worksheet_list = sh.worksheets()
            #print(worksheet_list)
            #print(sh.sheet1.get('A1'))
            temp_worksheet = sheet.worksheet("temperaturas")
            temp_dataframe = pd.DataFrame(temp_worksheet.get_all_records())
            video_worksheet = sheet.worksheet("FINAL EDITS")
            #values_list = video_worksheet.row_values(1)
            self.videodf = pd.DataFrame(video_worksheet.get_all_records())
            self.tempdf = temp_dataframe.head(9).astype({"temp_start":"int","temp_end":"int"})
            return True
        except Exception as e:
            self.log.critical("gsheet not working" + str(e))
            return False

    def dataframe_to_code(self, df):
        data = np.array2string(df.to_numpy(), separator=', ')
        data = data.replace(" nan", " float('nan')")
        cols = df.columns.tolist()
        return f"""pd.DataFrame({data}, columns={cols})"""

    def save_data_file(self):
        self.tempdf.to_csv(self.tempsfile + '.csv', index=False)
        self.videodf.to_csv(self.videofile + '.csv', index=False)
        # FIXME: does not work with video dataframe, should use better format
        '''
        with open(self.tempsfile, "w") as f:
            f.write(self.dataframe_to_code(self.tempdf))
        with open(self.videofile, "w") as f:
            f.write(self.dataframe_to_code(self.videodf))
        '''


    def load_data_file(self):
        
        self.tempdf = pd.read_csv(self.tempsfile + '.csv')
        self.videodf = pd.read_csv(self.videofile + '.csv')



    def cat_from_temp(self, temp):
        tf = pd.DataFrame({ 'Value': { 0: temp }})
        s1=self.tempdf.temp_start.values
        s2=self.tempdf.temp_end.values
        s=tf.Value.values[:,None]
        return np.dot((s>=s1)&(s<=s2),self.tempdf.CATEGORIA)[0]

    def filenames_from_cat(self, node, cat):
        #la = self.videodf.query('`Usage` == `Y` and CHANNEL == `BOB` and `FEELING` == ' + cat )
        if node == 'A':
            channel = 'BOB'
        elif node == 'B':
            channel = 'ALICE'
        else:
            channel = 'unknown'
        #la = self.videodf.query('USE == "Y" and CHANNEL == @channel or CHANNEL == "BOTH" and FEELING == @cat')
        la = self.videodf.query('(CHANNEL == @channel or CHANNEL == "BOTH") and USE == "Y" and (AVAILABLE == "USB") and FEELING == @cat')

        #fnames = la['FILE NAME'].tolist()
        fnames = la['NOTES'].tolist()

        return fnames

    def test_cat(self):
        for n in ("A", "B"):
            print()
            print("node: " + n)
            print()
            for c in self.tempdf.CATEGORIA:
                print(c + ': ' + str(self.filenames_from_cat(n, c)))

    def get_random_file(self, node, temp):
            cat = cat_from_temp()




if __name__ == "__main__":
    p = Videochooser()
    p.load_data_gsheet()
    p.save_data_file()
    p.load_data_file()
    p.test_cat()
    #cat = p.cat_from_temp(12)
    #print(cat)
    #fn = p.filenames_from_cat("A", cat)
    #print(fn)


 
