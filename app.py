# app.py

# Required imports
import os
from flask import Flask, request, jsonify
from firebase_admin import firestore, initialize_app
import comparison
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Initialize Firestore DB
default_app = initialize_app()
db = firestore.client()
col_ref = db.collection('testing')


@app.route('/add_question', methods=['POST'])
def createQuestion():
    """
        createQuestion() : Add document to Firestore collection with request body.
        Ensure you pass a custom ID as part of json body in post request,
        e.g. json={'question': 'What color is the sky?'}
    """
    try:
        id = col_ref.document().id
        question = request.json['question']
        col_ref.document(id).set({"id": id, "question": request.json['question']})
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"

@app.route('/add_answer', methods=['POST'])
def createAnswer():
    """
        createAnswer() : Add document to Firestore a specific question's collection with request body.
        Ensure you pass the question and answer as part of json body in post request, along with whether it's correct or not
        e.g. json={'question': 'What color is the sky?', 'answer': 'Blue', 'correct': True}
    """
    try:
        qid = request.json['id']
        newAnswer = request.json['answer']
        if "correct" in request.json:
            correct = request.json['correct']
        else:
            question = col_ref.document(qid).get()
            answersCol = col_ref.document(qid).collection("correct_answers")
            answers = [a.to_dict()['answer'] for a in answersCol.stream()]
            correct = comparison.findSimilarity(answers, newAnswer)
        # determine whether the answer is correct or not
        if correct > comparison.confidenceThreshold:
            col_ref.document(qid).collection('correct_answers').document().set(request.json)
        else:
            col_ref.document(qid).collection('incorrect_answers').document().set(request.json)
        return jsonify({"correct": correct}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"


@app.route('/list', methods=['GET'])
def read():
    """
        read() : Fetches documents from Firestore collection as JSON.
        todo : Return document that matches query ID.
        all_todos : Return all documents.
    """
    try:
        # Check if ID was passed to URL query
        qid = request.args.get('id')
        if qid:
            question = col_ref.document(qid).get()
            answersCol = col_ref.document(qid).collection("correct_answers")
            incorrectAnswersCol = col_ref.document(qid).collection("incorrect_answers")
            answers = [a.to_dict() for a in answersCol.stream()]
            incorrectAnswers = [i.to_dict() for i in incorrectAnswersCol.stream()]
            return jsonify(question.to_dict(), answers, incorrectAnswers), 200
        else:
            all_todos = [doc.to_dict() for doc in col_ref.stream()]
            return jsonify(all_todos), 200
    except Exception as e:
        return f"An Error Occurred: {e}"


@app.route('/update', methods=['POST', 'PUT'])
def update():
    """
        update() : Update document in Firestore collection with request body.
        Ensure you pass a custom ID as part of json body in post request,
        e.g. json={'id': '1', 'title': 'Write a blog post today'}
    """
    try:
        qid = request.json['id']
        col_ref.document(qid).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"


def delete_collection(coll_ref, batch_size):
    docs = coll_ref.limit(batch_size).stream()
    deleted = 0

    for doc in docs:
        print(u'Deleting doc {} => {}'.format(doc.id, doc.to_dict()))
        doc.reference.delete()
        deleted = deleted + 1

    if deleted >= batch_size:
        return delete_collection(coll_ref, batch_size)


@app.route('/delete', methods=['GET', 'DELETE'])
def delete():
    """
        delete() : Delete a document from Firestore collection.
    """
    try:
        # Check for ID in URL query
        qid = request.args.get('id')
        delete_collection(col_ref.document(qid).collection("correct_answers"), 10)
        delete_collection(col_ref.document(qid).collection("incorrect_answers"), 10)
        col_ref.document(qid).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"




port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)