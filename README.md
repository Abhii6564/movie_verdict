# Movie Success Predictor

A machine learning project to predict the financial success of movies based on features like budget, genre, and social media presence.

## 🚀 Features
- **Predictive Model**: A Random Forest classifier trained on the IMDB 5000 dataset.
- **Interactive Dashboard**: A Streamlit-based web application for real-time predictions.
- **Data Insights**: Automated chart generation for budget trends, ROI distribution, and genre analysis.

## 🛠️ Tech Stack
- **Python**: Core logic and data processing.
- **Scikit-Learn**: Machine learning model training.
- **Pandas/Numpy**: Data manipulation.
- **Streamlit**: Web interface for the dashboard.
- **Matplotlib/Seaborn**: Data visualization.

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd movie_success_prediction
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the dashboard:
   ```bash
   streamlit run app.py
   ```

## 📊 Project Structure
- `app.py`: Streamlit application.
- `train_model.py`: Script to train the Random Forest model.
- `model.pkl`: Serialized trained model.
- `movie_metadata.csv`: Dataset used for training.
- `project_report.md`: Detailed project analysis.
