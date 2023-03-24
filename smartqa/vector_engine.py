from typing import List, Literal, Callable
from dataclasses import dataclass
from itertools import islice
import numpy as np
from annoy import AnnoyIndex
from .proc_data.line_indexer import LineIndexer


MetricType = Literal["angular", "euclidean", "manhattan", "hamming", "dot"]

@dataclass
class LineOffsetIndex:
    line_number :int
    offset      :int
    length      :int

    @staticmethod
    def from_line_indexer(line_indexer:LineIndexer) -> List['LineOffsetIndex']:
        res = []
        for line_number, (offset, length) in line_indexer.index.items():
            res.append(LineOffsetIndex(
                line_number=line_number,
                offset=offset,
                length=length
            ))
        return res

class VectorEngine:

    def __init__(self, 
                 dim:int, 
                 emb_fn,
                 metric:MetricType="angular",
                 tree_num=10) -> None:
        self.dim = dim
        self.tree_num = tree_num
        self.emb_fn = emb_fn
        self.index = AnnoyIndex(dim, metric=metric)
    
    def search(self, vector, n=10) -> List[int]:
        return self.index.get_nns_by_vector(vector, n=n)

    def init(self, file_path:str, indexs:List[LineOffsetIndex], batch_size=64):
        indexs.sort(key=lambda x: x.line_number)
        indexs_it = iter(indexs)
        file = open(file_path, "rb")
        file.seek(0)
        while True:
            batch_indexs = list(islice(indexs_it, batch_size))
            if not batch_indexs:
                break
            start_pos = batch_indexs[0].offset
            end_pos = batch_indexs[-1].offset + batch_indexs[-1].length
            file.seek(start_pos)
            lines = file.read(end_pos - start_pos + 1).decode().strip().splitlines()
            self.add_batch_sentence(
                list(map(lambda x:x.line_number, batch_indexs)),
                lines
            )
        self.index.build(self.tree_num)
        file.close()

    def add_batch_sentence(self, indexs:List[int], lines:List[str]) -> None:
        self.add_batch_vector(indexs, self.emb_fn(lines))

    def add_batch_vector(self, indexs:List[int], vectors:np.ndarray) -> None:

        assert len(indexs) == len(vectors)
        assert len(vectors.shape) == 2
        assert vectors.shape[1] == self.dim

        for ind,vec in zip(indexs, vectors):
            self.index.add_item(ind, vec)
        