# Blood Test Analyzer - Bug Fixes & Improvements

A FastAPI-based blood test report analyzer using CrewAI agents powered by Groq's Llama models.

## Major Bugs Fixed

### 1. **Missing PDF Processing Dependencies**
- **Issue**: `PDFLoader` was undefined, causing import errors
- **Fix**: Added proper imports for `PyPDFLoader` from `langchain_community.document_loaders`
- **Added**: `pypdf==4.2.0` and `langchain-community==0.1.52` to requirements

### 2. **Incompatible Tool Implementation**
- **Issue**: Tools were implemented as regular methods but CrewAI expected `BaseTool` instances
- **Fix**: Converted `BloodTestReportTool` to inherit from `crewai.tools.BaseTool`
- **Added**: Proper Pydantic schemas for tool inputs

### 3. **LLM Configuration Issues**
- **Issue**: Undefined `llm` variable and incorrect OpenAI dependencies
- **Fix**: Configured Groq LLM using CrewAI's `LLM` class with proper API key handling
- **Model**: Using `groq/llama-3.1-8b-instant` for optimal performance

### 4. **Token Limit Exceeded**
- **Issue**: Groq API rate limits (6000 tokens/minute) exceeded by large PDF content
- **Fix**: Implemented content truncation to 6000 characters max
- **Optimization**: Reduced agent verbosity and disabled memory to minimize token usage

### 5. **Incomplete Tool Functionality**
- **Issue**: Nutrition and Exercise tools returned placeholder messages
- **Fix**: Implemented intelligent analysis based on blood markers:
  - **Nutrition Tool**: Detects vitamin deficiencies, cholesterol, glucose levels
  - **Exercise Tool**: Provides recommendations based on cardiovascular and metabolic markers

### 6. **Environment Variable Management**
- **Issue**: Missing `.env` file and improper API key handling
- **Fix**: Created proper environment configuration with Groq API key management

## Setup Instructions

### Prerequisites
- Python 3.8+
- Groq API key (get from [console.groq.com](https://console.groq.com))

### Installation

1. **Clone and navigate to project**
   ```bash
   cd blood-test-analyser-debug
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   - Edit `.env` file and add your Groq API key:
   ```env
   GROQ_API_KEY=gsk_your_actual_groq_api_key_here
   ```

4. **Start the server**
   ```bash
   python main.py
   ```
   Server runs on `http://localhost:8000`

## 📖 API Documentation

### Health Check
```http
GET /
```
**Response:**
```json
{
  "message": "Blood Test Report Analyser API is running"
}
```

### Analyze Blood Report
```http
POST /analyze
Content-Type: multipart/form-data
```

**Parameters:**
- `file` (required): PDF blood test report
- `query` (optional): Analysis question (default: "Summarise my Blood Test Report")

**Example Request:**
```bash
curl -X POST "http://localhost:8000/analyze" \
  -F "file=@data/blood_test_report.pdf" \
  -F "query=What are my vitamin levels?"
```


## AI Agents

### Doctor Agent
- **Role**: Senior Medical Doctor and Blood Test Specialist
- **Function**: Primary analysis of blood test reports
- **Tools**: PDF reader, medical analysis

### Nutritionist Agent
- **Role**: Clinical Nutritionist and Dietitian
- **Function**: Nutrition recommendations based on blood markers
- **Intelligence**: Detects vitamin deficiencies, metabolic issues

### Exercise Specialist Agent
- **Role**: Clinical Exercise Physiologist
- **Function**: Safe exercise recommendations
- **Intelligence**: Considers cardiovascular and metabolic health

### Verifier Agent
- **Role**: Medical Document Validator
- **Function**: Validates document authenticity and format

## 🧪 Testing

### Using Postman
1. Set method to `POST`
2. URL: `http://localhost:8000/analyze`
3. Body → form-data:
   - Key: `file` (Type: File) → Select your PDF
   - Key: `query` (Type: Text) → Enter your question

## 🔧 Technical Architecture

- **Framework**: FastAPI
- **AI Engine**: CrewAI with Groq Llama models
- **PDF Processing**: PyPDFLoader with token optimization
- **Environment**: Python-dotenv for configuration
- **Deployment**: Uvicorn ASGI server

## 📁 Project Structure

```
blood-test-analyser-debug/
├── main.py              # FastAPI application
├── agents.py            # AI agent definitions
├── task.py              # Task configurations
├── tools.py             # Custom tools (PDF, nutrition, exercise)
├── requirements.txt     # Dependencies
├── .env                 # Environment variables
└── data/               # Sample blood test reports
```


## Security Notes

- API keys stored in environment variables
- File cleanup after processing
- Input validation for uploaded files
