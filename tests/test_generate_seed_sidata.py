"""Tests for database/generate_seed_sidata.py utility functions."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "database"))

from generate_seed_sidata import escape_sql, int_or_null


class TestEscapeSql:
    def test_none_returns_null(self):
        assert escape_sql(None) == "NULL"

    def test_empty_string_returns_null(self):
        assert escape_sql("") == "NULL"

    def test_plain_string(self):
        assert escape_sql("hello") == "'hello'"

    def test_single_quote_escaped(self):
        assert escape_sql("it's") == "'it''s'"

    def test_multiple_single_quotes(self):
        assert escape_sql("it's a dog's life") == "'it''s a dog''s life'"

    def test_numeric_string(self):
        assert escape_sql("12345") == "'12345'"

    def test_unicode_string(self):
        assert escape_sql("Universitas Gadjah Mada") == "'Universitas Gadjah Mada'"

    def test_string_with_spaces(self):
        assert escape_sql("  padded  ") == "'  padded  '"


class TestIntOrNull:
    def test_none_returns_null(self):
        assert int_or_null(None) == "NULL"

    def test_empty_string_returns_null(self):
        assert int_or_null("") == "NULL"

    def test_whitespace_only_returns_null(self):
        assert int_or_null("   ") == "NULL"

    def test_valid_integer(self):
        assert int_or_null("42") == "42"

    def test_valid_integer_with_whitespace(self):
        assert int_or_null("  100  ") == "100"

    def test_non_numeric_returns_null(self):
        assert int_or_null("abc") == "NULL"

    def test_float_string_returns_null(self):
        assert int_or_null("3.14") == "NULL"

    def test_zero(self):
        assert int_or_null("0") == "0"

    def test_negative_integer(self):
        assert int_or_null("-5") == "-5"

    def test_large_number(self):
        assert int_or_null("999999") == "999999"
