import os
import sys
import shutil
import math
import tkinter as tk
from tkinter import messagebox

# --- 配置区域：支持的所有图片格式 ---
# 包含：通用格式、Web格式、相机RAW格式、设计源文件、HDR格式等
IMAGE_EXTENSIONS = {
    # 通用/网络格式
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.tif', '.ico',
    '.heic', '.heif', '.avif', '.jp2', '.j2k', '.jpf', '.jpx', '.jpm', '.mj2',
    
    # 佳能 (Canon)
    '.cr2', '.cr3', '.crw',
    # 尼康 (Nikon)
    '.nef', '.nrw',
    # 索尼 (Sony)
    '.arw', '.srf', '.sr2',
    # 富士 (Fujifilm)
    '.raf',
    # 奥林巴斯 (Olympus)
    '.orf',
    # 松下 (Panasonic)
    '.rw2',
    # 徕卡 (Leica)
    '.rwl', '.dng',
    # 宾得 (Pentax)
    '.pef', '.ptx',
    # 三星 (Samsung)
    '.srw',
    # 适马 (Sigma)
    '.x3f',
    # 哈苏 (Hasselblad)
    '.3fr', '.fff',
    # 柯达 (Kodak)
    '.kdc', '.dcr',
    # 柯尼卡美能达 (Minolta)
    '.mrw',
    # 飞思 (Phase One)
    '.iiq',
    # 爱普生 (Epson)
    '.erf',
    # 玛米亚 (Mamiya)
    '.mef',
    # 莫斯科 (Moscov)
    '.mos',
    
    # Adobe & 设计格式
    '.psd', '.psb', '.ai', '.eps', '.pdf', # 有些人会把 PDF/AI 当图存
    
    # 其他/老旧格式
    '.tga', '.icns', '.pcx', '.ppm', '.pgm', '.pbm', '.pnm', '.ras', '.wbmp', '.xpm', '.svg', '.dds', '.hdr', '.exr'
}

def main():
    # 1. 隐藏主窗口
    root = tk.Tk()
    root.withdraw()

    # 2. 获取当前路径
    if getattr(sys, 'frozen', False):
        current_dir = os.path.dirname(sys.executable)
    else:
        current_dir = os.path.dirname(os.path.abspath(__file__))

    parent_folder_name = os.path.basename(current_dir)

    # 3. 扫描文件 (不区分大小写)
    all_files = os.listdir(current_dir)
    image_files = []
    
    for f in all_files:
        # 跳过自身 EXE 文件，防止把自己也移进去
        if f.lower().endswith('.exe') or f.lower().endswith('.py'):
            continue
            
        _, ext = os.path.splitext(f)
        if ext.lower() in IMAGE_EXTENSIONS:
            image_files.append(f)

    # 4. 判空
    if not image_files:
        messagebox.showinfo("提示", "当前文件夹内没有找到已知的图片/照片文件。")
        return

    # 5. 智能排序 (兼容 Windows 的数字排序习惯)
    # 这里使用简单的字母排序，如果文件名是 1.jpg, 2.jpg, 10.jpg，默认排序可能是 1, 10, 2
    # 如果需要更智能的排序，可以使用 sort(key=lambda x: len(x)) 简单优化，或保持默认
    image_files.sort()

    # 6. 分组处理
    group_size = 3
    total_groups = math.ceil(len(image_files) / group_size)
    
    moved_count = 0

    try:
        for i in range(total_groups):
            start_index = i * group_size
            end_index = start_index + group_size
            chunk = image_files[start_index:end_index]

            # 7. 生成子文件夹名
            sub_folder_name = f"{parent_folder_name}_{i + 1}"

            # 特殊处理：不足3张的组
            if len(chunk) < group_size:
                sub_folder_name += f"_尾数不足{group_size}张"

            full_sub_folder_path = os.path.join(current_dir, sub_folder_name)

            if not os.path.exists(full_sub_folder_path):
                os.makedirs(full_sub_folder_path)

            # 8. 移动文件
            for img in chunk:
                src = os.path.join(current_dir, img)
                dst = os.path.join(full_sub_folder_path, img)
                
                # 防止同名文件覆盖报错
                if os.path.exists(dst):
                    root, ext = os.path.splitext(img)
                    dst = os.path.join(full_sub_folder_path, f"{root}_copy{ext}")
                
                shutil.move(src, dst)
                moved_count += 1

        messagebox.showinfo("成功", f"整理完成！\n\n共处理文件: {moved_count} 个\n生成文件夹: {total_groups} 个")

    except Exception as e:
        messagebox.showerror("错误", f"发生意外错误:\n{str(e)}")

if __name__ == "__main__":
    main()
