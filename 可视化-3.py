from pyecharts import *
import xlrd



#打开数据文件
workbook = xlrd.open_workbook('清洗后数据.xlsx')

# 获取workbook中所有的表格
sheet1 = workbook.sheet_by_index(0)
sheet2 = workbook.sheet_by_index(1)
sheet3 = workbook.sheet_by_index(2)
sheet4 = workbook.sheet_by_index(3)

# 打印所有表
# print(workbook.sheet_names())

# 获取第一个表的数据
a =sheet1.col_values(0)[1:]
b =sheet1.col_values(1)[1:]

# 获取第二个表的数据
a1 =sheet2.col_values(0)[1:]
b1 =sheet2.col_values(1)[1:]

# 获取第三个表的数据
a2 =sheet3.col_values(1)[1:] 
b2 =sheet3.col_values(2)[1:]

# 获取第四个表的数据
a3 =sheet4.col_values(1)[1:]
b3 =sheet4.col_values(2)[1:]



# 实例化page类
page = Page()

# Bar
bar=Bar("柱状图示例")
bar.add("数量",a,b,is_label_show=True,xaxis_interval=0,is_datazoom_show=True,datazoom_type='both',mark_point=["max", "min"])
page.add(bar)

bar1 = Bar("")
bar1.add("分数", b2, a2,is_label_show=True,is_datazoom_show=True, is_stack=True)
page.add(bar1)  # TODO 向page中添加图表

# Funnel
funnel=Funnel("漏斗图示例")
funnel.add('占比',a1,b1)
page.add(funnel)# TODO 向page中添加图表

# pie
pie = Pie("饼图-圆环图示例", title_pos='center')
pie.add("比例", a1, b1, radius=[40, 75], label_text_color=None,is_label_show=True, legend_orient='vertical', legend_pos='left')
page.add(pie)  # TODO 向page中添加图表



# line
line = Line("折线图示例")
line.add("评价数量",b3,a3 ,mark_point=["max", "min"], is_label_show=True,is_datazoom_show=True)
page.add(line)# TODO 向page中添加图表



page.render("可视化图.html")
print("可视化成功")