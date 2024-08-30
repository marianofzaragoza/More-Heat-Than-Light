from influxdb import InfluxDBClient
from config import DynamicConfigIni
import logging
import mhlog 

class MhInflux():
    def __init__(self, enable_appqueue=False):
        logging.setLoggerClass(mhlog.Logger)
        self.log = mhlog.getLog("influx", self)
        self.log.setLevel(logging.WARN)
 
        self.config = DynamicConfigIni()
        self.nodename = self.config.DEFAULT.nodename  # Access the nodename

        self.dbname = "example"

        self.client = InfluxDBClient('192.168.172.235', 8086, 'root', 'root', self.dbname)

        self.client.create_database(self.dbname)


    def update_stats(self, node, mtype, value, seconds, nanos):
        return 


    def store_line(self, node, mtype, value, seconds, nanos):

        now = datetime.datetime.today()
        txdate = datetime.utcfromtimestamp(seconds)
        json_body = [
            {
                "measurement": "mhpacket",
                "tags": {
                    "rxhost": self.nodename,
                },
                "time": int(now.strftime('%s')),

                "fields": {
                    "node": node,
                    "mtype": mtype,
                    "value": value,
                    "seconds": seconds,
                    "nanos": nanos,
                    "txtime": int(txdate.strftime('%s')),

                }
            }
        ]
        self.client.write_points(json_body)
    def read_line():
        result = client.query('select value from cpu_load_short;')

        print("Result: {0}".format(result))

if __name__ == "__main__":
    db = MhInflux()

    db.store_line()
