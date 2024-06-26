import tkinter as tk
from tkinter import ttk
import re

# 读取 Markdown 文件
def read_md_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

# 解析 Markdown 文件内容
def parse_md_content(content):
    pattern = re.compile(r'### (.*?)（.*?）\n\n\*\*全称\*\*：(.*?)\n\n\*\*中文\*\*：(.*?)\n\n\*\*介绍\*\*：(.*?)\n', re.DOTALL)
    matches = pattern.findall(content)
    return [{'缩写': m[0], '全称': m[1], '中文': m[2], '介绍': m[3].strip()} for m in matches]

# 创建 GUI 界面
class VocabularyApp:
    def __init__(self, root, data):
        self.root = root
        self.data = data
        self.hidden_columns = set()

        self.tree = ttk.Treeview(root, columns=('缩写', '全称', '中文', '介绍'), show='headings')
        self.tree.heading('缩写', text='缩写')
        self.tree.heading('全称', text='全称')
        self.tree.heading('中文', text='中文')
        self.tree.heading('介绍', text='介绍')

        # 插入数据并保存原始数据
        self.original_data = []
        for item in data:
            self.tree.insert('', 'end', values=(item['缩写'], item['全称'], item['中文'], item['介绍']))
            self.original_data.append((item['缩写'], item['全称'], item['中文'], item['介绍']))

        self.tree.pack(expand=True, fill='both')

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(fill='x')

        self.toggle_buttons = {}
        for col in ('缩写', '全称', '中文', '介绍'):
            button = tk.Button(self.button_frame, text=f'遮挡 {col}', command=lambda c=col: self.toggle_column(c))
            button.pack(side='left')
            self.toggle_buttons[col] = button

    def toggle_column(self, column):
        if column in self.hidden_columns:
            self.hidden_columns.remove(column)
            self.toggle_buttons[column].config(text=f'遮挡 {column}')
        else:
            self.hidden_columns.add(column)
            self.toggle_buttons[column].config(text=f'显示 {column}')
        self.update_treeview()

    def update_treeview(self):
        for i, item in enumerate(self.tree.get_children()):
            values = self.original_data[i]
            new_values = []
            for j, col in enumerate(('缩写', '全称', '中文', '介绍')):
                if col in self.hidden_columns:
                    new_values.append('***')
                else:
                    new_values.append(values[j])
            self.tree.item(item, values=new_values)

if __name__ == '__main__':
    file_path = 'vocabulary.md'  # 替换为你的 Markdown 文件路径
    content = read_md_file(file_path)
    data = parse_md_content(content)

    root = tk.Tk()
    root.title('Vocabulary App')
    app = VocabularyApp(root, data)
    root.mainloop()
