# Weather Dashboard 🌦️

A web dashboard for visualizing weather conditions, built with Python and Dash.

---

## 🚀 Features

- 📆 Displays daily weather conditions  
- 🎨 Clean UI using Dash and Plotly  
- 🐳 Dockerized for easy deployment  
- ☁️ Hosted on Scaleway Serverless Containers  

---
###🛠️ Technologies Used
Python
Dash
Plotly
Docker
Scaleway Serverless Containers
---

## 🧪 Run Locally

### Requirements

- Python 3.11+
- pip

### Steps

1. Clone the repository  
   ```bash
   git clone https://github.com/allienka/weather-dashboard.git
   cd weather-dashboard
   ```

2. Install dependencies  
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app  
   ```bash
   python app.py
   ```
   Visit the app at: [http://localhost:8050](http://localhost:8050)

---

## 🐳 Docker Usage

1. Build the image  
   ```bash
   docker build -t weather-dashboard .
   ```

2. Run the container  
   ```bash
   docker run -p 8050:8050 weather-dashboard
   ```

---

## ☁️ Deployment on Scaleway

This app is deployed using Scaleway Serverless Containers.

### 🔐 Scaleway Registry Info

- **Registry Namespace:** `funcscwweatherdashboards2snn3wrj`  
- **Image:** `weather-dashboard`  
- **Tag:** `latest`  
- **Container Port:** `8050`

### 🌍 Access the App:
[https://weatherdashboards2snn3wrj-weather-dashboards.functions.fnc.fr-par.scw.cloud](https://weatherdashboards2snn3wrj-weather-dashboards.functions.fnc.fr-par.scw.cloud)

