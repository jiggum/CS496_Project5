#-*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import random
p_tag = re.compile('(<[^>]*>)|(\xa0)|\n|\t')
p_tag_e_n = re.compile('(<[^>]*>)|(\xa0)|\t')

#크롤링할 URL 수집
def collect_crowl_urls():
    f = open("baseURL.txt", 'w')
    i = 1
    while(i<=510):
        try:
            i += 1
            res = urlopen('http://terms.naver.com/list.nhn?cid=48156&categoryId=48156&page='+str(i)).read().decode('utf-8')
            soup = BeautifulSoup(res, 'html.parser')
            p = re.compile('(?<=<a class="thmb" href=")[a-zA-Z0-9/&=;?.]*(?=">)')
            p_img = re.compile('<img .* class="lazyLoadImage" .* data-src=".*(?=" onerror=)')
            p_data_src = re.compile('(?<=data-src=").*')
            print(str(i))
            page_list = p.findall(str(soup))
            img_list =list(map( lambda s : p_data_src.findall(s)[0],p_img.findall(str(soup))))
            for j in range(len(page_list)):
                f.write(page_list[j]+","+img_list[j] +"\n")
                print(page_list[j]+","+img_list[j] +"\n")

        except:
            print(str(i))
            print("-error-")

    f.close();


#네이버 음식백과페이지 크롤링
def get_recipes():
    f = open("baseURL.txt", 'r')
    lines = f.readlines()
    f_w= open("test.txt",'w',encoding='UTF-8')
    def get_recip_item_basic(sub_url):
        sub_url_list = sub_url.split(",")
        page_url = sub_url_list[0]
        img_url = sub_url_list[1]

        res = urlopen('http://terms.naver.com'+page_url).read().decode('utf-8')
        soup = BeautifulSoup(res, 'html.parser')
        temp = str(soup).strip()
        main_ingredients =""
        sub_ingredients =""
        cooking_time =""
        cooking_amount =""
        recipe =""
        title = ""
        #print(soup)


        p = re.compile('(?<=<meta content=").*(?=" property="og:title">)')
        #print(p.findall(temp))
        title = parse_title(p.findall(temp))

        p = re.compile('(?<=주재료 :).*(?=<br>|<br><strong>· 부재료 :|</p>)')
        main_ingredients = parse_main_ingredients(p.findall(temp))
        if len(main_ingredients)==0:
            p = re.compile('(?<=재료</h3>).*(?=만드는 법</h3>)',re.DOTALL)
            main_ingredients = parse_main_ingredients(p.findall(temp))
        if len(main_ingredients) == 0:
            p = re.compile('(?<=재료 및 분량</h3>).*(?=만드는 법</h3>|조리 순서</h3>)|(?<=준비 재료</h3>).*(?=만드는 법</h3>|조리 순서</h3>)', re.DOTALL)
            main_ingredients = parse_main_ingredients(p.findall(temp))
        #print(p.findall(temp))


        p = re.compile('(?<=부재료 :).*')
        #print(p.findall(temp))
        sub_ingredients = parse_sub_ingredients(p.findall(temp))

        p = re.compile('(?<=조리시간 :).*(?=<br>|</p>)')
        #print(p.findall(temp))
        cooking_time = parse_cooking_time(p.findall(temp))

        p = re.compile('(?<=분량 :).*(?=<br>|</p>)')
        #print(p.findall(temp))
        cooking_amount = parse_cooking_amount(p.findall(temp))

        p = re.compile('(?<=요리과정</h4>).*(?=<em>2.</em> 음식정보</h3>|<dt>출처</dt>)',re.DOTALL)
        recipe = parse_recipe(p.findall(temp))
        if(len(recipe)==0):
            p = re.compile('(?<=만드는 법</h3>).*(?=<div class="box_tbl">|<div class="tmp_source">)', re.DOTALL)
            recipe = parse_recipe(p.findall(temp))
        if (len(recipe) == 0):
            p = re.compile('(?<=조리 방법</h3>).*(?=<div class="box_tbl">|<div class="tmp_source">|아톱 가이드</h3>)', re.DOTALL)
            recipe = parse_recipe(p.findall(temp))
        #print(p.findall(temp))

        #print("이미지 : ", img_url.strip())
        #print("음식명 : ", title)
        #print("주재료 : ", main_ingredients)
        #print("부재료 : ", sub_ingredients)
        #print("조리시간 : " + cooking_time)
        #print("분량 : " + cooking_amount)
        #print("요리과정 : ", recipe)
        ctx = {
            'title': title,
            'img_url' : img_url.strip(),
            'main_ingredients' : main_ingredients,
            'sub_ingredients' : sub_ingredients,
            'cooking_time' :cooking_time,
            'cooking_amount' : cooking_amount,
            'recipe' : recipe,
        }
        #print("=---------------------------------------------")
        return ctx
    def parse_title(init_strs):
        result_str = ""
        if(len(init_strs)>0):
            p = re.compile('만드는.*')
            result_str = p_tag.sub("", p.sub("", init_strs[0])).strip()
        return result_str
    def parse_main_ingredients(init_strs):
        result_str = ""
        p=re.compile('.*\.\.\..*')
        for str in init_strs:
            if(p.search(str) == None):
                result_str = list(map(lambda s: s.strip() ,re.split(",|\n|또는|·",p_tag_e_n.sub("",str.split("· 부재료 :")[0]))))
        result = []
        p_sub_p = re.compile('^\(.*\)')
        p_rm = re.compile(".*\)$|.*[0-9].*|.*※.*")
        for sub_li in list(map(lambda s: re.split('(\s[0-9])|([0-9])|(½|⅓|⅔|¼|¾|⅕|⅖|⅗|⅘|⅙|⅚|⅛|⅜|⅝|⅞)|(\()|(약간)|(·)|(적당량)', p_sub_p.sub("",s)), result_str)):
            if(sub_li[0]==None or len(sub_li[0])==0):
                continue
            item = []
            p_col=re.compile(".*:")
            if(p_rm.match(p_col.sub("",sub_li[0]).strip())):
                continue
            item.append(p_col.sub("",sub_li[0]).strip())
            sub_str = ""
            for i in range(1, len(sub_li)):
                if sub_li[i] != None:
                    sub_str += sub_li[i]
            item.append(sub_str.strip())
            result.append(item)
        result = list(dict((x[0], x) for x in result).values())
        return result
    def parse_sub_ingredients(init_strs):
        result_str = ""
        p=re.compile('.*\.\.\..*')
        for str in init_strs:
            if(p.search(str) == None):
                result_str = list(map(lambda s: s.strip() ,re.split(",|\n|또는|·",p_tag.sub("",str))))
        result = []
        p_sub_p = re.compile('^\(.*\)')
        p_rm = re.compile(".*\)$|.*[0-9].*|.*※.*")
        for sub_li in list(map(lambda s: re.split('(\s[0-9])|([0-9])|(½|⅓|⅔|¼|¾|⅕|⅖|⅗|⅘|⅙|⅚|⅛|⅜|⅝|⅞)|(\()|(약간)|(·)|(적당량)', p_sub_p.sub("",s)), result_str)):
            if (sub_li[0] == None or len(sub_li[0]) == 0):
                continue
            item = []
            p_col = re.compile(".*:")
            if (p_rm.match(p_col.sub("", sub_li[0]).strip())):
                continue
            item.append(p_col.sub("", sub_li[0]).strip())
            sub_str = ""
            for i in range(1, len(sub_li)):
                if sub_li[i] != None:
                    sub_str += sub_li[i]
            item.append(sub_str.strip())
            result.append(item)
        return result
    def parse_cooking_time(init_strs):
        result_str = ""
        if(len(init_strs)>0):
            p = re.compile('</?br>.*')
            result_str = p_tag.sub("",p.sub("",init_strs[0]))
        return result_str
    def parse_cooking_amount(init_strs):
        result_str = ""
        if len(init_strs)>0:
            p = re.compile('((\s?(기준))|(</?br>)).*')
            result_str = p_tag.sub("",p.sub("",init_strs[0]))
        return result_str
    def parse_recipe(init_strs):
        result_str = ""

        if len(init_strs)>0:
            p = re.compile('(4\) 요리팁).*|(<em>2.</em> 음식정보).*',re.DOTALL)
            result_str = re.split(r'<strong>[0-9]{2}\.</strong>|((<p class="txt">|<br>)|\n|\t)+[0-9]+.\s',p.sub("",init_strs[0]))

        result_str = [y for y in map(lambda s: p_tag.sub("",s).strip(), [x for x in result_str if x!=None]) if y !=""]

        return result_str

    count = 0
    for i in range(len(lines)):
        check = False
        temp = get_recip_item_basic(lines[i])
        if(len(temp["title"])>0 and len(temp['main_ingredients'])>0 and len(temp['recipe'])>0):
            check = True
        if check:
            count+=1
        print(i , check)
        for key in temp:
            print(key+" : ",temp[key])
        print("----------------------------- : " + str(count))
        if(check):
            f_w.write(str(temp)+"\n")
    #get_recip_item_basic("/entry.nhn?docId=3406066&amp;amp;&cid=48164&categoryId=48205")
    f.close()
    f_w.close()
