import streamlit as st
import os


# 加载 data/ 目录下的所有 txt 文件名
def load_file_names():
    file_names = []
    for filename in os.listdir("data/"):
        if filename.endswith(".txt"):
            file_names.append(filename)
    return file_names


# 加载选中的 txt 文件内容
def load_file_content(file_name):
    with open(f"data/{file_name}", "r", encoding="utf-8") as f:
        content = f.read()
    return content


# 主函数
def main():
    # 加载侧栏下拉框的选项
    options = load_file_names()

    # 在侧栏中创建下拉框
    selected_file = st.sidebar.selectbox("选择一个文件", options)

    # 加载选中的文件内容并在主区域展示
    content = load_file_content(selected_file)
    st.write(content)


if __name__ == "__main__":
    main()