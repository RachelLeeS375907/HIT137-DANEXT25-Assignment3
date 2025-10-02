"""
sentiment_model.py - Sentiment Analysis Model Implementation
Demonstrates: Inheritance, Multiple Inheritance, Polymorphism, Method Overriding
"""
from base_models import AIModel, LoggerMixin, timing_decorator, error_handler
from transformers import pipeline


class SentimentAnalysisModel(AIModel, LoggerMixin):
    def __init__(self):
        # Call parent constructors
        AIModel.__init__(
            self,
            model_name="distilbert-base-uncased-finetuned-sst-2-english",
            description="Sentiment Analysis model that classifies text as positive or negative"
        )
        self.__pipeline = None  # Private attribute for model pipeline
        self.log_info("SentimentAnalysisModel initialized")
    
    @timing_decorator  # Apply timing decorator
    @error_handler  # Apply error handling decorator
    def load_model(self) -> None:
        """
        Load the sentiment analysis model.
        Method overriding: Implements abstract method from AIModel
        """
        if not self._is_loaded:
            self.log_info(f"Loading model: {self.model_name}")
            self.__pipeline = pipeline(
                "sentiment-analysis",
                model=self.model_name
            )
            self._is_loaded = True
            self.log_info("Model loaded successfully")
    
    @timing_decorator
    @error_handler
    def process(self, input_data: str) -> dict:
        """
        Process text input for sentiment analysis.
        Method overriding: Implements abstract method from AIModel
        Polymorphism: Different behavior than other model implementations
        """
        if not self._is_loaded:
            self.load_model()
        
        self.log_info(f"Processing sentiment analysis for: {input_data[:50]}...")
        result = self.__pipeline(input_data)[0]
        
        return {
            "label": result["label"],
            "confidence": f"{result['score']:.4f}",
            "input_text": input_data
        }
    
    def get_model_info(self) -> dict:
        """
        Return model information.
        Method overriding: Implements abstract method from AIModel
        """
        #Enter in details for model information here
        return {
            "Model Name": self.model_name,
            "Category": "Text Classification",
            "Task": "Sentiment Analysis",
            "Description": self.description,
            "Input": "Text (string)",
            "Output": "Sentiment label (POSITIVE/NEGATIVE) with confidence score",
            "Use Case": "Analyze customer reviews, social media posts, feedback",
            "Model Size": "Small (~250MB)",
            "Provider": "Hugging Face"
        }
    
    # Additional method demonstrating polymorphism
    def analyze_batch(self, texts: list) -> list:
        """
        Analyze multiple texts at once.
        Demonstrates: Polymorphism - specific behavior for this model type
        """
        if not self._is_loaded:
            self.load_model()
        
        return [self.process(text) for text in texts]