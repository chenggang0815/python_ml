import pymysql

db = pymysql.connect("192.168.1.4", "risk", "risk.1234", "decision",charset='utf8')
cursor=db.cursor()

try:
    cursor.execute('''INSERT INTO decision.cg_test VALUES(2,'mary'),(3,'chenggang')''')
    db.commit()
    print('成功插入数据')
except:
    print("Error: unable to insert data")

try:
    cursor.execute('delete from decision.cg_test where id =1')
    db.commit()
    print('成功删除数据')
except:
    print('Error: unable to delete data')

cursor=db.cursor()
try:
    cursor.execute('select * from decision.cg_llcs limit 20')
    results=cursor.fetchall()
    for i in results:
        print(i)

except:
    print("Error: unable to fecth data")

# 关闭数据库连接
db.close()
