# Real-Time IoT Data Monitoring with ESP32, Firebase, and Machine Learning

## Project Overview

This project aims to build a real-time IoT monitoring application using an ESP32 microcontroller to capture data from sensors, which is then visualized and analyzed using Python's Tkinter. The data is sent and stored in a Firebase database, making it accessible for immediate analysis, monitoring, and predictive modeling using machine learning.
[](./diagram.png)


## Features

- **Real-Time Data Acquisition**: Using sensors connected to an ESP32, data is collected and transmitted in real time.
- **Firebase Integration**: The ESP32 sends the data to Firebase, where it is stored and available for real-time access.
- **Visualization**: A Tkinter-based GUI application fetches data from Firebase and displays it in real time.
- **Machine Learning Prediction**: Using historical data, a machine learning model is trained to predict future values, adding predictive insights to the real-time monitoring.
- **User-Friendly Interface**: Built with Python's Tkinter for ease of use and interaction with real-time sensor data.

## Project Structure

- **`main.ino`**: The Arduino file for ESP32 containing code for reading sensor data and uploading it to Firebase.
- **`Tkinter-app.py`**: The Python application that fetches data from Firebase, visualizes it in real time, and performs predictions.

## Components

### 1. Data Acquisition with ESP32
   The ESP32 microcontroller is equipped with various sensors to gather environmental data. The data is collected through these sensors, and the ESP32 is programmed to upload this data to Firebase. This is managed by an `.ino` file, which provides the main loop and logic for the ESP32.

### 2. ESP32 Configuration
   - **Hardware Setup**: The sensors are connected to the ESP32, which reads and processes sensor data. 
   - **Software Setup**: The `.ino` file for the ESP32 contains all necessary configurations to communicate with Firebase. 
   - **Libraries**: Ensure the ESP32 library and Firebase libraries are installed in the Arduino IDE for successful compilation.

### 3. Real-Time Visualization with Tkinter and Firebase
   Using Firebase's Realtime Database SDK and Python’s Tkinter library, the application fetches data from Firebase and displays it live. This component provides a clear visualization of the data, allowing for easier monitoring and analysis.

### 4. Predictive Modeling with Machine Learning
   - **Historical Data Collection**: Data collected over time is stored in Firebase, allowing it to be used for model training.
   - **Machine Learning Model**: Using a machine learning model (e.g., linear regression or a time-series model), the application predicts future sensor data values based on historical trends.
   - **Prediction Visualization**: Predictions are visualized alongside real-time data, enabling users to anticipate changes and detect potential anomalies.

## How to Build and Run

### Prerequisites

- **ESP32 Development Board**: The primary hardware for data acquisition.
- **Sensors**: Depending on the type of data being collected, appropriate sensors need to be connected to the ESP32.
- **Firebase Realtime Database**: Set up a Firebase project and create a real-time database for data storage.
- **Arduino IDE**: For programming the ESP32.
- **Python 3**: Required for running the Tkinter application and ML model.
- **Firebase Admin SDK**: To connect the Tkinter application to Firebase.
- **Tkinter Library**: For GUI development in Python.
- **Machine Learning Libraries**: Install libraries like `scikit-learn` and `pandas` for data processing and modeling.

### Step-by-Step Instructions

1. **Set up Firebase**: 
   - Create a Firebase project and set up the Realtime Database.
   - Obtain the credentials file for Firebase authentication.

2. **Upload Code to ESP32**:
   - Open the `Project Phase 2.ino` file in the Arduino IDE.
   - Update the Firebase authentication and Wi-Fi credentials.
   - Upload the code to the ESP32.

3. **Run the Tkinter Visualization**:
   - Install required Python packages:
     ```bash
     pip install firebase-admin scikit-learn pandas
     ```
   - Open `Tkinter-app.py` and run the script to start the real-time visualization and prediction.

### Hardware Used

- **ESP32**: Microcontroller for data acquisition and wireless data transmission.
- **Sensors**: Attach necessary sensors for data you wish to monitor (e.g., temperature, humidity).
- **Power Supply**: To power the ESP32 and connected sensors.

## Database Structure

The Firebase Realtime Database organizes the data in a JSON structure, allowing easy access and retrieval by both the ESP32 and the Tkinter application.

## Future Improvements

- Expanding the types of sensors and incorporating additional machine learning models.
- Adding more advanced visualization options for enhanced user interaction.
- Implementing offline data storage in case of network issues.
