import psycopg2

hostname = 'postgresql-ascscs.alwaysdata.net'
database = 'ascscs_securedrive'
username = 'ascscs'
pwd = '@7sdDgVUuhCXjD6'
port_id = 5432
conn = None
cur = None
try:
    conn = psycopg2.connect(
        host = hostname,
        dbname = database,
        user = username,
        password = pwd,
        port = port_id
    )

    cur = conn.cursor()

    insert_script = 'INSERT INTO USERS(email,password,auth) VALUES(%s,%s,%s)'
    insert_value = ('akash1@gmail.com', 'akash08','TRUE')
    cur.execute(insert_script,insert_value)
    conn.commit()





except Exception as error:
    print(error)
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()





