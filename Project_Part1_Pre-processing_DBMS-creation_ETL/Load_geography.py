import pyodbc
import csv

server = 'tcp:131.114.72.230'
database="Group_28_DB"
username="Group_28"
password="L1GGUHBQ"

connectionString = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password
cnxn = pyodbc.connect(connectionString)
cursor = cnxn.cursor()


geo_file = open(r"C:\Users\Gaetano\Desktop\ProgettoLAB\csv_output\geography.csv", "r")
csv_file = csv.DictReader(geo_file, delimiter = ",")

sql_query = "INSERT INTO Geography(country_id,language,continent) VALUES (?,?,?)"
i=1
for row in csv_file:
    val = (row["country_id"], row["language"], row["continent"])
    cursor.execute(sql_query, val)
    print("Loading row %d" %i)
    i=i+1

geo_file.close()
cnxn.commit()
cursor.close()
cnxn.close()
