# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from PIL import Image
import re


def isimg(filepath):
    valid = True
    try:
        Image.open(filepath).verify()
    except:
        valid = False
    return valid


def process_a(path, text, text2, option2):
    """从文件名中批量删除或替代某段文字。 """
    if option2 == 'y':
        for i in os.walk(path):
            for j in i[2]:
                old_path = os.path.join(i[0], j)
                new_path = os.path.join(i[0], j.replace(text, text2))
                if not new_path:
                    continue
                os.rename(old_path, new_path)
    elif option2 == 'n':
        for i in os.listdir(path):
            old_path = os.path.join(path, i)
            # 如只限文件， 可以对 old_path 进行 os.path.isfile() 判断
            new_path = os.path.join(path, i.replace(text, text2))
            if not new_path:
                continue
            os.rename(old_path, new_path)
    print("> 完成任务。")


def process_b(path, text, option2):
    """在文件名前头批量增加相同文字。 """
    if option2 == 'y':
        for i in os.walk(path):
            for j in i[2]:
                old_path = os.path.join(i[0], j)
                new_path = os.path.join(i[0], text+j)
                os.rename(old_path, new_path)
    elif option2 == 'n':
        i = os.walk(path).__next__()
        for j in i[2]:
            old_path = os.path.join(i[0], j)
            new_path = os.path.join(i[0], text+j)
            os.rename(old_path, new_path)
    print("> 完成任务。")


def process_c(path):
    """在文件名前头增加各级目录名(从刚刚输入目录开始）。 """
    option2 = input("> 是否包括子文件夹下的所有文件，选项(y/n)："
                    "  输入'q'返回。 \n$ ")
    if option2 in ['q', 'Q']:
        return menu2(path)
    if option2 == 'y':
        for i in os.walk(path):
            for j in i[2]:
                # i[0] 目录名， j 目录下的文件名
                old_path = os.path.join(i[0], j)
                # path 目录的相对目录名
                path_short = path.strip().split(os.sep)[-1]
                text = (path_short + i[0].replace(path, '')).replace(os.sep, '.') + '.'
                new_path = os.path.join(i[0], text+j)
                os.rename(old_path, new_path)
    elif option2 == 'n':
        i = os.walk(path).__next__()
        for j in i[2]:
            # i[0] 目录名， j 目录下的文件名
            old_path = os.path.join(i[0], j)
            text = path + '.'
            new_path = os.path.join(i[0], text + j)
            os.rename(old_path, new_path)
    print("> 完成任务。")


def process_d(path, text, option2):
    """在文件名后头批量增加相同文字(不影响文件扩展名)。 """
    if option2 == 'y':
        for i in os.walk(path):
            for j in i[2]:
                old_path = os.path.join(i[0], j)
                fname, fextension = os.path.splitext(j)
                new_path = os.path.join(i[0], fname+text+fextension)
                os.rename(old_path, new_path)
    elif option2 == 'n':
        i = os.walk(path).__next__()
        for j in i[2]:
            old_path = os.path.join(i[0], j)
            fname, fextension = os.path.splitext(j)
            new_path = os.path.join(i[0], fname + text + fextension)
            os.rename(old_path, new_path)
    print("> 完成任务。")


def process_e(path):
    """按文件创造时间顺序(LINUX系统中是按最后修改时间)，用数字为名(0, 1, 2...)批量修改文件名(不影响文件扩展名)。"""
    file_ctime_dict = {}
    for i in os.listdir(path):
        sub_path = os.path.join(path, i)
        if os.path.isfile(sub_path):
            created_time = os.path.getctime(sub_path)
            file_ctime_dict[sub_path] = created_time
    num = 1
    for j in sorted(file_ctime_dict.items(), key=lambda t: t[1]):
        os.rename(j[0], os.path.join(path, str(num)+'.'+j[0].split('.')[-1]))
        num = num + 1
    print("> 完成任务。")


def process_f(path):
    """把当前目录下面各级目录的所有子文件，合并到当前目录。"""
    for i in os.walk(path):
        for j in i[2]:
            old_path = os.path.join(i[0], j)
            new_path = os.path.join(path, j)
            os.rename(old_path, new_path)
    print("> 完成任务。")


def process_g(path):
    """批量删除文件扩展名。"""
    for i in os.listdir(path):
        sub_path = os.path.join(path, i)
        if os.path.isfile(sub_path):
            newname, fextension = os.path.splitext(sub_path)
            os.rename(sub_path, newname)
    print("> 完成任务。")


def process_h(path):
    """对某个文件夹下的所有文件，以文件名开头相同文字的长度进行分类，设置目录保存"""
    str_num = input('> 判断基准是所文件名中相同文字的数量，请回复数量： '
                    '  输入"q"返回。 \n$ ')
    if str_num in ['q', 'Q']:
        return menu2(path)
    try:
        num = int(str_num)
        assert num > 0
    except:
        print('> 输入内容出错，请输入数字正整数。')
        process_h(path)
    else:
        # 快速直接新建文件夹并 rename
        i = os.walk(path).__next__()
        for j in i[2]:
            old_path = os.path.join(i[0], j)
            new_dir = j[:num] if len(j) > num else j
            new_path = os.path.join(i[0], new_dir, j)
            os.renames(old_path, new_path)
        print("> 完成任务。")


def process_i(path):
    """对某个文件夹下的所有文件，根据文件名中的关键词进行分类，设置目录保存。"""
    text = input('> 请输入关键词(也就是文件夹名，多个关键词以斜杠"/"划分): \n'
                 '  例如: 北京/天津/重庆/上海/四川 成都/马云 \n'
                 '  文件名中未包含关键词，将不会被分类。 \n'
                 '  输入"q"返回。 \n$ ')
    if text in ['q', 'Q']:
        return menu2(path)
    if not text:
        print('> 输入内容出错，请输入正确规格的关键词。')
        process_i(path)
    else:
        tag_list = text.split('/')
        # 快速直接新建文件夹并 rename
        i = os.walk(path).__next__()
        for j in i[2]:
            old_path = os.path.join(i[0], j)
            for tag in tag_list:
                if tag in j:
                    new_path = os.path.join(i[0], tag, j)
                    os.renames(old_path, new_path)
        print("> 完成任务。")


def process_j(path):
    """把当前目录下面各级目录中所有非图片文件，合并到新建"not_img"目录中。"""
    for i in os.walk(path):
        for j in i[2]:
            old_path = os.path.join(i[0], j)
            if not isimg(old_path):
                new_path = os.path.join(path, 'not_img', j)
                os.renames(old_path, new_path)
    print("> 完成任务。")


def process_k(path):
    """某个目录下，文件数量太多，缓存量大影响读取速度时，按一定数量，分类保存。"""
    str_num = input('> 请回复每个文件夹下的文件数量(，输入"q"返回): \n$ ')
    if str_num in ['q', 'Q']:
        return menu2(path)
    try:
        num = int(str_num)
        assert num > 0
    except:
        print('> 输入内容出错，请输入数字正整数。')
        process_k(path)
    else:
        # num: 每个目录下的文件数， temp_num: 临时数; dir_num 目录名（数字表示），第一个 0
        temp_num = 0
        dir_num = 0
        i = os.walk(path).__next__()
        for j in i[2]:
            if temp_num == num:
                temp_num = 0  # 初始化 temp_num
                dir_num += num  # 修改 num 个文件路径后， 新建目录名
            old_path = os.path.join(i[0], j)
            new_path = os.path.join(i[0], str(dir_num), j)
            os.renames(old_path, new_path)
            temp_num += 1
        print("> 完成任务。")


def process_l(path):
    """根据<正则式>，对文件名进行分类，并设置目录保存。"""
    pattern_str = input('> 请输入一段正则式，如想对下列文件按音乐类型分类：\n'
                        '  文件:"1.摇滚-崔健-红旗下的蛋.mp3", "2.爵士-王若琳-偿还.mp3", \n'
                        '       "3.rap-海尔-black cab.mp3", "4.摇滚-谢天笑-向阳花.mp3", \n'
                        '       "5.民谣-赵照-一树桃花开.mp3", "6.民谣-赵照-当你老了.mp3"  \n'
                        '  正则式输入: r"^\\d+\\.(.+?)-.*"  \n\n'
                        '  如正则式匹配，则按第一组(第一个括号内)的匹配内容为分类后的文件夹名。\n'
                        '  如无括号，则按正则式所匹配的全部内容为分类后的文件夹名。\n'
                        '  如文件名不匹配正则式，将不会被分类。\n'
                        '  输入"q"返回。 \n$ ')
    if pattern_str in ['q', 'Q']:
        return menu2(path)
    try:
        pattern = eval(pattern_str)
    except:
        print("> 输入内容出错，请输入包括引号的正确正则式样式。")
    else:
        i = os.walk(path).__next__()
        for j in i[2]:
            match_result = re.search(pattern, j)
            if match_result:
                # 如括号分组，按括号内匹配的内容为新建文件夹名。
                try:
                    dir_name = match_result.group(1)
                except:
                    dir_name = match_result.group(0)
                old_path = os.path.join(i[0], j)
                new_path = os.path.join(i[0], dir_name, j)
                os.renames(old_path, new_path)
        print("> 完成任务。")


def menu3_1(path, option):
    """第三级菜单， 直接影响结果为 a, b, d"""
    text = input("> 请输入需要修改文字，输入'q'返回上级选项： \n$ ")
    if option == "a":
        text2 = input("> 请输入替代后的文字；直接敲回车键（Enter）删除文字： \n$ ")
    if text in ["q", "Q"]:
        menu2(path)
    elif text:
        while 1:
            option2 = input("> 是否包括子文件夹下的所有文件，选项(y/n)：")
            if option2 in ['y', 'n', 'Y', 'N']:
                if option == 'a':
                    return process_a(path, text, text2, option2.lower())
                elif option == 'b':
                    return process_b(path, text, option2.lower())
                elif option == 'd':
                    return process_d(path, text, option2.lower())
            else:
                print('> 输入的选项有误， 请重新输入。')
    else:
        print("> 未输入文字，请重新输入。")
        menu3_1(path, option)


def menu2(path):
    """第二级菜单， 直接影响结果为 c, e, f, g"""
    option = input("> 请选择批量修改选项(回复字母)：\n"
                   "  \n"
                   "  [常用选项] \n"
                   "  a. 从文件名中批量删除或替代某段文字。\n"
                   "  b. 在文件名前头批量增加相同文字。\n"
                   "  d. 在文件名后头批量增加相同文字(文件名不包括扩展名)。\n"
                   "  \n"
                   "  [其他多级子目录下多文件处理] \n"
                   "  c. 在文件名前头增加各级目录名(从刚刚输入目录开始）。\n"
                   "  f. 把当前目录下面各级子目录的所有子文件，合并到当前目录。\n"
                   "  j. 把当前目录下面各级目录中所有<非图片文件>，合并到新建'not_img'目录中。\n"
                   "  \n"
                   "  [其他当前目录下的多文件处理] \n"
                   "  g. 批量删除文件<扩展名>。\n"
                   "  e. 按<文件创建时间>顺序，用数字为名(0, 1, 2...)批量修改文件名。\n"
                   "     (LINUX系统中是按最后修改时间， 文件扩展名不受影响)\n" 
                   "  h. 按文件名<开头相同>文字进行分类，并设置目录保存。\n"
                   "  i. 根据文件名中的<相同关键词>进行分类，并设置目录保存。\n"
                   "  l. 根据<正则式>，对文件名进行分类，并设置目录保存。\n"
                   "  k. 当前目录下文件数量太多，缓存量大影响读取速度时，按<数量>分类保存。\n"
                   "  \n"
                   "  q. 返回到上级选项。\n$ ")
    if not option:
        print('> 请输入选项后，按回车。')
        return menu2(path)
    option = option.strip().lower()
    if option == 'q':
        return
    elif option in ['a', 'b', 'd']:
        menu3_1(path, option)
    elif option == 'c':
        process_c(path)
    elif option == 'e':
        process_e(path)
    elif option == 'f':
        process_f(path)
    elif option == 'g':
        process_g(path)
    elif option == 'h':
        process_h(path)
    elif option == 'i':
        process_i(path)
    elif option == 'j':
        process_j(path)
    elif option == 'k':
        process_k(path)
    elif option == 'l':
        process_l(path)
    else:
        print('> 您输入的选项有误，请重新输入。')
        menu2(path)


def menu1():
    """主菜单"""
    print("【批量文件重命名&移动脚本】\n"
          " 用途： 可以轻松对文件夹下的各级子目录文件进行重命名等操作。\n"
          " 作者： guzdy\n"
          " 邮箱： guz.jin@gmail.com\n")
    while 1:
        path = input("> 请输入需要批量修改名字的文件夹路径，输入'q'退出： \n$ ")
        if path in ["q", "Q"]:
            print('> MultiRename 退出程序。')
            return
        elif os.path.isdir(path):
            path = os.path.abspath(path)
            menu2(path)
        else:
            print('> 您输入的文件夹路径有误，请重新输入。')


if __name__ == "__main__":
    menu1()
