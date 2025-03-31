from models.questions import Question, jsonify
from models import db

def get_all_questions() -> list[dict[str, int | str]]:
    questions = Question.query.all()

    questions_data = [
        {
            "id": question.id,
            "text": question.text
        }
        for question in questions
    ]

    return questions_data


def create_new_question(raw_data: dict[str, str]) -> Question:
    new_obj = Question(text=raw_data["text"])

    db.session.add(new_obj)
    db.session.commit()

    return new_obj
def get_question_by_id(id: int) -> Question:
    obj = Question.query.get(id)
    return obj



### sasa ###

@questions_bp.route('/<int:id>', methods=["GET", "PUT", "DELETE"])
def retrieve_question(id: int):
    if request.method == "GET":
        question_by_id = get_question_by_id(id=id)
        if not question_by_id:
            return jsonify(
                {
                    "error": f"ID {id} not found."
                }
            ), 404

        return jsonify(question_by_id)
# Реализзовать эндпоинт на обновление конкретного вопроса по его ID
    if request.method == "PUT":
        question_by_id = get_question_by_id(id=id)
        if not question_by_id:
            return jsonify(
                {
                    "error": f"ID {id} not found."
                }
            ), 404
        data = request.json
        if not data or "text" not in data:
            return jsonify(
                {
                    "error": "No required field provided.('text')"
                }
            ), 400
        updated_question = update_question(obj=question_by_id, new_data=data)
        return jsonify(
            {
                "id": updated_question.id,
                "text": updated_question.text
            }
        ), 200

    if request.method == "DELETE":
        return f"QUESTION DELETE BY ID - {id}"