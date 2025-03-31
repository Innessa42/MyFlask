from flask import Blueprint, request

answers_bp = Blueprint('answers', __name__)

@answers_bp.route("", methods=["GET", "POST"])
def work_with_answers():
    if request.method == "GET":
        return "polucim spisoc vseh otvetov"
    if request.method == "POST":
        return "Sozdanie otveta na zapros"

@answers_bp.route("/<int:id>", methods=["GET"])
def retrieve_answer(id):
    return f'Otvet na zapros {id}'































