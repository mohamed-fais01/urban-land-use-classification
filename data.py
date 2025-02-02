import os
import json
import pandas as pd
from tkinter import messagebox
from geopy.distance import geodesic

def get_combined_places(self):
        # Combine local and OSM data with elevation info
        local_places = self.get_local_places()
        osm_places = self.query_osm_places()
        
        # Add elevation data to OSM places
        for place in osm_places:
            elevation, elevation_class = self.get_elevation(place['lat'], place['lng'])
            place['elevation'] = elevation if elevation is not None else 0
            place['elevation_class'] = elevation_class if elevation_class is not None else 'Unknown'
        
        return local_places + osm_places

def get_local_places(self):
        places = []
        self.google_prediction_sources = {'model': 0, 'rule-based': 0}
        
        for place in self.data:
            try:
                distance = geodesic(
                    (self.user_lat, self.user_lng),
                    (place['location']['lat'], place['location']['lng'])
                ).km
                
                if distance <= self.current_radius / 1000:
                    predicted_land_use, source = self.predict_land_use(
                        place.get('name', ''),
                        place.get('place_type', '')
                    )
                    self.google_prediction_sources[source] += 1
                    
                    # Get elevation data with error handling
                    elevation, elevation_class = self.get_elevation(
                        place['location']['lat'],
                        place['location']['lng']
                    )
                    
                    places.append({
                        'id': len(places) + 1,
                        'name': place.get('name', 'Unnamed'),
                        'lat': place['location']['lat'],
                        'lng': place['location']['lng'],
                        'place_type': place.get('place_type', ''),
                        'land_use': predicted_land_use,
                        'prediction_source': source,
                        'distance': round(distance, 2),
                        'elevation': elevation if elevation is not None else 0,
                        'elevation_class': elevation_class if elevation_class is not None else 'Unknown'
                    })
            except Exception as e:
                print(f"Error processing place: {str(e)}")
                continue
        
        self.google_total = sum(self.google_prediction_sources.values())
        return places

def load_data(self):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            json_file_path = os.path.join(script_dir, 'sri_lanka_places.json')
            
            # Check if file exists
            if not os.path.exists(json_file_path):
                # Create sample data if file doesn't exist
                self.data = [
                    {
                        "name": "Sample Place",
                        "place_type": "commercial",
                        "location": {"lat": 6.927079, "lng": 79.861243},
                        "land_use": "Commercial"
                    }
                ]
                # Save sample data
                with open(json_file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.data, f, indent=4)
            else:
                # Load existing data
                with open(json_file_path, encoding='utf-8') as f:
                    self.data = json.load(f)

            # Convert to DataFrame
            places_list = []
            for place in self.data:
                places_list.append({
                    'name': place.get('name', ''),
                    'place_type': place.get('place_type', ''),
                    'lat': place['location']['lat'],
                    'lng': place['location']['lng'],
                    'land_use': place.get('land_use', '')
                })
            
            self.df = pd.DataFrame(places_list)
            #self.classify_land_use(name='name',place_type='place_type')
            # Initialize the model
            self.initialize_model()
            
        except Exception as e:
            messagebox.showwarning("Warning", f"Data loading issue: {str(e)}\nUsing empty dataset.")
            self.data = []
            self.df = pd.DataFrame(columns=['name', 'place_type', 'lat', 'lng', 'land_use'])

