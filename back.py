from flask import Flask, render_template, send_file, request, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import os

app = Flask(__name__)

# Funkcija, lai ielādētu datus no SQLite datubāzes
def load_data():
    conn = sqlite3.connect('f1.db')
    df = pd.read_sql_query("SELECT * FROM results", conn)
    conn.close()
    return df

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/stats')
def stats():
    return render_template("stats.html")

@app.route('/drivers')
def drivers():
    return render_template('drivers.html')

@app.route('/news')
def news():
    return render_template('news.html')

@app.route('/chart/<name>')
def chart(name):
    df = load_data()

    os.makedirs('static/charts', exist_ok=True)

    if name == "top5_pilots":
        top5 = df.groupby("driver")["points"].sum().sort_values(ascending=False).head(5)
        plt.figure(figsize=(8, 5))
        top5.plot(kind='bar', color='#ef233c')
        plt.title("Top 5 Piloti pēc Punktiem")
        plt.ylabel("Punkti")
        plt.xticks(rotation=45)
        plt.tight_layout()
        path = "static/charts/top5_pilots.png"
        plt.savefig(path)
        plt.close()
        return send_file(path, mimetype='image/png')

    elif name == "team_comparison":
        teams = df.groupby("team")["points"].sum().sort_values(ascending=False)
        plt.figure(figsize=(10, 5))
        teams.plot(kind='bar', color='#8d99ae')
        plt.title("Komandu Punkti")
        plt.ylabel("Punkti")
        plt.xticks(rotation=45)
        plt.tight_layout()
        path = "static/charts/team_comparison.png"
        plt.savefig(path)
        plt.close()
        return send_file(path, mimetype='image/png')

    return "Grafiks nav atrasts", 404

if __name__ == '__main__':
    app.run(debug=True)
