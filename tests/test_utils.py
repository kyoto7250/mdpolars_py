import unittest

from polars import read_csv
from polars.testing import assert_frame_equal

from mdpolars import utils


class TestUtils(unittest.TestCase):
    def test_simple_pattern_from_md(self):
        df = utils.from_md(
            """
            | Syntax    | Description |
            | --------- | ----------- |
            | Header    | Title       |
            | Paragraph | Text        |
            """
        )
        assert_frame_equal(df, read_csv("tests/fixtures/simple_pattern.csv"))

        df = utils.from_md(
            """
            +------------+-------------+
            | Syntax     | Description |
            +------------+-------------+
            | Header     | Title       |
            | Paragraph  | Text        |
            +------------+-------------+
            """
        )
        assert_frame_equal(df, read_csv("tests/fixtures/simple_pattern.csv"))

        df = utils.from_md(
            """
            | Syntax    | Description |
            | :-------- | ----------: |
            | Header    | Title       |
            | Paragraph | Text        |
            """
        )
        assert_frame_equal(df, read_csv("tests/fixtures/simple_pattern.csv"))

    def test_header_only_from_md(self) -> None:
        df = utils.from_md(
            """
            | Syntax    | Description |
            | --------- | ----------- |
            """
        )
        assert_frame_equal(df, read_csv("tests/fixtures/header_only.csv"))

        df = utils.from_md(
            """
            +------------+-------------+
            | Syntax     | Description |
            +------------+-------------+
            """
        )
        assert_frame_equal(df, read_csv("tests/fixtures/header_only.csv"))

        df = utils.from_md(
            """
            | Syntax    | Description |
            | :-------- | ----------: |
            """
        )
        assert_frame_equal(df, read_csv("tests/fixtures/header_only.csv"))

    def test_one_column_from_md(self):
        df = utils.from_md(
            """
            | Syntax    |
            | --------- |
            | Header    |
            | Paragraph |
            """
        )
        assert_frame_equal(df, read_csv("tests/fixtures/one_column.csv"))

        df = utils.from_md(
            """
            +------------+
            | Syntax     |
            +------------+
            | Header     |
            | Paragraph  |
            +------------+
            """
        )
        assert_frame_equal(df, read_csv("tests/fixtures/one_column.csv"))

        df = utils.from_md(
            """
            | Syntax    |
            | :-------- |
            | Header    |
            | Paragraph |
            """
        )
        assert_frame_equal(df, read_csv("tests/fixtures/one_column.csv"))

    def test_one_column_header_only_from_md(self):
        df = utils.from_md(
            """
            | Syntax    |
            | --------- |
            """
        )
        assert_frame_equal(df, read_csv("tests/fixtures/one_column_header_only.csv"))
        df = utils.from_md(
            """
            +------------+
            | Syntax     |
            +------------+
            """
        )
        assert_frame_equal(df, read_csv("tests/fixtures/one_column_header_only.csv"))

        df = utils.from_md(
            """
            | Syntax    |
            | :-------- |
            """
        )
        assert_frame_equal(df, read_csv("tests/fixtures/one_column_header_only.csv"))

    def test_no_header_from_md(self):
        df = utils.from_md(
            """
            | Syntax    | Description |
            """
        )
        assert_frame_equal(
            df, read_csv("tests/fixtures/header_only.csv", has_header=False)
        )

        df = utils.from_md(
            """
            | Syntax    | Description |
            | Header    | Title       |
            | Paragraph | Text        |
            """
        )
        assert_frame_equal(
            df, read_csv("tests/fixtures/simple_pattern.csv", has_header=False)
        )

    def test_with_header_from_md(self):
        df = utils.from_md(
            """
            | Column 1  | Column 2    |
            | --------- | ----------- |
            | Header    | Title       |
            | Paragraph | Text        |
            """,
            schema=["Syntax", "Description"],
        )
        assert_frame_equal(df, read_csv("tests/fixtures/simple_pattern.csv"))
