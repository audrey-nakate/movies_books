import pandas as pd
import numpy as np
import ast
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from keras.regularizers import l2
import tensorflow as tf
from keras.layers import Input, Embedding, Dense, Flatten, Concatenate, Dot, Dropout, BatchNormalization
from keras.models import Model
from keras.callbacks import EarlyStopping, ReduceLROnPlateau

# loading datasets
user_item_interactions = pd.read_csv("D:\\Year 3 Semester 2\\computerScienceProject\\movie_ratings.csv")  # Columns: user_id, item_id, rating
book_metadata = pd.read_csv("D:\\Year 3 Semester 2\\computerScienceProject\\BX-Books.csv", sep=";", on_bad_lines='skip', encoding="latin-1")  # Columns: item_id, genre, author, year
book_metadata.columns = ["ISBN","title","Author","Year_Of_Publication","Publisher","Image-URL-S","Image-URL-M","Image-URL-L"]
movie_metadata = pd.read_csv("D:\\Year 3 Semester 2\\computerScienceProject\\tmdb_5000_movies.csv")  # Columns: item_id, genre, director, year
credits_df = pd.read_csv("D:\\Year 3 Semester 2\\computerScienceProject\\tmdb_5000_credits.csv")

book_metadata = book_metadata.head(5000)
book_metadata['id'] = np.random.randint(0, 5050, size=len(book_metadata))

# Custom function to clean the lines
def clean_line(line):
    # Remove extra quotation marks and whitespace
    return line.replace('"', '').strip()

# Read the file and apply the custom cleaner
with open("D:\\Year 3 Semester 2\\computerScienceProject\\book_ratings.csv", 'r', encoding='latin-1') as file:
    lines = file.readlines()

# Clean each line
cleaned_lines = [clean_line(line) for line in lines]

# Write cleaned lines to a new file for easier reading
cleaned_file_path = "D:\\Year 3 Semester 2\\computerScienceProject\\cleaned_book_ratings.csv"
with open(cleaned_file_path, 'w', encoding='latin-1') as file:
    file.writelines('\n'.join(cleaned_lines))

# Load the cleaned CSV file
ratings_df = pd.read_csv(cleaned_file_path, sep=";", encoding="latin-1")

# Display the first few rows and column names to verify
ratings_df.head(), ratings_df.columns


# Load the cleaned CSV file
ratings_df = pd.read_csv(cleaned_file_path, sep=";", encoding="latin-1")

# Remove trailing commas from column names and data
ratings_df.columns = [col.split(',')[0] for col in ratings_df.columns]
ratings_df = ratings_df.applymap(lambda x: str(x).split(',')[0])

# Display the first few rows and column names to verify
ratings_df.head(), ratings_df.columns


ratings_df = ratings_df.head(5000)
extracted_col = book_metadata['id']
ratings_df.insert(1, 'id', extracted_col)
ratings_df['Item_ID'] = book_metadata['ISBN']
ratings_df = ratings_df.drop('Item_ID', axis=1)

#merge the two datasets
movie_metadata = movie_metadata.merge(credits_df, on='title')

#selecting relevant columns
movies_final = movie_metadata[[ 'id', 'title', 'genres', 'runtime', 'overview', 'keywords', 'cast', 'crew']]

#check for null values
print(movies_final.isna().sum())

#drop null values
movies_final.dropna(inplace=True)

#function to extract genre name
def convert(obj):
    l = []

    for i in ast.literal_eval(obj):
        l.append(i['name'])
    return l

movies_final['genres'] = movies_final['genres'].apply(convert)

movies_final['keywords'] = movies_final['keywords'].apply(convert)

#function to extract first three cast names
def convert3(obj):
    l = []
    counter = 0

    for i in ast.literal_eval(obj):
        if counter != 3:
            l.append(i['name'])
            counter += 1
        else:
            break
    return l

movies_final['cast'] = movies_final['cast'].apply(convert3)

# to extract director's name
def extract_director(obj):
    l = []

    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            l.append(i['name'])
            break
    return l

movies_final['crew'] = movies_final['crew'].apply(extract_director)

movies_final['overview'] = movies_final['overview'].apply(lambda x: x.split()) 

# removing spaces between words
movies_final['genres'] = movies_final['genres'].apply(lambda x : [i.replace(" ", "") for i in x])
movies_final['keywords'] = movies_final['keywords'].apply(lambda x : [i.replace(" ", "") for i in x])
movies_final['cast'] = movies_final['cast'].apply(lambda x : [i.replace(" ", "") for i in x])
movies_final['crew'] = movies_final['crew'].apply(lambda x : [i.replace(" ", "") for i in x])

movies_final['tags'] = movies_final['genres'] + movies_final['keywords'] + movies_final['cast'] + movies_final['crew'] + movies_final['overview']

movies = movies_final[['id', 'title', 'tags']]

movies_final['tags'] = movies_final['tags'].apply(lambda x: " ".join([i.replace(" ", "") for i in x]).lower())

ratings_df.columns = ['User-ID', 'id', 'RATINGS']

user_item_interactions = pd.concat([user_item_interactions, ratings_df], ignore_index=True)

user_item_interactions

book_metadata['Publisher'] = book_metadata['Publisher'].astype(str)
book_metadata['Author'] = book_metadata['Author'].astype(str)

book_metadata['tags'] = book_metadata['Author'] + " " + book_metadata['Publisher']

books_final = book_metadata[['id', 'title', 'tags']]

book_metadata['tags'] = book_metadata['tags'].apply(lambda x: " ".join([i.replace(" ", "") for i in x.split()]).lower())

# Combine book and movie metadata
books_final = book_metadata[['id', 'title', 'tags']]
books_final['item_type'] = 'book'
movies = movies_final[['id', 'title', 'tags']]
movies['item_type'] = 'movie'
item_metadata = pd.concat([books_final, movies])
item_metadata.reset_index(drop=True, inplace=True)
item_metadata = pd.get_dummies(item_metadata, columns=['item_type'])

from sklearn.decomposition import TruncatedSVD

item_metadata['tags'] = item_metadata['tags'].apply(lambda x: ' '.join(x) if isinstance(x, list) else x)

# One-hot encode tags
encoder = OneHotEncoder(sparse=True)
item_metadata_tags_encoded = encoder.fit_transform(item_metadata[['tags']])

svd = TruncatedSVD(n_components=100)
item_metadata_tags_encoded = svd.fit_transform(item_metadata_tags_encoded)


# Numerical features (id, item type)
numerical_features = item_metadata[['id', 'item_type_book', 'item_type_movie']].values

# Concatenate encoded categorical features with numerical features
item_metadata_processed = np.hstack((numerical_features, item_metadata_tags_encoded))

train_data, test_data = train_test_split(user_item_interactions, test_size=0.2, random_state=42)

# Print initial data sizes
print(f"Initial number of user-item interactions: {len(user_item_interactions)}")
print(f"Initial number of unique users: {user_item_interactions['User-ID'].nunique()}")
print(f"Initial number of unique items: {user_item_interactions['id'].nunique()}")

# Count interactions
item_interaction_count = user_item_interactions['id'].value_counts()
user_interaction_count = user_item_interactions['User-ID'].value_counts()

# Print interaction counts
print(f"Item interaction counts: {item_interaction_count.describe()}")
print(f"User interaction counts: {user_interaction_count.describe()}")

# Define thresholds
min_item_interactions = 2
min_user_interactions = 2

# Filter items and users
filtered_items = item_interaction_count[item_interaction_count >= min_item_interactions].index
filtered_users = user_interaction_count[user_interaction_count >= min_user_interactions].index

print(f"Number of items after filtering: {len(filtered_items)}")
print(f"Number of users after filtering: {len(filtered_users)}")

filtered_data = user_item_interactions[user_item_interactions['id'].isin(filtered_items) & user_item_interactions['User-ID'].isin(filtered_users)]

# Print data size after filtering
print(f"Number of user-item interactions after filtering: {len(filtered_data)}")

# Aggregate duplicate entries by taking the mean rating
user_item_interactions = filtered_data.groupby(['User-ID', 'id']).agg({'RATINGS': 'mean'}).reset_index()
user_item_interactions = user_item_interactions.drop_duplicates(subset=['User-ID', 'id'])

# Verify the number of unique users and items
num_users = user_item_interactions['User-ID'].nunique()
num_items = user_item_interactions['id'].nunique()
print(f"Number of unique users after processing: {num_users}")
print(f"Number of unique items after processing: {num_items}")

# Create interaction matrix
try:
    interaction_matrix = user_item_interactions.pivot(index='User-ID', columns='id', values='RATINGS').fillna(0).values
    print("Interaction matrix successfully created.")
except Exception as e:
    print(f"Error creating interaction matrix: {e}")

# Prepare inputs for training and testing
train_user_ids = np.array(train_data['User-ID'], dtype=np.int32)
train_item_ids = np.array(train_data['id'], dtype=np.int64)
train_ratings = np.array(train_data['RATINGS'], dtype=np.float32)
test_user_ids = np.array(test_data['User-ID'], dtype=np.int32)
test_item_ids = np.array(test_data['id'], dtype=np.int64)
test_ratings = np.array(test_data['RATINGS'], dtype=np.float32)
max_rating = max(np.max(test_ratings), np.max(train_ratings))
train_ratings /= max_rating
test_ratings /= max_rating

# Map item IDs to indices
item_id_to_index = {item_id: idx for idx, item_id in enumerate(item_metadata['id'])}
train_item_indices = np.array([item_id_to_index.get(item_id, -1) for item_id in train_item_ids])
test_item_indices = np.array([item_id_to_index.get(item_id, -1) for item_id in test_item_ids])

# Filter valid indices
train_valid_indices = train_item_indices != -1
train_user_ids = train_user_ids[train_valid_indices]
train_item_indices = train_item_indices[train_valid_indices]
train_ratings = train_ratings[train_valid_indices]
test_valid_indices = test_item_indices != -1
test_user_ids = test_user_ids[test_valid_indices]
test_item_indices = test_item_indices[test_valid_indices]
test_ratings = test_ratings[test_valid_indices]

# Prepare item features
train_item_features = item_metadata_processed[train_item_indices]
test_item_features = item_metadata_processed[test_item_indices]

max_user_id = max(train_user_ids.max(), test_user_ids.max())
max_item_index = item_metadata_processed.shape[0]
embedding_dim = 50

# Inputs
user_input = Input(shape=(1,), name='user_input')
item_input = Input(shape=(1,), name='item_input')
item_metadata_input = Input(shape=(item_metadata_processed.shape[1],), name='item_metadata_input')  # +1 for item type

# Collaborative Filtering Embeddings
user_embedding_cf = Embedding(max_user_id + 1, embedding_dim, embeddings_regularizer=l2(1e-6))(user_input)
item_embedding_cf = Embedding(max_item_index + 1, embedding_dim, embeddings_regularizer=l2(1e-6))(item_input)

# Content-Based Filtering Embeddings
item_embedding_cb = Dense(embedding_dim, activation='relu')(item_metadata_input)

# Flatten embeddings
user_flat_cf = Flatten()(user_embedding_cf)
item_flat_cf = Flatten()(item_embedding_cf)
item_flat_cb = Flatten()(item_embedding_cb)


# Reshape user_flat_cf to match the second axis of item_embedding
user_flat_cf_reshaped = Dense(100)(Flatten()(user_flat_cf))


# Combine collaborative and content-based embeddings
item_embedding = Concatenate()([item_flat_cf, item_flat_cb])
item_embedding = Dropout(0.5)(item_embedding)

# Dot product of user and item embeddings for collaborative filtering
user_item_dot = Dot(axes=1)([user_flat_cf_reshaped, item_embedding])

# Shared hidden layers for hybrid model
shared_hidden = Dense(128, activation='relu', kernel_regularizer=l2(1e-5))(user_item_dot)
# shared_hidden = BatchNormalization()(shared_hidden)
shared_hidden = Dropout(0.5)(shared_hidden)

# Output layer
output = Dense(1, activation='sigmoid', name='output')(shared_hidden)

# Model
model = Model(inputs=[user_input, item_input, item_metadata_input], outputs=[output])

# Compile model
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss='mse', metrics=['accuracy'])

# Summary
model.summary()

#function for  visualisation
def plot_loss(history):
  plt.plot(history.history['loss'], label='Loss')
  plt.plot(history.history['val_loss'], label="val_loss")
  plt.ylabel('loss')
  plt.xlabel('bc')
  plt.legend()
  plt.show()

def plot_acc(history):
  plt.plot(history.history['accuracy'], label='Accuracy')
  plt.plot(history.history['val_accuracy'], label="Val_accuracy")
  plt.ylabel('accuracy')
  plt.xlabel('mse')
  plt.legend()
  plt.show()

# Callbacks
early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=2, min_lr=0.00001)


# Train the model
history = model.fit(
    [train_user_ids, train_item_indices, train_item_features],
    train_ratings,
    epochs=20,
    batch_size=64,
    validation_split=0.1,
    callbacks=[early_stopping, reduce_lr]
)

plot_loss(history)

plot_acc(history)

#Evaluate the model
test_loss, test_accuracy = model.evaluate(
    [test_user_ids, test_item_indices, test_item_features],
    test_ratings
)
print(f'Test Loss: {test_loss:.4f}, Test Accuracy: {test_accuracy:.4f}')


model.save('recommender_model.h5')

