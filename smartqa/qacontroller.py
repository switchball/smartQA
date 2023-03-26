from typing import List
from .bootstrap import get_static_resource
from .embedding import embedding_paragraph_bert_batched


class QAController:

    def __init__(self, show_lines=5, threshold=None) -> None:
        self.index, self.vector_engine = get_static_resource()
        self.show_lines = show_lines
        self.threshold = threshold

    def process(self, line:str) -> List[str]:
        res = []
        vector = embedding_paragraph_bert_batched([line])[0]
        indexs = self.vector_engine.search(vector, self.show_lines, threshold=self.threshold)
        for ind in indexs:
            res.append(
                self.index.search_index(ind)
            )
        return res 
