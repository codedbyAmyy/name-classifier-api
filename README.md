# Name Classifier API

## 🚀 Endpoint
GET /api/classify?name={name}

## 🔧 Description
This API integrates with Genderize.io to predict gender based on a name.

## 📥 Example Request
/api/classify?name=John

## 📤 Example Response
{
  "status": "success",
  "data": {
    "name": "john",
    "gender": "male",
    "probability": 0.99,
    "sample_size": 1234,
    "is_confident": true,
    "processed_at": "2026-04-01T12:00:00Z"
  }
}

## ⚙️ Tech Stack
- FastAPI
- Python