# 读取excel中的数据，将学校名称保存为txt文件

import xlrd

# 初始化学校名称列表
schoolNameList = []

# 读取学校信息
def read_text(path):

    # 打开excel文件
    rbook = xlrd.open_workbook(path)

    # 选取第一个工作簿
    rsheet = rbook.sheet_by_index(0)

    # 循环该工作簿所有行
    for row in rsheet.get_rows():
        schoolName = row[1] # 学校名称所在列
        # 过滤数据
        if len(schoolName.value) == 0 or schoolName.value == "学校名称":
            pass
        else:
            schoolNameList.append(schoolName.value)

# 保存学校名称
def save_text(filename,data):

    with open(filename,'w+') as f:
        for name in data:
            print(name)
            f.write(str(name) + '\n')
        f.close()
        print('写入完毕')



if __name__ == '__main__':
    path = './school_info.xls'
    read_text(path)
    save_text('./school_name.txt',schoolNameList)