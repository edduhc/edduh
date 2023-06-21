import pymysql
from flask_restful import *
from flask import * 
from functions import *
import pymysql.cursors

# import JWT packages
from flask_jwt_extended import create_access_token, jwt_required,create_refresh_token

class LabSignup(Resource):
    def post(self):
        # Connect to Mysql
        json = request.json
        lab_name = json['lab_name']
        permit_id = json['parmit_id']
        email = json['email']
        phone = json['phone']
        password = json['password']

        # check password
        response = passwordvalidity(password)
        if response:
            if check_phone(phone):
                connection = pymysql.connect(host='localhost',
                                             user='root',
                                             password='1234qwerty',
                                             database='medilab')
                cursor = connection.cursor()
                sql = ''' Insert into laboratories(lab_name, permit_id, email, phone, password)
                values(%s,%s,%s,%s,%s)'''

                # Data
                data = (lab_name, permit_id, email, encrypt(phone), hash_password(password))
                try:
                    cursor.execute(sql, data)
                    connection.commit()
                    code = gen_random()
                    send_sms(phone, '''Thank you for joining Medilab. Your secret code: {}. Do not share. '''.
                                format(code))
                    return jsonify({'message': 'Successfully Registered'})
                   
                except:
                    connection.rollback()
                    return jsonify({'message': 'Registration Failed'})
                
            else:
                return jsonify({'message': 'Invalid phone +254'})
           

        else:
            return jsonify({'message': response})
        
class LabSignin(Resource):
    def post(self):
        json = request.json
        email = json['email']
        password = json['password']
        
        sql = "select * from laboratories where email = %s"
        connection = pymysql.connect(host='localhost',
                                             user='root',
                                             password='1234qwerty',
                                             database='medilab')
        
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, email)
        count = cursor.rowcount
        if count == 0:
            return jsonify({'message': 'Email does not exist'})
        else:
            lab = cursor.fetchone()
            hashed_password = lab['password']
            # verify
            if hash_verify(password, hashed_password):
                   # TODO WEB Tokens
                    access_token = create_access_token(identity=email,
                                                    fresh=True)
                    refresh_token = create_refresh_token(email)

                    return jsonify({'message': lab,
                                 'access_token': access_token,
                                 'refresh_token': refresh_token})
            
            else:
                 return jsonify({'message': 'Login failed'})
            

class LabProfile(Resource):
    @jwt_required(fresh=True) # Refresh token
    def post(self):
        json = request.json
        lab_id = json['lab_id']
        sql = "select * from laboratories where lab_id = %s"
        connection = pymysql.connect(host='localhost',
                                             user='root',
                                             password='1234qwerty',
                                             database='medilab')
        
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, lab_id)
        count = cursor.rowcount
        if count == 0:
            return jsonify({'message': 'Lab does not exist'})
        else:
            lab = cursor.fetchone()
            return jsonify({'message': lab})
        

class AddLabTests(Resource):
    def post(self):
        json = request.json
        lab_id = json['lab_id']
        test_name = json['test_name']
        test_description = json['test_description']
        test_cost = json['test_cost']
        test_discount = json['test_discount']
        availability = json['availability']
        more_info = json['more_info']

        connection = pymysql.connect(host='localhost',
                                             user='root',
                                             password='1234qwerty',
                                             database='medilab')
        
        cursor = connection.cursor()

        sql = '''Insert into lab_tests(lab_id,test_name, test_description, test_cost,test_discount,availability,
          more_info)values(%s,%s,%s,%s,%s,%s,%s)'''
        
        # data
        data = (lab_id,test_name, test_description, test_cost,test_discount,availability,
          more_info)
        # try:
        cursor.execute(sql, data)
        connection.commit()
        return jsonify({'message': 'Test Added'})
               
        # except:
            # connection.rollback()
            # return jsonify({'message': 'Test not added'})


      

class ViewLabTests(Resource):
     @jwt_required(refresh=True) #Refresh Token
     def post(self):
          json = request.json
          lab_id = json['lab_id']
          sql = "select * from lab_tests where lab_id = %s"
            

          connection = pymysql.connect(host='localhost',
                                             user='root',
                                             password='1234qwerty',
                                             database='medilab')
          cursor = connection.cursor(pymysql.cursors.DictCursor)
          cursor.execute(sql,lab_id)
          count = cursor.rowcount
          if count == 0:
               return jsonify({'message': 'No Test found'})
          else:
               tests = cursor.fetchall()
               return jsonify(tests)            


        

class ViewLabBookings(Resource):
     @jwt_required(refresh=True) #Refresh Token
     def post(self):
          json = request.json
          lab_id = json['lab_id']
          sql = "select * from bookings where lab_id = %s"
            

          connection = pymysql.connect(host='localhost',
                                             user='root',
                                             password='1234qwerty',
                                             database='medilab')
          cursor = connection.cursor(pymysql.cursors.DictCursor)
          cursor.execute(sql,lab_id)
          count = cursor.rowcount
          if count == 0:
               return jsonify({'message': 'No Bookings'})
          else:
               bookings = cursor.fetchall()
               for booking in bookings:
                    member_id = booking['member_id']
                    sql = '''select * from members where member_id = %s'''
                    cursor = connection.cursor(pymysql.cursors.DictCursor)
                    cursor.execute(sql, member_id)
                    member = cursor.fetchone()
                    booking['key'] = member


               import json
               jsonStr = json.dumps(bookings, indent=1 , sort_keys=True, default=str)
               # then convert json string to json object
               return json.loads(jsonStr)



class AddNurse(Resource):
    def post(self):
        json = request.json
        lab_id = json['lab_id']
        username = json['surname']
        others = json['others']
        gender = json['gender']
        email = json['email']
        phone = json['phone']
        password = gen_random(5)

        connection = pymysql.connect(host='localhost',
                                             user='root',
                                             password='1234qwerty',
                                             database='medilab')
        
        cursor = connection.cursor()

        sql = '''Insert into nurses(lab_id,username, others, gender,email,phone,password)values
        (%s,%s,%s,%s,%s,%s,%s)'''
        
        # data
        data = (lab_id, username, others, gender,email,encrypt(phone),hash_password(password))
        # try:
        try:
           cursor.execute(sql, data)
           connection.commit()
        
           send_sms(phone, '''Thank you for joining Medilab. Log in to Nurse App. Your OTP: Username{}.
           Do not share. '''.format(password, username))
           return jsonify({'message': 'Nurse Added'})
        except:
            connection.rollback()
            return jsonify({'message': 'Failed. Try again'})


class ViewNurses(Resource):
     @jwt_required(refresh=True) #Refresh Token
     def post(self):
          json = request.json
          lab_id = json['lab_id']
          sql = "select * from lab_tests where lab_id = %s"
            

          connection = pymysql.connect(host='localhost',
                                             user='root',
                                             password='1234qwerty',
                                             database='medilab')
          cursor = connection.cursor(pymysql.cursors.DictCursor)
          cursor.execute(sql,lab_id)
          count = cursor.rowcount
          if count == 0:
               return jsonify({'message': 'No Nurses found'})
          else:
               nurses = cursor.fetchall()
               return jsonify(nurses) 


class TaskAllocation(Resource):
    def post(self):
        json = request.json
        nurse_id = json['nurse_id']
        invoice_no = json['invoice_no']

        # check if above invoice is active
        sql = '''select * from nurse_lab_allocations where invoice_no = %s'''
        connection = pymysql.connect(host='localhost',
                                             user='root',
                                             password='1234qwerty',
                                             database='medilab')
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, (invoice_no))
        count = cursor.rowcount
        # if its found active, find the nurse allocated
        if count == 0:
            # Invoice does not exist in that table
            sql3 = '''insert into nurse_lab_allocation(nurse_id, invoice_no)values(%s,%s)'''
            cursor3 = connection.cursor()
            data = (nurse_id, invoice_no)
            cursor3.execute(sql3, data)
            connection.commit()
            # could we send an sms to this nurse?
            # yes, use nurse_id to get the phone, decrypt it
            # send text
            # use android push notifications - firebase
            return jsonify({'message': 'Allocation successful'})
        else:
             # Its found, what is the flag holding
            task = cursor.fetchone
            flag = task['flag']

            if flag == 'Active':
                # task = cursor.fetchone()
                # Below ID belongs to current nurse allocated
                current_nurse_id = task['nurse_id']
                # Query nurse table and get the nurse details
                sql2 = '''select * from nurses where nurse_id = %s'''
                cursor2 = connection.cursor(pymysql.cursors.DictCursor)
                cursor2.execute(sql2, current_nurse_id)
                # get nurse details
                nurse = cursor2.fetchone()
                surname = nurse['surname']
                others = nurse['others']
                message = '''Failed. Invioce No: {} Already Allocated to {} {}'''.format(invoice_no, surname, others)
                return jsonify({'message': message})
        
            elif flag == 'completed':
                return jsonify({'message': 'Completed'})
            
            elif flag == 'inactive':
                return jsonify({'message': 'inactive'})


