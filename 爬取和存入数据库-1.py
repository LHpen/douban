#导入包
import pymysql
import bs4
import requests
import re

#连接数据库
con =pymysql.connect(
    host="localhost",
    user="root",
    password="123456",
    db="movie",
    port=3306,
    use_unicode=True,
    charset="utf8"
)
#获取游标
cursor= con.cursor()



#请求网页
try:
    for i in range(0,50,25): #设置爬取的数量
        url = "https://movie.douban.com/top250?start={}&filter=".format(int(i))
        #设置请求头,如被封登录cookies来防止反爬
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }
        cookies = {
            'cookie': 'bid=e0-x-JMRWJU; gr_user_id=bd38a54d-f6f6-4581-812f-54bee18e6e68; _vwo_uuid_v2=D1F2B905DD84D187F0D39F9BE9CE73CCF|5eda4d43fa74ef681618d5014f9e22fc; douban-fav-remind=1; ll="108120"; viewed="30269348_30233991_3117898_26801374_3350010_1200840"; __utmc=30149280; __utmc=223695111; push_noty_num=0; push_doumail_num=0; __utmv=30149280.16039; __gads=ID=e971665a65e6f278:T=1560449519:S=ALNI_MZFS2WmZ5wrSiyS2cJmR9EfvjSDcQ; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1560500086%2C%22https%3A%2F%2Fopen.weixin.qq.com%2Fconnect%2Fqrconnect%3Fappid%3Dwxd9c1c6bbd5d59980%26redirect_uri%3Dhttps%253A%252F%252Fwww.douban.com%252Faccounts%252Fconnect%252Fwechat%252Fcallback%26response_type%3Dcode%26scope%3Dsnsapi_login%26state%3De0-x-JMRWJU%252523douban-web%252523https%25253A%252F%252Fmovie.douban.com%252Fsubject%252F1292052%252F%22%5D; _pk_ses.100001.4cf6=*; __utma=30149280.480877306.1535095302.1560452363.1560500086.28; __utmz=30149280.1560500086.28.27.utmcsr=open.weixin.qq.com|utmccn=(referral)|utmcmd=referral|utmcct=/connect/qrconnect; __utma=223695111.950917169.1560444124.1560453128.1560500086.4; __utmb=223695111.0.10.1560500086; __utmz=223695111.1560500086.4.3.utmcsr=open.weixin.qq.com|utmccn=(referral)|utmcmd=referral|utmcct=/connect/qrconnect; dbcl2="160397319:6ZpeKtCEwyQ"; ck=BBAp; douban-profile-remind=1; __utmt=1; __utmb=30149280.3.9.1560504224467; _pk_id.100001.4cf6=7991e268f9aa4410.1560444124.4.1560504237.1560453472.'
        }

        #请求URL
        req = requests.get(url, headers=headers, cookies=cookies)
        req.encoding='utf-8'

        #提取指定数据
        contents=req.text
        # print(contents)
        soup = bs4.BeautifulSoup(contents, "lxml")
        for tag in soup.find_all('div',class_='info'):
            #电影名称
            name = tag.find('span',class_='title').get_text()
            #评分
            rating_score = float(tag.find('span', class_='rating_num').get_text())

            people = tag.find('div', class_="star")
            span = people.findAll('span')
            #评价
            peoplecount = span[3].contents[0]
            #URL
            url = tag.find('a').get('href')


            #进入URL提取内容

            req = requests.get(url)
            # print(req)
            req.encoding = "utf-8"
            contents = req.text
            soup = bs4.BeautifulSoup(contents, "html.parser")
            for tag2 in soup.find_all('div', id='info'):

                m_countrylist = re.findall("<span class=\"pl\">制片国家/地区:</span>(.*)<br/>",str(tag2))
                m_propertylist = re.findall("<span property=\"v:genre\">(.*?)</span>",str(tag2))

                #提取内容
                countrylist = m_countrylist[0].split('/')
                m_country = ""
                for i in countrylist:
                    j = i.strip()
                    m_country = m_country + "," + j
                # 制片国家/地区
                m_country = m_country.strip(",")
                #类型
                m_property = ','.join(m_propertylist)

                #提取豆瓣评分
            for tag3 in soup.find_all('div', class_='rating_wrap clearbox'):
                stars = re.findall("<span class=\"rating_per\">(.*)</span>",str(tag3))
                #五星
                five = stars[0]
                #四星
                four = stars[1]
                #三星
                three = stars[2]
                #两星
                two = stars[3]
                #一星
                one = stars[4]

            print("正在爬取："+name + "        " + str(rating_score) + "           " + peoplecount + "    " + url)
            sql = "insert into movie(电影名称,评分,评价,URL,制片国家,类型,五星,四星,三星,两星,一星) values("+"'"+name+ "'," + "'" +str(rating_score)+ "',"+ "'" +peoplecount+ "'," + "'" +url+ "',"+ "'" +m_country+"',"+ "'" +m_property+ "',"+"'"+five+"',"+"'"+four+"',"+"'"+three+ "'," + "'" +two+ "'," + "'" +one+"'"")"
            cursor.execute(sql)
            con.commit()

            # 提取电影短评
            comment_url = url + "/comments?status=P"
            req = requests.get(comment_url)
            req.encoding = "utf-8"
            # print(req.text)
            contents = req.text
            #电影名
            movieName = re.findall("<title>(.*) 短评</title>", str(contents))
            #评论人的id名
            username = re.findall("<a href=\"https://www.douban.com/people/(.*)/\" class=\"\">", str(contents))
            #评分数
            stars = re.findall("<span class=\"allstar(.*) rating", str(contents))
            # print(movieName,username,stars)

            sql = "select id from movie where 电影名称=" + "'" + movieName[0] + "'"
            # print(sql)
            cursor.execute(sql)
            #获取查询结果的第一行数据
            data = cursor.fetchone()
            con.commit()

            #插入短评
            movieId = str(data[0])
            for i in range(len(stars)):
                sql = "insert into commentDetail(电影id,评分数,评论人id) values(" + "'" + movieId + "'," + "'" + stars[i] + "'," + "'" + username[i] + "')"
                # print(sql)
                cursor.execute(sql)
                con.commit()
except:
    cursor.execute("truncate table movie;truncate table commentdetail;")
    con.commit()
    print("出错了")