import pymysql
from flask_restful import *
from flask import * 
from functions import *
import pymysql.cursors

# import JWT packages
from flask_jwt_extended import create_access_token, jwt_required,create_refresh_token
from flask_jwt_extended import get_jwt


# Member Signup
class MemberSignup(Resource):
    def post(self):
        # Connect to Mysql
        json = request.json
        surname = json['surname']
        others = json['others']
        gender = json['gender']
        email = json['email']
        phone = json['phone']
        dob = json['dob']
        password = json['password']
        location_id = json['location_id']

        # validate password
        response = passwordvalidity(password)
        if response ==True:
            if check_phone(phone):
                connection = pymysql.connect(host='localhost',
                                             user='root',
                                             password='1234qwerty',
                                             database='medilab')
                cursor = connection.cursor()
                sql = ''' Insert into members(surname, others, gender, email, phone, dob, password, location_id)
                values(%s,%s,%s,%s,%s,%s,%s,%s)'''
                # provide data
                data = (surname, others, gender, encrypt(email), encrypt(phone), dob, hash_password(password),
                         location_id)
                try:
                    cursor.execute(sql, data)
                    connection.commit()
                    # send sms/email
                    code = gen_random()
                    send_sms(phone, '''Thank you for joining Medilab. Your secret code: {}. Do not share. '''.
                                format(code))
                    return jsonify({'message': 'Successfully Registered'})
                except:
                    connection.rollback()
                    return jsonify({'message': 'Failed. Try Again'})

                pass
            else:
                return jsonify({'message': 'Invalid phone +254'})
           

        else:
            return jsonify({'message': response})
        
class MemberSignin(Resource):
    def post(self):
        json = request.json
        surname = json['surname']
        password = json['password']
        # user enters a plain text email
        sql = "select * from members where surname = %s"
        

        connection = pymysql.connect(host='localhost',
                                             user='root',
                                             password='1234qwerty',
                                             database='medilab')
        
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, surname)
        count = cursor.rowcount
        if count == 0:
              return jsonify({'message': 'User does not exist'})
        else:
            member = cursor.fetchone()
            hashed_password = member['password']   # This pssword is hashed
            # Jane provided a plain password
            if hash_verify(password, hashed_password):
                 # TODO JSON WEB Tokens

                access_token = create_access_token(identity=surname,
                                                   fresh=True)
                refresh_token = create_refresh_token(surname)

                return jsonify({'message': member,
                                 'access_token': access_token,
                                 'refresh_token': refresh_token})
            
            else:
                 return jsonify({'message': 'Login failed'})
            

class MemberProfile(Resource):
    @jwt_required(fresh=True) # Refresh token
    def post(self):
        json = request.json
        member_id = json['member_id']
        sql = "select * from members where member_id = %s"
        connection = pymysql.connect(host='localhost',
                                             user='root',
                                             password='1234qwerty',
                                             database='medilab')
        
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, member_id)
        count = cursor.rowcount
        if count == 0:
            return jsonify({'message': 'Member does not exist'})
        else:
            member = cursor.fetchone()
            return jsonify({'message': member})
        
class AddDependant(Resource):
    def post(self):
        # Connect to Mysql
        json = request.json
        member_id = json['member_id']
        surname = json['surname']
        others = json['others']
        dob = json['dob']

        connection = pymysql.connect(host='localhost',
                                             user='root',
                                             password='1234qwerty',
                                             database='medilab')
        
        cursor = connection.cursor()
        sql = ''' Insert into dependants(member_id,surname, others, dob)values(%s,%s,%s,%s)'''
        data = (member_id,surname, others, dob)
        try:
            cursor.execute(sql, data)
            connection.commit()
            return jsonify({'message': 'Dependant Added'})
        except:
            connection.rollback()
            return jsonify({'message': 'Failed. Try again'})
        
class ViewDependants(Resource):
    def post(self):
          json = request.json
          member_id = json['member_id']
          sql = "select * from dependants where member_id = %s"
          connection = pymysql.connect(host='localhost',
                                              user='root',
                                             password='1234qwerty',
                                             database='medilab')
          cursor = connection.cursor(pymysql.cursors.DictCursor)
          cursor.execute(sql, member_id)
          count = cursor.rowcount
          if count == 0:
              return jsonify({'message': 'Member does not exist'})
          else:
              dependants = cursor.fetchall()
              return jsonify({'message': 'dependants'})
          
        
        
        
class Laboratories (Resource):
    def get(self):
        sql = "select * from laboratories"
        connection = pymysql.connect(host='localhost',
                                              user='root',
                                             password='1234qwerty',
                                             database='medilab')
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        count = cursor.rowcount
        if count == 0:
            return jsonify({'message': 'No laboratories'})
        else:
            laboratories = cursor.fetchall()
            return jsonify(laboratories)
    
class LabTests(Resource):
        def post(self):
            json = request.json
            lab_id = json['lab_id']
            connection = pymysql.connect(host='localhost',
                                              user='root',
                                             password='1234qwerty',
                                             database='medilab')
            sql = 'select * from lab_tests where lab_id = %s'
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql, lab_id)
            count = cursor.rowcount
            if count == 0:
                return jsonify({'message': 'No lab tests found'})
            else:
                lab_tests = cursor.fetchall()
                return jsonify(lab_tests)
            

class MakeBooking(Resource):
    def post(self):
        json = request.json
        member_id = json['member_id']
        booked_for = json['booked_for']
        dependant_id = json['dependant_id']
        test_id = json['test_id']
        appointment_date = json['appointment_date']
        appointment_time = json['appointment_time']
        where_taken = json['where_taken']
        latitude = json['latitude']
        longitude = json['longitude']
        lab_id = json['lab_id']
        invoice_no = json['invoice_no']


        connection = pymysql.connect(host='localhost',
                                            user='root',
                                            password='1234qwerty',
                                            database='medilab')
        cursor = connection.cursor()
        sql = ''' Insert into bookings(member_id,booked_for, dependant_id,test_id, appointment_date,
            appointment_time, where_taken, latitude,longitude, lab_id, invoice_no )
            values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) '''
        data = (member_id,booked_for, dependant_id,test_id, appointment_date,
            appointment_time, where_taken, latitude,longitude, lab_id, invoice_no)
        # try:
        cursor.execute(sql, data)
        connection.commit()
        # Get Member phone No
        sql = '''select * from members where member_id = %s'''
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, member_id)
        member = cursor.fetchone()
        phone = member['phone']
        send_sms(decrypt(phone), "Booking Scheduled on {} at {} : Invoice No. {} "
        .format(appointment_date, appointment_time, invoice_no))
        return jsonify({'message': 'Booking Received. '})
           
        # except:
        #     connection.rollback()
        #     return jsonify({'message': 'Booking Failed'})


class MyBookings(Resource):
    @jwt_required(refresh=True)
    def _init_(self):
        self.sql = "select * from bookings where member_id = %s"
        self.connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='1234qwerty',
                                     database='medilab')

        cursor = self.connection.cursor(pymysql.cursors.DictCursor)

    def get(self):
        json = request.json
        member_id = json['member_id']
        self.cursor.execute(self.sql, member_id)
        count = self.cursor.rowcount
        if count == 0:
            return jsonify({'message': 'No Bookings'})
        else:
            bookings = self.cursor.fetchall()

            import json
            jsonStr = json.dumps(bookings, indent=1, sort_keys=True,
                                 default=str)
            return json.loads(jsonStr)
        


class MakePayment(Resource):
    def post(self):
        json = request.json
        phone = json['phone']
        amount = json['amount']
        invoice_no = json['invoice_no']
        # Access Mpesa Functions locatated in functions.py
        mpesa_payment(amount, phone, invoice_no)
        return jsonify({'message': 'Sent - Complete Payment on Your Phone.'})