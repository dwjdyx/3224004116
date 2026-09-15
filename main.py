import sys
import re
from difflib import SequenceMatcher

# 读取文件内容
def read_file(path):

    try:
        # 使用utf-8编码打开文件并读取
        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            return f.read()

    # 文件不存在异常处理
    except FileNotFoundError:

        print("文件不存在:", path)

        return ""

    # 其他读取异常处理
    except Exception as e:

        print("读取文件失败:", e)

        return ""

# 文本预处理函数
def clean_text(text):
    # 如果是 GitHub 网页，提取代码区域
    code_lines = re.findall(
        r'<td[^>]*class="[^"]*blob-code-inner[^"]*"[^>]*>(.*?)</td>',
        text,
        re.S
    )

    if code_lines:
        text = "\n".join(code_lines)

    # 去除 HTML 标签
    text = re.sub(r"<[^>]+>", "", text)

    # 去除 HTML 转义字符
    text = text.replace("&nbsp;", " ")
    text = text.replace("&amp;", "&")
    text = text.replace("&lt;", "<")
    text = text.replace("&gt;", ">")
    text = text.replace("&quot;", '"')

    # 只保留中文、英文、数字
    text = re.sub(r"[^\u4e00-\u9fa5a-zA-Z0-9]", "", text)

    return text


# 创建N-gram特征集合
def create_ngram(text):

    # 使用集合保存文本中的片段，自动去重
    result = set()

    # 将add函数绑定，减少循环中的查找开销
    add = result.add

    # 获取文本长度
    length = len(text)

    # 生成长度为2的连续字符片段（二元组）
    for i in range(length-1):

        add(text[i:i+2])

    # 生成长度为3的连续字符片段（三元组）
    for i in range(length-2):

        add(text[i:i+3])

    # 返回N-gram集合
    return result


# 计算两个文本的相似度
def calculate_similarity(original, copy):
    if len(copy) == 0:
        return 0.0

    matcher = SequenceMatcher(None, original, copy)

    matches = 0
    for block in matcher.get_matching_blocks():
        matches += block.size

    return matches / len(copy)


# 主函数
def main():

    # 检查命令行参数数量是否正确

    if len(sys.argv) != 4:

        print(
            "Usage: python main.py 原文路径 抄袭路径 输出路径"
        )

        return


    # 获取命令行传入的三个文件路径
    original_path = sys.argv[1]
    copy_path = sys.argv[2]
    output_path = sys.argv[3]

    # 读取原文文件和抄袭文件
    original = read_file(original_path)
    copy = read_file(copy_path)

    # 对文本进行清洗，去除无关字符
    original = clean_text(original)
    copy = clean_text(copy)

    # 计算两个文本之间的重复率
    result = calculate_similarity(
        original,
        copy
    )

    # 将结果格式化为保留两位小数
    answer = "{:.2f}".format(result)

    # 将查重结果写入输出文件
    try:
        with open(
                output_path,
                "w",
                encoding="utf-8"
        ) as f:

            # 写入相似度结果
            f.write(
                "%.2f" % result
            )

    # 输出文件异常处理
    except Exception as e:

        print(
            "输出文件失败:",
            e
        )

        return

    # 输出程序运行结果
    print("查重完成！")
    print("重复率:", answer)
    print("结果已保存到:", output_path)


# Python程序入口
if __name__ == "__main__":

    main()