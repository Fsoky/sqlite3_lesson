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