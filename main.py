import sys
import re

def read_file(path):
    """
    读取文本文件
    """
    with open(path, "r", encoding="utf-8") as file:
        return file.read()

def clean_text(text):
    """
    文本预处理
    去除标点、空格、特殊字符
    """
    # 保留中文、英文、数字
    text = re.sub(
        r"[^a-zA-Z0-9\u4e00-\u9fa5]",
        "",
        text
    )
    return text

def create_ngram(text):

    result = set()

    for n in [2,3]:

        for i in range(len(text)-n+1):

            result.add(text[i:i+n])

    return result

def calculate_similarity(original, copy):

    """
    计算Jaccard相似度
    """
    original_set = create_ngram(original)
    copy_set = create_ngram(copy)

    # 防止空文本导致除0
    if len(original_set) == 0 or len(copy_set) == 0:
        return 0.0

    intersection = (
        original_set &
        copy_set
    )

    union = (
        original_set |
        copy_set
    )

    similarity = (
        len(intersection)
        /
        len(union)
    )

    return similarity

def main():

    # 参数检查

    if len(sys.argv) != 4:

        print(
            "Usage: python main.py 原文路径 抄袭路径 输出路径"
        )

        return


    original_path = sys.argv[1]
    copy_path = sys.argv[2]
    output_path = sys.argv[3]

    # 读取文件
    original = read_file(original_path)
    copy = read_file(copy_path)

    # 清洗
    original = clean_text(original)
    copy = clean_text(copy)

    # 计算重复率
    result = calculate_similarity(
        original,
        copy
    )

    # 保留两位小数
    answer = "{:.2f}".format(result)

    # 输出文件
    with open(
            output_path,
            "w",
            encoding="utf-8"
    ) as file:
        file.write(answer)

    print("查重完成！")
    print("重复率:", answer)
    print("结果已保存到:", output_path)


if __name__ == "__main__":
    main()
