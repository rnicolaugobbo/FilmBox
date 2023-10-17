import csv

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
user_name = ""
add_movie = True
show_list = True
clear_list = True
export = True

def add_comment(movie_name):
  user_input_comment = input("Write a comment about the movie: ")
  movies_and_ratings[movie_name]["comment"] = user_input_comment

def add_movie_and_rating():
  user_input_movie = input("Please type the name of a movie: ")
  if user_input_movie not in movies_and_ratings:
    movies_and_ratings[user_input_movie] = {}
  else:
    print("Movie is already on your list!")
  user_input_rating = input("Please give {} a rating from 1 to 5 stars: ".format(user_input_movie))
  while user_input_rating not in ["1", "2", "3", "4", "5"]:
    user_input_rating = input("Please type a number from 1 to 5: ")
  movies_and_ratings[user_input_movie]["rating"] = user_input_rating

  add_comment(user_input_movie)

def show_list():
  print(movies_and_ratings)

def clear_list():
  movies_and_ratings.clear()

while first_use:
  user_name = input("Please type your name: ")
  user_input_yes_no = input("Hello {}! Do you want to add your first movie to the list? (\"yes\" or \"no\"): ".format(user_name))
  user_input_yes_no.lower()
  while user_input_yes_no not in ["yes", "no"]:
    user_input_yes_no = input("Please type \"yes or \"no\": ")
  
  if user_input_yes_no == "no":
    print("Closing app...")
    exit()
  else:
    first_use = False

while is_active:
  add_movie_and_rating()
  print("Movie added to your list!")

  user_input = \
    input("Now that you have movie(s) in your list, you can: type \"1\" to see your list, type \"2\" to add another movie, type \"3\" to clear your list, \
type \"4\" to export your list as a CSV file or type \"5\" to leave the app")
  
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

      for item in movies_and_ratings:
        doc_writer.writerow(item)