import rasterio
import numpy as np
import folium

elevation_ranges = {
            'Very Low <50': (float('-inf'), 50),
            'Low 50-100': (50, 100),
            'Medium 100-200': (100, 200),
            'High 200-700': (200, 700),
            'Very High <700': (700, float('inf'))
        }


def get_elevation(dem_file, lat, lng):
        """Get elevation for a specific coordinate from DEM with error handling"""
        try:
            with rasterio.open(dem_file) as src:
                # Transform coordinates to pixel coordinates
                row, col = src.index(lng, lat)
                
                # Check if the coordinates are within the bounds of the raster
                if 0 <= row < src.height and 0 <= col < src.width:
                    # Read the elevation value
                    elevation = src.read(1)[row, col]
                    
                    # Handle nodata values
                    if elevation == src.nodata:
                        return 0, 'Unknown'
                    
                    # Classify elevation
                    elevation_class = classify_elevation(float(elevation))
                    
                    return float(elevation), elevation_class
                else:
                    return 0, 'Unknown'
        except Exception as e:
            print(f"Error reading elevation for coordinates ({lat}, {lng}): {str(e)}")
            return 0, 'Unknown'

def classify_elevation(elevation):
        """Classify elevation into five categories with error handling"""
        try:
            if not isinstance(elevation, (int, float)):
                return 'Unknown'
                
            for category, (min_val, max_val) in elevation_ranges.items():
                if min_val <= elevation < max_val:
                    return category
            return 'Unknown'
        except Exception as e:
            print(f"Error classifying elevation {elevation}: {str(e)}")
            return 'Unknown'



def generate_elevation_map(self):
        """Generate comprehensive elevation zone map with places"""
        try:
            # Get zone data
            zone_data = self.divide_elevation_zones()
            
            if zone_data is not None:
                map_obj = folium.Map(
                    location=[self.user_lat, self.user_lng],
                    zoom_start=13
                )
                
                # Add search radius circle
                folium.Circle(
                    location=[self.user_lat, self.user_lng],
                    radius=float(self.current_radius),
                    color='black',
                    weight=1,
                    fill=False,
                    popup='Search Area'
                ).add_to(map_obj)
                
                # Add elevation zones
                zone_colors = {
                    'Zone 1 (Lowest)': '#31a354',
                    'Zone 2': '#a1d99b',
                    'Zone 3': '#fee08b',
                    'Zone 4': '#fc8d59',
                    'Zone 5 (Highest)': '#d73027'
                }
                
                # Create feature groups for zones and places
                zone_layers = {}
                for zone_name in zone_colors.keys():
                    zone_layers[zone_name] = folium.FeatureGroup(name=f"Elevation {zone_name}")
                
                places_layer = folium.FeatureGroup(name='Places')
                
                # Add zone markers
                for zone_name, coordinates in zone_data['coordinates'].items():
                    for coord in coordinates:
                        folium.CircleMarker(
                            location=[coord['lat'], coord['lng']],
                            radius=3,
                            color=zone_colors[zone_name],
                            fill=True,
                            fill_color=zone_colors[zone_name],
                            fill_opacity=0.7,
                            popup=f"{zone_name}<br>Elevation: {coord['elevation']:.1f}m"
                        ).add_to(zone_layers[zone_name])
                
                # Add place markers
                for place in self.filtered_places:
                    if isinstance(place['land_use'], tuple):
                        land_use_value = place['land_use'][0]
                    else:
                        land_use_value = place['land_use']
                    
                    popup_html = f"""
                    <div style="min-width: 200px">
                        <b>{place['name']}</b><br>
                        Type: {place['place_type']}<br>
                        Land Use: {land_use_value}<br>
                        Distance: {place['distance']:.2f} km<br>
                        Elevation: {place['elevation']:.1f}<br>
                        <button onclick="window.open('https://www.google.com/maps/dir/{self.user_lat},{self.user_lng}/{place['lat']},{place['lng']}')">
                            Get Directions
                        </button>
                    </div>
                    """
                    
                    folium.Marker(
                        location=[place['lat'], place['lng']],
                        popup=folium.Popup(popup_html, max_width=300),
                        tooltip=place['name'],
                        icon=folium.Icon(color=self.get_marker_color(land_use_value))
                    ).add_to(places_layer)
                
                # Add all layers to map
                for layer in zone_layers.values():
                    layer.add_to(map_obj)
                places_layer.add_to(map_obj)
                
                # Create comprehensive legend
                legend_html = """
                <div style="position: fixed; 
                            bottom: 50px; left: 50px; 
                            border:2px solid grey; z-index:9999; 
                            background-color:white;
                            padding: 10px;
                            font-size:14px;">
                <p><strong>Elevation Zones</strong></p>
                """
                
                # Add elevation zone information
                for zone_name, stats in zone_data['statistics'].items():
                    legend_html += f"""
                    <p>
                        <span style="background-color:{zone_colors[zone_name]}; padding: 0 10px;">&nbsp;</span>
                        {zone_name}<br>
                        <small>{stats['min_elevation']:.1f}m - {stats['max_elevation']:.1f}m<br>
                        Mean: {stats['mean_elevation']:.1f}m<br>
                        Points: {stats['point_count']}</small>
                    </p>
                    """
                
                legend_html += "</div>"
                
                # Add layer control and legend
                folium.LayerControl().add_to(map_obj)
                map_obj.get_root().html.add_child(folium.Element(legend_html))
                
                return map_obj
            else:
                print("Failed to generate zone data")
                
        except Exception as e:
            print(f"Error generating elevation map: {str(e)}")
        
        return None


def divide_elevation_zones(dem_file, user_lat, user_lng, current_radius):
    """
    Divides the region within the search radius into 5 elevation zones based on actual elevation data.
    Returns a dictionary with zone boundaries and associated coordinates.
    """
    try:
        with rasterio.open(dem_file) as src:
            center_point = (user_lng, user_lat)
            radius_degrees = current_radius / 111320  # Convert meters to approximate degrees
            
            center_px = src.index(*center_point)
            radius_px = int(radius_degrees / src.res[0])  # Convert radius to pixels
            
            rows, cols = np.ogrid[-center_px[0]:src.height-center_px[0],
                                -center_px[1]:src.width-center_px[1]]
            mask = rows*rows + cols*cols <= radius_px*radius_px
            
            elevation_data = src.read(1)
            masked_elevations = elevation_data[mask]
            valid_elevations = masked_elevations[masked_elevations != src.nodata]
            
            if len(valid_elevations) == 0:
                raise ValueError("No valid elevation data found in the specified region")
            
            percentiles = np.percentile(valid_elevations, [20, 40, 60, 80])
            
            zones = {
                'Zone 1 (Lowest)': (float(np.min(valid_elevations)), float(percentiles[0])),
                'Zone 2': (float(percentiles[0]), float(percentiles[1])),
                'Zone 3': (float(percentiles[1]), float(percentiles[2])),
                'Zone 4': (float(percentiles[2]), float(percentiles[3])),
                'Zone 5 (Highest)': (float(percentiles[3]), float(np.max(valid_elevations)))
            }
            
            zone_coordinates = {zone_name: [] for zone_name in zones.keys()}
            
            rows, cols = np.where(mask)
            for row, col in zip(rows, cols):
                elevation = elevation_data[row, col]
                if elevation != src.nodata:
                    lng, lat = src.xy(row, col)
                    
                    for zone_name, (min_elev, max_elev) in zones.items():
                        if min_elev <= elevation <= max_elev:
                            zone_coordinates[zone_name].append({
                                'lat': lat,
                                'lng': lng,
                                'elevation': float(elevation)
                            })
                            break
            
            zone_stats = {}
            for zone_name, coordinates in zone_coordinates.items():
                if coordinates:
                    elevations = [coord['elevation'] for coord in coordinates]
                    zone_stats[zone_name] = {
                        'min_elevation': min(elevations),
                        'max_elevation': max(elevations),
                        'mean_elevation': sum(elevations) / len(elevations),
                        'point_count': len(coordinates)
                    }
            
            return {
                'zones': zones,
                'coordinates': zone_coordinates,
                'statistics': zone_stats
            }
            
    except Exception as e:
        print(f"Error dividing elevation zones: {str(e)}")
        return None