import re 
from dataclasses import dataclass
from typing import List


@dataclass
class RawTextMeta:
    """
    ---
    db: xpaidia
    title: {title}
    link: {url}
    category: default
    pinned: false
    ---
    """
    db      :str
    title   :str
    link    :str
    category:str
    pinned  :str



class RawTextProcessor:

    def __init__(
        self,
        paragraph_start="^#",
        min_line_chars=20,
        min_token_num=6
    ) -> None:
        
        self.paragraph_start_rg = paragraph_start
        self.min_line_chars = min_line_chars
        self.min_token_num = min_token_num


    @staticmethod
    def extract_meta(text:str) -> RawTextMeta:
        rg_expr = (
            r"\-\-\-\s"
            r"db: (?P<db>\w*)\n"
            r"title: (?P<title>.*)\n"
            r"link: (?P<link>[^\s]+)\n"
            r"category: (?P<category>\w*)\n"
            r"pinned: (?P<pinned>\w*)\n"
            r"\-\-\-"
        )
        matchobj = re.search(rg_expr, text)

        if matchobj is None:
            return None
        
        return RawTextMeta(**matchobj.groupdict())
    
    def if_line_dirty(self, line:str) -> bool:
        
        if re.search(self.paragraph_start_rg, line):
            return False

        if len(line) < self.min_line_chars:
            return True
        
        matchobj = re.search(
            "[\\u4e00-\\u9fa5]{%d,}|([a-zA-Z]+\\s){%d,}" %(
                self.min_token_num, self.min_token_num
            ), 
            line)
        if matchobj is None:
            return True
        
        return False

    def proc_raw_text(self, text:str) -> str:
        lines = text.splitlines()
        lines = [l.strip() for l in lines if l.strip()]
        fn = lambda l : not self.if_line_dirty(l)
        return list(filter(fn, lines))

    def merge_paragraph_title(self, lines:List[str]) -> List[str]:
        res = []
        last_title_flag = False
        for line in reversed(lines):
            if re.search(self.paragraph_start_rg, line) and not last_title_flag:
                if res:
                    res[-1] = line.strip('#').strip().strip(".。")\
                                + "。" + res[-1]
                else:
                    res.append(
                        line.strip('#').strip().strip(".。") + "。"
                    )
                last_title_flag = True
            else:
                if re.search(self.paragraph_start_rg, line):
                    line = line.strip('#').strip().strip(".。") + "。"
                    last_title_flag = True
                else:
                    
                    last_title_flag = False
                res.append(line.strip())
                
        return list(reversed(res))
