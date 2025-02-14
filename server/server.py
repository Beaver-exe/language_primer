from flask import Flask, jsonify, request, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

groups = []
students = []

@app.route('/api/groups', methods=['GET'])
def get_groups():
    """
    Route to get all groups
    return: Array of group objects
    """
    # TODO: (sample response below)
    return jsonify(groups)

@app.route('/api/students', methods=['GET'])
def get_students():
    """
    Route to get all students
    return: Array of student objects
    """
    # TODO: (sample response below)
    return jsonify(students)

@app.route('/api/groups', methods=['POST'])
def create_group():
    """
    Route to add a new group
    param groupName: The name of the group (from request body)
    param members: Array of member names (from request body)
    return: The created group object with new students added
    """
    
    # Getting the request body (DO NOT MODIFY)
    group_data = request.json
    group_name = group_data.get("groupName")
    group_members = group_data.get("members")
    
    member_ids = []
    for member_name in group_members:
        existing_student = next((student for student in students if student["name"] == member_name), None)
        if existing_student:
            member_ids.append(existing_student["id"])
        else:
            new_student_id = len(students) + 1
            new_student = {
                "id": new_student_id,
                "name": member_name
            }
            students.append(new_student)
            member_ids.append(new_student_id)
    
    group_id = len(groups) + 1
    new_group = {
        "id": group_id,
        "groupName": group_name,
        "members": member_ids
    }
    
    groups.append(new_group)
    return jsonify(new_group)


@app.route('/api/groups/<int:group_id>', methods=['DELETE'])
def delete_group(group_id):
    """
    Route to delete a group by ID
    param group_id: The ID of the group to delete
    return: Empty response with status code 204
    """
    group = next((g for g in groups if g['id'] == group_id), None)
    if group is None:
        abort(404, "Group not found")
    
    groups.remove(group)
    return '', 204  # Return 204 (do not modify this line)

@app.route('/api/groups/<int:group_id>', methods=['GET'])
def get_group(group_id):
    """
    Route to get a group by ID (for fetching group members)
    param group_id: The ID of the group to retrieve
    return: The group object with member details
    """
    # TODO: (sample response below)
    group = next((g for g in groups if g['id'] == group_id), None)
    if group is None:
        abort(404, "Group not found")
    
    # Retrieve member details from the student list
    group_with_members = {
        "id": group["id"],
        "groupName": group["groupName"],
        "members": [student for student in students if student["id"] in group["members"]]
    }
    return jsonify(group_with_members)

if __name__ == '__main__':
    app.run(port=3902, debug=True)
