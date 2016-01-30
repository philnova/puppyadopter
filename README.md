# puppyadopter
Toy Flask app demonstrating CRUD operations using SQLAlchemy and WTForms

## Summary

puppyadopter is an example website built to explore CRUD concepts in Flask, the microframework for Python. It utilizes WTForms to build and validate HTML forms, then executes the correspoinding CRUD operations the user asks for using SQLAlchemy.

The site allows users to register to adopt puppies from local shelters, add new puppies to shelter databases, and edit and delete database information. puppyadopter was built as a proof-of-concept, not a product. All puppy and shelter information is fictional!

As building this site was intended to be a learning experience, I've refrained from creating any styling for the site. Admittedly, it doesn't look awesome. But then again, I'm no designer.

## Structure

puppyadopter is designed as a standard Flask application, using Flask best practices. The user can call runserver.py to host the site locally on port 8910. Then, they can use localhost to interact with the underlying database.

If loading the site for the first time, make sure to run models.py, then puppypopulator.py, to set up the database.

Views, unsurprisingly, are contained in views.py and views_wtf.py. These files are equivalent and either may be used; views_wtf.py makes use of the Flask extension WTForms for form generation and validation. views.py does this the hard way.
