---
## **Presentation Video Link**
https://drive.google.com/file/d/14k7aC8pyleztVMZV1BaIT1MlKch8UmmS/view?usp=drive_link
# Django Fuel Route Optimization API

This API calculates optimal fuel stops for a given route in the USA based on fuel prices and vehicle range. It provides a map of the route and calculates the total money spent on fuel for the journey.

---

## **Assignment Description**

**Objective**:  
Build a Django-based API that:
1. Accepts start and finish locations within the USA.
2. Returns:
   - A map of the route.
   - Optimal fuel stops (cost-effective, based on fuel prices).
   - Total money spent on fuel (assuming the vehicle achieves 10 miles per gallon with a 500-mile range per tank).

---

## **Features**

- **Routing**: Uses a free routing API (HERE Maps API) to calculate the route.
- **Fuel Optimization**: Identifies cost-effective fuel stops along the route based on fuel prices provided.
- **Minimal API Calls**: Limits API calls to the routing service to ensure quick responses.
- **RESTful Design**: Built using Django REST Framework for seamless integration.
- **High Performance**: Optimized to return results quickly by preprocessing fuel station data.

---

## **Tech Stack**

- **Framework**: Django 3.2.23
- **APIs**:
  - [HERE Geocoding and Routing API](https://developer.here.com/)
- **Key Libraries**:
  - `geopy`: For distance calculations.
  - `requests`: For making HTTP requests to external APIs.
  - `python-dotenv`: For managing environment variables.

---

## **Requirements**

- **Python**: 3.8+
- **Dependencies**:
  ```plaintext
  Django==3.2.23
  djangorestframework==3.15.1
  geopy==2.4.1
  requests==2.32.3
  python-dotenv==1.0.1
  pytz==2024.2
  ```

---

## **Setup Instructions**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repository/fuel-route-optimization.git
   cd fuel-route-optimization
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   - Create a `.env` file in the project root and add your HERE API key:
     ```plaintext
     HERE_API_KEY=your_here_api_key
     ```

5. **Run Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```

---

## **Usage**

### **Endpoint**

- **URL**: `/route/`
- **Method**: `GET`
- **Query Parameters**:
  - `start`: Starting location (e.g., `New York, NY`).
  - `finish`: Ending location (e.g., `Los Angeles, CA`).

### **Example Request**:
```plaintext
GET http://127.0.0.1:8000/api/route/?start=New York, NY&finish=Los Angeles, CA
```

### **Example Response**:
```json
{
    "route": {
        "id": "route-id",
        "sections": [
            {
                "departure": {
                    "time": "2025-01-15T02:52:50-07:00",
                    "place": {
                        "location": {
                            "lat": 40.7128,
                            "lng": -74.0060
                        }
                    }
                },
                "arrival": {
                    "time": "2025-01-16T06:48:32-05:00",
                    "place": {
                        "location": {
                            "lat": 34.0522,
                            "lng": -118.2437
                        }
                    }
                },
                "transport": {
                    "mode": "car"
                }
            }
        ]
    },
    "fuel_data": {
        "stops": [
            {
                "location": "Fuel Stop Name, City, State",
                "price_per_gallon": 3.25
            },
            {
                "location": "Fuel Stop Name, City, State",
                "price_per_gallon": 3.15
            }
        ],
        "total_fuel_cost": 250.00
    }
}
```

---

## **Code Walkthrough**

### **Fuel Stop Calculation**
- Dynamically calculates fuel stops along the route based on:
  - Maximum vehicle range (500 miles).
  - Fuel prices provided in the dataset.

### **Key Features**
1. **Optimal Fuel Stops**:
   - Considers fuel prices and proximity to the route.
2. **Minimal API Calls**:
   - One or two calls to the HERE Routing API, minimizing latency.

### **Performance Optimizations**:
- Preprocessed fuel station data ensures quick lookup and avoids repeated geocoding calls.

---
