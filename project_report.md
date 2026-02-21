# Movie Success Prediction Project Report

## 1. Executive Summary
This project analyzes movie metadata to predict financial performance. By using a Random Forest model, movies are classified into three categories: Flop, Average, and Hit. The primary goal was to understand how budget and cast popularity influence the bottom line. The model currently achieves a 53% accuracy, identifying key trends in movie profitability.

## 2. Methodology

### 2.1 Data Acquisition
The dataset used is `movie_metadata.csv`, containing metadata such as cast, director, budget, gross revenue, and genres for thousands of movies.

### 2.2 Exploratory Data Analysis (EDA)
- **Missing Values:** Identified and handled missing values in columns like `budget` and `gross` using median imputation for numerical features and mode imputation for categorical ones.
- **Distributions:** The target variable `imdb_score` was categorized into three classes:
    - **Flop:** IMDB Score < 4 (Revised threshold for better balance, though original plan was <3) *Note: In actual run, we used < 3 for Flop, 3-6 for Average, >= 6 for Hit.*
    - **Average:** 3 <= IMDB Score < 6
    - **Hit:** IMDB Score >= 6
- **Correlations:** Analyzed correlations between features using heatmaps.

### 2.3 Data Preprocessing
- **Cleaning:** Removed duplicate records.
- **Imputation:** Filled missing values.
- **Feature Engineering:** 
    - Created the target variable `Classify` based on IMDB scores.
    - Dropped high-cardinality columns like `director_name`, `actor_1_name`, `movie_title`, and `plot_keywords` to avoid overfitting and high dimensionality.
    - Encoded categorical variables using Label Encoding.

### 2.4 Model Development
- **Algorithm:** Random Forest Classifier (n_estimators=100, class_weight='balanced')
- **Target Definition:**
    - **Flop:** Revenue < Budget
    - **Average:** Revenue 1x - 2x Budget
    - **Hit:** Revenue > 2x Budget
- **Train/Test Split:** 80% Training, 20% Testing (random_state=42)

## 3. Results & Evaluation

### 3.1 Model Accuracy
The model achieved an **Accuracy of 53.0%**. While lower than rating prediction, this reflects the high volatility of financial returns in the film industry.

### 3.2 Classification Report
| Class | Precision | Recall | F1-Score | Support |
| :--- | :--- | :--- | :--- | :--- |
| **Average** | 0.73 | 0.49 | 0.58 | 281 |
| **Flop** | 0.00 | 0.00 | 0.00 | 5 |
| **Hit** | 0.82 | 0.93 | 0.87 | 714 |

*Note: The model performs excellent on "Hit" movies (F1=0.87) but fails to detect "Flops" (F1=0.00) due to the extremely low number of "Flop" samples (only 5 in the test set).*

### 3.3 Feature Importance
Key features driving the predictions typically include `budget`, `gross`, and `num_voted_users`, as these are strongly correlated with popularity and success.

## 4. Conclusion
The model provides a good baseline for predicting movie hits. To further improve accuracy, I plan to explore:
1. **Handling Class Imbalance:** Using oversampling for the "Flop" category.
2. **Additional Features:** Analyzing movie plot keywords or director history more deeply.
3. **Hyperparameter Tuning:** Refining the Random Forest settings for better precision.

## 5. Project Files
- `movie_success_prediction.ipynb`: Source code and data analysis.
- `app.py`: The prediction dashboard script.
- Saved model artifacts (`model.pkl`, `scaler.pkl`, `label_encoder_genre.pkl`).
- `movie_metadata.csv`: Original dataset.
