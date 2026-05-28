"""Unit tests for Provider Foundation (#1)."""

import unittest
from providers.base import ProviderError, ProviderParseError, ProviderMetadata, SignalProvider
from providers._coerce import _coerce_float, _coerce_int


class TestProviderErrorHierarchy(unittest.TestCase):
    def test_provider_error_is_runtime_error_subclass(self):
        self.assertTrue(issubclass(ProviderError, RuntimeError))

    def test_provider_parse_error_is_provider_error_subclass(self):
        self.assertTrue(issubclass(ProviderParseError, ProviderError))

    def test_provider_parse_error_can_be_raised_and_caught(self):
        with self.assertRaises(ProviderParseError) as ctx:
            raise ProviderParseError("parse failed")
        self.assertEqual(str(ctx.exception), "parse failed")


class TestCoerceFloat(unittest.TestCase):
    def test_returns_none_for_nan(self):
        self.assertIsNone(_coerce_float(float('nan')))

    def test_returns_none_for_inf(self):
        self.assertIsNone(_coerce_float(float('inf')))

    def test_returns_none_for_negative_inf(self):
        self.assertIsNone(_coerce_float(float('-inf')))

    def test_returns_none_for_none(self):
        self.assertIsNone(_coerce_float(None))

    def test_returns_float_for_valid_string(self):
        self.assertEqual(_coerce_float("3.14"), 3.14)

    def test_returns_float_for_valid_int(self):
        self.assertEqual(_coerce_float(42), 42.0)


class TestCoerceInt(unittest.TestCase):
    def test_returns_none_for_none(self):
        self.assertIsNone(_coerce_int(None))

    def test_returns_int_for_valid_string(self):
        self.assertEqual(_coerce_int("42"), 42)

    def test_returns_int_for_valid_float(self):
        self.assertEqual(_coerce_int(42.9), 42)

    def test_raises_value_error_for_invalid_string(self):
        with self.assertRaises(ValueError):
            _coerce_int("not a number")


class TestSignalProviderAbstract(unittest.TestCase):
    def test_cannot_instantiate_directly(self):
        with self.assertRaises(TypeError):
            SignalProvider()


class TestProviderMetadata(unittest.TestCase):
    def test_is_frozen(self):
        meta = ProviderMetadata(provider_id="test", display_name="Test", capabilities=())
        with self.assertRaises(Exception):
            meta.provider_id = "modified"

    def test_describe_returns_metadata(self):
        # Create a concrete subclass for testing
        class ConcreteProvider(SignalProvider):
            provider_id = "test_provider"
            display_name = "Test Provider"
            capabilities = ("test",)

            def search_abbreviation(self, abbrev: str) -> list:
                return []

        provider = ConcreteProvider()
        meta = provider.describe()
        self.assertEqual(meta.provider_id, "test_provider")
        self.assertEqual(meta.display_name, "Test Provider")
        self.assertEqual(meta.capabilities, ("test",))


if __name__ == "__main__":
    unittest.main()