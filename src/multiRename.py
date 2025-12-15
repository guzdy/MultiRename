import os
from PIL import Image
import re

# =================配置区=================
# 默认开启安全模式（只打印不执行），按 'z' 键切换
DRY_RUN = True 
# =======================================

def isimg(filepath):
    valid = True
    try:
        Image.open(filepath).verify()
    except:
        valid = False
    return valid

def safe_rename(src, dst):
    """安全重命名封装函数"""
    if src == dst:
        return
    
    # 获取文件名用于显示，避免路径太长看不清
    fname_src = os.path.basename(src)
    fname_dst = os.path.basename(dst)

    if DRY_RUN:
        print(f"[预览] {fname_src}  --->  {fname_dst}")
    else:
        try:
            if os.path.exists(dst):
                print(f"[跳过] 目标文件已存在: {fname_dst}")
                return
            os.rename(src, dst)
            print(f"[成功] {fname_src} -> {fname_dst}")
        except Exception as e:
            print(f"[错误] {fname_src}: {e}")

def get_files(path, recursive_option):
    """辅助函数：根据选项获取文件遍历生成器"""
    if recursive_option == 'y':
        return os.walk(path)
    else:
        # 构造一个类似 os.walk 的生成器，只产生当前目录的数据
        return [(path, [], os.listdir(path))]

# ----------------- 原有功能 (已升级为 safe_rename) -----------------

def process_a(path, text, text2, option2):
    """从文件名中批量删除或替代某段文字。"""
    for root, dirs, files in get_files(path, option2):
        for j in files:
            if text in j:
                old_path = os.path.join(root, j)
                new_path = os.path.join(root, j.replace(text, text2))
                safe_rename(old_path, new_path)
    print("> 任务结束。")

def process_b(path, text, option2):
    """在文件名前头批量增加相同文字。"""
    for root, dirs, files in get_files(path, option2):
        for j in files:
            old_path = os.path.join(root, j)
            new_path = os.path.join(root, text + j)
            safe_rename(old_path, new_path)
    print("> 任务结束。")

def process_c(path):
    """在文件名前头增加各级目录名。"""
    option2 = input("> 是否包括子文件夹下的所有文件 (y/n/q): \n$ ").lower()
    if option2 == 'q': return menu2(path)

    for root, dirs, files in get_files(path, option2):
        for j in files:
            old_path = os.path.join(root, j)
            # 获取相对路径结构作为前缀
            path_short = path.strip().split(os.sep)[-1]
            rel_path = root.replace(path, '')
            prefix = (path_short + rel_path).replace(os.sep, '.') + '.'
            # 去除开头可能多余的点
            if prefix.startswith('.'): prefix = prefix[1:]
            
            new_path = os.path.join(root, prefix + j)
            safe_rename(old_path, new_path)
    print("> 任务结束。")

def process_d(path, text, option2):
    """在文件名后头批量增加相同文字(不影响文件扩展名)。"""
    for root, dirs, files in get_files(path, option2):
        for j in files:
            fname, fext = os.path.splitext(j)
            old_path = os.path.join(root, j)
            new_path = os.path.join(root, fname + text + fext)
            safe_rename(old_path, new_path)
    print("> 任务结束。")

def process_e(path):
    """按文件创建时间顺序重命名。"""
    file_ctime_dict = {}
    # 这里只处理单层目录，避免跨目录序号混乱
    for i in os.listdir(path):
        sub_path = os.path.join(path, i)
        if os.path.isfile(sub_path):
            file_ctime_dict[sub_path] = os.path.getctime(sub_path)
    
    num = 1
    # 按时间排序
    for full_path, ctime in sorted(file_ctime_dict.items(), key=lambda t: t[1]):
        root, filename = os.path.split(full_path)
        fname, fext = os.path.splitext(filename)
        new_path = os.path.join(root, str(num) + fext)
        safe_rename(full_path, new_path)
        num += 1
    print("> 任务结束。")

def process_f(path):
    """把子目录文件移动到当前目录。"""
    for root, dirs, files in os.walk(path):
        if root == path: continue # 跳过根目录自己
        for j in files:
            old_path = os.path.join(root, j)
            new_path = os.path.join(path, j)
            safe_rename(old_path, new_path)
    print("> 任务结束。")

def process_g(path):
    """批量删除文件扩展名。"""
    for j in os.listdir(path):
        sub_path = os.path.join(path, j)
        if os.path.isfile(sub_path):
            fname, fext = os.path.splitext(sub_path)
            safe_rename(sub_path, fname)
    print("> 任务结束。")

def process_h(path):
    """按开头相同文字长度归档。"""
    str_num = input('> 输入判断相同文字的数量 (数字): \n$ ')
    if not str_num.isdigit(): return print("请输入数字。")
    num = int(str_num)
    
    for root, dirs, files in os.walk(path):
        for j in files:
            old_path = os.path.join(root, j)
            folder_name = j[:num] if len(j) > num else "其他"
            target_dir = os.path.join(root, folder_name)
            
            if not DRY_RUN and not os.path.exists(target_dir):
                os.makedirs(target_dir)
                
            new_path = os.path.join(target_dir, j)
            safe_rename(old_path, new_path)
    print("> 任务结束。")

def process_i(path):
    """按关键词归档。"""
    text = input('> 输入关键词(以斜杠"/"划分): \n$ ')
    tag_list = text.split('/')
    
    for root, dirs, files in os.walk(path):
        for j in files:
            for tag in tag_list:
                if tag in j:
                    old_path = os.path.join(root, j)
                    target_dir = os.path.join(root, tag)
                    
                    if not DRY_RUN and not os.path.exists(target_dir):
                        os.makedirs(target_dir)
                        
                    new_path = os.path.join(target_dir, j)
                    safe_rename(old_path, new_path)
    print("> 任务结束。")

def process_j(path):
    """移动非图片文件。"""
    target_dir = os.path.join(path, 'not_img')
    if not DRY_RUN and not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for root, dirs, files in os.walk(path):
        if 'not_img' in root: continue
        for j in files:
            old_path = os.path.join(root, j)
            if not isimg(old_path):
                new_path = os.path.join(target_dir, j)
                safe_rename(old_path, new_path)
    print("> 任务结束。")

def process_k(path):
    """按数量归档。"""
    # 略微简化逻辑，保持原风格
    try:
        num = int(input('> 每个文件夹文件数量: \n$ '))
    except: return
    
    count = 0
    dir_idx = 0
    # 获取迭代器
    iterator = os.walk(path).__next__() # 只处理第一层
    
    for j in iterator[2]:
        if count % num == 0:
            dir_idx += num
        
        old_path = os.path.join(path, j)
        target_dir = os.path.join(path, str(dir_idx))
        
        if not DRY_RUN and not os.path.exists(target_dir):
            os.makedirs(target_dir)
            
        new_path = os.path.join(target_dir, j)
        safe_rename(old_path, new_path)
        count += 1
    print("> 任务结束。")

def process_l(path):
    """正则归档。"""
    pattern_str = input('> 输入正则式 (例如 r"^(\d+)-.*"): \n$ ')
    try:
        pattern = eval(pattern_str)
    except:
        return print("> 正则错误。")

    for root, dirs, files in os.walk(path):
        for j in files:
            match = re.search(pattern, j)
            if match:
                folder = match.group(1) if match.groups() else match.group(0)
                old_path = os.path.join(root, j)
                target_dir = os.path.join(root, folder)
                
                if not DRY_RUN and not os.path.exists(target_dir):
                    os.makedirs(target_dir)
                    
                new_path = os.path.join(target_dir, j)
                safe_rename(old_path, new_path)
    print("> 任务结束。")

# ----------------- 新增功能 -----------------

def process_m(path):
    """大小写转换。"""
    mode = input("> 选择模式:\n  1. 全部小写 (abc.txt)\n  2. 全部大写 (ABC.TXT)\n  3. 首字母大写 (Abc.txt)\n$ ")
    option2 = input("> 是否包括子文件夹 (y/n): \n$ ").lower()

    for root, dirs, files in get_files(path, option2):
        for j in files:
            fname, fext = os.path.splitext(j)
            if mode == '1':
                new_name = j.lower()
            elif mode == '2':
                new_name = j.upper()
            elif mode == '3':
                new_name = fname.title() + fext.lower()
            else:
                continue
            
            safe_rename(os.path.join(root, j), os.path.join(root, new_name))
    print("> 任务结束。")

def process_n(path):
    """批量修改扩展名。"""
    old_ext = input("> 原后缀 (直接回车代表所有, 不带点): \n$ ").strip()
    new_ext = input("> 新后缀 (例如 jpg, 不带点): \n$ ").strip()
    if not new_ext: return
    
    option2 = input("> 是否包括子文件夹 (y/n): \n$ ").lower()
    
    for root, dirs, files in get_files(path, option2):
        for j in files:
            fname, fext = os.path.splitext(j)
            # 如果指定了原后缀，且当前文件不匹配，则跳过
            if old_ext and fext.replace('.','') != old_ext:
                continue
            
            new_name = fname + '.' + new_ext
            safe_rename(os.path.join(root, j), os.path.join(root, new_name))
    print("> 任务结束。")

def process_o(path):
    """清洗文件名 (空格处理)。"""
    mode = input("> 1. 去除空格\n> 2. 空格变下划线\n> 3. 点变下划线(保留后缀点)\n$ ")
    option2 = input("> 是否包括子文件夹 (y/n): \n$ ").lower()

    for root, dirs, files in get_files(path, option2):
        for j in files:
            fname, fext = os.path.splitext(j)
            new_fname = fname
            if mode == '1':
                new_fname = fname.replace(" ", "")
            elif mode == '2':
                new_fname = fname.replace(" ", "_")
            elif mode == '3':
                new_fname = fname.replace(".", "_")
            
            safe_rename(os.path.join(root, j), os.path.join(root, new_fname + fext))
    print("> 任务结束。")

def process_p(path):
    """【新功能】文件名数字批量计算。"""
    print("> 功能说明: 提取文件名中的数字进行加减运算，并重新补零格式化。")
    print("> 例如: 输入 -100 和位数 3。 文件 'img_101.jpg' -> 'img_001.jpg'")
    
    try:
        calc_num = int(input("> 请输入要加减的数字 (例如 -100 或 5): \n$ "))
        padding = int(input("> 请输入目标数字位数 (例如 3 代表 001): \n$ "))
    except ValueError:
        print("请输入整数。")
        return

    option2 = input("> 是否包括子文件夹 (y/n): \n$ ").lower()

    for root, dirs, files in get_files(path, option2):
        for j in files:
            # 使用正则查找文件名中的第一组数字
            match = re.search(r"(\d+)", j)
            if match:
                original_num_str = match.group(1)
                original_num = int(original_num_str)
                
                # 计算新数字
                new_num = original_num + calc_num
                
                # 只有当结果为正数时才处理 (或者你可以允许负数，视需求而定)
                if new_num >= 0:
                    # 格式化，例如 {:03d}
                    new_num_str = "{:0{}d}".format(new_num, padding)
                    
                    # 替换文件名中第一次出现的这个数字字符串
                    # 注意：这里简单使用 replace 可能会替换掉非预期位置的数字，但在大多数命名规范中是安全的
                    # 更严谨的做法是只替换正则匹配到的位置
                    new_name = j.replace(original_num_str, new_num_str, 1)
                    
                    safe_rename(os.path.join(root, j), os.path.join(root, new_name))
                else:
                    if DRY_RUN: print(f"[警告] 计算结果为负数，跳过: {j} ({original_num}{calc_num})")

    print("> 任务结束。")

# ----------------- 菜单逻辑 -----------------

def menu3_1(path, option):
    text = input("> 请输入需要修改文字，输入'q'返回： \n$ ")
    if text in ["q", "Q"]: return menu2(path)
    
    if option == "a":
        text2 = input("> 请输入替代后的文字；直接回车删除： \n$ ")
    else:
        text2 = ""

    option2 = input("> 是否包括子文件夹 (y/n)：").lower()
    
    if option == 'a': process_a(path, text, text2, option2)
    elif option == 'b': process_b(path, text, option2)
    elif option == 'd': process_d(path, text, option2)

def menu2(path):
    global DRY_RUN
    while True:
        mode_status = "【预览模式】(安全)" if DRY_RUN else "【狂暴模式】(危险!)"
        print("\n----------------------------------------")
        print(f"当前状态: {mode_status}  | 路径: {os.path.basename(path)}")
        print("----------------------------------------")
        print("  [常用] \n"
              "  a. 替换/删除文字    b. 头部添加文字    d. 尾部添加文字\n"
              "  m. 大小写转换       n. 修改扩展名      o. 清洗(去空格/符号)\n"
              "  \n"
              "  [高级] \n"
              "  p. 文件名数字计算 (如 101 -> 001) \n"
              "  c. 添加目录名为前缀 \n"
              "  h. 按开头相同文字归档 \n"
              "  i. 按关键词归档 \n"
              "  l. 正则归档 \n"
              "  \n"
              "  [其他] \n"
              "  f. 摊平文件夹       j. 移除非图片      g. 删除扩展名 \n"
              "  e. 按时间重命名     k. 按数量分堆 \n"
              "  \n"
              "  z. 切换 安全/执行 模式 \n"
              "  q. 返回上一级")
        
        option = input("\n> 请选择选项: ").strip().lower()
        
        if option == 'q': return
        elif option == 'z': 
            DRY_RUN = not DRY_RUN
            print(f">>> 模式已切换 <<<")
            continue
            
        elif option in ['a', 'b', 'd']: menu3_1(path, option)
        elif option == 'c': process_c(path)
        elif option == 'e': process_e(path)
        elif option == 'f': process_f(path)
        elif option == 'g': process_g(path)
        elif option == 'h': process_h(path)
        elif option == 'i': process_i(path)
        elif option == 'j': process_j(path)
        elif option == 'k': process_k(path)
        elif option == 'l': process_l(path)
        elif option == 'm': process_m(path)
        elif option == 'n': process_n(path)
        elif option == 'o': process_o(path)
        elif option == 'p': process_p(path)
        else: print("> 选项错误。")

def menu1():
    print("【增强版批量文件管理脚本 v2.0】\n"
          " 特性：支持安全预览、数字计算、扩展名修改等。\n"
          " 注意：默认开启预览模式，操作前请按 z 切换模式。\n")
    while True:
        path = input("> 请输入文件夹路径 (q 退出): \n$ ")
        if path.lower() in ["q", "exit"]: break
        
        # 移除可能存在的引号（Windows复制路径常见问题）
        path = path.replace('"', '').replace("'", "").strip()
        
        if os.path.isdir(path):
            menu2(os.path.abspath(path))
        else:
            print('> 路径无效。')

if __name__ == "__main__":
    menu1()
