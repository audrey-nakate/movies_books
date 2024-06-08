from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import tensorflow as tf

# Load the trained model
model = tf.keras.models.load_model('recommender_model.h5')

# Initialize FastAPI app
# app = FastAPI()

# Data class for input
class RecommendationRequest(BaseModel):
    user_id: int
    item_metadata: list

# Endpoint to get recommendations
# @app.post("/recommend")
def recommend(request: RecommendationRequest):
    user_id = np.array([request.user_id])
    item_metadata = np.array([request.item_metadata])

    # Assuming item IDs range from 0 to max_item_index
    item_indices = np.arange(len(item_metadata))

    # Prepare inputs for the model
    predictions = model.predict([user_id, item_indices, item_metadata])

    # Get top N recommendations
    top_n = 10
    recommended_indices = np.argsort(predictions.flatten())[-top_n:][::-1]
    
    return {"recommendations": recommended_indices.tolist()}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
