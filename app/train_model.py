import pandas as pd
import joblib
import json
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Custom label function to compute if goal can be achieved
def label_can_achieve_goal(row):
    try:
        surplus = row['income'] - row['expenses']
        if surplus > 0 and row['emergency_savings'] > 0 and row['assets'] > row['total_liability']:
            return 1
        else:
            return 0
    except:
        return 0

def train_model():
    BASE_DIR = Path(__file__).resolve().parent.parent
    csv_path = BASE_DIR / "dataset.csv"
    
    df = pd.read_csv(csv_path).dropna()

    # Encode categorical
    if 'investment_risk' in df.columns:
        df['investment_risk'] = LabelEncoder().fit_transform(df['investment_risk'])

    # One-hot encode goal_type
    if 'goal_type' in df.columns:
        df = pd.get_dummies(df, columns=['goal_type'])

    # Handle dynamic goal columns: ensure consistent columns for future predictions
    ALL_GOAL_TYPES = ['Retirement', 'House', 'Education', 'Emergency Fund', 'Vacation', 'Investment']  # Extend this if needed
    for goal in ALL_GOAL_TYPES:
        col = f'goal_type_{goal}'
        if col not in df.columns:
            df[col] = 0

    # Compute custom labels
    df['can_achieve_goal'] = df.apply(label_can_achieve_goal, axis=1)

    # Features
    feature_columns = [
        'income', 'expenses', 'assets', 'investment_risk',
        'emergency_savings', 'total_liability'
    ] + [col for col in df.columns if col.startswith('goal_type_')]

    X = df[feature_columns]
    y1 = df['is_saving_enough']
    y2 = df['can_achieve_goal']

    # Train/Test split
    X_train1, _, y_train1, _ = train_test_split(X, y1, test_size=0.2, random_state=42)
    X_train2, _, y_train2, _ = train_test_split(X, y2, test_size=0.2, random_state=42)

    # Train models
    model1 = RandomForestClassifier(n_estimators=100, random_state=42)
    model1.fit(X_train1, y_train1)

    model2 = RandomForestClassifier(n_estimators=100, random_state=42)
    model2.fit(X_train2, y_train2)

    # Save models and features
    MODEL_DIR = BASE_DIR / "app" / "model"
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    joblib.dump(model1, MODEL_DIR / 'saving_model.pkl')
    joblib.dump(model2, MODEL_DIR / 'goal_model.pkl')

    #  Save feature names
    feature_names = X.columns.tolist()
    with open(MODEL_DIR / 'features.json', 'w') as f:
        json.dump(feature_names, f)

    print(" Models and features saved successfully.")

if __name__ == '__main__':
    train_model()
