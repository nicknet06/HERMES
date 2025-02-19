# from app import app
# from models import db, EmergencyService
# from datetime import datetime
# from sqlalchemy import inspect
# # Empty array for emergency services in Greece - to be populated
# services = [
#     {
#       "name": "Athens General Hospital",
#       "service_type": "hospital",
#       "city": "Athens",
#       "latitude": 37.95,
#       "longitude": 23.72,
#       "address": "Athens General Hospital Address",
#       "phone": "+30 210100000"
#     },
#     {
#       "name": "Athens Police Department",
#       "service_type": "police",
#       "city": "Athens",
#       "latitude": 37.98,
#       "longitude": 23.68,
#       "address": "Athens Police Department Address",
#       "phone": "+30 210200000"
#     },
#     {
#       "name": "Athens Fire Department 1",
#       "service_type": "fire",
#       "city": "Athens",
#       "latitude": 37.92,
#       "longitude": 23.80,
#       "address": "Athens Fire Department Address 1",
#       "phone": "199"
#     },
#     {
#       "name": "Athens Fire Department 2",
#       "service_type": "fire",
#       "city": "Athens",
#       "latitude": 38.00,
#       "longitude": 23.75,
#       "address": "Athens Fire Department Address 2",
#       "phone": "199"
#     },
#     {
#       "name": "Thessaloniki General Hospital",
#       "service_type": "hospital",
#       "city": "Thessaloniki",
#       "latitude": 40.65,
#       "longitude": 22.93,
#       "address": "Thessaloniki General Hospital Address",
#       "phone": "+30 210100001"
#     },
#     {
#       "name": "Thessaloniki Police Department",
#       "service_type": "police",
#       "city": "Thessaloniki",
#       "latitude": 40.68,
#       "longitude": 22.95,
#       "address": "Thessaloniki Police Department Address",
#       "phone": "+30 210200001"
#     },
#     {
#       "name": "Thessaloniki Fire Department 1",
#       "service_type": "fire",
#       "city": "Thessaloniki",
#       "latitude": 40.62,
#       "longitude": 22.92,
#       "address": "Thessaloniki Fire Department Address 1",
#       "phone": "199"
#     },
#     {
#       "name": "Thessaloniki Fire Department 2",
#       "service_type": "fire",
#       "city": "Thessaloniki",
#       "latitude": 40.66,
#       "longitude": 22.97,
#       "address": "Thessaloniki Fire Department Address 2",
#       "phone": "199"
#     },
#     {
#       "name": "Patras General Hospital",
#       "service_type": "hospital",
#       "city": "Patras",
#       "latitude": 38.25,
#       "longitude": 21.75,
#       "address": "Patras General Hospital Address",
#       "phone": "+30 210100002"
#     },
#     {
#       "name": "Patras Police Department",
#       "service_type": "police",
#       "city": "Patras",
#       "latitude": 38.27,
#       "longitude": 21.77,
#       "address": "Patras Police Department Address",
#       "phone": "+30 210200002"
#     },
#     {
#       "name": "Patras Fire Department 1",
#       "service_type": "fire",
#       "city": "Patras",
#       "latitude": 38.22,
#       "longitude": 21.72,
#       "address": "Patras Fire Department Address 1",
#       "phone": "199"
#     },
#     {
#       "name": "Patras Fire Department 2",
#       "service_type": "fire",
#       "city": "Patras",
#       "latitude": 38.29,
#       "longitude": 21.78,
#       "address": "Patras Fire Department Address 2",
#       "phone": "199"
#     },
#     {
#       "name": "Heraklion General Hospital",
#       "service_type": "hospital",
#       "city": "Heraklion",
#       "latitude": 35.33,
#       "longitude": 25.15,
#       "address": "Heraklion General Hospital Address",
#       "phone": "+30 210100003"
#     },
#     {
#       "name": "Heraklion Police Department",
#       "service_type": "police",
#       "city": "Heraklion",
#       "latitude": 35.35,
#       "longitude": 25.12,
#       "address": "Heraklion Police Department Address",
#       "phone": "+30 210200003"
#     },
#     {
#       "name": "Heraklion Fire Department 1",
#       "service_type": "fire",
#       "city": "Heraklion",
#       "latitude": 35.31,
#       "longitude": 25.18,
#       "address": "Heraklion Fire Department Address 1",
#       "phone": "199"
#     },
#     {
#       "name": "Heraklion Fire Department 2",
#       "service_type": "fire",
#       "city": "Heraklion",
#       "latitude": 35.37,
#       "longitude": 25.17,
#       "address": "Heraklion Fire Department Address 2",
#       "phone": "199"
#     },
#     {
#       "name": "Larissa General Hospital",
#       "service_type": "hospital",
#       "city": "Larissa",
#       "latitude": 39.63,
#       "longitude": 22.42,
#       "address": "Larissa General Hospital Address",
#       "phone": "+30 210100004"
#     },
#     {
#       "name": "Larissa Police Department",
#       "service_type": "police",
#       "city": "Larissa",
#       "latitude": 39.66,
#       "longitude": 22.44,
#       "address": "Larissa Police Department Address",
#       "phone": "+30 210200004"
#     },
#     {
#       "name": "Larissa Fire Department 1",
#       "service_type": "fire",
#       "city": "Larissa",
#       "latitude": 39.62,
#       "longitude": 22.41,
#       "address": "Larissa Fire Department Address 1",
#       "phone": "199"
#     },
#     {
#       "name": "Larissa Fire Department 2",
#       "service_type": "fire",
#       "city": "Larissa",
#       "latitude": 39.67,
#       "longitude": 22.43,
#       "address": "Larissa Fire Department Address 2",
#       "phone": "199"
#     },
#     {
#       "name": "Volos General Hospital",
#       "service_type": "hospital",
#       "city": "Volos",
#       "latitude": 39.36,
#       "longitude": 22.94,
#       "address": "Volos General Hospital Address",
#       "phone": "+30 210100005"
#     },
#     {
#       "name": "Volos Police Department",
#       "service_type": "police",
#       "city": "Volos",
#       "latitude": 39.37,
#       "longitude": 22.93,
#       "address": "Volos Police Department Address",
#       "phone": "+30 210200005"
#     },
#     {
#       "name": "Volos Fire Department 1",
#       "service_type": "fire",
#       "city": "Volos",
#       "latitude": 39.35,
#       "longitude": 22.95,
#       "address": "Volos Fire Department Address 1",
#       "phone": "199"
#     },
#     {
#       "name": "Volos Fire Department 2",
#       "service_type": "fire",
#       "city": "Volos",
#       "latitude": 39.36,
#       "longitude": 22.93,
#       "address": "Volos Fire Department Address 2",
#       "phone": "199"
#     },
#     {
#       "name": "Ioannina General Hospital",
#       "service_type": "hospital",
#       "city": "Ioannina",
#       "latitude": 39.66,
#       "longitude": 20.85,
#       "address": "Ioannina General Hospital Address",
#       "phone": "+30 210100006"
#     },
#     {
#       "name": "Ioannina Police Department",
#       "service_type": "police",
#       "city": "Ioannina",
#       "latitude": 39.67,
#       "longitude": 20.86,
#       "address": "Ioannina Police Department Address",
#       "phone": "+30 210200006"
#     },
#     {
#       "name": "Ioannina Fire Department 1",
#       "service_type": "fire",
#       "city": "Ioannina",
#       "latitude": 39.65,
#       "longitude": 20.82,
#       "address": "Ioannina Fire Department Address 1",
#       "phone": "199"
#     },
#     {
#       "name": "Ioannina Fire Department 2",
#       "service_type": "fire",
#       "city": "Ioannina",
#       "latitude": 39.68,
#       "longitude": 20.88,
#       "address": "Ioannina Fire Department Address 2",
#       "phone": "199"
#     },
#     {
#       "name": "Kavala General Hospital",
#       "service_type": "hospital",
#       "city": "Kavala",
#       "latitude": 40.93,
#       "longitude": 24.42,
#       "address": "Kavala General Hospital Address",
#       "phone": "+30 210100007"
#     },
#     {
#       "name": "Kavala Police Department",
#       "service_type": "police",
#       "city": "Kavala",
#       "latitude": 40.95,
#       "longitude": 24.43,
#       "address": "Kavala Police Department Address",
#       "phone": "+30 210200007"
#     },
#     {
#       "name": "Kavala Fire Department 1",
#       "service_type": "fire",
#       "city": "Kavala",
#       "latitude": 40.91,
#       "longitude": 24.40,
#       "address": "Kavala Fire Department Address 1",
#       "phone": "199"
#     },
#     {
#       "name": "Kavala Fire Department 2",
#       "service_type": "fire",
#       "city": "Kavala",
#       "latitude": 40.97,
#       "longitude": 24.44,
#       "address": "Kavala Fire Department Address 2",
#       "phone": "199"
#     },
#     {
#       "name": "Chania General Hospital",
#       "service_type": "hospital",
#       "city": "Chania",
#       "latitude": 35.50,
#       "longitude": 24.02,
#       "address": "Chania General Hospital Address",
#       "phone": "+30 210100008"
#     },
#     {
#       "name": "Chania Police Department",
#       "service_type": "police",
#       "city": "Chania",
#       "latitude": 35.53,
#       "longitude": 24.04,
#       "address": "Chania Police Department Address",
#       "phone": "+30 210200008"
#     },
#     {
#       "name": "Chania Fire Department 1",
#       "service_type": "fire",
#       "city": "Chania",
#       "latitude": 35.48,
#       "longitude": 24.01,
#       "address": "Chania Fire Department Address 1",
#       "phone": "199"
#     },
#     {
#       "name": "Chania Fire Department 2",
#       "service_type": "fire",
#       "city": "Chania",
#       "latitude": 35.54,
#       "longitude": 24.05,
#       "address": "Chania Fire Department Address 2",
#       "phone": "199"
#     },
#     {
#       "name": "Kalamata General Hospital",
#       "service_type": "hospital",
#       "city": "Kalamata",
#       "latitude": 37.04,
#       "longitude": 22.12,
#       "address": "Kalamata General Hospital Address",
#       "phone": "+30 210100009"
#     },
#     {
#       "name": "Kalamata Police Department",
#       "service_type": "police",
#       "city": "Kalamata",
#       "latitude": 37.06,
#       "longitude": 22.14,
#       "address": "Kalamata Police Department Address",
#       "phone": "+30 210200009"
#     },
#     {
#       "name": "Kalamata Fire Department 1",
#       "service_type": "fire",
#       "city": "Kalamata",
#       "latitude": 37.02,
#       "longitude": 22.11,
#       "address": "Kalamata Fire Department Address 1",
#       "phone": "199"
#     },
#     {
#       "name": "Kalamata Fire Department 2",
#       "service_type": "fire",
#       "city": "Kalamata",
#       "latitude": 37.08,
#       "longitude": 22.15,
#       "address": "Kalamata Fire Department Address 2",
#       "phone": "199"
#     },
#     {
#       "name": "Alexandroupoli General Hospital",
#       "service_type": "hospital",
#       "city": "Alexandroupoli",
#       "latitude": 40.85,
#       "longitude": 25.87,
#       "address": "Alexandroupoli General Hospital Address",
#       "phone": "+30 210100010"
#     },
#     {
#       "name": "Alexandroupoli Police Department",
#       "service_type": "police",
#       "city": "Alexandroupoli",
#       "latitude": 40.86,
#       "longitude": 25.88,
#       "address": "Alexandroupoli Police Department Address",
#       "phone": "+30 210200010"
#     },
#     {
#       "name": "Alexandroupoli Fire Department 1",
#       "service_type": "fire",
#       "city": "Alexandroupoli",
#       "latitude": 40.84,
#       "longitude": 25.87,
#       "address": "Alexandroupoli Fire Department Address 1",
#       "phone": "199"
#     },
#     {
#       "name": "Alexandroupoli Fire Department 2",
#       "service_type": "fire",
#       "city": "Alexandroupoli",
#       "latitude": 40.85,
#       "longitude": 25.88,
#       "address": "Alexandroupoli Fire Department Address 2",
#       "phone": "199"
#     },
#     {
#       "name": "Katerini General Hospital",
#       "service_type": "hospital",
#       "city": "Katerini",
#       "latitude": 40.26,
#       "longitude": 22.49,
#       "address": "Katerini General Hospital Address",
#       "phone": "+30 210100011"
#     },
#     {
#       "name": "Katerini Police Department",
#       "service_type": "police",
#       "city": "Katerini",
#       "latitude": 40.28,
#       "longitude": 22.50,
#       "address": "Katerini Police Department Address",
#       "phone": "+30 210200011"
#     },
#     {
#       "name": "Katerini Fire Department 1",
#       "service_type": "fire",
#       "city": "Katerini",
#       "latitude": 40.25,
#       "longitude": 22.48,
#       "address": "Katerini Fire Department Address 1",
#       "phone": "199"
#     },
#     {
#       "name": "Katerini Fire Department 2",
#       "service_type": "fire",
#       "city": "Katerini",
#       "latitude": 40.29,
#       "longitude": 22.52,
#       "address": "Katerini Fire Department Address 2",
#       "phone": "199"
#     },
#     {
#       "name": "Serres General Hospital",
#       "service_type": "hospital",
#       "city": "Serres",
#       "latitude": 41.09,
#       "longitude": 23.55,
#       "address": "Serres General Hospital Address",
#       "phone": "+30 210100012"
#     },
#     {
#       "name": "Serres Police Department",
#       "service_type": "police",
#       "city": "Serres",
#       "latitude": 41.08,
#       "longitude": 23.54,
#       "address": "Serres Police Department Address",
#       "phone": "+30 210200012"
#     },
#     {
#       "name": "Serres Fire Department 1",
#       "service_type": "fire",
#       "city": "Serres",
#       "latitude": 41.10,
#       "longitude": 23.56,
#       "address": "Serres Fire Department Address 1",
#       "phone": "199"
#     },
#     {
#       "name": "Serres Fire Department 2",
#       "service_type": "fire",
#       "city": "Serres",
#       "latitude": 41.09,
#       "longitude": 23.55,
#       "address": "Serres Fire Department Address 2",
#       "phone": "199"
#     },
# {
#       "name": "Rhodes General Hospital",
#       "service_type": "hospital",
#       "city": "Rhodes",
#       "latitude": 36.434,
#       "longitude": 28.217,
#       "address": "Rhodes General Hospital Address",
#       "phone": "+30 210100020"
#     },
#     {
#       "name": "Rhodes Police Department",
#       "service_type": "police",
#       "city": "Rhodes",
#       "latitude": 36.437,
#       "longitude": 28.221,
#       "address": "Rhodes Police Department Address",
#       "phone": "+30 210200020"
#     },
#     {
#       "name": "Rhodes Fire Department 1",
#       "service_type": "fire",
#       "city": "Rhodes",
#       "latitude": 36.430,
#       "longitude": 28.215,
#       "address": "Rhodes Fire Department Address 1",
#       "phone": "199"
#     },
#     {
#       "name": "Rhodes Fire Department 2",
#       "service_type": "fire",
#       "city": "Rhodes",
#       "latitude": 36.438,
#       "longitude": 28.220,
#       "address": "Rhodes Fire Department Address 2",
#       "phone": "199"
#     },
#     {
#       "name": "Corfu General Hospital",
#       "service_type": "hospital",
#       "city": "Corfu",
#       "latitude": 39.625,
#       "longitude": 19.921,
#       "address": "Corfu General Hospital Address",
#       "phone": "+30 210100021"
#     },
#     {
#       "name": "Corfu Police Department",
#       "service_type": "police",
#       "city": "Corfu",
#       "latitude": 39.628,
#       "longitude": 19.925,
#       "address": "Corfu Police Department Address",
#       "phone": "+30 210200021"
#     },
#     {
#       "name": "Corfu Fire Department 1",
#       "service_type": "fire",
#       "city": "Corfu",
#       "latitude": 39.623,
#       "longitude": 19.920,
#       "address": "Corfu Fire Department Address 1",
#       "phone": "199"
#     },
#     {
#       "name": "Corfu Fire Department 2",
#       "service_type": "fire",
#       "city": "Corfu",
#       "latitude": 39.629,
#       "longitude": 19.926,
#       "address": "Corfu Fire Department Address 2",
#       "phone": "199"
#     },
#     {
#       "name": "Mykonos General Hospital",
#       "service_type": "hospital",
#       "city": "Mykonos",
#       "latitude": 37.446,
#       "longitude": 25.328,
#       "address": "Mykonos General Hospital Address",
#       "phone": "+30 210100022"
#     },
#     {
#       "name": "Mykonos Police Department",
#       "service_type": "police",
#       "city": "Mykonos",
#       "latitude": 37.448,
#       "longitude": 25.330,
#       "address": "Mykonos Police Department Address",
#       "phone": "+30 210200022"
#     },
#     {
#       "name": "Mykonos Fire Department 1",
#       "service_type": "fire",
#       "city": "Mykonos",
#       "latitude": 37.445,
#       "longitude": 25.327,
#       "address": "Mykonos Fire Department Address 1",
#       "phone": "199"
#     },
#     {
#       "name": "Mykonos Fire Department 2",
#       "service_type": "fire",
#       "city": "Mykonos",
#       "latitude": 37.449,
#       "longitude": 25.329,
#       "address": "Mykonos Fire Department Address 2",
#       "phone": "199"
#     },
#     {
#       "name": "Santorini General Hospital",
#       "service_type": "hospital",
#       "city": "Santorini",
#       "latitude": 36.393,
#       "longitude": 25.461,
#       "address": "Santorini General Hospital Address",
#       "phone": "+30 210100023"
#     },
#     {
#       "name": "Santorini Police Department",
#       "service_type": "police",
#       "city": "Santorini",
#       "latitude": 36.395,
#       "longitude": 25.463,
#       "address": "Santorini Police Department Address",
#       "phone": "+30 210200023"
#     },
#     {
#       "name": "Santorini Fire Department 1",
#       "service_type": "fire",
#       "city": "Santorini",
#       "latitude": 36.392,
#       "longitude": 25.460,
#       "address": "Santorini Fire Department Address 1",
#       "phone": "199"
#     },
#     {
#       "name": "Santorini Fire Department 2",
#       "service_type": "fire",
#       "city": "Santorini",
#       "latitude": 36.396,
#       "longitude": 25.464,
#       "address": "Santorini Fire Department Address 2",
#       "phone": "199"
#     },
#     {
#       "name": "Zakynthos General Hospital",
#       "service_type": "hospital",
#       "city": "Zakynthos",
#       "latitude": 37.787,
#       "longitude": 20.904,
#       "address": "Zakynthos General Hospital Address",
#       "phone": "+30 210100024"
#     },
#     {
#       "name": "Zakynthos Police Department",
#       "service_type": "police",
#       "city": "Zakynthos",
#       "latitude": 37.789,
#       "longitude": 20.906,
#       "address": "Zakynthos Police Department Address",
#       "phone": "+30 210200024"
#     },
#     {
#       "name": "Zakynthos Fire Department 1",
#       "service_type": "fire",
#       "city": "Zakynthos",
#       "latitude": 37.786,
#       "longitude": 20.903,
#       "address": "Zakynthos Fire Department Address 1",
#       "phone": "199"
#     },
#     {
#       "name": "Zakynthos Fire Department 2",
#       "service_type": "fire",
#       "city": "Zakynthos",
#       "latitude": 37.790,
#       "longitude": 20.907,
#       "address": "Zakynthos Fire Department Address 2",
#       "phone": "199"
#     },
#     {
#       "name": "Chios General Hospital",
#       "service_type": "hospital",
#       "city": "Chios",
#       "latitude": 38.367,
#       "longitude": 26.135,
#       "address": "Chios General Hospital Address",
#       "phone": "+30 210100025"
#     },
#     {
#       "name": "Chios Police Department",
#       "service_type": "police",
#       "city": "Chios",
#       "latitude": 38.369,
#       "longitude": 26.137,
#       "address": "Chios Police Department Address",
#       "phone": "+30 210200025"
#     },
#     {
#       "name": "Chios Fire Department 1",
#       "service_type": "fire",
#       "city": "Chios",
#       "latitude": 38.366,
#       "longitude": 26.134,
#       "address": "Chios Fire Department Address 1",
#       "phone": "199"
#     },
#     {
#       "name": "Chios Fire Department 2",
#       "service_type": "fire",
#       "city": "Chios",
#       "latitude": 38.370,
#       "longitude": 26.138,
#       "address": "Chios Fire Department Address 2",
#       "phone": "199"
#     },
#     {
#       "name": "Lesvos General Hospital",
#       "service_type": "hospital",
#       "city": "Mytilene",
#       "latitude": 39.104,
#       "longitude": 26.554,
#       "address": "Lesvos General Hospital Address",
#       "phone": "+30 210100026"
#     },
#     {
#       "name": "Lesvos Police Department",
#       "service_type": "police",
#       "city": "Mytilene",
#       "latitude": 39.106,
#       "longitude": 26.556,
#       "address": "Lesvos Police Department Address",
#       "phone": "+30 210200026"
#     },
#     {
#       "name": "Lesvos Fire Department 1",
#       "service_type": "fire",
#       "city": "Mytilene",
#       "latitude": 39.103,
#       "longitude": 26.553,
#       "address": "Lesvos Fire Department Address 1",
#       "phone": "199"
#     },
#     {
#       "name": "Lesvos Fire Department 2",
#       "service_type": "fire",
#       "city": "Mytilene",
#       "latitude": 39.107,
#       "longitude": 26.557,
#       "address": "Lesvos Fire Department Address 2",
#       "phone": "199"
#     },
#     {
#       "name": "Samos General Hospital",
#       "service_type": "hospital",
#       "city": "Samos",
#       "latitude": 37.686,
#       "longitude": 26.911,
#       "address": "Samos General Hospital Address",
#       "phone": "+30 210100027"
#     },
#     {
#       "name": "Samos Police Department",
#       "service_type": "police",
#       "city": "Samos",
#       "latitude": 37.688,
#       "longitude": 26.913,
#       "address": "Samos Police Department Address",
#       "phone": "+30 210200027"
#     },
#     {
#       "name": "Samos Fire Department 1",
#       "service_type": "fire",
#       "city": "Samos",
#       "latitude": 37.685,
#       "longitude": 26.910,
#       "address": "Samos Fire Department Address 1",
#       "phone": "199"
#     },
#     {
#       "name": "Samos Fire Department 2",
#       "service_type": "fire",
#       "city": "Samos",
#       "latitude": 37.689,
#       "longitude": 26.914,
#       "address": "Samos Fire Department Address 2",
#       "phone": "199"
#     },
#     {
#         "name": "Syros General Hospital",
#         "service_type": "hospital",
#         "city": "Syros",
#         "latitude": 37.447,
#         "longitude": 24.942,
#         "address": "Syros General Hospital Address",
#         "phone": "+30 210100028"
#     }
#     ,
#     {
#       "name": "Syros Police Department",
#       "service_type": "police",
#       "city": "Syros",
#       "latitude": 37.449,
#       "longitude": 24.944,
#       "address": "Syros Police Department Address",
#       "phone": "+30 210200028"
#     },
#     {
#       "name": "Syros Fire Department 1",
#       "service_type": "fire",
#       "city": "Syros",
#       "latitude": 37.446,
#       "longitude": 24.941,
#       "address": "Syros Fire Department Address 1",
#       "phone": "199"
#     },
#     {
#       "name": "Syros Fire Department 2",
#       "service_type": "fire",
#       "city": "Syros",
#       "latitude": 37.450,
#       "longitude": 24.945,
#       "address": "Syros Fire Department Address 2",
#       "phone": "199"
#     }
#   ]
#
#
# def init_services():
#   try:
#     with app.app_context():
#       # Create both tables
#       db.create_all()
#       print("Created/Updated database tables")
#
#       # Clear and re-add emergency services
#       EmergencyService.query.delete()
#
#       for service_data in services:
#         service = EmergencyService(**service_data)
#         db.session.add(service)
#
#       db.session.commit()
#       print("\nEmergency Services Initialization Report")
#       print("---------------------------------------")
#       print(f"Successfully initialized {len(services)} emergency services!")
#       print(f"Added {len([s for s in services if s['service_type'] == 'hospital'])} hospitals")
#       print(f"Added {len([s for s in services if s['service_type'] == 'police'])} police stations")
#       print(f"Added {len([s for s in services if s['service_type'] == 'fire'])} fire stations")
#       print(f"Current Date and Time (UTC): 2025-02-16 16:46:29")
#       print(f"Current User's Login: nicknet06")
#       print("---------------------------------------")
#
#   except Exception as e:
#     db.session.rollback()
#     print(f"Error initializing services: {e}")
#     raise e
#
#
# if __name__ == '__main__':
#   print("\nStarting Emergency Services Initialization...")
#   print(f"Current Date and Time (UTC): 2025-02-16 16:46:29")
#   print(f"Current User's Login: nicknet06")
#
#   with app.app_context():
#     init_services()

from datetime import datetime, timedelta
from models import db, EmergencyService, Equipment, Vehicle, Personnel
import random


def generate_hospital_data(service_id):
    # Equipment
    equipment = [
        Equipment(
            service_id=service_id,
            name='MRI Machine',
            type='diagnostic',
            quantity=2,
            available=2,
            condition='good',
            last_maintenance=datetime.utcnow() - timedelta(days=30)
        ),
        Equipment(
            service_id=service_id,
            name='X-Ray Machine',
            type='diagnostic',
            quantity=3,
            available=2,
            condition='good',
            last_maintenance=datetime.utcnow() - timedelta(days=15)
        ),
        Equipment(
            service_id=service_id,
            name='Ventilator',
            type='life-support',
            quantity=10,
            available=8,
            condition='good',
            last_maintenance=datetime.utcnow() - timedelta(days=7)
        )
    ]

    # Vehicles
    vehicles = [
        Vehicle(
            service_id=service_id,
            type='ambulance',
            model='Mercedes Sprinter',
            plate_number=f'AMB-{random.randint(1000, 9999)}',
            status='available',
            capacity=2
        ),
        Vehicle(
            service_id=service_id,
            type='ambulance',
            model='Ford Transit',
            plate_number=f'AMB-{random.randint(1000, 9999)}',
            status='in-use',
            capacity=2
        )
    ]

    # Personnel
    specialties = ['Emergency Medicine', 'Surgery', 'Cardiology', 'Pediatrics']
    roles = ['Doctor', 'Nurse', 'Paramedic']
    shifts = ['morning', 'evening', 'night']

    personnel = []
    for i in range(10):
        personnel.append(
            Personnel(
                service_id=service_id,
                name=f'Medical Staff {i + 1}',
                role=random.choice(roles),
                speciality=random.choice(specialties),
                status=random.choice(['on-duty', 'off-duty']),
                shift=random.choice(shifts)
            )
        )

    return equipment, vehicles, personnel


def generate_police_data(service_id):
    # Equipment
    equipment = [
        Equipment(
            service_id=service_id,
            name='Body Camera',
            type='surveillance',
            quantity=20,
            available=15,
            condition='good',
            last_maintenance=datetime.utcnow() - timedelta(days=10)
        ),
        Equipment(
            service_id=service_id,
            name='Radar Gun',
            type='traffic',
            quantity=5,
            available=4,
            condition='good',
            last_maintenance=datetime.utcnow() - timedelta(days=20)
        )
    ]

    # Vehicles
    vehicles = [
        Vehicle(
            service_id=service_id,
            type='patrol',
            model='Ford Police Interceptor',
            plate_number=f'POL-{random.randint(1000, 9999)}',
            status='available',
            capacity=4
        ),
        Vehicle(
            service_id=service_id,
            type='motorcycle',
            model='BMW R1250RT-P',
            plate_number=f'POL-{random.randint(1000, 9999)}',
            status='available',
            capacity=1
        )
    ]

    # Personnel
    specialties = ['Traffic', 'Investigation', 'Patrol', 'Special Operations']
    personnel = []
    for i in range(8):
        personnel.append(
            Personnel(
                service_id=service_id,
                name=f'Officer {i + 1}',
                role='Police Officer',
                speciality=random.choice(specialties),
                status=random.choice(['on-duty', 'off-duty']),
                shift=random.choice(['morning', 'evening', 'night'])
            )
        )

    return equipment, vehicles, personnel


def generate_fire_data(service_id):
    # Equipment
    equipment = [
        Equipment(
            service_id=service_id,
            name='Fire Hose',
            type='firefighting',
            quantity=10,
            available=8,
            condition='good',
            last_maintenance=datetime.utcnow() - timedelta(days=5)
        ),
        Equipment(
            service_id=service_id,
            name='Breathing Apparatus',
            type='safety',
            quantity=15,
            available=12,
            condition='good',
            last_maintenance=datetime.utcnow() - timedelta(days=15)
        ),
        Equipment(
            service_id=service_id,
            name='Thermal Camera',
            type='rescue',
            quantity=3,
            available=3,
            condition='good',
            last_maintenance=datetime.utcnow() - timedelta(days=25)
        )
    ]

    # Vehicles
    vehicles = [
        Vehicle(
            service_id=service_id,
            type='fire-engine',
            model='Rosenbauer AT3',
            plate_number=f'FIRE-{random.randint(1000, 9999)}',
            status='available',
            capacity=6
        ),
        Vehicle(
            service_id=service_id,
            type='ladder-truck',
            model='Pierce Arrow XT',
            plate_number=f'FIRE-{random.randint(1000, 9999)}',
            status='available',
            capacity=4
        )
    ]

    # Personnel
    specialties = ['Firefighting', 'Rescue', 'Hazmat', 'Emergency Medical']
    personnel = []
    for i in range(12):
        personnel.append(
            Personnel(
                service_id=service_id,
                name=f'Firefighter {i + 1}',
                role='Firefighter',
                speciality=random.choice(specialties),
                status=random.choice(['on-duty', 'off-duty']),
                shift=random.choice(['morning', 'evening', 'night'])
            )
        )

    return equipment, vehicles, personnel


def init_resources():
    with app.app_context():
        # Clear existing data
        Equipment.query.delete()
        Vehicle.query.delete()
        Personnel.query.delete()

        # Generate data for each service
        services = EmergencyService.query.all()
        for service in services:
            if service.service_type == 'hospital':
                equipment, vehicles, personnel = generate_hospital_data(service.id)
            elif service.service_type == 'police':
                equipment, vehicles, personnel = generate_police_data(service.id)
            elif service.service_type == 'fire':
                equipment, vehicles, personnel = generate_fire_data(service.id)
            else:
                continue

            # Add all resources to database
            for e in equipment:
                db.session.add(e)
            for v in vehicles:
                db.session.add(v)
            for p in personnel:
                db.session.add(p)

        db.session.commit()
        print("Resources initialized successfully!")


if __name__ == '__main__':
    from app import app

    init_resources()