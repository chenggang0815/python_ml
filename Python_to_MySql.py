
import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='192.168.1.4',
                             user='risk',
                             password='risk.1234',
                             db='decision',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

id=list('hello world')
name=list('hello world')

n=len(id)
print(n)
for i in range(n):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
        cursor.execute(sql, (id[i],name[i]))
    connection.commit()
