import os
import re
import sys
from tkinter import *
from tkinter.ttk import Combobox
# 创建一个窗口
root = Tk()
# 设置窗口标题
root.title('翻译工具')
# 设置窗口大小
root.geometry('1024x768')


# 创建两个text控件,各占一半
text1 = Text(root, width=75, height=55,bg="#2e2e2e",fg="white")
text2 = Text(root, width=70, height=55,bg="#0c0c0c",fg="pink")
text1.place(x=0, y=0, anchor='nw')
text2.place(x=530, y=0, anchor='nw')
# 创建一个下拉列表，用于遍历所有的rpy文件
com1 = Combobox(root,width=30)
com1.place(x=30, y=725, anchor='nw')
# 默认选择第一个

# 创建获取待翻译内容的按钮
btn1 = Button(root, text='获取待翻译内容')
btn1.place(x=300, y=720, anchor='nw')
# 创建翻译对话部分按钮
btn2 = Button(root, text='翻译对话部分',width=20)
btn2.place(x=550, y=720, anchor='nw')
# 创建替换翻译按钮
btn2 = Button(root, text='替换 strings 部分',width=20)
btn2.place(x=550, y=720, anchor='nw')

def get_all_rpy():
    all_rpy = []
    for root,dirs,files in os.walk('./code'):
        for file in files:
            if file.endswith('.rpy'):
                all_rpy.append(root+'/'+file)
                # print(file)
        print(root)
    return all_rpy
com1['value'] = get_all_rpy()

# 当com1 发生变动时，获取com1的内容
def get_com1():
    fileadd= com1.get()
    return fileadd
# 获取完整的rpy文件地址

def open_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        return f.read()

# 遍历所有的注释字段
def get_all_comments(file_content):
    all_comments = []
    all_wait_tran = []
    string_comments = []
    a = 0
    # 获取文件行数
    file_lines = file_content.split('\n')
    for line in file_lines:
        a += 1
        if line.startswith('translate Chinese') and not line.startswith('translate Chinese strings'):
            # 获取translate Chinese下面两行的内容
            En_tran = file_lines[file_lines.index(line) + 2]
            wait_tran = file_lines[file_lines.index(line) + 3]
            # 截取En_tran引号中的内容
            try :
                speak_content = re.search('"(.*?)"',En_tran).group(1)
                all_wait_tran.append(speak_content)
            except:
                speak_content = ''
            all_comments.append(wait_tran+"["+str(a+3)+"]")      
    return all_comments,all_wait_tran

def show_all_wait_tran():
    filepath = get_com1()
    # 判断文件是否存在
    if os.path.exists(filepath):
        # 获取com1中的内容，如果为空提示选择文件
        print(filepath)
        filename = open_file(filepath)
    else:
        filename = ''
        print('请选择文件')
        print(filepath)
    all_comments,all_wait_tran = get_all_comments(filename)
    text1.delete(1.0, END)
    for waitran in all_wait_tran:
        text1.insert(INSERT, waitran + '\n')
    return filepath
btn1['command'] = show_all_wait_tran

def tran():
    filepath = show_all_wait_tran()
    filename = open_file(filepath)
    all_comments,all_wait_tran = get_all_comments(filename)
    # 获取text2中的内容
    text2content = text2.get(1.0, END)
    all_tran = []
    # 统计函数
    text2line = text2content.split('\n')

    # 遍历所有的行
    for line in text2content:
        if line:
            # 截取[]中的内容
            try:
                tran = re.search('\[(.*?)\]', line).group(1)
                all_tran.append(tran)
            except:
                tran = ''
    # 遍历所有的all_wait_tran字段
    filename = open_file(filepath) 
    a = 0
    for comments in all_comments:
        a += 1
        # 取出wait_tran中[]的数字
        try:
            comments_num = int(re.search('\[(.*?)\]', comments).group(1))
            print(comments_num)
            # 打开指定的rpy文件       
            file_lines = filename.split('\n')
            # 获取comments_num对应的行数的内容
            line_content = file_lines[int(comments_num-1)]
            print(line_content)
            # 替换line_content中的引号内容
            try:
                # 查找line_content中引号的位置
                start = line_content.index('"')
                end = line_content.rindex('"')
                # 在start和end之间插入text2line中的内容
                line_content = line_content[:start+1] + text2line[a-1] + line_content[end:]
                
                print(line_content)
            except:
                line_content = line_content
            # 替换掉原来的内容
            file_lines[comments_num-1] = line_content 
            # 新的filename输出到text1中
            filename = '\n'.join(file_lines)
            print(file_lines)        
        except:
            comments_num = ''
        print(comments_num)
    
    # 把filename加载到text1中
    text1.delete(1.0, END)
    text1.insert(INSERT, filename)  

btn2['command'] = tran
# 保存文件
def save_file():
    # 获取text1中的内容
    text1content = text1.get(1.0, END)
    # 获取com1中的内容
    filepath = './code/'+com1.get()
    # 判断文件是否存在
    if os.path.exists(filepath):
        print(text1content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text1content)
            f.close()
    else:
        print('请选择文件')
btn3 = Button(root, text='保存文件', command=save_file)
btn3.place(x=400, y=720, anchor='nw')
root.mainloop()