from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime
from sqlalchemy.sql import func
from sqlalchemy import event
from sqlalchemy.orm import Session

db = SQLAlchemy()

#---------------------------------------------------------USERS-------------------------------------------------------------------
class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(345), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

#---------------------------------------------------------RESIDENTS-------------------------------------------------------------------
class Residents(db.Model):
    __tablename__ = "residents"
    r_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    r_hhid = db.Column(db.String(10), nullable=True)
    r_surname = db.Column(db.String(255), index=True, nullable=False)
    r_firstname = db.Column(db.String(255), index=True, nullable=False)
    r_midname = db.Column(db.String(255), index=True, nullable=False)
    r_suffix = db.Column(db.String(255), index=True, nullable=True)
    r_phylsysid = db.Column(db.String(50), unique=True, nullable=True)
    r_prk = db.Column(db.String(255), index=True, nullable=False)
    r_region = db.Column(db.String(255), index=True, nullable=False)
    r_city = db.Column(db.String(255), index=True, nullable=False)
    r_province = db.Column(db.String(255), index=True, nullable=False)
    r_brgy = db.Column(db.String(255), index=True, nullable=False)
    r_bdate = db.Column(db.Date, index=True, nullable=False)
    r_bplace = db.Column(db.String(255), index=True, nullable=False)
    r_gender = db.Column(db.String(255), index=True, nullable=False)
    r_civil = db.Column(db.String(255), index=True, nullable=False)
    r_religioussect = db.Column(db.String(255), index=True, nullable=False)
    r_citizenship = db.Column(db.String(255), index=True, nullable=False)
    r_occupation = db.Column(db.String(255), index=True, nullable=False)
    r_contact = db.Column(db.String(15), index=True, unique=True, nullable=False)
    r_education = db.Column(db.String(255), index=True, nullable=False)
    r_regdate = db.Column(db.Date, index=True, nullable=False, default=date.today)

#---------------------------------------------------------HOUSEHOLDS-------------------------------------------------------------------
class Households(db.Model):
    __tablename__ = 'households'
    
    household_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(50))
    house_occupancy = db.Column(db.String(50))
    lot_occupancy = db.Column(db.String(50))
    head_lname = db.Column(db.String(100))
    head_fname = db.Column(db.String(100))
    head_midname = db.Column(db.String(100))
    birth_place = db.Column(db.String(100))
    purok = db.Column(db.String(50))
    barangay = db.Column(db.String(50))
    district = db.Column(db.String(50))
    contact = db.Column(db.String(15))
    documents = db.Column(db.String(255))  # Can store image URLs or BLOB data
    hh_input_date = db.Column(db.Date, default=datetime.utcnow)

    # Relationship to household members (backref)
    members = db.relationship('HouseholdMembers', backref='household', lazy=True, cascade="all, delete-orphan")
    verifications = db.relationship('HouseholdsVerification', backref='household', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Households {self.household_id}>'

class HouseholdMembers(db.Model):
    __tablename__ = 'household_members'

    member_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    household_id = db.Column(db.Integer, db.ForeignKey('households.household_id'))
    lname = db.Column(db.String(100))
    fname = db.Column(db.String(100))
    mid_initial = db.Column(db.String(1))
    head_relation = db.Column(db.String(50))
    birth_date = db.Column(db.Date)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    civil_status = db.Column(db.String(20))
    ethnicity = db.Column(db.String(50))
    religion = db.Column(db.String(50))
    educ_attainment = db.Column(db.String(100))
    educ_status = db.Column(db.String(50))
    occupation = db.Column(db.String(100))
    monthly_income = db.Column(db.Integer)
    emplymnt_status = db.Column(db.String(50))
    pension = db.Column(db.String(50)) 
    monthly_pension = db.Column(db.Integer)
    social_security = db.Column(db.String(50))
    health_problem = db.Column(db.String(255))
    disability = db.Column(db.String(255)) 

    def __repr__(self):
        return f'<HouseholdMembers {self.member_id} of Households {self.household_id}>'

class HouseholdsVerification(db.Model):
    __tablename__ = 'households_verification'
    
    verification_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    household_id = db.Column(db.Integer, db.ForeignKey('households.household_id'))
    verifier = db.Column(db.String(100))
    status = db.Column(db.String(50))  # e.g., 'pending', 'approved'
    date_verified = db.Column(db.Date)
    description = db.Column(db.Text)

class Announcement(db.Model):
    __tablename__ = 'announcements'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    def __repr__(self):
        return f'<Announcement {self.id}>'
