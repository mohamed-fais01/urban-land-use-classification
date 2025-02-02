import folium
import os
import webbrowser
import datetime
from tkinter import messagebox
from folium.plugins import HeatMap, MarkerCluster
import matplotlib.pyplot as plt
import numpy as np

def generate_selected_map(self, event=None, filtered_data=None):
        if filtered_data is None:
            filtered_data = self.filtered_places
            
        if not filtered_data:
            messagebox.showwarning("Warning", "No data to visualize")
            return
            
        map_type = self.map_type.get()
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if map_type == "Standard Markers":
            map_obj = self.generate_standard_map()
        elif map_type == "Heat Map":
            map_obj = self.generate_heat_map()
        elif map_type == "Cluster Map":
            map_obj = self.generate_cluster_map()
        elif map_type == "Choropleth":
            map_obj = self.generate_choropleth_map()
        elif map_type == "Elevation_Map":
            map_obj = self.generate_elevation_map()
        elif map_type == "3D Terrain Map":
            map_obj = self.generate_3d_terrain_map()
        else:
            map_obj = self.generate_standard_map()
            
        filename = os.path.abspath(os.path.join(
            self.maps_folder,
            f"map_{map_type.lower().replace(' ', '_')}_{timestamp}.html"
        ))
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Save and open map
        map_obj.save(filename)
        webbrowser.open('file://' + filename)


def generate_heat_map(self):
        map_obj = folium.Map(
            location=[self.user_lat, self.user_lng],
            zoom_start=13
        )
        
        # Add heat map layer
        heat_data = [[p['lat'], p['lng']] for p in self.filtered_places]
        HeatMap(
            heat_data,
            radius=15,
            blur=10,
            max_zoom=1
        ).add_to(map_obj)
        
        return map_obj

def generate_choropleth_map(self):
        """Generate a proper choropleth map showing land use density"""
        map_obj = folium.Map(
            location=[self.user_lat, self.user_lng],
            zoom_start=13
        )
        
        # Create a feature group for each land use type
        land_use_groups = {}
        
        # Get unique land uses and assign colors
        unique_land_uses = set(place['land_use'] for place in self.filtered_places)
        color_scale = plt.cm.Set3(np.linspace(0, 1, len(unique_land_uses)))
        color_map = dict(zip(unique_land_uses, 
                            [f'#{"%02x%02x%02x" % tuple(map(lambda x: int(x * 255), color[:3]))}' 
                            for color in color_scale]))
        
        # Create legend HTML
        legend_html = """
        <div style="position: fixed; 
                    bottom: 50px; right: 50px; 
                    border:2px solid grey; z-index:9999; 
                    background-color:white;
                    padding: 10px;
                    font-size:14px;">
        <p><strong>Land Use Types</strong></p>
        """
        
        for land_use, color in color_map.items():
            # Create feature group for land use type
            land_use_groups[land_use] = folium.FeatureGroup(name=land_use)
            
            # Add to legend
            legend_html += f"""
            <p>
                <span style="color:{color};">●</span> {land_use}
            </p>
            """
        
        legend_html += "</div>"
        
        # Add places to respective feature groups
        for place in self.filtered_places:
            land_use = place['land_use']
            color = color_map[land_use]
            
            folium.CircleMarker(
                location=[place['lat'], place['lng']],
                radius=8,
                popup=f"{place['name']}<br>{place['place_type']}<br>{land_use}",
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.7
            ).add_to(land_use_groups[land_use])
        
        # Add all feature groups to map
        for group in land_use_groups.values():
            group.add_to(map_obj)
        
        # Add legend
        map_obj.get_root().html.add_child(folium.Element(legend_html))
        
        # Add layer control
        folium.LayerControl().add_to(map_obj)
        
        return map_obj

def generate_cluster_map(self):
        map_obj = folium.Map(
            location=[self.user_lat, self.user_lng],
            zoom_start=13
        )
        
        # Create marker cluster
        marker_cluster = MarkerCluster(name="Clusters")
        
        # Add markers to cluster
        for place in self.filtered_places:
            popup_html = f"""
            <div style="min-width: 200px">
                <b>{place['name']}</b><br>
                Type: {place['place_type']}<br>
                Land Use: {place['land_use']}<br>
                Distance: {place['distance']:.2f} km
            </div>
            """
            
            folium.Marker(
                location=[place['lat'], place['lng']],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=place['name']
            ).add_to(marker_cluster)
        
        marker_cluster.add_to(map_obj)
        return map_obj

def generate_standard_map(self):
        map_obj = folium.Map(
            location=[self.user_lat, self.user_lng],
            zoom_start=13
        )
        
        # Add existing circle for search radius
        folium.Circle(
            location=[self.user_lat, self.user_lng],
            radius=float(self.current_radius),
            color='blue',
            popup='Search Area'
        ).add_to(map_obj)
        
        # Create legend HTML with both land use and elevation
        legend_html = """
        <div style="position: fixed; 
                    bottom: 50px; right: 50px; 
                    border:2px solid grey; z-index:9999; 
                    background-color:white;
                    padding: 10px;
                    font-size:14px;">
        <p><strong>Land Use Types</strong></p>
        """
        
        # Add land use legend entries
        unique_land_uses = set()
        for place in self.filtered_places:
            if isinstance(place['land_use'], tuple):
                land_use_value = place['land_use'][0]
            else:
                land_use_value = place['land_use']
            unique_land_uses.add(land_use_value)
        
        for land_use in sorted(unique_land_uses):
            color = self.get_marker_color(land_use)
            legend_html += f"""
            <p>
                <i class="fa fa-map-marker" style="color:{color};"></i> {land_use}
            </p>
            """
            
        # Add elevation legend
        legend_html += """
        <p><strong>Elevation Ranges</strong></p>
        """
        for category, color in self.elevation_colors.items():
            legend_html += f"""
            <p>
                <span style="background-color:{color}; padding: 0 10px;">&nbsp;</span> {category}
            </p>
            """
        
        legend_html += "</div>"
        
        # Create elevation layer
        elevation_layer = folium.FeatureGroup(name='Elevation')
        
        # Add markers with both land use and elevation information
        for place in self.filtered_places:
            if isinstance(place['land_use'], tuple):
                land_use_value, prediction_source = place['land_use']
            else:
                land_use_value = place['land_use']
                prediction_source = 'N/A'
            
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
            
            # Add elevation circle
            folium.CircleMarker(
                location=[place['lat'], place['lng']],
                radius=5,
                popup=folium.Popup(popup_html, max_width=2),
                color=self.elevation_colors[place['elevation_class']],
                #fill=True,
                fill_color=self.elevation_colors[place['elevation_class']],
                fill_opacity=0.3
            ).add_to(elevation_layer)
            
            # Add land use marker
            folium.Marker(
                location=[place['lat'], place['lng']],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=place['name'],
                icon=folium.Icon(color=self.get_marker_color(land_use_value))
            ).add_to(map_obj)
        
        # Add elevation layer to map
        elevation_layer.add_to(map_obj)
        
        # Add layer control
        folium.LayerControl().add_to(map_obj)
        
        # Add legend to map
        map_obj.get_root().html.add_child(folium.Element(legend_html))
        
        return map_obj

def generate_all_maps(self):
        map_types = {
            'standard': self.generate_standard_map,
            'heat': self.generate_heat_map,
            'cluster': self.generate_cluster_map,
            'choropleth': self.generate_choropleth_map,
            'Elevation_Map': self.generate_elevation_map

        }
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create maps directory if it doesn't exist
        os.makedirs(self.maps_folder, exist_ok=True)
        
        generated_files = []
        for map_name, map_func in map_types.items():
            try:
                map_obj = map_func()
                filename = os.path.abspath(os.path.join(
                    self.maps_folder,
                    f"map_{map_name}_{timestamp}.html"
                ))
                map_obj.save(filename)
                generated_files.append(filename)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate {map_name} map: {str(e)}")
        
        # Open the standard map in browser if available
        if generated_files:
            webbrowser.open('file://' + generated_files[0])