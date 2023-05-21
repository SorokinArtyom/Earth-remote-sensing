import sqlite3 as sql
import grpc
import images_pb2
import images_pb2_grpc
import random
import base64

con = sql.connect('310.158.sqlitedb')
#con = sql.connect('310.158.sqlitedb')
cur = con.cursor()

yx = list(cur.execute('SELECT x, y FROM t'))


coord = random.choice(yx)

#photos = list(cur.execute(f'SELECT id FROM t where x={coord[0]} AND y={coord[1]}'))
#b64string = base64.b64encode(photos[0][0])

#print(type(b64string.decode()))

with grpc.insecure_channel('localhost:7000') as channel:
    stub = images_pb2_grpc.send_imagesStub(channel=channel)

    response = stub.sendImage(images_pb2.img(image=str(random.randint(1,70))+".jpg"))

# sleep(2)


con.commit()
cur.close()
con.close()
input('OK')