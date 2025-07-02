import datetime

class Logger:
    def __init__(self, filename="history.txt"):
        self.filename = filename

    def log_action(self, action, details=""):
        """Log an action with timestamp and details to the history file."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {action}: {details}\n"
        
        try:
            with open(self.filename, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Error writing to log file: {str(e)}")

    def log_display_map(self):
        """Log when the map is displayed."""
        self.log_action("Display Map", "Map and roads displayed")

    def log_add_location(self, location_data):
        """Log when a new location is added."""
        details = f"Added location ID: {location_data['id']}, Name: {location_data['name']}, Type: {location_data['type']}"
        self.log_action("Add Location", details)

    def log_add_road(self, road_data):
        """Log when a new road is added."""
        details = f"Added road from ID: {road_data['from_id']} to ID: {road_data['to_id']}, Vehicles: {road_data['allowed_vehicles']}, Oneway: {road_data['is_oneway']}"
        self.log_action("Add Road", details)

    def log_delete_location(self, location_id):
        """Log when a location is deleted."""
        details = f"Deleted location ID: {location_id}"
        self.log_action("Delete Location", details)

    def log_find_path(self, path_data, start_name, end_name, total_time):
        """Log when a path is found."""
        details = f"Path from {start_name} to {end_name}, Vehicle: {path_data['vehicle']}, Metric: {path_data['metric']}, Total time: {total_time:.2f} minutes"
        self.log_action("Find Path", details)

    def log_find_nearby(self, search_data, selected_id, vehicle, total_time):
        """Log when nearby locations are searched."""
        details = f"Searched for {search_data['location_type']} near ID: {search_data['start']}, Selected ID: {selected_id}, Vehicle: {vehicle}, Total time: {total_time:.2f} minutes"
        self.log_action("Find Nearby", details)

    def log_statistics(self):
        """Log when statistics are displayed."""
        self.log_action("Display Statistics", "Statistics displayed")