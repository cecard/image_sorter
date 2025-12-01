import os
import sys
import shutil
import math
import tkinter as tk
from tkinter import messagebox

# 支持的图片格式
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp', '.tiff', '.heic'}

def main():
    # 1. 隐藏主窗口，只显示弹窗
    root = tk.Tk()
    root.withdraw()

    # 2. 获取 EXE 所在的当前目录
    if getattr(sys, 'frozen', False):
        # 如果是打包后的 EXE
        current_dir = os.path.dirname(sys.executable)
    else:
        # 如果是 Python 脚本运行
        current_dir = os.path.dirname(os.path.abspath(__file__))

    # 获取主文件夹的名字 (例如 "我的相册")
    parent_folder_name = os.path.basename(current_dir)

    # 3. 扫描所有图片文件
    all_files = os.listdir(current_dir)
    image_files = []
    
    for f in all_files:
        _, ext = os.path.splitext(f)
        if ext.lower() in IMAGE_EXTENSIONS:
            image_files.append(f)

    # 4. 如果没有图片，弹窗提示并退出
    if not image_files:
        messagebox.showinfo("提示", "当前文件夹内没有找到图片文件。")
        return

    # 5. 按名称排序 (确保顺序正确)
    image_files.sort()

    # 6. 分组处理
    group_size = 3
    total_groups = math.ceil(len(image_files) / group_size)
    
    moved_count = 0

    try:
        for i in range(total_groups):
            # 获取当前组的 3 张图片 (切片操作)
            start_index = i * group_size
            end_index = start_index + group_size
            chunk = image_files[start_index:end_index]

            # 7. 生成子文件夹名字
            # 正常命名: 主文件夹名_1, 主文件夹名_2
            sub_folder_name = f"{parent_folder_name}_{i + 1}"

            # 特殊处理: 如果是最后一组且不足 3 张
            if len(chunk) < group_size:
                sub_folder_name += f"_尾数不足{group_size}张"

            full_sub_folder_path = os.path.join(current_dir, sub_folder_name)

            # 创建子文件夹 (如果存在则忽略)
            if not os.path.exists(full_sub_folder_path):
                os.makedirs(full_sub_folder_path)

            # 8. 移动图片
            for img in chunk:
                src = os.path.join(current_dir, img)
                dst = os.path.join(full_sub_folder_path, img)
                shutil.move(src, dst)
                moved_count += 1

        messagebox.showinfo("成功", f"整理完成！\n\n共处理图片: {moved_count} 张\n生成文件夹: {total_groups} 个")

    except Exception as e:
        messagebox.showerror("错误", f"发生意外错误:\n{str(e)}")

if __name__ == "__main__":
    main()
