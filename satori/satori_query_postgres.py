import psycopg2

def search_for_email(host, port, database, user, password, sql_query):

	try:
		result = ''
		connector = psycopg2.connect(database=database, user=user, password=password, host=host, port=port, sslmode='require')
		cur = connector.cursor()
		cur.execute(sql_query)
		#connector.commit()
		rows = cur.fetchall()
		for row in rows:
			result += str(row) + '</br>'
		return (result, sql_query)
	except Exception as err:
		print(err)
		return (str(err), sql_query)