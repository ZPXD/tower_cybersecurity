import pytz
import random

from flask import Flask, session, render_template

import flask_wtf
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField #, ...
from wtforms.validators import DataRequired #, ...



'''
Panuj nad formularzami:
1. Najważniejsze pola.
2. Najważniejsze sprawdzenia czy pole jest wypełnione spoko.


ZPXD, Łukasz Pintal.
'''




app = Flask(__name__)
app.secret_key = 'abcd'

@app.route('/', methods=['POST', 'GET'])
@app.route('/some_page_with_form', methods=['POST', 'GET'])
def some_page_with_form():
	
	form_level_1 = Form_level_1()
	if form_level_1.validate_on_submit():
		return redirect(url_for('index'))

	form_level_2 = Form_level_2()
	original = form_level_2.add_three_strings()
	if form_level_2.validate_on_submit() and original == form_level_2.check_city.data:
		return redirect(url_for('index'))

	return render_template('index.html', form=form_level_2)
	

# Liczby
from wtforms import DecimalField
from wtforms import DecimalRangeField
from wtforms import FloatField
from wtforms import IntegerField

# Zakres.
from wtforms import IntegerRangeField
from wtforms import RadioField

# Wybór.
from wtforms import BooleanField
from wtforms import SelectMultipleField
from wtforms import SelectFieldBase

# Przesłanie.
from wtforms import FileField
from wtforms import MultipleFileField

# Ok.
from wtforms import SubmitField

# 
from wtforms import Field
from wtforms import Label
from wtforms import FieldList
from wtforms import FormField
from wtforms import HiddenField
from wtforms import Flags
from wtforms import TelField

# Sprawdzanie formularza.
from wtforms.validators import DataRequired
from wtforms.validators import InputRequired
from wtforms.validators import Length
from wtforms.validators import Email


class Form_level_1(FlaskForm):

	# 1. Tekstowe:
	from wtforms import TextAreaField
	from wtforms import StringField
	tekst_krotki = StringField()
	tekst_dlugi = StringField()
	tekst_wieloliniowy = TextAreaField()

	# 2. Tekstowe specjalne:
	from wtforms import URLField
	from wtforms import SearchField
	from wtforms import EmailField
	from wtforms import PasswordField
	link_www = URLField()
	wyszukiwanie = SearchField()
	email = EmailField()
	haslo = PasswordField()
	haslo_drugi_raz = None

	# 3. Wybór
	
	# Wybór A/B - "Checkbox".
	# from wtforms.fields import BooleanField
	# wybor_ab = BooleanField()

	# Pojedyńczy wybór z listy.

	# Wielorkotny wybór z listy.

	# 4. Prześlij plik

	# 5. Czas i data.         
	from wtforms import DateField  # '%Y-%m-%d'
	from wtforms import DateTimeField  # '%Y-%m-%d %H:%M:%S'
	from wtforms import DateTimeLocalField  # '%Y-%m-%d %H:%M:%S' 
	from wtforms import TimeField # '%H:%M'
	data = DateTimeField()
	data_goscia = DateTimeLocalField()
	dzien = DateField()
	godzina = TimeField()
	# Wybór 1 pozycji z listy.


	# Przycisk:
	ok = SubmitField('ok')


class Form_level_2(FlaskForm):

	telefon = None

	# 2. Botoogarniacze.
	add_three_strings = 
	NAPISZ_INNE_SPRAWDZENIE = StringField()

	# Przycisk:
	ok = SubmitField('ok')


	def add_three_strings(self):
		'''
		Function creates three parts oft field.

		returns: original city name.
		'''
		def cities_names():
			timezones = pytz.all_timezones
			cities = [c.split('/')[1] for c in timezones if 'Europe/' in c]
			return cities

		cities = cities_names()
		one = random.choice(cities)
		a, b = '', ''
		for i, char in enumerate(one):
			if i > len(one)/2:
				a += char
			else:
				b += char
		name_parts = [a, b[:-1], b[-1]]
		random.shuffle(name_parts)
		session['a'] = name_parts[0]
		session['b'] = name_parts[1]
		session['c'] = name_parts[2]
		return one



if __name__ == '__main__':
	app.run()
