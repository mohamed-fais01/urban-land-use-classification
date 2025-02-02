import tkinter as tk
from tkinter import ttk
import os
from Elevation import divide_elevation_zones, generate_elevation_map , get_elevation, classify_elevation
from rule_based import classify_land_use, get_marker_color
from model import initialize_model, predict_land_use
from osm_places import query_osm_places
from tabs import setup_main_tab, setup_analysis_tab, setup_visualization_tab, setup_export_tab
from save_and_export import export_model_report, export_analysis_report, export_all_maps, export_data, save_results
from maps import generate_all_maps, generate_standard_map, generate_cluster_map, generate_choropleth_map, generate_heat_map, generate_selected_map
from filters import apply_visualization_filters, reset_visualization_filters, update_land_use_filter_values
from data import load_data, get_local_places, get_combined_places
from table_and_update import update_table, on_search, on_search_table, update_statistics, update_chart, edit_place

class LandUseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Land Use Classification App")
        #self.root.state('zoomed')
        
        # Initialize variables
        self.filtered_places = []
        self.user_lat = None
        self.user_lng = None
        self.current_radius = None
        self.maps_folder = "generated_maps"
        self.analysis_folder = "analysis_results"
        self.data = []
        self.df = None
        self.model = None
        self.tfidf = None
        self.label_encoder = None
        self.X_test = None
        self.y_test = None
        
        # Create output folders
        for folder in [self.maps_folder, self.analysis_folder]:
            os.makedirs(folder, exist_ok=True)
        
        self.setup_gui()
        self.load_data()
        self.dem_file = "SLMerge.tif"
        
        # Add elevation colors for visualization
        self.elevation_colors = {
            'Very Low <50': '#d73027',   # red
            'Low 50-100': '#fc8d59',        # orange
            'Medium 100-200': '#fee08b',     # Yellow
            'High 200-700': '#a1d99b',       # green
            'Very High <700': '#31a354'   # lightgreen
        }

    def divide_elevation_zones(self):
        return  divide_elevation_zones(self.dem_file, self.user_lat, self.user_lng, self.current_radius)
        
    def generate_elevation_map(self):
        return generate_elevation_map(self)

    def get_elevation(self,lat,lng):
        return get_elevation(self.dem_file, lat, lng)
    
    def classify_elevation(self, elevation):
        return classify_elevation(elevation)       

    @staticmethod
    def classify_land_use(name, place_type):
     return classify_land_use(name, place_type)
        
    def initialize_model(self):
      return initialize_model(self)

    def query_osm_places(self):
        return query_osm_places(self)

    def setup_main_tab(self):
        return setup_main_tab(self)

    def save_results(self):
        return save_results(self)

    def setup_analysis_tab(self):
        return setup_analysis_tab(self)

    def setup_visualization_tab(self):
        return setup_visualization_tab(self)
        
    def update_land_use_filter_values(self):
        return update_land_use_filter_values(self)

    def setup_export_tab(self):
        return setup_export_tab(self) 

    def load_data(self):
        return load_data(self)


    def export_model_report(self):
        return export_model_report(self)

    def predict_land_use(self, name, place_type):
        return predict_land_use(self, name, place_type)


    def on_search(self):
        return on_search(self)

    def get_combined_places(self):
        return get_combined_places(self)

    def get_local_places(self):
        return get_local_places(self)

    
    def generate_all_maps(self):
        return generate_all_maps(self)

    def generate_standard_map(self):
        return generate_standard_map(self)

    def generate_cluster_map(self):
        return generate_cluster_map(self)

    def generate_choropleth_map(self):
        return generate_choropleth_map(self)

    def update_statistics(self):
        return update_statistics(self)

    def update_chart(self, event=None):
        return update_chart(self, event)

    def export_data(self, format_type):
        return export_data(self, format_type)

    def export_analysis_report(self):
        return export_analysis_report(self)

    def export_all_maps(self):
        return export_all_maps(self)

    def apply_visualization_filters(self):
        return apply_visualization_filters(self)

    def reset_visualization_filters(self):
        return reset_visualization_filters(self)

    def generate_selected_map(self, event=None, filtered_data=None):
        return generate_selected_map(self, event, filtered_data)

    def generate_heat_map(self):
        return generate_heat_map(self)

    @staticmethod
    def get_marker_color(land_use):
        return get_marker_color(land_use)

    def edit_place(self):
        return edit_place(self)

    def update_table(self, places):
        return update_table(self, places)

    def on_search_table(self, *args):
        return on_search_table(self, *args)
    
    def setup_gui(self):
        # Create main container with tabs
        self.tab_control = ttk.Notebook(self.root)
        
        # Create and add tabs
        self.tab_main = ttk.Frame(self.tab_control)
        self.tab_analysis = ttk.Frame(self.tab_control)
        self.tab_visualization = ttk.Frame(self.tab_control)
        self.tab_export = ttk.Frame(self.tab_control)
        
        self.tab_control.add(self.tab_main, text='Main')
        self.tab_control.add(self.tab_analysis, text='Analysis')
        self.tab_control.add(self.tab_visualization, text='Visualization')
        self.tab_control.add(self.tab_export, text='Export')
        
        self.tab_control.pack(expand=1, fill="both")
        
        # Setup individual tabs
        self.setup_main_tab()
        self.setup_analysis_tab()
        self.setup_visualization_tab()
        self.setup_export_tab()

if __name__ == "__main__":
    root = tk.Tk()
    app = LandUseApp(root)
    root.mainloop()