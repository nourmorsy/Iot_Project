import tkinter as tk
from tkinter import scrolledtext, Frame
from firebase_admin import credentials, initialize_app, db
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import matplotlib.dates as mdates
from sklearn.linear_model import LinearRegression
import pandas as pd
# Initialize Firebase admin SDK
databaseURL = 'https://esp32-895b5-default-rtdb.firebaseio.com/'
cred_obj = credentials.Certificate('Key.json')
default_app = initialize_app(cred_obj, {'databaseURL': databaseURL})

# Set up the Tkinter application
class DataMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Firebase Data Monitor")
        self.model = LinearRegression()
        self.cnt = 0
        # Create a frame for the text display
        self.text_frame = Frame(root)
        self.text_frame.pack(side="right", fill="both", expand=True)
        
        self.display = scrolledtext.ScrolledText(self.text_frame, width=70, height=10)
        self.display.pack(pady=20)
        # Create a frame for the chart
        self.chart_frame = Frame(root)
        self.chart_frame.pack(side="left", fill="both", expand=True)
        #create a frame for the chart
        self.chart_frame2 = Frame(root)
        self.chart_frame2.pack(side="bottom", fill="both", expand=True)
        # create a frame for the chart
        # self.chart_frame3 = Frame(root)
        # self.chart_frame3.pack(side="bottom", fill="both", expand=True)
        # # #create a frame for the chart
        # self.chart_frame4 = Frame(root)
        # self.chart_frame4.pack(side="bottom", fill="both", expand=True)
        # Setting up the chart
        self.fig, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side="left", fill="both", expand=True)
        #setting up the chart
        self.fig2, self.bx = plt.subplots(figsize=(5, 4))
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self.chart_frame2)
        self.canvas2.draw()
        self.canvas2.get_tk_widget().pack(side="bottom", fill="both", expand=True)
        # #setting up the chart
        # self.fig3, self.cx = plt.subplots(figsize=(5, 4))
        # self.canvas3 = FigureCanvasTkAgg(self.fig3, master=self.chart_frame3)
        # self.canvas3.draw()
        # self.canvas3.get_tk_widget().pack(side="left", fill="both", expand=True)
        # # #setting up the chart
        # self.fig4, self.dx = plt.subplots(figsize=(5, 4))
        # self.canvas4 = FigureCanvasTkAgg(self.fig4, master=self.chart_frame4)
        # self.canvas4.draw()
        # self.canvas4.get_tk_widget().pack(side="bottom", fill="both", expand=True)
        self.dates = []
        self.Temperatures = []
        self.Humidity = []
        self.temp = []
        self.humi = []
        self.time = []
        self.predict_temp = []
        self.predict_humi = []
        # Initialize the Firebase listener in the app
        self.ref = db.reference("/temp-humi")
        self.ref.listen(self.firebase_listener)

    def firebase_listener(self, event):
        try:
            # Check for dict structure and key existence
            if isinstance(event.data, dict) and 'Temperature' in event.data and 'timestamp' in event.data:
                # Handling possible milliseconds timestamp format
                timestamp = datetime.fromtimestamp(event.data['timestamp'] / 1000)
                Temperature = event.data['Temperature']
                Humidity = event.data['Humidity']
                self.temp.append(Temperature)
                self.time.append(self.cnt)
                self.humi.append(Humidity)
                self.update_chart(timestamp, Temperature,Humidity)
                event_data = f"Event Type: {event.event_type}\nPath: {event.path}\nData: {event.data}\n\n"
                self.update_display(event_data)
                self.cnt+=1
                if self.cnt %10 == 0:
                    self.train()
                    print("Model trained")
                    self.predict()
        except Exception as e:
            print(f"Error processing event data: {e}")
    def train(self):
        X = {"timestamp": self.time}
        y = {"Temperature":self.temp,"Humidity":self.humi}
        X = pd.DataFrame(X)
        y = pd.DataFrame(y)
        self.model.fit(X.values.reshape(-1,1), y)
    def predict(self):
        dates = []
        for i in range(1,11):
            dates.append(self.cnt+i)
            self.predict_temp.append(self.model.predict([[self.cnt+i]])[0][0])
            self.predict_humi.append(self.model.predict([[self.cnt+i]])[0][1])
        if len(self.dates) > 10:  # Limit the lists to last 10 entries
            self.predict_temp = self.predict_temp[-10:]
            self.predict_humi = self.predict_humi[-10:]
        print(f"predict the next tempriatures: {self.predict_temp}")
        print(f"predict the next humidity: {self.predict_humi}")
        # self.cx.clear()
        # self.cx.plot(dates, self.predict_temp, marker='o')
        # self.cx.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        # self.cx.xaxis.set_major_locator(mdates.SecondLocator(interval=10))
        # self.cx.set_xlabel("Time")
        # self.cx.set_ylabel("predicted Temperatures")
        # self.fig3.autofmt_xdate()
        # self.canvas3.draw()
        # ----------------------------------------------------------------------------------------
        # self.dx.clear()
        # self.dx.plot(dates, self.predict_humi, marker='o')
        # self.dx.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        # self.dx.xaxis.set_major_locator(mdates.SecondLocator(interval=10))
        # self.dx.set_xlabel("Time")
        # self.dx.set_ylabel("predicted Humidity")
        # self.fig4.autofmt_xdate()
        # self.canvas4.draw()

    def update_display(self, message):
        # Update the display with new Firebase event data, keeping only last 10 entries
        self.display.config(state=tk.NORMAL)
        self.display.insert(tk.END, message)
        self.display_contents = self.display.get('1.0', tk.END).split('\n\n')
        if len(self.display_contents) > 10:  # Keep only the last 10 records
            self.display.delete('1.0', tk.END)
            new_content = '\n\n'.join(self.display_contents[-11:])
            self.display.insert(tk.END, new_content)
        self.display.config(state=tk.DISABLED)
        self.display.see(tk.END)

    def update_chart(self, timestamp, Temperature , Humidity):
        # Add new data to the chart and redraw, keeping only last 10 entries
        self.dates.append(timestamp)
        self.Temperatures.append(Temperature)
        self.Humidity.append(Humidity)
        if len(self.dates) > 10:  # Limit the lists to last 10 entries
            self.dates = self.dates[-10:]
            self.Temperatures = self.Temperatures[-10:]
            self.Humidity = self.Humidity[-10:]
        
        self.ax.clear()
        self.ax.plot(self.dates, self.Temperatures, marker='o')
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        self.ax.xaxis.set_major_locator(mdates.SecondLocator(interval=10))
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Temperatures")
        self.fig.autofmt_xdate()
        self.canvas.draw()
        # ----------------------------------------------------------------------------------------
        self.bx.clear()
        self.bx.plot(self.dates, self.Humidity, marker='o')
        self.bx.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        self.bx.xaxis.set_major_locator(mdates.SecondLocator(interval=10))
        self.bx.set_xlabel("Time")
        self.bx.set_ylabel("Humidity")
        self.fig2.autofmt_xdate()
        self.canvas2.draw()

# Create the main window and pass it to the DataMonitorApp class
if __name__ == "__main__":
    root = tk.Tk()
    app = DataMonitorApp(root)
    root.mainloop()
