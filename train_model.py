import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
import warnings

warnings.filterwarnings('ignore')

print("Loading data...")
try:
    df = pd.read_csv('movie_metadata.csv')
except FileNotFoundError:
    print("Error: movie_metadata.csv not found!")
    exit()

# Preprocessing
print("Preprocessing...")
df.drop_duplicates(inplace=True)

# Imputation
num_cols = df.select_dtypes(include=[np.number]).columns
imputer_num = SimpleImputer(strategy='median')
df[num_cols] = imputer_num.fit_transform(df[num_cols])

cat_cols = df.select_dtypes(include=['object']).columns
imputer_cat = SimpleImputer(strategy='most_frequent')
df[cat_cols] = imputer_cat.fit_transform(df[cat_cols])

# Feature Selection and Encoding
df['main_genre'] = df['genres'].apply(lambda x: x.split('|')[0] if isinstance(x, str) else str(x))

# --- NEW TARGET DEFINITION: FINANCIAL SUCCESS ---
# We use Return on Investment (ROI) or simply Ratio = Gross / Budget
# Flop: Ratio < 1.0 (Lost Money)
# Average: 1.0 <= Ratio < 2.0 (Recovered cost but not huge hit)
# Hit: Ratio >= 2.0 (Doubled the budget or more)

def classify_financial(row):
    budget = row['budget']
    gross = row['gross']
    
    if budget == 0: return 'Average' # Edge case treatment
    
    ratio = gross / budget
    
    if ratio < 1.0:
        return 'Flop'
    elif ratio < 2.0:
        return 'Average'
    else:
        return 'Hit'

df['Classify'] = df.apply(classify_financial, axis=1)

print("Class Distribution (Financial):")
print(df['Classify'].value_counts())

# Features
features = ['main_genre', 'cast_total_facebook_likes', 'budget', 'title_year']
X = df[features]
y = df['Classify']

# Encoding
print("Encoding and Scaling...")
le_genre = LabelEncoder()
X['main_genre'] = le_genre.fit_transform(X['main_genre'])

with open('label_encoder_genre.pkl', 'wb') as f:
    pickle.dump(le_genre, f)

# Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

# Modeling
print("Training Model...")
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Using balanced weights
model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
model.fit(X_train, y_train)

# Evaluation
accuracy = model.score(X_test, y_test)
print(f"Model Training Complete. Accuracy: {accuracy:.4f}")

# Saving Model
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
print("Artifacts saved: model.pkl, scaler.pkl, label_encoder_genre.pkl")
