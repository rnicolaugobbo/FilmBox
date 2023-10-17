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
user_name = ""

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
  movies_and_ratings[user_input_movie]["rating"] = user_input_rating

  add_comment(user_input_movie)

def show_list():
  print(movies_and_ratings)

while first_use:
  user_name = input("Please type your name: ")
  user_input_yes_no = input("Hello {}! Do you want to add your first movie to the list? (\"yes\" or \"no\"): ".format(user_name))
  while user_input_yes_no not in ["yes", "no"]:
    user_input_yes_no = input("Please type \"yes or \"no\": ")
  first_use = False

while is_active:
  add_movie_and_rating()
  print("Movie added to your list!")

  