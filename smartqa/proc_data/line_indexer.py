from typing import Dict, Tuple, List, Union
import os, shutil
from concurrent.futures import ThreadPoolExecutor


class LineIndexer:

    def __init__(self, file_path:str) -> None:
        self.index = {}
        self.lines = 0
        self.offset = 0
        self.delimiter = b"\n"
        self.file_path = file_path
        self.file = None
        self.pool = ThreadPoolExecutor(64)

    def build_index(self, text_list:List[Union[bytes,str]]):
        for text in text_list:
            if isinstance(text, str):
                text = text.encode("utf-8")
            length = len(text)
            self.file.write(text + self.delimiter)
            self.index[self.lines] = (self.offset, length)
            self.lines += 1
            self.offset += length + 1

    def search_index(self, index) -> str:
        if index < self.lines:
            offset, length = self.index[index]
            self.file.seek(offset)
            return self.file.read(length).decode("utf-8")
        else:
            return None

    def index_single_file(self, file_path:str) -> None:
        with open(file_path, 'rb') as f:
            text_list = f.read().splitlines()
            self.build_index(text_list)

    def init(self, file_paths: List[str], proc_func=None) -> None:
        self.file = open(self.file_path, "wb")
        tmp_dir = "tmp"
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)

        if proc_func is not None:
            n_file_paths = [
                os.path.join(tmp_dir, os.path.basename(p))
                for p in file_paths
            ]
            list(self.pool.map(proc_func, file_paths, n_file_paths))
            file_paths = n_file_paths

        for file_path in file_paths:
            self.index_single_file(file_path)
        self.file.close()
        shutil.rmtree(tmp_dir)
        self.file = open(self.file_path, "rb")

    def save(self):
        pass

    def load(self, path):
        pass

    

# https://playgpt3.streamlit.app/?share=wnc5sgfo