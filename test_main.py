import unittest
import tempfile
import os
import subprocess
import sys

# 导入待测试的文本处理函数
from main import clean_text
from main import create_ngram
from main import calculate_similarity
from main import read_file
# 导入主程序函数，用于测试完整运行流程
from main import main

# 创建测试类，继承unittest.TestCase
class TestPaperCheck(unittest.TestCase):

    # 1. 测试文本清洗功能
    def test_clean_text(self):

        # 构造包含标点符号的测试文本
        text = "你好，世界！"

        # 调用文本清洗函数
        result = clean_text(text)

        # 判断清洗结果是否符合预期
        self.assertEqual(
            result,
            "你好世界"
        )


    # 2. 测试英文和数字是否能够正常保留
    def test_clean_english(self):

        # 构造包含英文、数字和中文的文本
        text = "ESP32测试"

        # 调用清洗函数
        result = clean_text(text)

        # 检查英文和数字是否被保留
        self.assertEqual(
            result,
            "ESP32测试"
        )


    # 3. 测试完全相同文本的相似度
    def test_same_text(self):

        # 两个完全相同的文本相似度应该为1
        result = calculate_similarity(
            "机器人控制系统",
            "机器人控制系统"
        )

        self.assertEqual(
            result,
            1.0
        )


    # 4. 测试完全不同文本的相似度
    def test_different_text(self):

        # 两个没有共同片段的文本相似度应该为0
        result = calculate_similarity(
            "机器人",
            "苹果香蕉"
        )

        self.assertEqual(
            result,
            0.0
        )


    # 5. 测试增加部分内容后的文本相似度
    def test_add_text(self):

        # 第二个文本在第一个文本基础上增加内容
        result = calculate_similarity(
            "嵌入式机器人",
            "嵌入式机器人系统"
        )

        # 增加内容后仍然应该存在相似部分
        self.assertGreater(
            result,
            0
        )


    # 6. 测试空文本情况
    def test_empty_text(self):

        # 两个空文本进行比较
        result = calculate_similarity(
            "",
            ""
        )

        # 空文本返回0，避免除0错误
        self.assertEqual(
            result,
            0.0
        )


    # 7. 测试ngram特征生成
    def test_ngram_length(self):

        # 对字符串生成ngram集合
        result = create_ngram(
            "abcdef"
        )

        # 判断生成结果不为空
        self.assertGreater(
            len(result),
            0
        )


    # 8. 测试长度不足的文本生成ngram
    def test_short_text(self):

        # 一个字符无法组成二元或三元片段
        result = create_ngram(
            "a"
        )

        # 结果集合应该为空
        self.assertEqual(
            len(result),
            0
        )


    # 9. 测试中文文本相似度计算
    def test_chinese_text(self):

        # 测试中文内容完全一致情况
        result = calculate_similarity(
            "四足机器人运动控制",
            "四足机器人运动控制"
        )

        self.assertEqual(
            result,
            1.0
        )


    # 10. 测试文本部分修改情况
    def test_modify_text(self):

        # 两个文本存在部分相同内容
        result = calculate_similarity(
            "嵌入式系统开发",
            "嵌入式软件开发"
        )

        # 修改后仍应该存在一定相似度
        self.assertGreater(
            result,
            0
        )


    # 11. 测试完整程序运行流程
    def test_main_run(self):

        import sys

        # 模拟命令行输入参数
        sys.argv = [
            "main.py",
            "test/orig.txt",
            "test/orig_add.txt",
            "test/result.txt"
        ]

        # 调用主程序
        main()

        # 读取程序生成的结果文件
        with open(
                "test/result.txt",
                "r",
                encoding="utf-8"
        ) as f:

            result = f.read()

        # 判断输出文件是否生成内容
        self.assertTrue(
            len(result) > 0
        )


    # 12. 测试命令行参数数量错误情况
    def test_wrong_argument(self):

        import sys

        # 设置错误数量的参数
        sys.argv = [
            "main.py"
        ]

        # 调用主程序测试异常处理
        main()


    # 13. 测试文件不存在情况
    def test_file_not_exist(self):

        # 测试读取不存在文件
        result = read_file(
            "not_exist.txt"
        )

        # 文件不存在时应该返回空字符串
        self.assertEqual(
            result,
            ""
        )


    # 14. 测试空文本生成ngram
    def test_empty_ngram(self):

        # 空字符串生成ngram
        result = create_ngram("")

        # 空文本不应该生成任何片段
        self.assertEqual(
            len(result),
            0
        )


    # 15. 测试空抄袭文本情况
    def test_empty_copy(self):

        # 原文本存在，抄袭文本为空
        result = calculate_similarity(
            "机器人控制系统",
            ""
        )

        # 空文本参与比较时返回0
        self.assertEqual(
            result,
            0
        )


# Python文件直接运行时执行测试
if __name__ == "__main__":

    unittest.main()