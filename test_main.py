import unittest
import tempfile
import os
import subprocess
import sys

from main import clean_text
from main import create_ngram
from main import calculate_similarity
from main import main

class TestPaperCheck(unittest.TestCase):

    # 1. 测试文本清洗
    def test_clean_text(self):

        text = "你好，世界！"

        result = clean_text(text)

        self.assertEqual(
            result,
            "你好世界"
        )

    # 2. 测试英文保留
    def test_clean_english(self):

        text = "ESP32测试"

        result = clean_text(text)

        self.assertEqual(
            result,
            "ESP32测试"
        )

    # 3. 测试完全相同文本
    def test_same_text(self):

        result = calculate_similarity(
            "机器人控制系统",
            "机器人控制系统"
        )

        self.assertEqual(
            result,
            1.0
        )

    # 4. 测试完全不同文本
    def test_different_text(self):

        result = calculate_similarity(
            "机器人",
            "苹果香蕉"
        )

        self.assertEqual(
            result,
            0.0
        )

    # 5. 测试增加内容
    def test_add_text(self):

        result = calculate_similarity(
            "嵌入式机器人",
            "嵌入式机器人系统"
        )

        self.assertGreater(
            result,
            0
        )

    # 6. 测试空文本
    def test_empty_text(self):

        result = calculate_similarity(
            "",
            ""
        )

        self.assertEqual(
            result,
            0.0
        )

    # 7. 测试ngram生成数量
    def test_ngram_length(self):

        result = create_ngram(
            "abcdef"
        )

        self.assertGreater(
            len(result),
            0
        )

    # 8. 测试短文本
    def test_short_text(self):

        result = create_ngram(
            "a"
        )

        self.assertEqual(
            len(result),
            0
        )

    # 9. 测试中文文本
    def test_chinese_text(self):

        result = calculate_similarity(
            "四足机器人运动控制",
            "四足机器人运动控制"
        )

        self.assertEqual(
            result,
            1.0
        )

    # 10. 测试部分修改文本
    def test_modify_text(self):
        result = calculate_similarity(
            "嵌入式系统开发",
            "嵌入式软件开发"
        )
        self.assertGreater(
            result,
            0
        )

    # 11.测试完整程序运行
    def test_main_run(self):
        import sys

        sys.argv = [
            "main.py",
            "test/orig.txt",
            "test/orig_add.txt",
            "test/result.txt"
        ]

        main()

        with open(
                "test/result.txt",
                "r",
                encoding="utf-8"
        ) as f:
            result = f.read()

        self.assertTrue(
            len(result) > 0
        )

    #12. 测试参数错误
    def test_wrong_argument(self):
        import sys

        sys.argv = [
            "main.py"
        ]

        main()

if __name__ == "__main__":
    unittest.main()