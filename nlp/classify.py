def classify_text(text: str) ->str:

    import pickle

    # # Load Logistic Regression model
    # with open('models/logistic_model.pkl', 'rb') as f:
    #     lr_model = pickle.load(f)

    # Load Random Forest model
    with open('models/random_forest_model.pkl', 'rb') as f:
        rf_model = pickle.load(f)

    with open('models/tfidf_vec.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    vectorized_text = vectorizer.transform([text])  # Convert raw text to feature vector
    y_pred_rf = rf_model.predict(vectorized_text)

    return  y_pred_rf[0]
