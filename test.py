import unittest
from unittest.mock import mock_open, patch
from io import StringIO
from main import parse_csv, generate_payout_report  # Импортируй из своего файла

class TestEmployeeReport(unittest.TestCase):

    def setUp(self):
        self.mock_csv_data = (
            "id,name,email,hours_worked,department,rate\n"
            "1,John Doe,john@example.com,40,engineering,30\n"
            "2,Jane Smith,jane@example.com,35,sales,25\n"
        )

    def test_parse_csv(self):
        with patch("builtins.open", mock_open(read_data=self.mock_csv_data)):
            result = parse_csv("fake.csv")
            expected = [
                {
                    "id": "1",
                    "name": "John Doe",
                    "email": "john@example.com",
                    "hours_worked": "40",
                    "department": "engineering",
                    "rate": "30"
                },
                {
                    "id": "2",
                    "name": "Jane Smith",
                    "email": "jane@example.com",
                    "hours_worked": "35",
                    "department": "sales",
                    "rate": "25"
                }
            ]
            self.assertEqual(result, expected)

    def test_generate_payout_report_output(self):
        test_data = [
            {
                "id": "1",
                "name": "John Doe",
                "email": "john@example.com",
                "hours_worked": "40",
                "department": "engineering",
                "rate": "30"
            },
            {
                "id": "2",
                "name": "Jane Smith",
                "email": "jane@example.com",
                "hours_worked": "35",
                "department": "sales",
                "rate": "25"
            }
        ]

        with patch("sys.stdout", new=StringIO()) as fake_out:
            generate_payout_report(test_data)
            output = fake_out.getvalue()
            self.assertIn("engineering", output)
            self.assertIn("sales", output)
            self.assertIn("John Doe", output)
            self.assertIn("Jane Smith", output)
            self.assertIn("$1200", output)  # 40 * 30
            self.assertIn("$875", output)   # 35 * 25

if __name__ == "__main__":
    unittest.main()
