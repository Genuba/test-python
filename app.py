# app.py
from flask import Flask, request, jsonify
from bd import conexion
from datetime import datetime, timezone
import psycopg2

app = Flask(__name__)

@app.get("/vulnerabilities")
def get_vulnerabilities():
    try:
        with conexion.cursor() as cursor:
            consulta = "SELECT vulnerability_id, level, description, request, created_on FROM vulnerability WHERE vulnerability_id = %s;"
            cursor.execute(consulta, (request.args['id']))
            
            vulnerabilities = cursor.fetchall()
            return jsonify(vulnerabilities)
    except psycopg2.Error as e:
        print(e)
        return {"error": "getting info error"}, 415

@app.post("/vulnerabilities")
def add_vulnerability():
    if request.is_json:
        vulnerability = request.get_json()
        dt = datetime.now(timezone.utc)
        try:
            with conexion.cursor() as cursor:
                consulta = "INSERT INTO vulnerability(level, description, request, created_on) VALUES (%s, %s, %s, %s);"
                cursor.execute(consulta, (vulnerability['level'], vulnerability['description'], vulnerability['request'], dt))
            conexion.commit()
            return {}, 201
        except psycopg2.Error as e:
            print(e)
            return {"error": "inserting error"}, 415
    return {"error": "Request must be JSON"}, 415