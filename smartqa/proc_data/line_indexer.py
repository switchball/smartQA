from typing import Dict, Tuple, List

class LineIndexer:
    def __init__(self) -> None:
        self.index = {}
        self.offset = 0
        self.delimiter = '\n'

    @staticmethod
    def line_desp_f(file_path, line_num) -> str:
        return f"{file_path}++++{line_num}"

    @staticmethod
    def parse_desp(line_desp) -> Tuple[str,int]:
        file_path, line_num = line_desp.split("++++")
        return (file_path, int(line_num))

    def build_index(self, text_list, filename):
        with open(filename, 'w') as f:
            for text in text_list:
                length = len(text)
                f.write(text + self.delimiter)
                index_key = self.line_desp_f(filename, self.offset)
                self.index[index_key] = (filename, self.offset, length)
                self.offset += length + 1

    def search_index(self, index):
        if index in self.index:
            filename, offset, length = self.index[index]
            with open(filename, 'r') as f:
                f.seek(offset)
                return f.read(length)
        else:
            return None

    def index_single_file(self, file_path:str) -> None:
        with open(file_path, 'r') as f:
            text_list = f.read().split(self.delimiter)
            self.build_index(text_list, file_path)

    def run(self, file_paths: List[str]) -> None:
        for file_path in file_paths:
            self.index_single_file(file_path)

li = LineIndexer()
li.index_single_file('/Users/art9/Workspaces/SelfProjects/smartQA/data/404 Not Found.txt')

print(li.index)

# https://playgpt3.streamlit.app/?share=wnc5sgfo