import re
import numpy as np 
import openai
from concurrent.futures import ThreadPoolExecutor
from transformers import AutoTokenizer, AutoModel


pool = ThreadPoolExecutor(128)
model_name = 'bert-base-uncased'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

def split_article(article:str, max_length:int=2048):
    # 清理文章文本，去掉多余的空格和换行符
    article = re.sub('\s+', ' ', article).strip()

    # 将文章分割成多个短段落
    paragraphs = []
    while len(article) > 0:
        if len(article) <= max_length:
            paragraphs.append(article)
            break
        else:
            # 寻找最后一个完整的句子
            last_sentence = article[:max_length].rfind('.')
            last_sentence = max(last_sentence, article[:max_length].rfind('。'))
            if last_sentence == -1:
                last_sentence = max_length
            paragraphs.append(article[:last_sentence])
            article = article[last_sentence+1:].strip()
    return paragraphs


def embedding_paragraph_openai(article:str):

    # 设置OpenAI API密钥
    openai.api_key = "YOUR_API_KEY"

    # 清理文章文本，去掉多余的空格和换行符
    article = re.sub('\s+', ' ', article).strip()

    # 使用OpenAI API进行向量化
    response = openai.Embedding.create(
        engine="text-davinci-002",
        input=article
    )

    # 提取向量
    vector = response["data"][0]["embedding"]
    return vector

def embedding_paragraph_bert(text:str):

    # 使用tokenizer将文本转换为模型输入格式
    inputs = tokenizer(text, return_tensors='pt')

    # 将模型输入传递给BERT模型，获取文本的嵌入
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state[0]

    # 输出结果
    t = embeddings.mean(dim=0)
    t = t.detach().numpy()
    return t.tolist()


def embedding_article(article:str, embedding_f):

    paragraphs = split_article(article)
    res = np.vstack(list(
        pool.map(embedding_f, paragraphs)
    ))
    return np.average(res, axis=0)
