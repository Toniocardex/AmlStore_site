#!/usr/bin/env python3
import math
import unittest

from commercial_pricing import (
    CLEAN_INTEGER_PRICE_THRESHOLD_EUR,
    format_eur_minor,
    normalize_commercial_price_minor,
)


class CommercialPricingTests(unittest.TestCase):
    def test_threshold_constant(self):
        self.assertEqual(CLEAN_INTEGER_PRICE_THRESHOLD_EUR, 50)

    def test_normalization_cases(self):
        cases = {
            0: 0,
            1990: 1990,
            3295: 3295,
            4999: 4999,
            5000: 5000,
            5001: 5100,
            8137: 8200,
            10810: 10900,
            14317: 14400,
            21105: 21200,
            37079: 37100,
            71069: 71100,
            89900: 89900,
            134827: 134900,
        }
        for raw, expected in cases.items():
            with self.subTest(raw=raw):
                self.assertEqual(normalize_commercial_price_minor(raw), expected)

    def test_non_eur_is_unchanged(self):
        self.assertEqual(normalize_commercial_price_minor(8137, "USD"), 8137)

    def test_preserve_cents_mode(self):
        self.assertEqual(
            normalize_commercial_price_minor(8137, mode="preserve-cents"), 8137
        )

    def test_manual_override_precedence(self):
        self.assertEqual(
            normalize_commercial_price_minor(
                71069, mode="manual", manual_public_price_minor=71900
            ),
            71900,
        )

    def test_manual_override_can_define_a_lower_commercial_price(self):
        self.assertEqual(
            normalize_commercial_price_minor(
                14317, mode="manual", manual_public_price_minor=13900
            ),
            13900,
        )

    def test_invalid_values(self):
        for value in (-1, 1.2, math.nan, math.inf, True):
            with self.subTest(value=value), self.assertRaises(ValueError):
                normalize_commercial_price_minor(value)

    def test_commercial_format(self):
        self.assertEqual(format_eur_minor(3295), "32,95")
        self.assertEqual(format_eur_minor(14400), "144,00")
        self.assertEqual(format_eur_minor(134900), "1.349,00")


if __name__ == "__main__":
    unittest.main()
