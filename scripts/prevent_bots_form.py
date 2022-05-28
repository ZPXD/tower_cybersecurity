'''

Formularze: odsiewanie botów  (Alternatywa dla Captcha*)


tym skryptem zwiększysz sznasę że informacje które,
zbierasz z formularza pochodzą od gości którzy są prawdziwi.

Alternatywa dla Captcha* - czyli dla zadania typu znajdź 3 obrazki które X albo odczytaj tekst ze zdjęcia - lepiej napisane boty ominą popularną wersję Captcha w mgnieniu oka.

W skrypcie aplikacji:
1. Biblioteki.
2. Fragment formularza (Flask WTF) z polem i funkcją tworzącą zadanie (napisz własne).
3. Pozwól przesłać informacje np. tylko gdy ktoś dobrze rozwiązał zadanie sprawdzajace.

W skrypcie HTML:
4. Elementy odpowiedzi na zadanie sprawdzające, czy gościmy raczej użytkownika niż bota: A i B (lub więcej).
5. Cześć formularza w której można odpowiedzieć na zadanie sprawdzające.


Skrypt będzie jeszcze sporo rozwijany, o to pytaj na spotkaniach wieży cybersecurity.


ZPXD, Łukasz Pintal.
'''



# 1. Biblioteki.
import pytz
import random
from flask import Flask, session, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField #, ...
from wtforms.validators import DataRequired #, ...


# 2. Fragment formularza (Flask WTF) z polem i funkcją tworzącą zadanie (napisz własne).

class YourForm(FlaskForm):
	check_city = StringField()
	NAPISZ_INNE_SPRAWDZENIE = StringField()
	ok = SubmitField('ok')

	def add_three_strings(self):
		'''
		Function creates three parts of city name in session 
		in random order
		to combine in check_city form field.

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

	def NAPISZ_INNE_SPRAWDZENIE():
		# Napisz inne sprawdzenie.
		#
		# Coś co będzie trudno ogarnąć maszynowo, np:
		# 1. Losuj miasto i jaka jest tam pogoda + check googlem tego
		# 2. Jaka jest w tym momencie 1 litera nagłówka na stronie gazety X? # pokazuj potem jak faktycznie była, bo może ktoś ma inne searche a nie wie
		# 3. Ile dni temu padał deszcz? # 
		# 4. Podaj dzień tygodnia słownie. (proste pytania rozbij na 2 cześci, aby wykluczyć część rozwiązań NLP)
		# 5. ...
		pass


# 3. Pozwól przesłać informacje np. tylko gdy ktoś dobrze rozwiązał zadanie sprawdzajace.
#    (Tylko fragment 2 linie ze środka).

app = Flask(__name__)
app.secret_key = 'abcd'
@app.route('/', methods=['POST', 'GET'])
@app.route('/some_page_with_form', methods=['POST', 'GET'])
def some_page_with_form():
	form = YourForm()


	# Sprawdź rozwiązanie ------------------------------------------------
	original = form.add_three_strings()
	if form.validate_on_submit() and original == form.check_city.data:
		# ----------------------------------------------------------------

		# Dalsza część formularza.
		return redirect(url_for('index'))
	return render_template('some_page_with_form.html', form=form)



# 4. Elementy odpowiedzi na zadanie sprawdzenia, czy gościmy raczej użytkownika niż bota:

# Na górze strony z formularzem umieść:
a = '''
<p>{{session['a']}}</p>
'''

# Na dole strony z fromularzem umieść:
b = '''
<p>{{session['b']}}</p>
'''

# Na dole, na górze lub w innym miejscu strony z fromularzem umieść jeszcze: 
c = '''
<p>{{session['c']}}</p>
'''


# 5. Cześć formularza w której można odpowiedzieć na zadanie sprawdzające.

# Wewnątrz formularza FlaskForm umieść:
form_flask_html = '''
<p>Połącz w całość trzy kawałki nazwy - jedna jest na samej górze a druga na samym dole tej strony a trzecia to sam napisz gdzie.</p>
<form method="post">
	{# Reszta formularza #}
	{{form.check_city}}
	{# Lub: #}
	{{form.NAPISZ_INNE_SPRAWDZENIE}}
	{# Reszta formularza #}
</form>
'''

# Lub 

# Wewnątrz formularza HTML (ale dodaj wtedy walidator w skrypcie py) umieść:
form_html = '''
<p>Połącz w całość trzy kawałki nazwy - jedna jest na samej górze a druga na samym dole tej strony.</p>
<form method="post">
    <!-- Reszta formularza -->
    <input name="check_city" id="check_city" required>
    <!-- Lub: -->
    <input name="NAPISZ_INNE_SPRAWDZENIE" id="NAPISZ_INNE_SPRAWDZENIE" required>
    <!-- Reszta formularza -->
</form>
'''





if __name__ == '__main__':
    app.run()
