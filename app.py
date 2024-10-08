from datetime import datetime
import os
from pprint import pp
from flask import Flask, request, jsonify, send_from_directory, session
import flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS, cross_origin
from flask_session import Session
import werkzeug
from config import ApplicationConfig
from models import Announcement, HouseholdMembers, Households, HouseholdsVerification, db, User, Residents
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from werkzeug.utils import secure_filename
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import json
import uuid
from werkzeug.security import generate_password_hash


app = Flask(__name__)

app.config.from_object(ApplicationConfig)
app.config['JWT_SECRET_KEY'] = 'QWERTYUIOP741852963123456789'  # This sets the secret key properly
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/btrrs'  # Example database config

bcrypt = Bcrypt(app)
CORS(app, supports_credentials=True)
server_session = Session(app)
db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

ma = Marshmallow(app)

#---------------------------------------------------------RESIDENTS_CRUD-------------------------------------------------------------------
class ResidentSchema(ma.Schema):
    class Meta:
        fields = (
            'r_id',
            'r_surname',
            'r_firstname',
            'r_midname',
            'r_suffix',
            'r_hhid',
            'r_phylsysid',
            'r_prk',
            'r_region',
            'r_city',
            'r_province',
            'r_brgy',
            'r_bdate',
            'r_bplace',
            'r_gender',
            'r_civil',
            'r_religioussect',
            'r_citizenship',
            'r_occupation',
            'r_contact',
            'r_education',
            'r_regdate'
            )
resident_schema = ResidentSchema()
residents_schema = ResidentSchema(many=True)

@app.route('/residents', methods=['GET'])       
def residents_list():
    all_residents = Residents.query.all()
    results = residents_schema.dump(all_residents)
    return jsonify(results)

@app.route('/resident_details/<r_id>', methods=['GET'])
def resident_details(r_id): 
    resident = Residents.query.get(r_id)
    return resident_schema.jsonify(resident)

@app.route('/update_resident/<r_id>', methods=['PUT'])
def update_resident(r_id):
    resident = Residents.query.get(r_id)

    r_surname = request.json['r_surname']
    r_firstname = request.json['r_firstname']
    r_midname = request.json['r_midname']
    r_suffix = request.json['r_suffix']
    r_hhid = request.json['r_hhid']
    r_phylsysid = request.json['r_phylsysid']
    r_prk = request.json['r_prk']
    r_region = request.json['r_region']
    r_city = request.json['r_city']
    r_province = request.json['r_province']
    r_brgy = request.json['r_brgy']
    r_bdate = request.json['r_bdate']
    r_bplace = request.json['r_bplace']
    r_gender = request.json['r_gender']
    r_civil = request.json['r_civil']
    r_religioussect = request.json['r_religioussect']
    r_citizenship = request.json['r_citizenship']
    r_occupation = request.json['r_occupation']
    r_contact = request.json['r_contact']
    r_education = request.json['r_education']
    r_regdate = request.json['r_regdate']

    resident.r_surname = r_surname
    resident.r_firstname = r_firstname
    resident.r_midname = r_midname
    resident.r_suffix = r_suffix
    resident.r_hhid = r_hhid
    resident.r_phylsysid = r_phylsysid
    resident.r_prk = r_prk
    resident.r_region = r_region
    resident.r_city = r_city
    resident.r_province = r_province
    resident.r_brgy = r_brgy
    resident.r_bdate = r_bdate
    resident.r_bplace = r_bplace
    resident.r_gender = r_gender
    resident.r_civil = r_civil
    resident.r_religioussect = r_religioussect
    resident.r_citizenship = r_citizenship
    resident.r_occupation = r_occupation
    resident.r_contact = r_contact
    resident.r_education = r_education
    resident.r_regdate = r_regdate

    db.session.commit()
    return resident_schema.jsonify(resident)

@app.route('/delete_resident/<r_id>', methods=['DELETE'])
def delete_resident(r_id):
    resident = Residents.query.get(r_id)
    db.session.delete(resident)
    db.session.commit()
    return resident_schema.jsonify(resident)

@app.route('/add_resident', methods=['POST'])
def add_resident():
    r_surname = request.json['r_surname']
    r_firstname = request.json['r_firstname']
    r_midname = request.json['r_midname']
    r_suffix = request.json['r_suffix']
    r_hhid = request.json['r_hhid']
    r_phylsysid = request.json['r_phylsysid']
    r_prk = request.json['r_prk']
    r_region = request.json['r_region']
    r_city = request.json['r_city']
    r_province = request.json['r_province']
    r_brgy = request.json['r_brgy']
    r_bdate = request.json['r_bdate']
    r_bplace = request.json['r_bplace']
    r_gender = request.json['r_gender']
    r_civil = request.json['r_civil']
    r_religioussect = request.json['r_religioussect']
    r_citizenship = request.json['r_citizenship']
    r_occupation = request.json['r_occupation']
    r_contact = request.json['r_contact']
    r_education = request.json['r_education']
    r_regdate = request.json['r_regdate']

    print(r_surname)
    print(r_firstname)
    print(r_midname)
    print(r_suffix)
    print(r_hhid)
    print(r_phylsysid)
    print(r_prk)
    print(r_region)
    print(r_city)
    print(r_province)
    print(r_brgy)
    print(r_bdate)
    print(r_bplace)
    print(r_gender)
    print(r_civil)
    print(r_religioussect)
    print(r_citizenship)
    print(r_occupation)
    print(r_contact)
    print(r_education)
    print(r_regdate)

    residents = Residents(
        r_surname=r_surname,
        r_firstname=r_firstname,
        r_midname=r_midname,
        r_suffix=r_suffix,
        r_hhid=r_hhid,
        r_phylsysid=r_phylsysid,
        r_prk=r_prk,
        r_region=r_region,
        r_city=r_city,
        r_province=r_province,
        r_brgy=r_brgy,
        r_bdate=r_bdate,
        r_bplace=r_bplace,
        r_gender=r_gender,
        r_civil=r_civil,
        r_religioussect=r_religioussect,
        r_citizenship=r_citizenship,
        r_occupation=r_occupation,
        r_contact=r_contact,
        r_education=r_education,
        r_regdate=r_regdate
    )

    db.session.add(residents)
    db.session.commit()
    return resident_schema.jsonify(residents)

#---------------------------------------------------------HOUSEHOLDS-------------------------------------------------------------------

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/add_household', methods=['POST'])
def add_household():
    data = request.form
    files = request.files

    document_paths = {}
    for doc in ['barangay_cert', 'medical_cert', 'no_income_cert', 'employment_cert', 'valid_id']:
        if doc in files:
            file = files[doc]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                
                try:
                    file.save(file_path)
                    document_paths[doc] = unique_filename  # Save the unique filename
                    print(f"Saved {doc} to {file_path}")
                    print("Document Paths:", document_paths)
                except Exception as e:
                    return jsonify({'error': f'Failed to save {doc}: {str(e)}'}), 500

    try:
        new_household = Households(
            category=data['category'],
            house_occupancy=data['house_occupancy'],
            lot_occupancy=data['lot_occupancy'],
            head_lname=data['head_lname'],
            head_fname=data['head_fname'],
            head_midname=data.get('head_midname'),
            birth_place=data.get('birth_place'),
            purok=data.get('purok'),
            barangay=data.get('barangay'),
            district=data.get('district'),
            contact=data.get('contact'),
            documents=json.dumps(document_paths),  # Store file names as a JSON string
            hh_input_date=data.get('hh_input_date', datetime.utcnow().date())
        )

        db.session.add(new_household)
        db.session.commit()

        household_id = new_household.household_id

        new_verification = HouseholdsVerification(
            household=new_household,
            verifier='To be assigned',
            status='Pending',
            date_verified=None,
            description='Initial verification pending'
        )
        db.session.add(new_verification)
        db.session.commit()

        return jsonify({'message': 'Household and related records added successfully', 'household_id': household_id}), 201

    except Exception as e:
        return jsonify({'error': f'Failed to add household: {str(e)}'}), 500
    
@app.route('/uploads/<filename>', methods=['GET'])
@cross_origin()  # Allow this specific route to handle cross-origin requests
def uploaded_file(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        return jsonify({'error': f'File not found: {str(e)}'}), 404



@app.route('/add_members', methods=['POST'])
def add_members():
    data = request.get_json()  # Get JSON data from request

    if not isinstance(data, list):
        return jsonify({'error': 'Request body must be a list of members'}), 400

    for member_data in data:
        household_id = member_data.get('household_id')
        if not household_id:
            return jsonify({'error': 'Missing household_id in member data'}), 400

        # Ensure the household exists
        household = Households.query.get(household_id)
        if not household:
            return jsonify({'error': f'Household with id {household_id} does not exist'}), 404

        new_member = HouseholdMembers(
            household_id=household_id,
            lname=member_data.get('lname'),
            fname=member_data.get('fname'),
            mid_initial=member_data.get('mid_initial'),
            head_relation=member_data.get('head_relation'),
            birth_date=member_data.get('birth_date'),
            age=member_data.get('age'),
            gender=member_data.get('gender'),
            civil_status=member_data.get('civil_status'),
            ethnicity=member_data.get('ethnicity'),
            religion=member_data.get('religion'),
            educ_attainment=member_data.get('educ_attainment'),
            educ_status=member_data.get('educ_status'),
            occupation=member_data.get('occupation'),
            monthly_income=member_data.get('monthly_income'),
            emplymnt_status=member_data.get('emplymnt_status'),
            pension=member_data.get('pension'),
            monthly_pension=member_data.get('monthly_pension'),
            social_security=member_data.get('social_security'),
            health_problem=member_data.get('health_problem'),
            disability=member_data.get('disability')
        )

        db.session.add(new_member)

    db.session.commit()

    return jsonify({'message': 'Members added successfully'}), 201

@app.route('/add_verifications', methods=['POST'])
def add_verifications():
    data = request.get_json()  # Get JSON data from request

    if not isinstance(data, list):
        return jsonify({'error': 'Request body must be a list of verifications'}), 400

    for verification_data in data:
        household_id = verification_data.get('household_id')
        if not household_id:
            return jsonify({'error': 'Missing household_id in verification data'}), 400

        # Ensure the household exists
        household = Households.query.get(household_id)
        if not household:
            return jsonify({'error': f'Household with id {household_id} does not exist'}), 404

        new_verification = HouseholdsVerification(
            household_id=household_id,
            verifier=verification_data.get('verifier'),
            status=verification_data.get('status'),
            date_verified=verification_data.get('date_verified'),
            description=verification_data.get('description')
        )

        db.session.add(new_verification)

    db.session.commit()

    return jsonify({'message': 'Verifications added successfully'}), 201

@app.route('/get_household/<int:household_id>', methods=['GET'])
def get_household(household_id):
    # Retrieve the household by ID
    household = Households.query.get(household_id)
    if not household:
        return jsonify({'error': f'Household with id {household_id} not found'}), 404

    # Serialize the household data
    household_data = {
        'household_id': household.household_id,
        'category': household.category,
        'house_occupancy': household.house_occupancy,
        'lot_occupancy': household.lot_occupancy,
        'head_lname': household.head_lname,
        'head_fname': household.head_fname,
        'head_midname': household.head_midname,
        'birth_place': household.birth_place,
        'purok': household.purok,
        'barangay': household.barangay,
        'district': household.district,
        'contact': household.contact,
        'documents': household.documents,
        'hh_input_date': household.hh_input_date.isoformat() if household.hh_input_date else None,
        'members': [
            {
                'member_id': member.member_id,
                'lname': member.lname,
                'fname': member.fname,
                'mid_initial': member.mid_initial,
                'head_relation': member.head_relation,
                'birth_date': member.birth_date.isoformat() if member.birth_date else None,
                'age': member.age,
                'gender': member.gender,
                'civil_status': member.civil_status,
                'ethnicity': member.ethnicity,
                'religion': member.religion,
                'educ_attainment': member.educ_attainment,
                'educ_status': member.educ_status,
                'occupation': member.occupation,
                'monthly_income': member.monthly_income,
                'emplymnt_status': member.emplymnt_status,
                'pension': member.pension,
                'monthly_pension': member.monthly_pension,
                'social_security': member.social_security,
                'health_problem': member.health_problem,
                'disability': member.disability
            }
            for member in household.members
        ],
        'verifications': [
            {
                'verification_id': verification.verification_id,
                'verifier': verification.verifier,
                'status': verification.status,
                'date_verified': verification.date_verified.isoformat() if verification.date_verified else None,
                'description': verification.description
            }
            for verification in household.verifications
        ]
    }

    return jsonify(household_data), 200


@app.route('/update_household/<int:household_id>', methods=['PUT'])
def update_household(household_id):
    data = request.get_json()
    
    # Find the household by ID
    household = Households.query.get(household_id)
    if not household:
        return jsonify({'error': f'Household with id {household_id} not found'}), 404
    
    # Update household fields
    if 'category' in data:
        household.category = data['category']
    if 'house_occupancy' in data:
        household.house_occupancy = data['house_occupancy']
    if 'lot_occupancy' in data:
        household.lot_occupancy = data['lot_occupancy']
    if 'head_lname' in data:
        household.head_lname = data['head_lname']
    if 'head_fname' in data:
        household.head_fname = data['head_fname']
    if 'head_midname' in data:
        household.head_midname = data['head_midname']
    if 'birth_place' in data:
        household.birth_place = data['birth_place']
    if 'purok' in data:
        household.purok = data['purok']
    if 'barangay' in data:
        household.barangay = data['barangay']
    if 'district' in data:
        household.district = data['district']
    if 'contact' in data:
        household.contact = data['contact']
    if 'documents' in data:
        household.documents = data['documents']
    if 'hh_input_date' in data:
        household.hh_input_date = datetime.strptime(data['hh_input_date'], '%Y-%m-%d').date()

    db.session.commit()
    return jsonify({'message': 'Household updated successfully'}), 200

@app.route('/update_member/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    data = request.get_json()

    # Find the member by ID
    member = HouseholdMembers.query.get(member_id)
    if not member:
        return jsonify({'error': f'Member with id {member_id} not found'}), 404

    # Update member fields
    if 'household_id' in data:
        member.household_id = data['household_id']
    if 'lname' in data:
        member.lname = data['lname']
    if 'fname' in data:
        member.fname = data['fname']
    if 'mid_initial' in data:
        member.mid_initial = data['mid_initial']
    if 'head_relation' in data:
        member.head_relation = data['head_relation']
    if 'birth_date' in data:
        member.birth_date = datetime.strptime(data['birth_date'], '%Y-%m-%d').date()
    if 'age' in data:
        member.age = data['age']
    if 'gender' in data:
        member.gender = data['gender']
    if 'civil_status' in data:
        member.civil_status = data['civil_status']
    if 'ethnicity' in data:
        member.ethnicity = data['ethnicity']
    if 'religion' in data:
        member.religion = data['religion']
    if 'educ_attainment' in data:
        member.educ_attainment = data['educ_attainment']
    if 'educ_status' in data:
        member.educ_status = data['educ_status']
    if 'occupation' in data:
        member.occupation = data['occupation']
    if 'monthly_income' in data:
        member.monthly_income = data['monthly_income']
    if 'emplymnt_status' in data:
        member.emplymnt_status = data['emplymnt_status']
    if 'pension' in data:
        member.pension = data['pension']
    if 'monthly_pension' in data:
        member.monthly_pension = data['monthly_pension']
    if 'social_security' in data:
        member.social_security = data['social_security']
    if 'health_problem' in data:
        member.health_problem = data['health_problem']
    if 'disability' in data:
        member.disability = data['disability']

    db.session.commit()
    return jsonify({'message': 'Member updated successfully'}), 200

@app.route('/update_verification/<int:household_id>', methods=['PUT'])
def update_verification(household_id):
    data = request.get_json()

    # Find the verification by household_id
    verification = HouseholdsVerification.query.filter_by(household_id=household_id).first()
    if not verification:
        return jsonify({'error': f'Verification record for household with id {household_id} not found'}), 404

    # Update verification fields
    if 'verifier' in data:
        verification.verifier = data['verifier']
    if 'status' in data:
        verification.status = data['status']
    if 'date_verified' in data:
        verification.date_verified = datetime.strptime(data['date_verified'], '%Y-%m-%d').date()
    if 'description' in data:
        verification.description = data['description']

    db.session.commit()
    return jsonify({'message': 'Verification updated successfully'}), 200

@app.route('/delete_member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    # Find the member by ID
    member = HouseholdMembers.query.get(member_id)
    if not member:
        return jsonify({'error': f'Member with id {member_id} not found'}), 404

    # Delete the member record
    db.session.delete(member)
    db.session.commit()

    return jsonify({'message': 'Member deleted successfully'}), 200


@app.route('/delete_household/<int:household_id>', methods=['DELETE'])
def delete_household(household_id):
    # Find the household by ID
    household = Households.query.get(household_id)
    if not household:
        return jsonify({'error': f'Household with id {household_id} not found'}), 404

    # Delete the household record
    db.session.delete(household)
    db.session.commit()

    return jsonify({'message': 'Household and related records deleted successfully'}), 200

@app.route('/households_list', methods=['GET'])
def households_list():
    households = Households.query.all()
    households_data = [
        {
            'household_id': household.household_id,
            'category': household.category,
            'house_occupancy': household.house_occupancy,
            'lot_occupancy': household.lot_occupancy,
            'head_lname': household.head_lname,
            'head_fname': household.head_fname,
            'head_midname': household.head_midname,
            'birth_place': household.birth_place,
            'purok': household.purok,
            'barangay': household.barangay,
            'district': household.district,
            'contact': household.contact,
            'documents': household.documents,
            'hh_input_date': household.hh_input_date.isoformat() if household.hh_input_date else None
        }
        for household in households
    ]
    return jsonify(households_data), 200



#---------------------------------------------------------AUTHENTICATION-------------------------------------------------------------------
@app.route("/@me")
def get_current_user():
    try:
        user_id = session.get("user_id")

        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401

        user = User.query.filter_by(id=user_id).first()

        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify({
            "email": user.email,
            "full_name": user.full_name
        }), 200

    except Exception as e:
        print(f"Error fetching current user: {e}")  # Log the error
        return jsonify({"error": "Internal server error"}), 500

@app.route("/register", methods=["POST"])
def register_user():
    full_name = request.json["full_name"]
    email = request.json["email"]
    password = request.json["password"]

    user_exists = User.query.filter_by(email=email).first() is not None

    if user_exists:
        return jsonify({"error": "User already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(full_name=full_name, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    session["user_id"] = new_user.id

    return jsonify({
        "id": new_user.id,
        "full_name": new_user.full_name,
        "email": new_user.email
    })

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')  # Use 'email' here
    password = request.json.get('password')

    user = User.query.filter_by(email=email).first()  # Check by email
    if user and bcrypt.check_password_hash(user.password, password):  # Verify hashed password
        session["user_id"] = user.id  # Optional: Store user ID in session
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200

    return jsonify({"error": "Bad credentials"}), 401



@app.route("/logout", methods=["POST"])
def logout_user():
    session.pop("user_id", None)  # Provide default value to avoid KeyError
    return jsonify({"message": "Logged out successfully"}), 200



#------------------------------------------------------------------------------------------------------#
@app.route('/announcementad', methods=['GET', 'POST'])
def manage_announcements():
    if request.method == 'POST':
        data = request.json
        title = data.get('title')
        content = data.get('content')  # Updated to 'content'

        # Error handling for missing data
        if not title or not content:
            return jsonify({"error": "Title and content are required"}), 400

        # Create a new announcement
        new_announcement = Announcement(title=title, description=content)  # Use 'content'
        db.session.add(new_announcement)
        db.session.commit()

        # Return the created announcement details
        return jsonify({
            'id': new_announcement.id,
            'title': new_announcement.title,
            'content': new_announcement.description  # Updated to 'content'
        }), 201

    if request.method == 'GET':
        # Get all announcements
        announcements = Announcement.query.all()
        return jsonify([{
            'id': announcement.id,
            'title': announcement.title,
            'content': announcement.description  # Updated to 'content'
        } for announcement in announcements]), 200

@app.route('/announcementad/<int:id>', methods=['GET'])
def get_announcement(id):
    # Get a specific announcement by ID
    announcement = Announcement.query.get(id)
    if announcement:
        return jsonify({
            'id': announcement.id,
            'title': announcement.title,
            'content': announcement.description  # Updated to 'content'
        }), 200
    return jsonify({"error": "Announcement not found"}), 404

@app.route('/announcementad/<int:id>', methods=['PUT'])
def update_announcement(id):
    data = request.json
    title = data.get('title')
    content = data.get('content')  # Updated to 'content'

    # Error handling for missing data
    if not title or not content:
        return jsonify({"error": "Title and content are required"}), 400

    # Find the announcement by ID
    announcement = Announcement.query.get(id)

    if not announcement:
        return jsonify({"error": "Announcement not found"}), 404

    # Update the announcement's title and description
    announcement.title = title
    announcement.description = content  # Updated to 'content'
    db.session.commit()

    # Return the updated announcement details
    return jsonify({
        'id': announcement.id,
        'title': announcement.title,
        'content': announcement.description  # Updated to 'content'
    }), 200

if __name__ == "__main__":
    app.run(debug=True)
