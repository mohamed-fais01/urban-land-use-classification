import os
import webbrowser
import datetime
from tkinter import messagebox
import tkinter as tk


def update_land_use_filter_values(self):
        """Update the land use filter dropdown with available values"""
        if self.filtered_places:
            unique_land_uses = sorted(set(place['land_use'] for place in self.filtered_places))
            self.land_use_filter['values'] = ['All'] + list(unique_land_uses)
            self.land_use_filter.set('All')

def reset_visualization_filters(self):
        """Reset all visualization filters"""
        self.land_use_filter.set("All")
        self.distance_filter.delete(0, tk.END)
        self.generate_selected_map(filtered_data=self.filtered_places)

def apply_visualization_filters(self):
        """Apply filters to the visualization with error handling"""
        try:
            # Get filter values
            selected_land_use = self.land_use_filter.get()
            max_distance_str = self.distance_filter.get().strip()
            
            # Store original data
            original_places = self.filtered_places.copy()
            filtered_data = original_places.copy()
            
            # Apply land use filter
            if selected_land_use and selected_land_use != "All":
                filtered_data = [p for p in filtered_data 
                            if p['land_use'] == selected_land_use]
            
            # Apply distance filter
            if max_distance_str:
                try:
                    max_dist = float(max_distance_str)
                    filtered_data = [p for p in filtered_data 
                                if p['distance'] <= max_dist]
                except ValueError:
                    messagebox.showwarning("Warning", 
                                        "Invalid distance value. Please enter a number.")
                    return
            
            if not filtered_data:
                messagebox.showinfo("Info", "No places match the selected filters")
                return
            
            # Update visualization with filtered data
            self.filtered_places = filtered_data
            self.update_table(filtered_data)
            self.update_chart()
            
            # Generate new map with filtered data
            map_type = self.map_type.get() if hasattr(self, 'map_type') else "Standard Markers"
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
            else:
                map_obj = self.generate_standard_map()
                
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.abspath(os.path.join(
                self.maps_folder,
                f"filtered_map_{timestamp}.html"
            ))
            
            map_obj.save(filename)
            webbrowser.open('file://' + filename)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply filters: {str(e)}")