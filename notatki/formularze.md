## Forularze

1. Treść formularza
2. CRSF
3. Kapcza
4. Przesył danych pomiędzy odwiedzającym stronę a miejscem docelowym i odwrotnie, między stroną www a odbiorcą.
5. Przechwytywanie i zapisywanie danych z formularzy w bezpieczny sposób.
6. Komunikacja zwrotna w formularzach.
7. Użycie informacji przesłanych z formularza.
8. Ofensywny antywirus.
9. Formularz - wymagania wstępne, labirynty, gry itp.



### 1. Treść formularza:
#### a) Text 
#### - Ilość znaków.
#### b) Wartości specialne:
#### - URL - Czy url to url? (i czy ma perspektywę działać) i czy to nie scam
#### - Email - Czy email to email? (i czy ma perspektywę działać)
#### - Hasło - Czy hasło to hasło? (i czy ma perspektywę działać)
#### - Synchronizacja strefy czasowej 
#### c) Plik - Czy to nie szkodliwy plik? Gdzie i jak zapisywać - kwarantanna?



### 2. CSRF token / Cross-Site Request Forgery i secret_key.

Jeżeli używasz rozwiązania WTF-Forms Flask:

w pliku aplikacji (np. `app.py`) dodaj:
```
app.secret_key = '65u665urutryjtr'
```

w pliku index.html przy formularzu dodaj:
```
<form method="POST">
    {{ form.csrf_token }}
```

```
<form method="POST">
    {{ form.hidden_tag }}
```


### 3. Captcha

Captcha to metoda sprawdzająca czy formularz wypełnia prawdziwy gość.
Znana jako np. "zaznacz wszystkie obrazki zawierające samochód".

TL;DR mają znikomą moc. Powstrzymają bardzo prosty flood, ale każdy porządny bot złamie to w mniej niz sekundę. 
Napisz własny walidator który będzie w stanie ograniczyć większą część botów - np: zadaj pytanie które będzie cieżko odczytać skryptami języka naturalnego.
"Jaka była pogoda 3 dni temu w X(którego nazwa składa się z 3 kawałków do znalezienia na górze i na dole strony w <s>TYM</s> kolorze, a pozostałe w innych kolorach)".

Zobacz np. gotowy skrypt ze sprawdzeniem: w (github)[github].

### 4. Przesył danych pomiędzy odwiedzającym stronę a miejscem docelowym i odwrotnie, między stroną www a odbiorcą.
- szyfrowanie (lub nie) danych
- nienaruszalność danych
- wiarygodność źródła
- świadomość stanu powyższych

a. SSL
b. Multichannel

### 5. Przechwytywanie i zapisywanie danych z formularzy w bezpieczny sposób.

Szyfrowanie, backup, porównawacza.
Sprawdź skrypty w wieży cybersrcurity.

### 6. Komunikacja zwrotna w formularzach.

Dymki z informacją typu "Za krótkie hasło byczku.".

### 7. Użycie danych z formularza:

Nie wszystkie prawidłowo wypełnione formularze dają dobre dane.

Np. gdy ktoś wypełni pole z datą urodzenia podając inny wiek lub poda zamiast imienia inną nazwę.

Informacje z formularza, w zależności od jego zamysłu, mogą wymagać jeszcze ich przebrania przed użyciem np.:
1. Wulgaryzmy na forum gdzie chcemy dbać o kulturę wypowiedzi
2. Naruszenia regulaminu - np. oferty w dziale gdzie nie ma handlu
3. Spam na skrzynce mailowej 
4. ETC. 

Zastanów się przed jakimi wyzwaniami stoi Twój formularz i napisz walidacje które zapewnią wysoką jakość komunikacji.
Pamiętaj, że informacje w ogóle mają potencjał mylący a w dzisiejszych czasam jest możliwe aby generować je w niebotycznych ilościach.

### 8. Ofensywny antywirus.

1. Edukuj odbiorców swojego formularza.
2. 

TBD.

### 9. Formularz - wymagania wstępne, labirynty, gry itp.

Czasem, w zależności czy programujesz otwartą platformę, czy coś innego, chcesz aby formularze czy różne opcje były dosępne tylko dla niektórych.

Możesz np. wybrać aby formularz pokazał się na Twojej stronie w innej formie dla różnych sytuacji, osób, etc.

Np. 
- jeżeli ktoś nie jest zarejestrowany na innej stronie, to jego posty trafiają przed publikacją do weryfikacji
- jeżel użytkownik nie napisze 10 zweryfikowanych postów, jego wpisy są wyświetlane tylko jemu
- formularz z kontaktem na serio jest tylko w środy, w resztę dni maile idą do kosza. KMWTW.
- ITP.
























