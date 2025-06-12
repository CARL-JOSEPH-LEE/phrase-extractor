import sys
import jieba
import re

# 支持的断句标点集合
SENTENCE_DELIMITERS = r'[，。；？！\n：“”（）《》、]'

def split_text_into_sentences(text):
    """使用正则表达式根据多种标点切分句子，并去除标点和空白"""
    sentences = re.split(SENTENCE_DELIMITERS, text)
    return [s.strip() for s in sentences if s.strip()]

def generate_phrases_with_jieba(sentence, min_len=2, max_len=7):
    """使用jieba分词后，生成所有连续词语组合的短语"""
    words = list(jieba.cut(sentence, cut_all=False))  # 精确模式分词
    n = len(words)
    phrases = set()

    # 遍历所有可能的词语连续组合
    for i in range(n):
        current_length = 0
        phrase = ""
        for j in range(i, n):
            word = words[j]
            # 如果当前词是“的、得、地”，跳过该组合
            if word in ["的", "得", "地"]:
                break
            phrase += word
            current_length += len(word)

            if current_length > max_len:
                break
            if current_length >= min_len:
                phrases.add(phrase)

    return phrases

def main():
    all_phrases = set()

    # 读取整个输入文本
    text = sys.stdin.read().strip()

    # 切分成句子
    sentences = split_text_into_sentences(text)

    # 对每个句子提取短语
    for sentence in sentences:
        phrases = generate_phrases_with_jieba(sentence)
        all_phrases.update(phrases)

    # 按长度和字典序排序输出
    sorted_phrases = sorted(all_phrases, key=lambda x: (len(x), x))

    # 输出结果
    for phrase in sorted_phrases:
        print(phrase)

if __name__ == '__main__':
    main()