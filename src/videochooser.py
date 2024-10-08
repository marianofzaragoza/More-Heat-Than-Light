from config import DynamicConfigIni
import logging
import mhlog 
import numpy as np
import pathlib
import config
import gspread
import pandas as pd
import random
import os
class Videochooser():
    def __init__(self, gsheet=False):
        logging.setLoggerClass(mhlog.Logger)
        self.log = mhlog.getLog("newplaylist", self)
        self.log.setLevel(logging.WARN)
        srcdir = pathlib.Path(__file__).parent.resolve()
 
        self.tempsfile = str(srcdir) + '/temperaturas.dataframe'
        self.videofile = str(srcdir) + '/finaledits.dataframe'
        self.statesfile = str(srcdir) + '/states.dataframe'
        
        self.last_filename = 'startup'

        self.config = DynamicConfigIni()
        self.videodir = self.config.playlist.videodir_final


        self.nodename = self.config.DEFAULT.nodename  # Access the nodename
        if gsheet:
            self.log.critical("loading data from gsheet, takes some seconds....")
            self.load_data_gsheet()
        else:
            self.load_data_file()




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
            states_worksheet = sheet.worksheet("STATES")
            #values_list = video_worksheet.row_values(1)
            self.videodf = pd.DataFrame(video_worksheet.get_all_records())
            self.tempdf = temp_dataframe.head(9).astype({"temp_start":"int","temp_end":"int","MIDIA":"int","MIDIB":"int"})
            self.statesdf = pd.DataFrame(video_worksheet.get_all_records()).head(6)

            return True
        except Exception as e:
            self.log.critical("gsheet not working" + str(e))
            self.load_data_file()
            return False

    def dataframe_to_code(self, df):
        data = np.array2string(df.to_numpy(), separator=', ')
        data = data.replace(" nan", " float('nan')")
        cols = df.columns.tolist()
        return f"""pd.DataFrame({data}, columns={cols})"""

    def save_data_file(self):
        self.tempdf.to_csv(self.tempsfile + '.csv', index=False)
        self.videodf.to_csv(self.videofile + '.csv', index=False)
        self.statesdf.to_csv(self.statesfile + '.csv', index=False)

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
        self.statesdf = pd.read_csv(self.statesfile + '.csv')

    def state_from_temp(self, a_temp, b_temp):
        '''
        #tf = pd.DataFrame({ 'Value': { 0: temp }})
        atemp_min=self.tempdf.ATEMP_MIN.values
        atemp_max=self.tempdf.ATEMP_MAX.values
        btemp_min=self.tempdf.BTEMP_MIN.values
        btemp_max=self.tempdf.BTEMP_MAX.values
        state = np.dot((s>=s1)&(s<=s2),self.statesdf.STATE)[0]
        '''
        if a_temp < 20 and b_temp < 20 and abs(a_temp - b_temp) < 1:
            return "ENTANGLEMENT"
        elif abs(a_temp - b_temp) > 10:
            return "BROKENCHANNEL"
        else:
            return "TRANSMISSION"
 


    def cat_from_temp(self, temp):
        tf = pd.DataFrame({ 'Value': { 0: temp }})
        s1=self.tempdf.temp_start.values
        s2=self.tempdf.temp_end.values
        s=tf.Value.values[:,None]
        '''
        copy = self.tempdf 
        lala = np.where(
                (self.tempdf['temp_start'] <= temp) 
                & (    self.tempdf['temp_end'] <= temp  )
                , self.tempdf, np.nan)
        
        print(lala)
        '''
        res =  np.dot((s>s1)&(s<=s2),self.tempdf.CATEGORIA)
        '''
        print(type(res))
        print(res)
        '''
        return res[0]

    def filenames_from_cat(self, node, cat):
        #la = self.videodf.query('`Usage` == `Y` and CHANNEL == `BOB` and `FEELING` == ' + cat )
        
        if node == 'A':
            channel = 'ALICE'
        elif node == 'B':
            channel = 'BOB'
        else:
            channel = 'unknown'
        #la = self.videodf.query('USE == "Y" and CHANNEL == @channel or CHANNEL == "BOTH" and FEELING == @cat')
        la = self.videodf.query('(CHANNEL == @channel or CHANNEL == "BOTH") and USE == "Y" and (AVAILABLE == "UPLOADED") and FEELING == @cat')

        fnames = la['FILE NAME'].tolist()
        #fnames = la['NOTES'].tolist()

        return fnames
    def note_from_cat(self, node, cat):
        try:
            la = self.tempdf.query('(CATEGORIA == @cat)')
            an = la['MIDIA'].iloc[0]
            bn = la['MIDIB'].iloc[0]
            if node == 'A':
                n = an
            elif node == 'B':
                n = bn
            else:
                n = an
        except IndexError as e:
            n = 23
            self.log.critical('node: ' + node + ' cat: ' + str(cat) + '   ' + str(e))
        #print('A: ' + str(an), 'B: ' + str(bn))
        return n
    
    def get_all_cat(self):
        ac = list()
        for c in self.tempdf.CATEGORIA:
            ac.append(str(c))
        return c

    def test_cat(self):
        for n in ("A", "B"):
            print()
            print("node: " + n)
            print()
            for c in self.tempdf.CATEGORIA:
                midi = self.note_from_cat(n, c)
                print(c + ' : ' + str(midi) + ' '  + str(self.filenames_from_cat(n, c)))

    def get_broken_channel_file(self, channel):
        self.log.critical('bc0 ' + channel)
        return "BROKENCHANNEL_" + channel + '.mov'

    def get_random_file(self, node, temp_a, temp_b, entanglement=False):
            state = self.state_from_temp(temp_a, temp_b)
            if node == 'A':
                temp = temp_a
            elif node == 'B':
                temp = temp_b
            else:
                #self.log.critical(f'midi: node {node} has no known channel configured, using A')
                temp = temp_a
 
            if (state == "ENTANGLEMENT" and entanglement==True) or (self.last_filename == "ENTANGLEMENT.mov" and state == "ENTANGLEMENT"):
                filename = 'ENTANGLEMENT.mov'
 
            elif (state == "TRANSMISSION" or state == "BROKENCHANNEL" or state == "ENTANGLEMENT") and entanglement == False:
                cat = self.cat_from_temp(temp)
                filenames = self.filenames_from_cat(node, cat)
                try:
                    filename = random.choice(filenames)
                except IndexError as e:
                    self.log.info("no video found for: " + node + ' at: ' + str(temp_a) + ' bt:' + str(temp_b) + ' state: ' + state + ' cat: ' + cat)
                    filename = 'VIDEO_MISSING.mov'

            if not os.path.isfile(self.videodir + '/' + filename):
                self.log.critical('file missing: ' + filename)
                filename = 'VIDEO_MISSING.mov'
            self.last_filename == filename
            return filename

    def get_midi_note(self, node, temp_a, temp_b):
            #print("get midi note")
            state = self.state_from_temp(temp_a, temp_b)
            if node == 'A':
                temp = temp_a
            elif node == 'B':
                temp = temp_b
            else:
                #self.log.critical(f'midi: node {node} has no known channel configured, using A')
                temp = temp_a
     
            if state == "TRANSMISSION":
                cat = self.cat_from_temp(temp)
                note = self.note_from_cat(node, cat)
                self.log.info("got note " + str(note))
            elif state == "ENTANGLEMENT":
                note = False
            elif state == "BROKENCHANNEL":
                note = False
            return note



if __name__ == "__main__":
    p = Videochooser()
    p.load_data_gsheet()
    p.save_data_file()
    p.load_data_file()
    p.test_cat()
    print(p.state_from_temp(10, 10))
    print(p.state_from_temp(30, 30))
    print(p.state_from_temp(0, 100))
    print(p.get_random_file('A', 10, 10))
    print(p.get_random_file('A', 30, 30))
    print(p.get_random_file('B', 0, 100))
    print(p.get_broken_channel_file('A'))

    cat = p.cat_from_temp(22)
    print(cat)
    print('notes')
    note = p.note_from_cat('A',cat)
    #fn = p.filenames_from_cat("A", cat)
    #print(fn)


 
