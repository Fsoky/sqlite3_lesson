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