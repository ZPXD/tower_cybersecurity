#### SQLincecjtion

Ten wpis jest tylko zaznaczeniemm istnienia poważnego problemu.
Wykazuje jak łatwo jest napisać dziuerawą aplikacje i tego nie zauważyć.

Wpis ten całkowicie nie wyczerpuje problemu, zagadnienie jest głębsze ... nawet przytoczone bezpieczne metody w pewnych sytuacjach mogą nie zapewnić bezpieczeństwa.

**Proste uzycie zapytania SQL w ten sposób niesie za sobą ryzyko podatności na metodę ataku SQLInjection.**

`cursor.execute("select * form users where name = %s" % request.GET['name'])`

`cursor.execute("SELECT admin FROM users WHERE username = '" + username + '");`

`cursor.execute("SELECT admin FROM users WHERE username = '%s' % username);`

`cursor.execute("SELECT admin FROM users WHERE username = '{}'".format(username));`

`cursor.execute(f"SELECT admin FROM users WHERE username = '{username}'");`

---

_Ta sama funkcjonalność ale zabezpiecznona przed prostym uzyciem SQLInjection._

`cursor.execute(model.users.__table__.select().where(model.users.name == request.GET['name']))`

`cursor.execute("SELECT admin FROM users WHERE username = %s'", (username, ));`

`cursor.execute("SELECT admin FROM users WHERE username = %(username)s", {'username': username});`

_Wskazówka:_ Unikaj czystego używania SQL, używaj ORM -> dane będą bezpieczniejsze.

Linki:

[[Solved] SQLAlchemy + SQL Injection - Local Coder](https://localcoder.org/sqlalchemy-sql-injection)

[Preventing SQL Injection Attacks With Python – Real Python](https://realpython.com/prevent-python-sql-injection/)

[SQL Injection in Python | SecureFlag Security Knowledge Base](https://knowledge-base.secureflag.com/vulnerabilities/sql_injection/sql_injection_python.html)

[SQL Injection and SQLAlchemy — Rhaptos2 User Server](https://rhaptos2user.readthedocs.io/en/latest/sqlinjection.html)
