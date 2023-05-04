import psycopg2
import os

def test_function():
	# Connect to your postgres DB
	password = os.getenv('STEAMPOWERED_PG_PASSWORD')
	
	conn = psycopg2.connect(f"host=postgres dbname=steampowered user=steampowered password={password}")

	# Open a cursor to perform database operations
	cur = conn.cursor()

	# Execute a query
	cur.execute("SELECT * FROM information_schema.tables where table_catalog = 'steampowered';")

	# Retrieve query results
	records = cur.fetchall()

	print ( records )
