import psycopg2

con = psycopg2.connect(
  database="postgres",
  user="postgres",
  password="postgres",
  host="localhost",
  port="5432"
)

print("Database opened successfully")
cur = con.cursor()
"""

cur.execute(
  "INSERT INTO prompts (user_id,prompt,steps,scale,width,height,model,negative) VALUES ('125011869', 'cat in boat, rainbow', '10', '9', '256', '512', 'deliberate_v11.ckpt [10a699c0f3]', 'red color')"
)

# Редактирование
# cur.execute("UPDATE prompts set prompt = 'car' where user_id = '125011869'")

con.commit()
print("Record inserted successfully")
"""



cur.execute("SELECT user_id,prompt from prompts")

rows = cur.fetchall()
for row in rows:
   print("user_id =", row[0])
   print("prompt =", row[1])

print("Operation done successfully")


con.close()