from database import Database
import json
d = Database()
d.c.execute(f"""SELECT count_clothes('', '', money(-1))""")
print(d.c.fetchall()[0][0])