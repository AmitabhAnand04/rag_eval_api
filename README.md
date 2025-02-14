# MagicAudit RAGAS APIs

## Overview
The MagicAudit RAGAS APIs provide an evaluation framework for question-answering models by generating test datasets, collecting responses, and evaluating model performance using various metrics. This API set integrates with Azure Cosmos DB to store and retrieve evaluation data.

## API Endpoints

### 1. Upload File & Generate Testset
**Endpoint:** `POST /upload/`

**Description:**
- Accepts a PDF file and generates a test set from its contents.
- Stores the generated test set in Cosmos DB.
- Returns a unique `fileID` for future reference.

**Request:**
- **File:** PDF file (multipart/form-data)
- **testset_size:** Integer (default: 2)

**Response:**
```json
{
  "fileID": "123456",
  "message": "Item stored with file id 123456",
  "response": [ ... ]
}
```

### 2. Retrieve Testset
**Endpoint:** `GET /get_testset/`

**Description:**
- Fetches the generated test set from Cosmos DB using a given `fileID`.
- Returns the dataset excluding the response field (user needs to manually enter responses in the UI).

**Request Parameters:**
- **fileID:** String (required)

**Response:**
- JSON object containing the test set.

### 3. Submit Responses
**Endpoint:** `POST /submit/`

**Description:**
- Updates the stored test set with user-provided responses.
- Validates the request body and stores responses in Cosmos DB.

**Request Parameters:**
- **fileID:** String (query parameter, required)

**Request Body:**
```json
{
  "responses": {
    "questionID": "Response", 
    "questionID": "Response" 
  }
}
```

**Response:**
- Success/Error message.

### 4. Evaluate Responses
**Endpoint:** `POST /evaluate/`

**Description:**
- Runs evaluation metrics on the responses in the test set.
- Stores computed metrics in Cosmos DB.

**Request Parameters:**
- **fileID:** String (required)

**Response:**
- Computed evaluation metrics stored in Cosmos DB.

### 5. Retrieve Evaluation Scores
**Endpoint:** `GET /get_scores/`

**Description:**
- Fetches stored evaluation scores and results for a given `fileID`.

**Request Parameters:**
- **fileID:** String (required)

**Response:**
- JSON object containing question-answer pairs along with computed evaluation metrics.

## Use Cases
- Generating structured test sets from documents.
- Collecting human responses for benchmarking.
- Evaluating response accuracy using predefined metrics.
- Retrieving stored evaluations for further analysis.

## Dependencies
- FastAPI
- Azure Cosmos DB
- Pandas
- Tempfile

## Future Enhancements
- Support for additional file formats (TXT, DOCX).
- Integration with non-profit and insurance chatbots for broader evaluation use cases.

