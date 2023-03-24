import streamlit as st
import os
from smartqa.qacontroller import QAController


@st.cache_resource
def load_controller():
    return QAController()

controller = load_controller()

# # 加载 data/ 目录下的所有 txt 文件名
# def load_file_names():
#     file_names = []
#     for filename in os.listdir("data/"):
#         if filename.endswith(".txt"):
#             file_names.append(filename)
#     return file_names


# # 加载选中的 txt 文件内容
# def load_file_content(file_name):
#     with open(f"data/{file_name}", "r", encoding="utf-8") as f:
#         content = f.read()
#     return content


# 主函数
def main():

    col1, col2 = st.columns([8, 2])
    with col1:
        text = st.text_input("请输入你的问题：")

    with col2:
        st.write("")
        st.write("")
        push = st.button("搜索")

    lines = []
    if text and push:
        lines = controller.process(text)

    if lines:
        st.markdown("\n\n---\n".join(lines))



if __name__ == "__main__":
    main()