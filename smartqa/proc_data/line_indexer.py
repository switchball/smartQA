from typing import Dict, Tuple


class LineIndexer:

    def __init__(self) -> None:
        self.index = 0
        self.index_line_desp:Dict[int,str] = {}
    
    @staticmethod
    def line_desp_f(file_path, line_num) -> str:
        return f"{file_path}++++{line_num}"
    
    def parse_desp(line_desp) -> Tuple[str,int]:
        pass

    def index_single_file(self, file_path) -> None:
        pass

    def run():
        pass