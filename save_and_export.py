from tkinter import ttk, messagebox
import datetime
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import webbrowser
import pandas as pd
from tkinter import filedialog

def save_results(self):
        """Save current results to a file"""
        if not self.filtered_places:
            messagebox.showwarning("Warning", "No results to save")
            return
        
        try:
            # Create filename with timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = f"land_use_results_{timestamp}"
            
            # Ask user for save location and format
            file_types = [
                ("CSV files", "*.csv"),
                ("Excel files", "*.xlsx"),
                ("JSON files", "*.json")
            ]
            
            filename = filedialog.asksaveasfilename(
                initialdir=self.analysis_folder,
                initialfile=default_filename,
                title="Save Results As",
                filetypes=file_types,
                defaultextension=".csv"
            )
            
            if not filename:
                return
                
            # Convert results to DataFrame
            df = pd.DataFrame(self.filtered_places)
            
            # Save based on file extension
            if filename.endswith('.csv'):
                df.to_csv(filename, index=False)
            elif filename.endswith('.xlsx'):
                df.to_excel(filename, index=False)
            elif filename.endswith('.json'):
                df.to_json(filename, orient='records', indent=2)
                
            messagebox.showinfo("Success", f"Results saved successfully to:\n{filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save results: {str(e)}")


def export_data(self, format_type):
        if not self.filtered_places:
            messagebox.showwarning("Warning", "No data to export")
            return
            
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            df = pd.DataFrame(self.filtered_places)
            
            file_types = {
                "csv": ("CSV files", "*.csv"),
                "excel": ("Excel files", "*.xlsx")
            }
            
            filename = filedialog.asksaveasfilename(
                initialdir=self.analysis_folder,
                title=f"Save as {format_type.upper()}",
                filetypes=[file_types[format_type], ("All files", "*.*")],
                defaultextension=file_types[format_type][1]
            )
            
            if filename:
                if format_type == "csv":
                    df.to_csv(filename, index=False)
                else:
                    df.to_excel(filename, index=False)
                    
                messagebox.showinfo("Success", f"Data exported successfully to {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")

def export_all_maps(self):
        """Export all map types to local folder"""
        if not self.filtered_places:
            messagebox.showwarning("Warning", "No data to visualize")
            return
            
        try:
            # Create export folder with timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            export_folder = os.path.join(self.maps_folder, f"maps_export_{timestamp}")
            os.makedirs(export_folder, exist_ok=True)
            
            # Generate and save all map types
            map_generators = {
                'standard': self.generate_standard_map,
                'heat': self.generate_heat_map,
                'cluster': self.generate_cluster_map,
                'choropleth': self.generate_choropleth_map,
                'Elevation_Map': self.generate_elevation_map
             

            }
            
            saved_maps = []
            for map_type, generator in map_generators.items():
                try:
                    map_obj = generator()
                    filename = os.path.join(export_folder, f"map_{map_type}.html")
                    map_obj.save(filename)
                    saved_maps.append((map_type, filename))
                except Exception as e:
                    print(f"Failed to generate {map_type} map: {str(e)}")
            
            # Create index.html
            index_html = f"""
            <html>
            <head>
                <title>Land Use Analysis Maps</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }}
                    .map-container {{ margin-bottom: 40px; }}
                    h1, h2, h3 {{ color: #333; }}
                    .nav {{ position: fixed; top: 20px; right: 20px; 
                        background: white; padding: 10px; border: 1px solid #ddd; }}
                    iframe {{ border: 1px solid #ddd; }}
                </style>
            </head>
            <body>
                <div class="nav">
                    <h3>Quick Navigation</h3>
                    {' '.join(f'<a href="#{map_type}">{map_type.title()}</a><br>' 
                            for map_type, _ in saved_maps)}
                </div>
                
                <h1>Land Use Analysis Maps</h1>
                <p><strong>Generated on:</strong> {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                <p><strong>Location:</strong> {self.user_lat}, {self.user_lng}</p>
                <p><strong>Search Radius:</strong> {self.current_radius} meters</p>
                <p><strong>Total Places:</strong> {len(self.filtered_places)}</p>
                
                {' '.join(f'''
                <div class="map-container" id="{map_type}">
                    <h2>{map_type.title()} Map</h2>
                    <iframe src="{os.path.basename(filename)}" 
                            width="100%" height="600px"></iframe>
                </div>'''
                for map_type, filename in saved_maps)}
            </body>
            </html>
            """
            
            index_path = os.path.join(export_folder, "index.html")
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(index_html)
                
            webbrowser.open('file://' + os.path.abspath(index_path))
            messagebox.showinfo("Success", 
                            f"Maps exported to:\n{export_folder}\n\nOpening index.html...")
            
        except Exception as e:
            messagebox.showerror("Error", f"Map export failed: {str(e)}")


def export_analysis_report(self):
        """Generate and export a comprehensive analysis report"""
        if not self.filtered_places:
            messagebox.showwarning("Warning", "No data to analyze")
            return
            
        try:
            # Create analysis folder if it doesn't exist
            os.makedirs(self.analysis_folder, exist_ok=True)
            
            # Generate timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(self.analysis_folder, f"analysis_report_{timestamp}.html")
            
            df = pd.DataFrame(self.filtered_places)
            
            # Create visualizations
            plt.figure(figsize=(10, 6))
            df['land_use'].value_counts().plot(kind='bar')
            plt.title("Land Use Distribution")
            plt.tight_layout()
            land_use_plot = os.path.join(self.analysis_folder, f"land_use_dist_{timestamp}.png")
            plt.savefig(land_use_plot)
            plt.close()
            
            plt.figure(figsize=(10, 6))
            sns.histplot(data=df, x='distance')
            plt.title("Distance Distribution")
            plt.tight_layout()
            distance_plot = os.path.join(self.analysis_folder, f"distance_dist_{timestamp}.png")
            plt.savefig(distance_plot)
            plt.close()
            
            # Generate HTML report
            html_content = f"""
            <html>
            <head>
                <title>Land Use Analysis Report</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }}
                    table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                    th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                    th {{ background-color: #f5f5f5; }}
                    img {{ max-width: 100%; height: auto; margin: 20px 0; }}
                    .section {{ margin: 30px 0; }}
                    h1, h2, h3 {{ color: #333; }}
                </style>
            </head>
            <body>
                <h1>Land Use Analysis Report</h1>
                <p><strong>Generated on:</strong> {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                
                <div class="section">
                    <h2>Search Parameters</h2>
                    <p><strong>Center Location:</strong> {self.user_lat}, {self.user_lng}</p>
                    <p><strong>Search Radius:</strong> {self.current_radius} meters</p>
                </div>
                
                <div class="section">
                    <h2>Summary Statistics</h2>
                    <table>
                        <tr><th>Metric</th><th>Value</th></tr>
                        <tr><td>Total Places</td><td>{len(df)}</td></tr>
                        <tr><td>Unique Land Uses</td><td>{df['land_use'].nunique()}</td></tr>
                        <tr><td>Average Distance</td><td>{df['distance'].mean():.2f} km</td></tr>
                        <tr><td>Maximum Distance</td><td>{df['distance'].max():.2f} km</td></tr>
                        <tr><td>Most Common Land Use</td><td>{df['land_use'].mode().iloc[0]}</td></tr>
                    </table>
                </div>
                
                <div class="section">
                    <h2>Land Use Distribution</h2>
                    <img src="{os.path.basename(land_use_plot)}" alt="Land Use Distribution">
                    {df['land_use'].value_counts().to_frame().to_html()}
                </div>
                
                <div class="section">
                    <h2>Distance Analysis</h2>
                    <img src="{os.path.basename(distance_plot)}" alt="Distance Distribution">
                    {df['distance'].describe().to_frame().to_html()}
                </div>
                
                <div class="section">
                    <h2>Detailed Place List</h2>
                    {df.to_html()}
                </div>
            </body>
            </html>
            """
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
                
            webbrowser.open('file://' + os.path.abspath(filename))
            messagebox.showinfo("Success", f"Analysis report generated: {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Report generation failed: {str(e)}")

def export_model_report(self):
        """Generate and export a comprehensive model analysis report"""
        if not hasattr(self, 'model') or self.model is None:
            messagebox.showwarning("Warning", "No trained model available")
            return
            
        try:
            # Create analysis folder if it doesn't exist
            os.makedirs(self.analysis_folder, exist_ok=True)
            
            # Generate timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Create training history plots
            plt.figure(figsize=(12, 4))
            
            # Plot training history
            plt.subplot(1, 2, 1)
            plt.plot(self.history.history['accuracy'], label='Training Accuracy')
            plt.plot(self.history.history['val_accuracy'], label='Validation Accuracy')
            plt.title('Model Accuracy')
            plt.xlabel('Epoch')
            plt.ylabel('Accuracy')
            plt.legend()
            
            plt.subplot(1, 2, 2)
            plt.plot(self.history.history['loss'], label='Training Loss')
            plt.plot(self.history.history['val_loss'], label='Validation Loss')
            plt.title('Model Loss')
            plt.xlabel('Epoch')
            plt.ylabel('Loss')
            plt.legend()
            
            plt.tight_layout()
            history_plot = os.path.join(self.analysis_folder, f"training_history_{timestamp}.png")
            plt.savefig(history_plot)
            plt.close()
            
            # Generate confusion matrix
            cm = confusion_matrix(self.y_test, self.y_pred_classes)
            plt.figure(figsize=(10, 8))
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                        xticklabels=[self.reverse_mapping[i] for i in range(len(self.reverse_mapping))],
                        yticklabels=[self.reverse_mapping[i] for i in range(len(self.reverse_mapping))])
            plt.title('Confusion Matrix')
            plt.xlabel('Predicted')
            plt.ylabel('True')
            plt.tight_layout()
            cm_plot = os.path.join(self.analysis_folder, f"confusion_matrix_{timestamp}.png")
            plt.savefig(cm_plot)
            plt.close()
            
            # Generate classification report
            class_report = classification_report(
                self.y_test,
                self.y_pred_classes,
                target_names=[self.reverse_mapping[i] for i in range(len(self.reverse_mapping))]
            )

            # Calculate prediction source statistics for both data sources
            prediction_stats = ""
            
            # OSM Data Statistics
            self.osm_total = sum(self.osm_prediction_sources.values())
            if self.osm_total > 0:
                osm_model_percent = (self.osm_prediction_sources['model']/self.osm_total)*100
                osm_rule_based_percent = (self.osm_prediction_sources['rule-based']/self.osm_total)*100
                prediction_stats += f"""
                <div class="metrics">
                    <h3>OSM Data Prediction Sources</h3>
                    <p><strong>Total predictions:</strong> {self.osm_total}</p>
                    <p><strong>ML Model predictions:</strong> {self.osm_prediction_sources['model']} ({osm_model_percent:.1f}%)</p>
                    <p><strong>Rule-based predictions:</strong> {self.osm_prediction_sources['rule-based']} ({osm_rule_based_percent:.1f}%)</p>
                </div>
                """
            
            # Google Places API Statistics
            self.google_total=sum(self.google_prediction_sources.values())
            if self.google_total > 0:
                google_model_percent = (self.google_prediction_sources['model']/self.google_total)*100
                google_rule_based_percent = (self.google_prediction_sources['rule-based']/self.google_total)*100
                prediction_stats += f"""
                <div class="metrics">
                    <h3>Google Places API Prediction Sources</h3>
                    <p><strong>Total predictions:</strong> {self.google_total}</p>
                    <p><strong>ML Model predictions:</strong> {self.google_prediction_sources['model']} ({google_model_percent:.1f}%)</p>
                    <p><strong>Rule-based predictions:</strong> {self.google_prediction_sources['rule-based']} ({google_rule_based_percent:.1f}%)</p>
                </div>
                """
            
            # Combined Statistics
            total_predictions = self.osm_total + self.google_total
            if total_predictions > 0:
                total_model = self.osm_prediction_sources['model'] + self.google_prediction_sources['model']
                total_rule_based = self.osm_prediction_sources['rule-based'] + self.google_prediction_sources['rule-based']
                total_model_percent = (total_model/total_predictions)*100
                total_rule_based_percent = (total_rule_based/total_predictions)*100
                prediction_stats += f"""
                <div class="metrics">
                    <h3>Combined Prediction Sources</h3>
                    <p><strong>Total predictions:</strong> {total_predictions}</p>
                    <p><strong>ML Model predictions:</strong> {total_model} ({total_model_percent:.1f}%)</p>
                    <p><strong>Rule-based predictions:</strong> {total_rule_based} ({total_rule_based_percent:.1f}%)</p>
                </div>
                """
            
            # Generate HTML report
            html_content = f"""
            <html>
            <head>
                <title>Land Use Classification Model Report</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }}
                    pre {{ background-color: #f5f5f5; padding: 15px; border-radius: 5px; }}
                    .section {{ margin: 30px 0; }}
                    h1, h2 {{ color: #333; }}
                    .metrics {{ background-color: #f8f9fa; padding: 20px; border-radius: 5px; }}
                    img {{ max-width: 100%; height: auto; margin: 20px 0; }}
                </style>
            </head>
            <body>
                <h1>Land Use Classification Model Report</h1>
                <p><strong>Generated on:</strong> {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                
                <div class="section">
                    <h2>Model Architecture</h2>
                    <pre>{''.join(self.model_summary)}</pre>
                </div>
                
                <div class="section">
                    <h2>Training Metrics</h2>
                    <div class="metrics">
                        <p><strong>Final Test Accuracy:</strong> {self.test_accuracy:.4f}</p>
                        <p><strong>Final Test Loss:</strong> {self.test_loss:.4f}</p>
                    </div>
                </div>
                
                <div class="section">
                    <h2>Training History</h2>
                    <img src="{os.path.basename(history_plot)}" alt="Training History">
                </div>
                
                <div class="section">
                    <h2>Confusion Matrix</h2>
                    <img src="{os.path.basename(cm_plot)}" alt="Confusion Matrix">
                </div>
                <div class="metrics">
                    <h3>Google Places API Prediction Sources</h3>
                    <p><strong>Total predictions:</strong> {self.google_total}</p>
                    <p><strong>ML Model predictions:</strong> {self.google_prediction_sources['model']} ({google_model_percent:.1f}%)</p>
                    <p><strong>Rule-based predictions:</strong> {self.google_prediction_sources['rule-based']} ({google_rule_based_percent:.1f}%)</p>
                </div>
                <div class="metrics">
                    <h3>OSM Data Prediction Sources</h3>
                    <p><strong>Total predictions:</strong> {self.osm_total}</p>
                    <p><strong>ML Model predictions:</strong> {self.osm_prediction_sources['model']} ({osm_model_percent:.1f}%)</p>
                    <p><strong>Rule-based predictions:</strong> {self.osm_prediction_sources['rule-based']} ({osm_rule_based_percent:.1f}%)</p>
                </div>
                <div class="metrics">
                    <h3>Combined Prediction Sources</h3>
                    <p><strong>Total predictions:</strong> {total_predictions}</p>
                    <p><strong>ML Model predictions:</strong> {total_model} ({total_model_percent:.1f}%)</p>
                    <p><strong>Rule-based predictions:</strong> {total_rule_based} ({total_rule_based_percent:.1f}%)</p>
                </div>
                <div class="section">
                    <h2>Classification Report</h2>
                    <pre>{class_report}</pre>
                </div>
            </body>
            </html>
            """
            
            # Save and open report
            report_path = os.path.join(self.analysis_folder, f"model_report_{timestamp}.html")
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
                
            webbrowser.open('file://' + os.path.abspath(report_path))
            messagebox.showinfo("Success", f"Model report generated successfully at:\n{report_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate model report: {str(e)}")