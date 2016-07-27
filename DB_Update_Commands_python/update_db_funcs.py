from pymongo import MongoClient
import ast
client = MongoClient()
client = MongoClient("mongodb://127.0.0.1:27019")
db = client.recipe

def update_recipes_to_DB():
    f= open("recipdb.txt",'r',encoding='UTF-8')

    foods = f.readlines()



    for i in range(len(foods)):
        temp = ast.literal_eval(foods[i])
        temp['rank'] = i
        db.foods.insert_one(temp)
        print(i)



    f.close()

def update_food_title_to_DB():
    f= open("ingredientsdb.txt",'r',encoding='UTF-8')

    ingredients = f.readlines()
    for i in range(len(ingredients)):
        temp = {
            'title':ingredients[i].strip()
        }
        db.ingredients.insert_one(temp)
        print(i)



    f.close()
