from flask import Flask, jsonify, request
app = Flask(__name__)
# In-memory database
students = [
    {"id": 1, "name": "Rushi", "course": "CSE"},
    {"id": 2, "name": "Ram", "course": "IT"},
    {"id": 3, "name": "Sunil", "course": "ENTC"},
    {"id": 4, "name": "Kunal", "course": "IT"},
    {"id": 5, "name": "Ishita", "course": "EEC"},
    {"id": 6, "name": "Lalita", "course": "IT"}
]
# CREATE (POST)
@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    students.append(data)
    return jsonify({"message": "Student added!", "students": students})
# READ (GET all)
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students)
# READ (GET by id)
@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    student = next((s for s in students if s["id"] == id), None)
    return jsonify(student) if student else jsonify({"error": "Not found"}), 404
# UPDATE (PUT)
@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.get_json()
    for s in students:
        if s["id"] == id:
            s.update(data)
    return jsonify({"message": "Student updated!", "student": s})
    return jsonify({"error": "Not found"}), 404
# DELETE
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    global students
    students = [s for s in students if s["id"] != id]
    return jsonify({"message": "Student deleted!", "students": students})

if __name__ == '__main__':
    app.run(debug=True)