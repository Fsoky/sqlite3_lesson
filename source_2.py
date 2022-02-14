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