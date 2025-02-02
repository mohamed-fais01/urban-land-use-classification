def get_marker_color(land_use):
        """Return color for markers based on land use type"""
        color_mapping = {
            "Educational": "pink",
            "Healthcare": "red",
            "Residential": "green",
            "Recreational": "purple",
            "Commercial": "blue",
            "Industrial": "brown",
            "Agricultural": "orange",
            "Government": "white",
            "Religious": "darkred",
            "Transport": "lightgreen",
            "Tourism": "beige",
            "Green Spaces": "darkgreen",
            "Infrastructure": "darkblue",
            "Mixed-Use": "lightred",
            "Cultural": "lightblue",
            "Others": "gray"
        }
        return color_mapping.get(land_use, "gray")


def classify_land_use(name, place_type):
        # Land use mapping dictionary
        land_use_mapping = {
                "school": "Educational",
                "university": "Educational",
                "city_hall": "Educational",
                "college": "Educational",
                "hospital": "Healthcare",
                "doctor": "Healthcare",
                "physiotherapist": "Healthcare",
                "dentist": "Healthcare",
                "clinic": "Healthcare",
                "pharmacy": "Healthcare",
                "residential": "Residential",
                "residence": "Residential",
                "apartment": "Residential",
                "house": "Residential",
                "park": "Recreational",
                "toilet": "Recreational",
                "stadium": "Recreational",
                "playground": "Recreational",
                "amusement_park": "Recreational",
                "shelter": "Recreational",
                "restaurant": "Commercial",
                "marketplace": "Commercial",
                "fast_food": "Commercial",
                "mall": "Commercial",
                "store": "Commercial",
                "showroom": "Commercial",
                "supermarket": "Commercial",
                "gym": "Commercial",
                "hardware": "Commercial",
                "fuel": "Commercial",
                "car": "Commercial",
                "store": "Commercial",
                "lawyer": "Commercial",
                "cloth": "Commercial",
                "electronic": "Commercial",
                "fabric": "Commercial",
                "cafe": "Commercial",
                "office": "Commercial",
                "bank": "Commercial",
                "theatre": "Commercial",
                "theater": "Commercial",
                "florist": "Commercial",
                "fast_food": "Commercial",
                "cinema": "Commercial",
                "movie_theater": "Commercial",
                "meal_delivery": "Commercial",
                "movie_rental": "Commercial",
                "lodging": "Commercial",
                "hostel": "Commercial",
                "library": "Educational",
                "hotel": "Commercial",
                "atm": "Commercial",
                "aquarium": "Recreational",
                "bench": "Recreational",
                "zoo": "Recreational",
                "art_gallery": "Cultural",
                "bakery": "Commercial",
                "bicycle_store": "Commercial",
                "book_store": "Commercial",
                "beauty_salon": "Commercial",
                "hair_care": "Commercial",
                "accounting": "Commercial",
                "real_estate_agency": "Commercial",
                "insurance_agency": "Commercial",
                "shipping": "Commercial",
                "laundry": "Commercial",
                "casino": "Commercial",
                "cassino": "Commercial",
                "pvt ltd": "Commercial",
                "spa": "Commercial",
                "pub": "Commercial",
                "car_dealer": "Commercial",
                "jewel": "Commercial",
                "jewelry": "Commercial",
                "art_work": "Commercial",
                "bar": "Commercial",
                "night_club": "Commercial",
                "music": "Commercial",
                "airport": "Infrastructure",
                "museum": "Infrastructure",
                "industrial": "Industrial",
                "agricultural": "Agricultural",
                "government_office": "Government",
                "townhall": "Government",
                "police": "Government",
                "Department": "Government",
                "post_box": "Government",
                "embassy": "Government",
                "church": "Religious",
                "synagogue": "Religious",
                "place_of_worship": "Religious",
                "mosque": "Religious",
                "temple": "Religious",
                "train_station": "Transport",
                "bus_station": "Transport",
                "hotel": "Tourism",
                "travel_agency": "Tourism",
                "resort": "Tourism",
                "historical_landmark": "Tourism",
                "mixed_use": "Mixed-Use",
                "green_space": "Green Spaces"
            }
        
        name = str(name).lower()
        place_type = str(place_type).lower()
               # Try matching place_type first
        for key, value in land_use_mapping.items():
            if key in place_type:
                return value

                       
                # Try matching name if place_type didn't match
        for key, value in land_use_mapping.items():
            if key in name:
                return value
                        
            return "Others"
     