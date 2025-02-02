from tkinter import messagebox
import pandas as pd
import tkinter as tk
from tkinter import ttk
import seaborn as sns


def update_chart(self, event=None):
        """Fixed chart updating function"""
        if not self.filtered_places or not hasattr(self, 'ax'):
            return
            
        self.ax.clear()
        df = pd.DataFrame(self.filtered_places)
        
        selected_chart = self.chart_type.get()
        
        if selected_chart == "Land Use Distribution":
            # Create land use distribution bar chart
            land_use_counts = df['land_use'].value_counts()
            land_use_counts.plot(kind='bar', ax=self.ax, color='skyblue')
            self.ax.set_title("Distribution of Land Use Types")
            self.ax.set_xlabel("Land Use Category")
            self.ax.set_ylabel("Count")
            
        elif selected_chart == "Distance Distribution":
            # Create distance distribution histogram
            sns.histplot(data=df, x='distance', bins=20, ax=self.ax, color='skyblue')
            self.ax.set_title("Distribution of Distances")
            self.ax.set_xlabel("Distance (km)")
            self.ax.set_ylabel("Count")
            
        elif selected_chart == "Place Type Distribution":
            # Create place type distribution bar chart
            df['place_type'].value_counts().head(10).plot(kind='bar', ax=self.ax, color='skyblue')
            self.ax.set_title("Top 10 Place Types")
            self.ax.set_xlabel("Place Type")
            self.ax.set_ylabel("Count")
        
        # Adjust layout
        self.ax.tick_params(axis='x', rotation=45, labelsize=8)
        self.fig.tight_layout()
        
        # Redraw canvas
        self.canvas.draw()

def edit_place(self):
        selected_item = self.table.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a place to edit")
            return
            
        item_values = self.table.item(selected_item[0])['values']
        place_id = int(item_values[0])
        
        # Create edit dialog
        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Edit Place #{place_id}")
        
        # Add fields
        ttk.Label(edit_window, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = ttk.Entry(edit_window)
        name_entry.insert(0, item_values[1])
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(edit_window, text="Place Type:").grid(row=1, column=0, padx=5, pady=5)
        type_entry = ttk.Entry(edit_window)
        type_entry.insert(0, item_values[2])
        type_entry.grid(row=1, column=1, padx=5, pady=5)
        
        def save_changes():
            for place in self.filtered_places:
                if place['id'] == place_id:
                    place['name'] = name_entry.get()
                    place['place_type'] = type_entry.get()
                    place['land_use'] = self.predict_land_use(
                        place['name'],
                        place['place_type']
                    )
                    place.get('prediction_source', 'N/A'), 
                    break
                    
            self.update_table(self.filtered_places)
            edit_window.destroy()
            
        ttk.Button(edit_window, text="Save", command=save_changes).grid(
            row=2, column=0, columnspan=2, pady=10
        )

def update_statistics(self):
        if not self.filtered_places:
            return
            
        df = pd.DataFrame(self.filtered_places)
        
        stats = {
            'Total Places': len(df),
            'Unique Land Uses': df['land_use'].nunique(),
            'Most Common Land Use': df['land_use'].mode().iloc[0],
            'Average Distance': f"{df['distance'].mean():.2f} km",
            'Max Distance': f"{df['distance'].max():.2f} km"
        }
        
        self.stats_text.delete(1.0, tk.END)
        for key, value in stats.items():
            self.stats_text.insert(tk.END, f"{key}: {value}\n")

def on_search_table(self, *args):
        search_term = self.search_var.get().lower()
        
        for row in self.table.get_children():
            self.table.delete(row)
            
        for place in self.filtered_places:
            if any(search_term in str(value).lower() 
                  for value in place.values()):
                self.table.insert("", "end", values=(
                    place['id'],
                    place['name'],
                    place['place_type'],
                    place['land_use'],
                    place.get('prediction_source', 'N/A'), 
                    place['distance'],
                    f"{place['elevation']:.1f}"

                ))

def update_table(self, places):
        for row in self.table.get_children():
            self.table.delete(row)
            
        for place in places:
            self.table.insert("", "end", values=(
                place['id'],
                place['name'],
                place['place_type'],
                place['land_use'],
                place.get('prediction_source', 'N/A'), 
                place['distance'],
                f"{place['elevation']:.1f}"
            ))

def on_search(self):
        try:
            coords = self.entry_coords.get().strip()
            self.user_lat, self.user_lng = map(float, coords.split(','))
            self.current_radius = float(self.entry_radius.get())
            
            # Get places from both local data and OSM
            self.filtered_places = self.get_combined_places()
            
            # Update GUI
            self.update_table(self.filtered_places)
            self.update_statistics()
            self.generate_all_maps()
            
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {str(e)}")