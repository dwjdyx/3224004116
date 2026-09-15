import unittest
import sys
from main import (
    read_file,
    clean_text,
    calculate_similarity,
    main
)

class TestMain(unittest.TestCase):

    def test_read_file(self):
        with open("test.txt","w",encoding="utf-8") as f:
            f.write("机器人控制系统")

        self.assertEqual(
            read_file("test.txt"),
            "机器人控制系统"
        )


    def test_clean_text(self):

        result = clean_text(
            "机器人控制系统，运行正常！"
        )

        self.assertEqual(
            result,
            "机器人控制系统运行正常"
        )


    def test_same_text(self):

        self.assertEqual(
            calculate_similarity(
                "机器人控制系统",
                "机器人控制系统"
            ),
            1.0
        )


    def test_different_text(self):

        self.assertEqual(
            calculate_similarity(
                "机器人控制",
                "天气分析"
            ),
            0
        )


    def test_add_text(self):

        self.assertGreater(
            calculate_similarity(
                "机器人控制系统",
                "机器人控制系统增加功能"
            ),
            0
        )


    def test_delete_text(self):

        self.assertGreater(
            calculate_similarity(
                "机器人控制系统可以自动运行",
                "机器人控制系统"
            ),
            0
        )


    def test_empty_text(self):

        self.assertEqual(
            calculate_similarity(
                "",
                "机器人"
            ),
            0
        )


    def test_file_not_exist(self):

        self.assertEqual(
            read_file(
                "none.txt"
            ),
            ""
        )


    def test_main_output(self):

        with open("orig.txt","w",encoding="utf-8") as f:
            f.write("机器人控制系统")

        with open("copy.txt","w",encoding="utf-8") as f:
            f.write("机器人控制系统")


        sys.argv=[
            "main.py",
            "orig.txt",
            "copy.txt",
            "answer.txt"
        ]

        main()

        with open(
            "answer.txt",
            encoding="utf-8"
        ) as f:

            result=f.read()

        self.assertEqual(
            result,
            "1.00"
        )


if __name__ == "__main__":
    unittest.main()