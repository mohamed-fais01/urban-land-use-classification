import requests
import rasterio
from geopy.distance import geodesic
from tkinter import messagebox

def query_osm_places(self):
        try:
            overpass_url = "http://overpass-api.de/api/interpreter"
            radius_km = self.current_radius / 1000  # Convert to kilometers
            
            query = f"""
            [out:json][timeout:25];
            (
              node["amenity"](around:{self.current_radius},{self.user_lat},{self.user_lng});
              way["amenity"](around:{self.current_radius},{self.user_lat},{self.user_lng});
              node["building"](around:{self.current_radius},{self.user_lat},{self.user_lng});
              way["building"](around:{self.current_radius},{self.user_lat},{self.user_lng});
            );
            out body;
            >;
            out skel qt;
            """
            
            response = requests.get(overpass_url, params={'data': query}, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            osm_places = []
            self.osm_prediction_sources = {'model': 0, 'rule-based': 0}

            # Open DEM file once for all places
            with rasterio.open(self.dem_file) as src:
                for element in data.get('elements', []):
                    if 'tags' in element:
                        try:
                            tags = element['tags']
                            place_type = tags.get('amenity') or tags.get('building') or 'unspecified'
                            name = tags.get('name', 'Unnamed')
                            
                            # Get coordinates
                            if element['type'] == 'node':
                                lat, lng = element['lat'], element['lon']
                            else:  # way or relation
                                if 'center' in element:
                                    lat, lng = element['center']['lat'], element['center']['lon']
                                else:
                                    continue
                            
                            # Calculate distance
                            distance = geodesic(
                                (self.user_lat, self.user_lng),
                                (lat, lng)
                            ).km

                            # Get prediction and source
                            predicted_land_use, source = self.predict_land_use(name, place_type)
                            self.osm_prediction_sources[source] += 1

                            # Get elevation data
                            try:
                                # Transform coordinates to pixel coordinates
                                row, col = src.index(lng, lat)
                                
                                # Check if coordinates are within bounds
                                if 0 <= row < src.height and 0 <= col < src.width:
                                    elevation = float(src.read(1)[row, col])
                                    
                                    # Handle nodata values
                                    if elevation == src.nodata:
                                        elevation = 0
                                        elevation_class = 'Unknown'
                                    else:
                                        elevation_class = self.classify_elevation(elevation)
                                else:
                                    elevation = 0
                                    elevation_class = 'Unknown'
                            except Exception as e:
                                print(f"Error reading elevation for coordinates ({lat}, {lng}): {str(e)}")
                                elevation = 0
                                elevation_class = 'Unknown'
                            
                            osm_places.append({
                                'id': len(osm_places) + 1,
                                'name': name,
                                'lat': lat,
                                'lng': lng,
                                'place_type': place_type,
                                'land_use': predicted_land_use,
                                'prediction_source': source,
                                'distance': round(distance, 2),
                                'elevation': elevation,
                                'elevation_class': elevation_class
                            })
                        except Exception as e:
                            print(f"Error processing OSM element: {str(e)}")
                            continue

            self.osm_total = sum(self.osm_prediction_sources.values())
            return osm_places
            
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to fetch OSM data: {str(e)}")
            return []
        except rasterio.errors.RasterioError as e:
            messagebox.showerror("Error", f"Failed to read DEM file: {str(e)}")
            return []
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
            return []