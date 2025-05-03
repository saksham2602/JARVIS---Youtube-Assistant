import joblib
import nltk
from nltk.stem import WordNetLemmatizer
import warnings
import os

class IntentPredictor:
    def __init__(self):
        """Load pre-trained model files with comprehensive error handling"""
        try:
            # Suppress scikit-learn version warning
            warnings.filterwarnings("ignore", category=UserWarning, 
                                 message="Trying to unpickle estimator.*")
            
            # Ensure all NLTK resources are available
            self._download_nltk_resources()
            
            # Verify model files exist
            if not all(os.path.exists(f) for f in ["intent_classifier_model.pkl", "vectorizer.pkl"]):
                raise FileNotFoundError("Model files missing")
                
            # Load models with explicit pickle protocol
            self.model = joblib.load("intent_classifier_model.pkl")
            self.vectorizer = joblib.load("vectorizer.pkl")
            self.lemmatizer = WordNetLemmatizer()
            
            print("✅ Intent classifier loaded successfully")
        except Exception as e:
            print(f"❌ Critical initialization error: {str(e)}")
            raise

    def _download_nltk_resources(self):
        """Download all required NLTK resources with fallbacks"""
        resources = {
            'punkt': ['tokenizers/punkt', 'tokenizers/punkt_tab'],
            'wordnet': [],
            'omw-1.4': []
        }
        
        for resource, sub_paths in resources.items():
            try:
                nltk.data.find(f'tokenizers/{resource}')
                for path in sub_paths:
                    try:
                        nltk.data.find(path)
                    except LookupError:
                        print(f"⬇️ Downloading NLTK sub-resource: {path}")
                        nltk.download(resource, quiet=True)
            except LookupError:
                print(f"⬇️ Downloading NLTK resource: {resource}")
                nltk.download(resource, quiet=True)
                nltk.download('omw-1.4', quiet=True)  # Required for WordNet

    def predict(self, text):
        """Robust prediction with full error handling"""
        try:
            # Preprocess text
            words = nltk.word_tokenize(text)
            words = [self.lemmatizer.lemmatize(word.lower()) for word in words]
            processed_text = ' '.join(words)
            
            # Predict intent
            return self.model.predict([processed_text])[0]
        except Exception as e:
            print(f"⚠️ Prediction error: {str(e)}")
            return "error"

# Initialize predictor with verification
try:
    predictor = IntentPredictor()
    # Verify basic functionality
    test_pred = predictor.predict("test prediction")
    if test_pred == "error":
        raise RuntimeError("Predictor failed basic functionality test")
except Exception as e:
    print(f"❌ Failed to initialize predictor: {str(e)}")
    predictor = None

if __name__ == "__main__":
    if predictor:
        test_phrases = [
            "pause the video",
            "increase volume a little",
            "search for machine learning tutorials"
        ]
        for phrase in test_phrases:
            result = predictor.predict(phrase)
            print(f"'{phrase}' → {result}")
    else:
        print("Cannot run tests - predictor not initialized correctly")