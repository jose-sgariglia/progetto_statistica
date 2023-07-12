import requests;
import mysql.connector

# Parser HTML
from bs4 import BeautifulSoup;

# API per avere i continenti delle nazioni
import pycountry_convert as pc  



# Ottenere il nome dei continenti dal nome di un paese

def country_to_continent(country_name: str) -> str:
    try:
        country_alpha2 = pc.country_name_to_country_alpha2(country_name)
        country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
        country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
        return country_continent_name
    
    except KeyError:
        return 'Unknown'



# Connessione al DB

mydb = mysql.connector.connect(
  host = "YOUR HOST",
  user = "YOUR USER",
  password = "YOUR PASSWORD",
  database = "YOUR DATABASES"
)



# Inizializzazione del db

def init_db() -> None:
    url = "https://rhesusnegative.net/themission/bloodtypefrequencies/"

    page = requests.get(url, headers={"User-Agent": "XY"})
    soup = BeautifulSoup(page.content, 'html.parser')

    mycursor = mydb.cursor()
    list = []

    # Query SQL
    insert_sql = 'INSERT INTO country(name, population, `0+`, `a+`, `b+`, `ab+`, `0-`, `a-`, `b-`, `ab-`, continent) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    

    for row in soup.select('tr')[1:-3]:
        item = []
        
        item.append(row.select('th')[0].text.strip())
        item.append(int(row.select('td')[0].text.replace(',', '')))
        for col in row.select('td')[1:]:
            item.append(
                float(
                    col.text.replace('%', '') 
                    if col.text.replace('%', '').count('.') == 1 
                    else col.text.replace('%', '').replace('.', ',', 1).replace('.', '').replace(',', '.')
                )
            )

        item.append(country_to_continent(item[0]))
        list.append(tuple(item))
        

    mycursor.executemany(insert_sql, list)
    mydb.commit()

    print(mycursor.rowcount, "was inserted.")

    pass



if __name__  == '__main__':
    init_db()    
    pass
