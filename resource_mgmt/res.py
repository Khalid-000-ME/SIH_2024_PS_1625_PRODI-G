import numpy as np
import pandas as pd
import random
import time
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

class ResourceManager:
    def __init__(self):
        # Initial state of the resources
        self.resources = {
            'projectors': {'status': False, 'usage': 0},
            'fans': {'status': False, 'usage': 0},
            'lights': {'status': False, 'usage': 0}
        }
        
        # Data storage for AI model
        self.history = {resource: [] for resource in self.resources}
        self.model = LinearRegression()
        self.scaler = StandardScaler()
    
    def get_resource_data(self):
        # Simulate real-time data acquisition
        for resource in self.resources:
            self.resources[resource]['usage'] = random.uniform(0, 100)
            self.history[resource].append(self.resources[resource]['usage'])
            if len(self.history[resource]) > 100:  # Keep last 100 data points
                self.history[resource].pop(0)
    
    def train_model(self):
        # Prepare data for training
        for resource, usages in self.history.items():
            if len(usages) < 10:
                continue
            X = np.array(range(len(usages))).reshape(-1, 1)
            y = np.array(usages)
            X_scaled = self.scaler.fit_transform(X)
            self.model.fit(X_scaled, y)
    
    def predict_usage(self):
        # Predict future usage
        predictions = {}
        for resource, usages in self.history.items():
            if len(usages) < 10:
                predictions[resource] = self.resources[resource]['usage']
                continue
            X_new = np.array([[len(usages)]])
            X_new_scaled = self.scaler.transform(X_new)
            predicted_usage = self.model.predict(X_new_scaled)
            predictions[resource] = predicted_usage[0]
        return predictions
    
    def regulate_resources(self):
        predictions = self.predict_usage()
        for resource, predicted_usage in predictions.items():
            if predicted_usage > 80:  # If predicted usage is more than 80%
                self.turn_off_resource(resource)
            elif predicted_usage < 20:  # If predicted usage is less than 20%
                self.turn_on_resource(resource)
    
    def turn_on_resource(self, resource):
        if not self.resources[resource]['status']:
            self.resources[resource]['status'] = True
            print(f"{resource.capitalize()} turned ON")
    
    def turn_off_resource(self, resource):
        if self.resources[resource]['status']:
            self.resources[resource]['status'] = False
            print(f"{resource.capitalize()} turned OFF")
    
    def display_status(self):
        for resource, data in self.resources.items():
            status = 'ON' if data['status'] else 'OFF'
            print(f"{resource.capitalize()}: Status={status}, Usage={data['usage']:.2f}%")
    
    def run(self):
        while True:
            self.get_resource_data()
            self.train_model()  # Train model with new data
            self.regulate_resources()
            self.display_status()
            time.sleep(5)  # Wait for 5 seconds before the next check

if __name__ == "__main__":
    manager = ResourceManager()
    manager.run()
