
from datetime import timedelta
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
app = Flask(__name__)

# set up jwt
app.secret_key = "hfjdfhgjkdfhgjkdf865785"
jwt = JWTManager(app)

app.secret_key = "hfjdfhgjkdfhgjkdf865785"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)

# make the app an api
api = Api(app)
from views.views import MemberSignup, MemberSignin, MemberProfile, AddDependant, ViewDependants, Laboratories, LabTests
from views.views import MakeBooking
from views.views import MyBookings
from views.views import MakePayment

# confiure the views/Endpoints
api.add_resource(MemberSignup, '/api/member_signup')
api.add_resource(MemberSignin, '/api/member_signin')
api.add_resource(MemberProfile, '/api/member_profile')
api.add_resource(AddDependant, '/api/add_dependant')
api.add_resource(ViewDependants, '/api/view_dependant')
api.add_resource(Laboratories, '/api/laboratories')
api.add_resource(MakeBooking, '/api/make_booking')
api.add_resource(LabTests, '/api/lab_tests')
api.add_resource(MyBookings, '/api/my_bookings')
api.add_resource( MakePayment, '/api/ MakePayment')

# print(__name__)
from views.views_dashboard import LabSignup, LabSignin, LabProfile, AddLabTests
from views.views_dashboard import ViewLabTests,ViewLabBookings,AddNurse,ViewNurses,TaskAllocation


api.add_resource( LabSignup, '/api/lab_signup')
api.add_resource( LabSignin, '/api/lab_signin')
api.add_resource( LabProfile, '/api/lab_profile')
api.add_resource( AddLabTests, '/api/add_tests')
api.add_resource(ViewLabTests, "/api/view_lab_tests")
api.add_resource(ViewLabBookings, "/api/view_bookings")
api.add_resource(AddNurse, "/api/add_nurse")
api.add_resource(ViewNurses, "/api/view_nurses")
api.add_resource(TaskAllocation, "/api/task_allocation")




from views.view_nurse import NurseLogin,ViewAssignments,ViewInvoiceDetails
api.add_resource(NurseLogin, "/api/nurse_login")
api.add_resource(ViewAssignments, "/api/view_assignments")
api.add_resource(ViewInvoiceDetails, "/api/view_details")

if __name__ == "__main__":
    app.run(debug=True)


# make the app an api
# api = Api(app)
