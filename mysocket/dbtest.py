import pymysql


class dbTest:
    host = "localhost"
    port = 3306
    user = "root"
    passwd = "123456"
    db = "battery1"

    def executeGetSQL(self, sql, keys):
        dbconnection = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd,
                                       db=self.db, charset="utf8")
        cursor = dbconnection.cursor()
        result = None
        r_list = []
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            r_list = []
            for i in result:
                data = {}
                for j in range(0, len(keys)):
                    data[keys[j]] = i[j]
                r_list.append(data)
        except Exception as e:
            print(e)
            dbconnection.rollback()
        dbconnection.commit()
        dbconnection.close()
        return r_list


if __name__ == "__main__":
    db = dbTest()
    keys = ["ID", "currState", "nextState", "IP", "PortNum", "Addr", "ovenPlanID_id"]
    keystr = ",".join(keys)
    sql = 'SELECT ' + keystr + ' FROM apps_ovendevicetable'
    print(db.executeGetSQL(sql, keys))
