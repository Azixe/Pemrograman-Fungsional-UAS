from mysql.connector import Error
import mysql.connector
import json
from flask import Flask, request, jsonify
from markupsafe import escape
import pymysql

app = Flask(__name__)


def db_conn():
    conn = None
    try:
        conn = pymysql.connect(
            host="localhost",
            database="earth_federation_database",
            port=3306,
            user="root",
            password="",
            cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.Error as e:
        print(e)
    return conn


@app.route("/")
def land():
    return ("Welcome To Earth Federation's Mobile Suit Database")


@app.route("/mobile-suits", methods=['GET', 'POST'])
def main():
    conn = db_conn()
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute("SELECT * from MS")
        ms = [
            dict(
                Model_id=row['Model_id'],
                Model_name=row['Model_name'],
                Manufacturer=row['Manufacturer'],
                Operator=row['Operator'],
                Unit_type=row["Unit_type"],
                Fixed_weapons=row["Fixed_weapons"],
                Handheld_weapons=row["Handheld_weapons"],
                Armor=row["Armor"],
                Power_plant=row["Power_plant"]
            )
            for row in cursor.fetchall()
        ]
        if ms is not None:
            return jsonify(ms)

    if request.method == "POST":
        add_model_id = request.form['Model_id']
        add_model_name = request.form['Model_name']
        add_manufacturer = request.form['Manufacturer']
        add_operator = request.form['Operator']
        add_unit_type = request.form['Unit_type']
        add_fixed_weapons = request.form['Fixed_weapons']
        add_handheld_weapons = request.form['Handheld_weapons']
        add_armor = request.form['Armor']
        add_power_plant = request.form['Power_plant']
        
        cursor.execute(
            "insert into MS (Model_id, Model_name, Manufacturer, Operator, Unit_type, Fixed_weapons, Handheld_weapons, Armor, Power_plant) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (add_model_id, add_model_name, add_manufacturer, add_operator, add_unit_type, add_fixed_weapons, add_handheld_weapons, add_armor, add_power_plant))
        conn.commit()
        return ("New Mobile Suit data succesfully created.")


@app.route("/mobile-suits/<string:model_id>", methods=['GET', 'PUT', 'DELETE'])
def info(model_id):
    conn = db_conn()
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute("select * from ms where model_id = %s", (model_id))
        ms = cursor.fetchone()

        if ms is not None:
            return jsonify(ms)

    if request.method == 'PUT':
        model_name = request.form['Model_name']
        manufacturer = request.form['Manufacturer']
        operator = request.form['Operator']
        unit_type = request.form['Unit_type']
        fixed_weapons = request.form['Fixed_weapons']
        handheld_weapons = request.form['Handheld_weapons']
        armor = request.form['Armor']
        power_plant = request.form['Power_plant']
        cursor.execute(
            "update MS set Model_name = %s, Manufacturer = %s, Operator = %s, Unit_type = %s, Fixed_weapons = %s, Handheld_weapons = %s, Armor = %s, Power_plant = %s where Model_id = %s", (model_name, manufacturer, operator, unit_type, fixed_weapons, handheld_weapons, armor, power_plant, model_id))
        conn.commit()
        return ("Mobile Suit data with model_id = {} updated!".format(model_id))

    if request.method == 'DELETE':
        cursor.execute("delete from MS where Model_id = %s", (model_id))
        conn.commit()
        return ("Mobile Suit data with model_id = {} Deleted!".format(model_id))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)