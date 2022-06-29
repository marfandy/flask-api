from datetime import datetime, date, timedelta
from flask import request, make_response, jsonify
from flask_restful import Resource, Api
from app.configs import SECRET_KEY, app
from models.employee import Activity, Attendance, Employee
from app.configs import db
from dependency.authbearer import TokenBearer


auth = TokenBearer()

token_required = auth.token_required
api = Api(app)


class LoginResource(Resource):
    def post(self):
        username = request.form["username"]
        password = request.form["password"]

        data = Employee.query.filter(
            Employee.username == username, Employee.password == password).first()

        if data:
            response = auth.create_token(data)
            return response

        return make_response(jsonify({"message": "User not found!"}), 400)


class LogoutResource(Resource):
    @token_required
    def post(self):
        print(auth.decode_jwt())
        user = Employee.query.filter(
            Employee.username == auth.decode_jwt()).first()

        user.login = False
        user.save()

        return make_response(jsonify({"message": "sukses logout"}), 400)


class EmployeeRegisterResource(Resource):
    def get(self):
        datas = Employee.query.all()

        response = [{"id": data.id, "name": data.name, "username": data.username, "password": data.password, "login": data.login}
                    for data in datas]

        return make_response(jsonify({"message": "success", "data": response}), 200)

    def post(self):
        name = request.form["name"]
        username = request.form["username"]
        password = request.form["password"]

        employee = Employee(name=name, username=username, password=password)
        employee.save()

        return make_response(jsonify({"message": "Inser success!"}), 202)


class EmployeeUpdateResource(Resource):
    @token_required
    def get(self, id):
        data = Employee.query.get(id)

        if data:
            response = {
                "id": data.id,
                "username": data.username,
                "name": data.name
            }

            return make_response(jsonify({"message": "success", "data": response}), 200)

        return make_response(jsonify({"message": "not found!"}), 404)

    @token_required
    def put(self, id):
        data = Employee.query.get(id)
        if data:
            username = request.form["username"]
            name = request.form["name"]

            data.username = username
            data.name = name
            data.save()

            return make_response(jsonify({"message": "update success"}), 200)
        return make_response(jsonify({"message": "not found!"}), 404)

    @token_required
    def delete(self, id):
        data = Employee.query.get(id)
        if data:
            db.session.delete(data)
            db.session.commit()
            return make_response(jsonify({"message": "delete success"}), 200)
        return make_response(jsonify({"message": "not found!"}), 404)


class AttendanceInResource(Resource):
    @token_required
    def get(self):
        datas = Attendance.query.all()

        response = [{"id": data.id, "check_in": data.check_in, "check_out": data.check_out, "person_id": data.person_id}
                    for data in datas]

        return make_response(jsonify({"message": "success", "data": response}), 200)

    @token_required
    def post(self):
        user = Employee.query.filter(
            Employee.username == auth.decode_jwt()).first()

        attendance_in = Attendance.query.filter(
            Attendance.person_id == user.id,
            Attendance.check_in != None,
            Attendance.check_out == None
        ).first()

        if attendance_in:
            return make_response(jsonify({"message": "Already checkin, not checkout yet"}), 400)

        attendace = Attendance(person_id=user.id, check_in=datetime.now())
        attendace.save()
        return make_response(jsonify({"message": "checkin success!"}), 202)


class AttendanceOutResource(Resource):
    @token_required
    def post(self):
        user = Employee.query.filter(
            Employee.username == auth.decode_jwt()).first()

        attendance_out = Attendance.query.filter(
            Attendance.person_id == user.id, Attendance.check_out == None).first()

        if not attendance_out:
            return make_response(jsonify({"message": "not checkin yet"}), 400)

        attendance_out.check_out = datetime.now()
        attendance_out.save()
        return make_response(jsonify({"message": "checkout success!"}), 202)


class ActivityResource(Resource):
    @token_required
    def get(self):
        filter_date = request.args.get("date")
        if filter_date:
            datas = Activity.query.filter(
                Activity.created_at.like(f'{filter_date}%'))
        else:
            datas = Activity.query.all()

        response = [{"id": data.id, "person_id": data.person_id, "action": data.action, "created_at": data.created_at}
                    for data in datas]

        return make_response(jsonify({"message": "success", "data": response}), 200)

    @token_required
    def post(self):
        action = request.form["action"]
        if action == None or action == "":
            return make_response(jsonify({"message": "field action is required"}), 400)

        user = Employee.query.filter(
            Employee.username == auth.decode_jwt()).first()

        attendance_in = Attendance.query.filter(
            Attendance.person_id == user.id,
            Attendance.check_in != None,
            Attendance.check_out == None
        ).first()
        if not attendance_in:
            return make_response(jsonify({"message": "not checkin yet"}), 400)

        activity = Activity(
            person_id=user.id, action=action, created_at=datetime.now())
        activity.save()
        return make_response(jsonify({"message": "Inser success!"}), 202)


class ActivityUpdateResource(Resource):
    @token_required
    def get(self, id):
        data = Activity.query.get(id)

        if data:
            response = {
                "id": data.id,
                "person_id": data.person_id,
                "action": data.action,
                "created_at": data.created_at,
            }

            return make_response(jsonify({"message": "success", "data": response}), 200)

        return make_response(jsonify({"message": "not found!"}), 404)

    @token_required
    def put(self, id):
        action = request.form["action"]
        if action == None or action == "":
            return make_response(jsonify({"message": "field action is required"}), 400)

        data = Activity.query.get(id)
        if data:
            data.action = action
            data.save()

            return make_response(jsonify({"message": "update success"}), 200)
        return make_response(jsonify({"message": "not found!"}), 404)

    @token_required
    def delete(self, id):
        data = Activity.query.get(id)
        if data:
            db.session.delete(data)
            db.session.commit()
            return make_response(jsonify({"message": "delete success"}), 200)
        return make_response(jsonify({"message": "not found!"}), 404)


api.add_resource(EmployeeRegisterResource,
                 "/api/register", methods=["GET", "POST"])
api.add_resource(EmployeeUpdateResource, "/api/user/<id>",
                 methods=["GET", "PUT", "DELETE"])

api.add_resource(AttendanceInResource, "/api/attendance-in",
                 methods=["GET", "POST"])
api.add_resource(AttendanceOutResource, "/api/attendance-out",
                 methods=["POST"])

api.add_resource(ActivityResource, "/api/activity",
                 methods=["GET", "POST"])
api.add_resource(ActivityUpdateResource, "/api/activity/<id>",
                 methods=["GET", "PUT", "DELETE"])

api.add_resource(LoginResource, "/api/login", methods=["POST"])
api.add_resource(LogoutResource, "/api/logout", methods=["POST"])

if __name__ == "__main__":
    app.run(debug=True, port=8000)
