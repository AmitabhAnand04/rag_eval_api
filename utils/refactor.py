import json
import uuid
import pandas as pd
from services.cosmos_service import insert_items

def transform_data(input_list):
    output = {"id": str(uuid.uuid4()), "testset": []}
    
    for idx, item in enumerate(input_list, start=1):
        transformed_item = {
            "questionID": str(uuid.uuid4()),
            "user_input": item["user_input"],
            "reference_contexts": item["reference_contexts"],
            "reference": item["reference"],
            "synthesizer_name": item["synthesizer_name"]
        }
        output["testset"].append(transformed_item)
    
    # return json.dumps(output)
    return output

def transform_to_df(data):
    return pd.DataFrame(data)

