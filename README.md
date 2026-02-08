# Intelligent FYP Recommendation API

This API provides intelligent final-year project recommendations using NLP and embeddings-based similarity. Built with **FastAPI**, it supports querying, searching, trends, and chatbot interactions.

---

## Base URL

```
http://<your-domain-or-ip>/
```

All endpoints accept **JSON** input and output.

---

## Endpoints

### 1️⃣ GET `/projects`

**Purpose:** Fetch all projects or filtered projects.

**Query Parameters (optional):**

| Parameter    | Type   | Description                                                             |
| ------------ | ------ | ----------------------------------------------------------------------- |
| `difficulty` | string | Filter projects by difficulty (e.g., Beginner, Intermediate, Advanced). |
| `hardware`   | string | Filter projects by hardware requirement.                                |
| `category`   | string | Filter projects by category (e.g., AI, Web, Robotics).                  |

**Response Example:**

```json
[
  {
    "id": 1,
    "title": "Deep Learning Medical Diagnosis",
    "description": "Analyze X-rays to detect diseases.",
    "difficulty": "Intermediate",
    "category": "AI",
    "hardware": "GPU",
    "technologies": ["Python", "TensorFlow", "Keras"]
  }
]
```

---

### 2️⃣ GET `/projects/{id}`

**Purpose:** Fetch a single project by its ID.

**Path Parameter:**

| Parameter | Type | Description          |
| --------- | ---- | -------------------- |
| `id`      | int  | Project ID to fetch. |

**Response Example:**

```json
{
  "id": 1,
  "title": "Deep Learning Medical Diagnosis",
  "description": "Analyze X-rays to detect diseases.",
  "difficulty": "Intermediate",
  "category": "AI",
  "hardware": "GPU",
  "technologies": ["Python", "TensorFlow", "Keras"]
}
```

---

### 3️⃣ POST `/recommend`

**Purpose:** Recommend projects based on user preferences.

**Request Body Example:**

```json
{
  "user_id": "123",
  "preferences": {
    "difficulty": "Beginner",
    "category": "AI",
    "hardware": "CPU",
    "interests": ["NLP", "Computer Vision"]
  }
}
```

**Response Example:**

```json
[
  {
    "id": 5,
    "title": "Simple NLP Chatbot",
    "description": "Create a rule-based chatbot for FAQs.",
    "difficulty": "Beginner",
    "category": "AI",
    "hardware": "CPU",
    "technologies": ["Python", "NLTK"]
  }
]
```

---

### 4️⃣ POST `/search`

**Purpose:** Search projects by keywords or technologies.

**Request Body Example:**

```json
{
  "query": "TensorFlow, computer vision"
}
```

**Response Example:**

```json
[
  {
    "id": 2,
    "title": "Real-Time Face Detection",
    "description": "Detect faces in real-time using TensorFlow.",
    "difficulty": "Intermediate",
    "category": "AI",
    "hardware": "GPU",
    "technologies": ["Python", "TensorFlow", "OpenCV"]
  }
]
```

---

### 5️⃣ GET `/trends`

**Purpose:** Fetch trending or popular projects.

**Response Example:**

```json
[
  {
    "id": 7,
    "title": "Deep Learning for Speech Recognition",
    "popularity_score": 98,
    "category": "AI"
  }
]
```

---

### 6️⃣ POST `/personalized_recommendations`

**Purpose:** Get recommendations based on past user interactions.

**Request Body Example:**

```json
{
  "user_id": "123"
}
```

**Response Example:**

```json
[
  {
    "id": 3,
    "title": "Student Grade Predictor",
    "description": "Predict student performance using ML.",
    "difficulty": "Beginner",
    "category": "AI",
    "hardware": "CPU",
    "technologies": ["Python", "Scikit-learn"]
  }
]
```

---

### 7️⃣ POST `/chatbot`

**Purpose:** Interact with the AI chatbot for project suggestions or guidance.

**Request Body Example:**

```json
{
  "message": "Suggest beginner AI projects for Python"
}
```

**Response Example:**

```json
{
  "response": "Here are 3 beginner-friendly AI projects: 1. Simple Chatbot, 2. Home Value Prediction, 3. Student Grade Predictor."
}
```

---

## Authentication

* Optional **HuggingFace token** for embeddings/chatbot models: set as environment variable `HF_TOKEN`.
* API keys for LongCat (if used) should also be in `.env`.

---

## Environment Variables (`.env`)

```
HF_TOKEN=<your_huggingface_token>
LONGCAT_API_KEYS="ak_1,ak_2,ak_3"
```

---

## Installation & Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload
```

**Access docs:** `http://localhost:8000/docs` (Swagger UI)
**OpenAPI JSON:** `http://localhost:8000/openapi.json`

---

## Notes

* Responses are **JSON only**.
* All filtering is **optional**, returning full list if no filters provided.
* Chatbot and embeddings-based endpoints require **HF_TOKEN** for faster model access.
* Designed to be **Docker-friendly** for deployment on Railway, Render, or Fly.io.
