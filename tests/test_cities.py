import ee_interface_function as eef
from src.ee_interface_function import cities
import unittest
import pytest

def test_cities_missingfile():
    with pytest.raises(FileNotFoundError) as exc_info:
        cities("empty") 
        assert "No such file or directory" in str(exc_info)










# def test_abakaliki_coordinates(self):
#         test_file_path = "cities.txt"

#         # Call the cities function with the test file path
#         city_data = cities(file_path=test_file_path)

#         # Check if Abakaliki is present in the city data
#         self.assertIn("Abakaliki", city_data)

#         # Check the latitude and longitude of Abakaliki
#         abakaliki_data = city_data["Abakaliki"]
#         expected_latitude = 6.3242  # Replace with the expected latitude
#         expected_longitude = 7.1139  # Replace with the expected longitude

#         # Assert the values are approximately equal (adjust the delta as needed)
#         self.assertAlmostEqual(abakaliki_data["latitude"], expected_latitude, delta=0.001)
#         self.assertAlmostEqual(abakaliki_data["longitude"], expected_longitude, delta=0.001)

# if __name__ == '__main__':
#     unittest.main()