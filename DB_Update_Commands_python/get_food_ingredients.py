import re
import ast

f= open("test.txt",'r',encoding='UTF-8')
f_w= open("ingredientsdb.txt",'w',encoding='UTF-8')

lines = f.readlines()
ingredients = []
for line in lines:

    for ingre in ast.literal_eval(line)["main_ingredients"]:
        if ingre[0] not in ingredients:

            ingredients.append(ingre[0])
    for ingre in ast.literal_eval(line)["sub_ingredients"]:
        if ingre[0] not in ingredients:
            ingredients.append(ingre[0])
p = re.compile(".*※.*")
for i in ingredients:
    if not p.match(i):
        print(i)
        f_w.write(i+"\n")
print(len(ingredients))

f.close()
f_w.close()