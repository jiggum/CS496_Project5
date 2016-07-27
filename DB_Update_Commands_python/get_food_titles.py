import re
import ast
f= open("test.txt",'r',encoding='UTF-8')
f_w= open("titles.txt",'w',encoding='UTF-8')

lines = f.readlines()
titles = []
for line in lines:
    titles.append(ast.literal_eval(line)["title"])

for i in titles:
    print(i)
    f_w.write(i+"\n")
print(len(titles))

f.close()
f_w.close()