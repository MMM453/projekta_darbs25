from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import sqlite3
import os

app = Flask(__name__)
DB_PATH = "f1.db"
CSV_UPLOADED_FLAG = "csv_uploaded.flag"

# Funkcija, lai ielādētu datus no datubāzes
def get_drivers():
    conn = sqlite3.connect(DB_PATH)
    drivers = pd.read_sql_query("SELECT * FROM drivers", conn)
    conn.close()
    return drivers

# Funkcija, lai iegūtu komandas no datubāzes
def get_teams():
    conn = sqlite3.connect(DB_PATH)
    teams = pd.read_sql_query("SELECT DISTINCT team FROM drivers", conn)
    conn.close()
    return teams

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/stats')
def stats():
    return render_template("stats.html")

@app.route('/news')
def news():
    return render_template('news.html')

@app.route('/drivers', methods=['GET', 'POST'])
def drivers():
    csv_uploaded = os.path.exists(CSV_UPLOADED_FLAG)
    
    if request.method == 'POST' and not csv_uploaded:
        # CSV faila apstrāde
        file = request.files['file']
        if file and file.filename.endswith('.csv'):
            df = pd.read_csv(file)
            conn = sqlite3.connect(DB_PATH)
            df.to_sql('drivers', conn, if_exists='append', index=False)
            conn.close()
            
            # Atzīmē, ka CSV ir augšupielādēts
            open(CSV_UPLOADED_FLAG, 'w').close()
            return redirect(url_for('drivers'))
    
    # Ielādē datus no datubāzes
    drivers = get_drivers()
    teams = get_teams()
    return render_template('drivers.html', drivers=drivers, teams=teams, csv_uploaded=csv_uploaded)

# Pirms servera startēšanas dzēš iepriekšējos datus un CSV atzīmi
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
if os.path.exists(CSV_UPLOADED_FLAG):
    os.remove(CSV_UPLOADED_FLAG)
    
# Izveido datubāzi un tabulu, ja tās nav
conn = sqlite3.connect(DB_PATH)
conn.execute('''
    CREATE TABLE drivers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        country TEXT NOT NULL,
        team TEXT NOT NULL
    )
''')
conn.close()

if __name__ == '__main__':
    app.run(debug=True)
