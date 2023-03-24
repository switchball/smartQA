import os
from glob import glob
from functools import lru_cache
from .config import RAW_TEXT_DIR, ASSETS_DIR
from ..proc_data.raw_text_proc import RawTextProcessor
from ..proc_data.line_indexer import LineIndexer
from ..embedding import embedding_paragraph_bert_batched
from ..vector_engine import VectorEngine, LineOffsetIndex


@lru_cache
def get_static_resource():

    text_processor = RawTextProcessor()
    line_indexer = LineIndexer("data/assets/line_indexer.txt")
    line_indexer.init(glob(os.path.join("data/text", "*.txt")), text_processor.proc_file)

    vector_engine = VectorEngine(384, emb_fn=embedding_paragraph_bert_batched)
    vector_engine.init(line_indexer.file_path, LineOffsetIndex.from_line_indexer(line_indexer))

    return line_indexer, vector_engine

