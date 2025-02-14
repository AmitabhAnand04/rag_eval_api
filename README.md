# MagicAudit RAGAS APIs

## Overview
The MagicAudit RAGAS APIs provide an evaluation framework for question-answering models by generating test datasets, collecting responses, and evaluating model performance using various metrics. This API set integrates with Azure Cosmos DB to store and retrieve evaluation data.

## API Endpoints

### Base Url: https://app-rageval-api-dev.azurewebsites.net/v1/

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
```json
[
    {
        "questionID":"62d22251-d344-4014-b830-3b1c68d804a7",
        "user_input":"What heart disease mean and what types there is?",
        "reference_contexts":["Context"],
        "reference":"reference",
        "synthesizer_name":"single_hop_specifc_query_synthesizer",
        "response":"Response for cerebrovascular disease"
    },
    {
        "questionID":"62d22251-d344-4014-b830-3b1c68d804a7",
        "user_input":"Question",
        "reference_contexts":["Context"],
        "reference":"reference",
        "synthesizer_name":"single_hop_specifc_query_synthesizer",
        "response":"Response for cerebrovascular disease"
    }
]
```

### 3. Submit Responses
**Endpoint:** `POST /submit/`

**Description:**
- Updates the stored test set with user-provided responses.
- Validates the request body and stores responses in Cosmos DB.
- It supports partial update of testset.
- 
**Request Parameters:**
- **fileID:** String (query parameter, required)

**Request Body:**
```json
{
    "responses": {
        "questionID": {
            "response": "Response",
            "reference": "Reference",
            "reference_contexts": []
        },
        "questionID": {
            "response": "Response"
        }
    }
}
```

**Response:**
- Success/Error message.
- Updated item with ID: 636ba648-f530-4e14-94aa-50a5a8c304e2 for questionIDs: ['d9406015-e165-4804-ad60-ce21a41e8098', '227b7d98-2c79-449d-ace7-bad4df37cd0b']

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
```json
{
    "fileID":"2eed3f93-9822-4715-9b37-ade11e713dc3",
    "scores":[
        {
            "questionID":"21c08461-192a-45d4-b83c-e894bd7b34d9",
            "user_input":"Wht is cerebrovasculr diseas?",
            "response":"Response for cerebrovascular disease",
            "context_precision":0.9999999999,
            "context_recall":1,
            "res_relevency":0,
            "faithfulness":0.25,
            "answer_correctness":0.6479359410978902
        },
        {
            "questionID":"615429a9-3e7f-4f19-92af-2410bd4b784c",
            "user_input":"What is a pulmonary embolism?",
            "response":"Response for pulmonary embolism",
            "context_precision":0.9999999999,
            "context_recall":1,
            "res_relevency":0,
            "faithfulness":0.25,
            "answer_correctness":0.6419360515174874
        }
    ]
}
```

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

