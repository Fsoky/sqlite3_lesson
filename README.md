# [SQLite 3 | Как работать с базой данных в Python?](https://youtu.be/y0YWRqrhTBY)
Исходный код с ролика.


### Основные методы для работы с БД
```py
import sqlite3

with sqlite3.connect("thebest.db") as db:
	cursor = db.cursor()

	cursor.execute("""CREATE TABLE IF NOT EXISTS articles(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		author VARCHAR,
		topic VARCHAR,
		content TEXT
	)""")

	values = [
		("Фипик", "Что будет завтра?", "Всё будет хорошо, не грусти."),
		("Летта", "Хорошие новости", "У тебя всё получится!"),
		("Эрвик", "Совет дня", "Не обращай внимания на негатив!")
	]

	cursor.executemany("INSERT INTO articles(author, topic, content) VALUES(?, ?, ?)", values)

	"""
	.fetchone() - Возвращает первую, единственную запись.
	.fetchall() - Возвращает список с записями.
	.fetchmany(size) - Возвращает список записей с указаным количеством (size).
	"""

	cursor.execute("SELECT * FROM articles")
	print(cursor.fetchone())

	cursor.execute("""CREATE TABLE IF NOT EXISTS email(
		`from` VARCHAR,
		`to` VARCHAR,
		subject VARCHAR,
		content TEXT
	)""")

	cursor.execute("INSERT INTO email VALUES('Фсоки', 'Зритель', 'Фантастический денёк', 'Знай, ты самый лучший!')")

	for data in cursor.execute("SELECT * FROM email"):
		print(f"\nОт: {data[0]}\nКому: {data[1]}\nТема: {data[2]}\nСообщение: {data[3]}")
```

### Регистрация/авторизация и казино
```py
import sqlite3
import hashlib
import random


def md5sum(value):
	return hashlib.md5(value.encode()).hexdigest()


with sqlite3.connect("database.db") as db:
	cursor = db.cursor()

	query = """
	CREATE TABLE IF NOT EXISTS users(
		id INTEGER PRIMARY KEY,
		name VARCHAR(30),
		age INTEGER(3),
		sex INTEGER NOT NULL DEFAULT 1,
		balance INTEGER NOT NULL DEFAULT 2000,
		login VARCHAR(15),
		password VARCHAR(20)
	);
	CREATE TABLE IF NOT EXISTS casino(
		name VARCHAR(50),
		description TEXT(300),
		balance BIGINT NOT NULL DEFAULT 10000
	)
	"""

	cursor.executescript(query)


def registration():
	name = input("Name: ")
	age = int(input("Age: "))
	sex = int(input("Sex: "))
	login = input("Login: ")
	password = input("Password: ")

	try:
		db = sqlite3.connect("database.db")
		cursor = db.cursor()

		db.create_function("md5", 1, md5sum)

		cursor.execute("SELECT login FROM users WHERE login = ?", [login])
		if cursor.fetchone() is None:
			values = [name, age, sex, login, password]

			cursor.execute("INSERT INTO users(name, age, sex, login, password) VALUES(?, ?, ?, ?, md5(?))", values)
			db.commit()
		else:
			print("Такой логин уже существует!")
			registration()
	except sqlite3.Error as e:
		print("Error", e)
	finally:
		cursor.close()
		db.close()


def log_in():
	login = input("Login: ")
	password = input("Password: ")

	try:
		db = sqlite3.connect("database.db")
		cursor = db.cursor()

		db.create_function("md5", 1, md5sum)

		cursor.execute("SELECT login FROM users WHERE login = ?", [login])
		if cursor.fetchone() is None:
			print("Такого логина не существует!")
		else:
			cursor.execute("SELECT password FROM users WHERE login = ? AND password = md5(?)", [login, password])
			if cursor.fetchone() is None:
				print("Пароль неверный!")
			else:
				play_casino(login)
	except sqlite3.Error as e:
		print("Error", e)
	finally:
		cursor.close()
		db.close()


def play_casino(login):
	print("\nCASINO 🥰😳")

	try:
		db = sqlite3.connect("database.db")
		cursor = db.cursor()

		cursor.execute("SELECT age FROM users WHERE login = ? AND age >= ?", [login, 18])
		if cursor.fetchone() is None:
			print("Вам недостаточно лет!")
		else:
			bet = int(input("Bet: "))
			number = random.randint(1, 100)

			balance = cursor.execute("SELECT balance FROM users WHERE login = ?", [login]).fetchone()[0]
			if balance < bet:
				print("Недостаточно средств, гуляй работать! 😉💖")
			elif balance <= 0:
				print("Недостаточно средств, гуляй работать! 😉💖")
			else:
				if number < 50:
					cursor.execute("UPDATE users SET balance = balance - ? WHERE login = ?", [bet, login])
					cursor.execute("UPDATE casino SET balance = balance + ?", [bet])

					print("You lose! ❤")
				else:
					cursor.execute("UPDATE users SET balance = balance + ? WHERE login = ?", [bet, login])
					cursor.execute("UPDATE casino SET balance = balance - ?", [bet])

					print("You win! 😉😳")

				db.commit()
				play_casino(login)
	except sqlite3.Error as e:
		print("Error", e)
	finally:
		cursor.close()
		db.close()


registration()
log_in()
```

### Работа с изображениями в SQLite 3
```py
import sqlite3
import io

from PIL import Image

with sqlite3.connect("users-avatar.db") as db:
	cursor = db.cursor()
	cursor.row_factory = sqlite3.Row

	cursor.execute("CREATE TABLE avatars(photo BLOB)")

	with open("clover.png", "rb") as file:
		cursor.execute("INSERT INTO avatars VALUES(?)", [file.read()])

	data = cursor.execute("SELECT photo FROM avatars").fetchone()["photo"]
	img = Image.open(io.BytesIO(data))
	img.show()
```
