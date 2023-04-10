import sqlite3 as sql

#con = sql.connect('310.158.sqlitedb')
#con = sql.connect('310.158.sqlitedb')
cur = con.cursor()


photos = cur.execute('SELECT b FROM t')

k = 1
for photo in photos:
        with open(f'{k}.jpg', 'wb') as file:
            file.write(photo[0])
            k+=1


con.commit()
cur.close()
con.close()
input('OK')