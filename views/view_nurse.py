import pymysql
from flask_restful import *
from flask import * 
from functions import *
import pymysql.cursors

# import JWT packages
from flask_jwt_extended import create_access_token, jwt_required,create_refresh_token

class NurseLogin(Resource):
    def post(self):
        json = request.json
        username = json['surname']
        password = json['password']
        sql = "select * from nurses where username = %s"
        connection = pymysql.connect(host='localhost',
                                    user='root',
                                    password='1234qwerty',
                                    database='medilab')
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, username)
        count = cursor.rowcount
        if count == 0:
            return jsonify({'message': 'username does not exist'})
        else:
            nurse = cursor.fetchone()
            hashed_password = nurse['password']
            
            if hash_verify(password, hashed_password):
                   # TODO WEB Tokens
                    access_token = create_access_token(identity=username,
                                                    fresh=True)
                    refresh_token = create_refresh_token(username)

                    return jsonify({'message': nurse,
                                 'access_token': access_token,
                                 'refresh_token': refresh_token})
            
            else:
                 return jsonify({'message': 'Login failed'})


class ViewAssignments(Resource):
     def post(self):
          json = request.json
          nurse_id = json['nurse_id']
          flag = json['flag']
          sql = "select * from nurse_lab_allocations where nurse_id = %s and flag = %s"
          connection = pymysql.connect(host='localhost',
                                    user='root',
                                    password='1234qwerty',
                                    database='medilab')
          cursor = connection.cursor(pymysql.cursors.DictCursor)
          cursor.execute(sql, (nurse_id, flag))
          count = cursor.rowcount
          if count == 0:
            message = "No {} Assignments".format(flag)
            return jsonify({'message': 'Assignment does not exist'})
          else:
            data = cursor.fetchall()
            return jsonify({'message': data})



class ViewInvoiceDetails(Resource):
    @jwt_required(fresh=True) # Refresh token
    def post(self):
          json = request.json
          invoice_no = json['invoice_no']
          sql = "select * from bookings where invoice_no = %s"
          connection = pymysql.connect(host='localhost',
                                    user='root',
                                    password='1234qwerty',
                                    database='medilab')
          cursor = connection.cursor(pymysql.cursors.DictCursor)
          cursor.execute(sql, invoice_no)
          count = cursor.rowcount
          if count == 0:
            message = "Invoice No {} Does not exist".format(invoice_no)
            return jsonify({'message': message})
          else:
            bookings = cursor.fetchall()
            import json
            jsonStr = json.dumps(bookings, indent=1, sort_keys=True, default=str) 
              # then convert json string to json object
            return json.loads(jsonStr) 


class ChangePass(Resource):
    def post(self):
        json = request.json
        nurse_id = json['nurse_id']
        current_password = json['current_password']
        new_password = json['new_password']
        confirm_password = json['confirm_password']
        sql = ''''''
