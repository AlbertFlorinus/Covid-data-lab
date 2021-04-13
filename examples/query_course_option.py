import mysql.connector as mysql

MYSQL_USER = "root"
MYSQL_PASS = str(input("input root password: "))

# change to your DB name instead of "Corona"
MYSQL_DATABASE = "Corona"
host_ip = "127.0.0.1" 

connection = mysql.connect(user=MYSQL_USER, password = MYSQL_PASS, database = MYSQL_DATABASE, host = host_ip)
cnx = connection.cursor(dictionary=True)

cmd = str(input("Input SQL Query: "))
cnx.execute(cmd)

for i in cnx:
    print(i)

connection.commit()
connection.close()
print("done")
