import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle
import os

def load_data(filepath):
    print(f"[INFO] Loading dataset from: {filepath}")
    df = pd.read_csv(filepath)
    print(f"[INFO] Dataset loaded successfully. Shape: {df.shape}")
    print(f"[INFO] Target distribution:\n{df['target'].value_counts()}")
    return df

def preprocess_data(df):
    X = df.drop(columns=['target'])
    y = df['target']
    
    print(f"[INFO] Features shape: {X.shape}")
    print(f"[INFO] Target shape: {y.shape}")
    print(f"[INFO] Feature columns: {list(X.columns)}")
    
    return X, y

def train_model(X_train, y_train):
    print("\n[INFO] Training Random Forest Classifier...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=2,
        min_samples_leaf=1,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    print("[INFO] Model training complete!")
    
    return model

def evaluate_model(model, X_test, y_test):
    """Evaluate the model and print metrics."""
    print("\n[INFO] Evaluating model on test data...")
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\n[RESULT] Test Accuracy: {accuracy * 100:.2f}%")
    print("\n[RESULT] Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['No Disease', 'Heart Disease']))
    print("\n[RESULT] Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    
    return accuracy

def save_model(model, output_path):
    """Save the trained model to a .pkl file."""
    print(f"\n[INFO] Saving model to: {output_path}")
    with open(output_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"[INFO] Model saved successfully! File size: {os.path.getsize(output_path)} bytes")

def get_feature_importance(model, feature_names):
    """Display feature importance scores."""
    print("\n[INFO] Feature Importance Scores:")
    importances = model.feature_importances_
    feature_importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importances
    }).sort_values('Importance', ascending=False)
    
    print(feature_importance_df.to_string(index=False))
    return feature_importance_df

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(base_dir, 'dataset.csv')
    model_output_path = os.path.join(base_dir, 'model.pkl')
    
    print("=" * 60)
    print("  AI Healthcare - Heart Disease Model Training")
    print("=" * 60)
    df = load_data(dataset_path)
    X, y = preprocess_data(df)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"\n[INFO] Train size: {X_train.shape[0]} samples")
    print(f"[INFO] Test size:  {X_test.shape[0]} samples")
    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)
    get_feature_importance(model, X.columns.tolist())
    save_model(model, model_output_path)
    
    print("\n" + "=" * 60)
    print("  Training pipeline completed successfully!")
    print(f"  Model saved to: {model_output_path}")
    print("=" * 60)

if __name__ == "__main__":
    main()
