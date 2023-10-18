import csv
import sqlite3

print("""
  ______ _ _           ____            
 |  ____(_) |         |  _ \           
 | |__   _| |_ __ ___ | |_) | _____  __
 |  __| | | | '_ ` _ \|  _ < / _ \ \/ /
 | |    | | | | | | | | |_) | (_) >  < 
 |_|    |_|_|_| |_| |_|____/ \___/_/\_\
                                       
                                       
""")
print("Welcome to FilmBox!")
print("With this app, you can add movies to a list and give them ratings and commnets!")
movies_and_ratings = {}
first_use = True
is_active = True
user_input_yes_no = ""
user_input = ""

def initialize_db():
  conn = sqlite3.connect("filmbox.db")
  cursor = conn.cursor()

  cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE
        )
    """)
  
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            title TEXT,
            rating INTEGER,
            comment TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
  
  conn.commit()
  return conn, cursor

conn, cursor = initialize_db()

def get_or_create_user(user_name):
  cursor.execute("SELECT id FROM users WHERE name = ?", (user_name,))
  user_id = cursor.fetchone()
  if user_id:
    print(f"Welcome back, {user_name}")
    return user_id[0], False
  else:
    cursor.execute("INSERT INTO users (name) VALUES (?)", (user_name,))
    return cursor.lastrowid, True

def load_movies_from_db():
  cursor.execute("SELECT title, rating, comment FROM movies WHERE user_id = ?", (user_id,))
  for row in cursor.fetchall():
    title, rating, comment = row
    movies_and_ratings[title] = {'rating': str(rating), 'comment': comment}

user_name = input("Please type your name: ")
user_id, is_new_user = get_or_create_user(user_name)

load_movies_from_db()

def add_comment(movie_name):
  user_input_comment = input("Write a comment about the movie: ")
  return user_input_comment

def save_movie_to_db(movie_name, rating, comment):
  cursor.execute("INSERT INTO movies (user_id, title, rating, comment) VALUES (?, ?, ?, ?)", (user_id, movie_name, rating, comment))
  conn.commit()

def add_movie_and_rating():
  while True:
    user_input_movie = input("Please type the name of a movie: ")
    if user_input_movie not in movies_and_ratings:
      break
    else:
      print("Movie is already on your list!")

  movies_and_ratings[user_input_movie] = {}

  user_input_rating = input("Please give {} a rating from 1 to 5 stars: ".format(user_input_movie))
  while user_input_rating not in ["1", "2", "3", "4", "5"]:
    user_input_rating = input("Please type a number from 1 to 5: ")
  movies_and_ratings[user_input_movie]["rating"] = user_input_rating
  
  comment = add_comment(user_input_movie)

  movies_and_ratings[user_input_movie]["comment"] = comment

  save_movie_to_db(user_input_movie, user_input_rating, comment)

  cursor.execute("INSERT OR REPLACE INTO movies (title, rating, comment) VALUES (?, ?, ?)", (user_input_movie, user_input_rating, comment))

  conn.commit()

def show_list():
  if not movies_and_ratings:
    print("Your movie list is empty!")
    return
  
  print("Movies in your list:")
  print("-" * 20)
  for movie_name, details in movies_and_ratings.items():
    print("Ttile:" + str(movie_name))
    print("Rating:", "★" * int(details["rating"]))
    print("Comment:", details.get("comment", "No comment provided."))
    print("-" * 20)

def clear_list():
  user_confirmation = input("Are you sure you want to clear your list? This action is not unduable! (\"yes\" or \"no\"): ")
  while user_confirmation.lower() not in ["yes", "no"]:
    user_confirmation = input("Please type \"yes\" or \"no\": ")
  if user_confirmation == "yes":
    movies_and_ratings.clear()
    cursor.execute("DELETE FROM movies")
  else:
    return "Action cancelled."

def add_first_movie():
  user_input_yes_no = input("Hello {}! Do you want to add your first movie to the list? (\"yes\" or \"no\"): ".format(user_name))
  user_input_yes_no.lower()
  while user_input_yes_no not in ["yes", "no"]:
    user_input_yes_no = input("Please type \"yes or \"no\": ")
  if user_input_yes_no == "no":
    print("Closing app...")
    exit()
  else:
    add_movie_and_rating()
    print("Movie added to your list!")

def main_menu():
  global is_new_user
  while True:
    if not movies_and_ratings and not is_new_user:
      print("Your movie list is empty!")
      add_first_movie()
      continue
    elif is_new_user:
      add_first_movie()
      is_new_user = False
      continue
    user_input = \
              input("Now that you have movie(s) in your list, you can: type \"1\" to see your list, type \"2\" to add another movie, type \"3\" to clear your list, \
type \"4\" to export your list as a CSV file or type \"5\" to leave the app: ")
    
    if user_input == "1":
      show_list()
    elif user_input == "2":
      add_movie_and_rating()
      print("Movie added to your list!")
    elif user_input == "3":
      clear_list()
    elif user_input == "4":
      fields = ["Film", "Rating", "Comment"]

      with open("films_rating_and_comments.csv", "w") as films_csv:
        doc_writer = csv.DictWriter(films_csv, fieldnames=fields)
        doc_writer.writeheader()

        for movie_name, details in movies_and_ratings.items():
          row_data = {"Film": movie_name, "Rating": details["rating"], "Comment": details["comment"]}
          doc_writer.writerow(row_data)
        print("Exporing your list as a CSV file...")
    elif user_input == "5":
      conn.close()
      print("Closing App...")
      exit()

main_menu()