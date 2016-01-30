#from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from puppyadopter import app

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from puppyadopter.models import Base, Shelter, Puppy, Owner, PuppyProfiles

import datetime

#app = Flask(__name__)

engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def mainPage():
	return render_template('mainpage.html')

@app.route('/shelters/')
def viewAllShelters():
	shelters = session.query(Shelter).all()
	return render_template('allshelters.html',shelters = shelters)

@app.route('/owners/')
def viewAllOwners():
	owners = session.query(Owner).all()
	owner_dict = {owner.name: [str(i.name) for i in session.query(Puppy).filter(Puppy.owners.contains(owner)).all()] for owner in owners}
	return render_template('allowners.html',owner_dict=owner_dict)

@app.route('/register/', methods=['GET', 'POST'])
def registerOwner():
	if request.method == 'POST':
		owner = Owner(name = request.form['name'])
		session.add(owner)
		session.commit()
		flash('Registered {0} as a new owner!'.format(owner.name))
		return redirect(url_for('mainPage'))
	else:
		return render_template('registerowner.html')

@app.route('/shelters/<int:shelter_id>/')
def viewOneShelter(shelter_id):
	shelter = session.query(Shelter).filter_by(id = shelter_id).one()
	puppies = session.query(Puppy).filter_by(shelter_id = shelter_id).all()
	if has_more_room(shelter):
		message = 'This shelter is accepting more puppies!'
	else:
		message = 'Sorry, we cannot accept more puppies!'
	return render_template('shelter.html', message = message, shelter = shelter, puppies = puppies)

@app.route('/shelters/<int:shelter_id>/puppies/<int:puppy_id>/')
def viewOnePuppy(shelter_id, puppy_id):
	shelter = session.query(Shelter).filter_by(id = shelter_id).one()
	puppy = session.query(Puppy).filter_by(id = puppy_id).one()
	return render_template('puppy.html', shelter = shelter, puppy = puppy)

@app.route('/shelters/<int:shelter_id>/new/',methods=['GET','POST'])
def newPuppy(shelter_id):
	shelter = session.query(Shelter).filter_by(id=shelter_id).one()
	if request.method == 'POST':
		if int(shelter.current_occupancy) < int(shelter.maximum_capacity):
			date = format_date(request.form['birth'])
			newPup = Puppy(name = str(request.form['name']), dateOfBirth = date,gender= str(request.form['gender']), weight=request.form['weight'], shelter_id = shelter_id)
			session.add(newPup)
			shelter.current_occupancy += 1
			session.add(shelter)
			session.commit()
			flash("New Puppy Added to {0}!".format(shelter.name))
		else:
			flash("Sorry, this shelter is full!")
		return redirect(url_for('viewOneShelter',shelter_id = shelter_id))
	else:
		return render_template('newpuppy.html',shelter=shelter)

def format_date(datestring):
	dateList = datestring.split('-')
	date = datetime.date(int(dateList[0]), int(dateList[1]), int(dateList[2]))
	return date

def has_more_room(shelter):
	if int(shelter.current_occupancy) < int(shelter.maximum_capacity):
		return True
	return False

@app.route('/shelters/<int:shelter_id>/puppies/<int:puppy_id>/edit/',methods=['GET','POST'])
def editPuppy(shelter_id, puppy_id):
	puppy = session.query(Puppy).filter_by(id = puppy_id).one()
	shelter = session.query(Shelter).filter_by(id = shelter_id).one()
	if request.method == 'POST':
		puppy.dateOfBirth = format_date(request.form['birth'])
		puppy.name = str(request.form['name'])
		puppy.gender= str(request.form['gender'])
		puppy.weight=request.form['weight']
		session.add(puppy)
		session.commit()
		flash("Puppy Edited: {0}".format(puppy.name))
		return redirect(url_for('viewOneShelter',shelter_id=shelter_id))
	else:
		return render_template('editpuppy.html',shelter_id=shelter_id,puppy = puppy)


@app.route('/shelters/<int:shelter_id>/puppies/<int:puppy_id>/delete/',methods=['GET','POST'])
def deletePuppy(shelter_id, puppy_id):
	puppy = session.query(Puppy).filter_by(id = puppy_id).one()
	shelter = session.query(Shelter).filter_by(id = shelter_id).one()
	if request.method == 'POST':
		puppy_name = puppy.name
		shelter.current_occupancy -= 1
		session.add(shelter)
		session.delete(puppy)
		session.commit()
		flash("Puppy Deleted: {0}".format(puppy_name))
		return redirect(url_for('viewOneShelter',shelter_id=shelter_id))
	else:
		return render_template('deletepuppy.html',shelter_id=shelter_id,puppy_id = puppy_id,puppy_name = puppy.name, shelter_name = shelter.name)

    

@app.route('/shelters/<int:shelter_id>/puppies/<int:puppy_id>/adopt/',methods=['GET','POST'])
def adoptPuppy(shelter_id, puppy_id):
	puppy = session.query(Puppy).filter_by(id = puppy_id).one()
	shelter = session.query(Shelter).filter_by(id = shelter_id).one()
	owner_list = session.query(Owner).all()
	if request.method == 'POST':
		new_owners = request.form.getlist('possible_owner')
		if new_owners:
			adopter_list = []
			for o_id in new_owners:
				o = session.query(Owner).filter_by(id = o_id).one()
				puppy.owners.append(o)
				adopter_list.append(str(o.name))
			shelter.current_occupancy -= 1
			session.add(shelter)
			session.add(puppy)
			session.commit()
			flash("Puppy {0} Adopted to {1}".format(puppy.name, adopter_list))
		return redirect(url_for('viewOneShelter',shelter_id=shelter_id))
	else:
		return render_template('adoptpuppy.html',shelter_id=shelter_id,puppy_id = puppy_id,puppy = puppy, owner_list = owner_list)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key' # gives us access to the session to flash messages
    app.debug = True
    app.run(host='0.0.0.0', port=5000)