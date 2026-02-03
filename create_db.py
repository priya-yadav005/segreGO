

import pymysql
import sys

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'root3105@'
DB_NAME = 'segrego_db'

try:

    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    cursor = connection.cursor()

    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    print(f"✓ Database '{DB_NAME}' created successfully!")

    cursor.close()
    connection.close()

except pymysql.Error as err:
    if err.args[0] == 2003:
        print("✗ Error: Cannot connect to MySQL server.")
        print("  Make sure MySQL is running on localhost:3306")
        print("  Default credentials: User='root', Password='admin'")
    else:
        print(f"✗ Database error: {err}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Error: {e}")
    print("Make sure MySQL server is running and accessible at localhost:3306")
    sys.exit(1)

print("\nNow running Django migrations...")
import os
os.system(f"{sys.executable} manage.py migrate")
