import pandas as pd
import numpy as np
#增加列头
names = [
    'id','电影名称','评分','评价','URL链接','制片国家','类型','五星','四星','三星','两星','一星'
]
df = pd.read_excel("movie.xls",header = None,names= names)

#清除评价后面的汉字
keywordlist = ['人评价']
df['评价'] = df['评价'].str.replace('|'.join(keywordlist), ' ')
# print(df)


#统计制片国家数量
production = df['制片国家'].str.split(',').apply(pd.Series)
a = production.apply(pd.value_counts).fillna('0')
a.columns = ['area_1','area_2','area_3','area_4']
a['area_1'] = a['area_1'].astype(int)
a['area_2'] = a['area_2'].astype(int)
a['area_3'] = a['area_3'].astype(int)
a['area_4'] = a['area_4'].astype(int)
a = a.apply(lambda x: x.sum(),axis = 1)
number = pd.DataFrame(a, columns = ['数量'])
# print(number.head(1000))

#统计电影类型数量
area_split = df['类型'].str.split(',').apply(pd.Series)
g = area_split.apply(pd.value_counts)
g = g.unstack().dropna().reset_index()
g.columns = ['level_0','类型', '数量']
typenumber = g.drop(['level_0'],axis = 1).groupby('类型').sum()
# print(typenumber.head(1000))




#评分排名
score = df[['评分','电影名称']].sort_values(by = ['评分'],ascending = False).head(100).reset_index()
# print(score)


#评价排名
evaluate = df[['评价','电影名称']].sort_values(by = ['评价'],ascending = False).head(100).reset_index()
# print(evaluate)

# 总排名
# print(df[['id','电影名称']].head(100))

writer = pd.ExcelWriter('清洗后数据.xlsx')
number.to_excel(writer, sheet_name = '电影制片国家数量统计', index = True)
typenumber.to_excel(writer, sheet_name = '电影类型数量总数统计', index = True)
score.to_excel(writer, sheet_name = '评分排名统计', index = False)
evaluate.to_excel(writer, sheet_name = '评价排名统计', index = False)
df[['id','电影名称']].to_excel(writer, sheet_name = '总排名', index = False)
print('保存完成')
writer.save()
writer.close()