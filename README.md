# SokoSQ-Backend-Test

# Weather API

A simple FastAPI application that provides a weather API, interacting with an SQLite database to store and retrieve weather data. The API allows users to add new weather data and retrieve weather data for a specific city. The project also includes tests to ensure the functionality works as expected.

## Setup Instructions

### Prerequisites

- Python 3.7+
- pip (Python package installer)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/weather_api.git
   cd weather_api

   ```

2. **Create and activate virtual Environment**

   ```bash
    python3 -m venv venv
    source venv/bin/activate

   ```

3. **Install the required dependencies**

   ```bash
       pip install -r requirements.txt

   ```

### Running the application

1. **Run the FastAPI application**

   ```bash
   uvicorn app.app:app --reload
   ```

   The API will be available at http://127.0.0.1:8000

   An API Documentation is located at http://localhost:8000/docs

2. **API Endpoints**

   ```bash
    POST /weather
    GET /weather/{city}
   ```

3. **Running The Test**

   ```bash
    pytest tests/test.py

   ```
