from tkinter import ttk
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def setup_export_tab(self):
        frame_export = ttk.LabelFrame(self.tab_export, text="Export Options")
        frame_export.pack(pady=10, padx=10, fill="x")
        
        ttk.Button(frame_export, text="Export to CSV", 
                   command=lambda: self.export_data("csv")).pack(pady=5)
        ttk.Button(frame_export, text="Export to Excel", 
                   command=lambda: self.export_data("excel")).pack(pady=5)
        ttk.Button(frame_export, text="Export Analysis Report", 
                   command=self.export_analysis_report).pack(pady=5)
        ttk.Button(frame_export, text="Export All Maps", 
                   command=self.export_all_maps).pack(pady=5)
        ttk.Button(frame_export, text="Export Model Evaluation", 
               command=self.export_model_report).pack(pady=5)


def setup_analysis_tab(self):
        # Statistics frame
        frame_stats = ttk.LabelFrame(self.tab_analysis, text="Statistics")
        frame_stats.pack(pady=10, padx=10, fill="x")
        
        self.stats_text = tk.Text(frame_stats, height=10, width=50)
        self.stats_text.pack(pady=10, padx=10)
        
        # Charts frame
        frame_charts = ttk.LabelFrame(self.tab_analysis, text="Charts")
        frame_charts.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Chart type selector
        ttk.Label(frame_charts, text="Select Chart Type:").pack(pady=5)
        self.chart_type = ttk.Combobox(frame_charts, 
                                      values=["Land Use Distribution", 
                                             "Distance Distribution",
                                             "Place Type Distribution"])
        self.chart_type.pack(pady=5)
        self.chart_type.bind("<<ComboboxSelected>>", self.update_chart)
        
        # Canvas for matplotlib
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_charts)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

def setup_visualization_tab(self):
        """Improved visualization tab setup with working filters"""
        frame_maps = ttk.LabelFrame(self.tab_visualization, text="Map Visualization")
        frame_maps.pack(pady=10, padx=10, fill="x")
        
        # Map type selector
        ttk.Label(frame_maps, text="Select Map Type:").pack(pady=5)
        self.map_type = ttk.Combobox(frame_maps, 
                                    values=["Standard Markers",
                                        "Heat Map",
                                        "Cluster Map",
                                        "Choropleth",
                                        "Elevation_Map"
                                ])
        self.map_type.pack(pady=5)
        self.map_type.bind("<<ComboboxSelected>>", self.generate_selected_map)
        
        # Filters frame
        frame_filters = ttk.LabelFrame(frame_maps, text="Filters")
        frame_filters.pack(pady=10, padx=10, fill="x")
        
        # Land use filter
        ttk.Label(frame_filters, text="Filter by Land Use:").pack(pady=5)
        self.land_use_filter = ttk.Combobox(frame_filters)
        self.land_use_filter.pack(pady=5)
        
        # Distance filter
        ttk.Label(frame_filters, text="Maximum Distance (km):").pack(pady=5)
        self.distance_filter = ttk.Entry(frame_filters)
        self.distance_filter.pack(pady=5)
        
        # Buttons
        ttk.Button(frame_filters, text="Apply Filters", 
                command=self.apply_visualization_filters).pack(pady=5)
        ttk.Button(frame_filters, text="Reset Filters", 
                command=self.reset_visualization_filters).pack(pady=5)


def setup_main_tab(self):
        # Input frame
        frame_inputs = ttk.LabelFrame(self.tab_main, text="Search Parameters")
        frame_inputs.pack(pady=10, padx=10, fill="x")
        
        # Coordinates input
        ttk.Label(frame_inputs, text="Coordinates (Lat, Lng):").grid(row=0, column=0, padx=5, pady=5)
        self.entry_coords = ttk.Entry(frame_inputs)
        self.entry_coords.grid(row=0, column=1, padx=5, pady=5)
        
        # Radius input
        ttk.Label(frame_inputs, text="Radius (m):").grid(row=0, column=2, padx=5, pady=5)
        self.entry_radius = ttk.Entry(frame_inputs)
        self.entry_radius.grid(row=0, column=3, padx=5, pady=5)
        
        # Search button
        ttk.Button(frame_inputs, text="Search", command=self.on_search).grid(row=0, column=4, padx=5, pady=5)
        
        # Table frame
        frame_table = ttk.LabelFrame(self.tab_main, text="Results")
        frame_table.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Search within results
        ttk.Label(frame_table, text="Filter Results:").pack(pady=5)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.on_search_table)
        ttk.Entry(frame_table, textvariable=self.search_var).pack(pady=5)
        
        # Create table
        columns = ("ID", "Name", "Place Type", "Land Use", "Prediction Source", "Distance (km)","Elevation")
        self.table = ttk.Treeview(frame_table, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            self.table.heading(col, text=col)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        
        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Buttons frame
        frame_buttons = ttk.Frame(self.tab_main)
        frame_buttons.pack(pady=10, padx=10)
        
        ttk.Button(frame_buttons, text="Edit Selected", command=self.edit_place).pack(side="left", padx=5)
        ttk.Button(frame_buttons, text="Generate Maps", command=self.generate_all_maps).pack(side="left", padx=5)
        ttk.Button(frame_buttons, text="Save Results", command=self.save_results).pack(side="left", padx=5)
        #ttk.Button(frame_buttons, text="Export Results", command=self.save_results).pack(side="left", padx=5)  # Changed text to be clearer
