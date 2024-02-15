import psycopg2

def search_for_email(host, port, database, user, password, sql_query):

	result = ''

	try:
		connector: psycopg2.connection = psycopg2.connect(
				database=database, user=user, password=password, host=host, port=port, sslmode='require'
			)
	except Exception as err:
		print(err)
		return (str(err), sql_query)
	else:
		cur = connector.cursor()

	try:
		cur.execute(sql_query)
	except Exception as err:
		print(err)
		connector.rollback()
		return (str(err), sql_query)
	
	try:
		rows = cur.fetchall()
		for row in rows:
			result += str(row) + '</br>'
	except Exception as err:
		print(err)
		connector.rollback()
		return (str(err), sql_query)
	else:
		connector.commit()
		return (result, sql_query)