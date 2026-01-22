from flask import Blueprint, request, jsonify
from models import (
    create_person, get_all_persons,
    create_case, get_all_cases
)

api = Blueprint("api", __name__)

@api.route("/persons", methods=["POST"])
def add_person():
    data = request.json
    create_person(
        data["first_name"],
        data["last_name"],
        data["role"]
    )
    return jsonify({"status": "Person gespeichert"}), 201

@api.route("/persons", methods=["GET"])
def list_persons():
    return jsonify(get_all_persons())

@api.route("/cases", methods=["POST"])
def add_case():
    data = request.json
    create_case(
        data["title"],
        data.get("description", ""),
        data.get("priority", "normal")
    )
    return jsonify({"status": "Case gespeichert"}), 201

@api.route("/cases", methods=["GET"])
def list_cases():
    return jsonify(get_all_cases())
