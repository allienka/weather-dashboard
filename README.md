# Weather Dashboard 🌦️

A web dashboard for visualizing weather conditions, built with Python and Dash.

## 🚀 Features
- Displays daily weather conditions
- Clean UI using Dash
- Dockerized for easy deployment
- Hosted on [Scaleway Serverless Containers](https://www.scaleway.com/en/serverless/containers/)

## 🧪 Run Locally

### Requirements
- Python 3.11+
- pip

### 1. Clone the repository
```bash
git clone https://github.com/allienka/weather-dashboard.git
cd weather-dashboard
2. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
3. Run the app
bash
Copy
Edit
python app.py
Visit: http://localhost:8050

🐳 Docker
Build the image
bash
Copy
Edit
docker build -t weather-dashboard .
Run the container
bash
Copy
Edit
docker run -p 8050:8050 weather-dashboard
☁️ Deployment on Scaleway
This app is deployed using Scaleway Serverless Containers.

Scaleway Registry Info
Registry Namespace: funcscwweatherdashboards2snn3wrj

Image: weather-dashboard

Tag: latest

Container Port: 8050

Public Endpoint
📍 https://<your-endpoint>.scw.cloud

🛠️ Technologies Used
Python

Dash

Plotly

Docker

Scaleway
