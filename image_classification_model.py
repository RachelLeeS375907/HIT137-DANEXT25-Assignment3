"""
image_classification_model.py - Image Classification Model Implementation
Demonstrates: Inheritance, Multiple Inheritance, Polymorphism, Method Overriding
"""
from base_models import AIModel, LoggerMixin, timing_decorator, error_handler
from transformers import pipeline
from PIL import Image


class ImageClassificationModel(AIModel, LoggerMixin):
    """
    Image Classification Model using Hugging Face transformers.
    
    Demonstrates:
    - Multiple Inheritance: Inherits from AIModel and LoggerMixin
    - Polymorphism: Implements abstract methods differently than SentimentAnalysisModel
    - Method Overriding: Overrides parent class methods
    - Encapsulation: Uses private attributes
    """
    
    def __init__(self):
        AIModel.__init__(
            self,
            model_name="google/vit-base-patch16-224",
            description="Vision Transformer model for image classification (1000 ImageNet classes)"
        )
        self.__pipeline = None
        self.log_info("ImageClassificationModel initialized")
    
    @timing_decorator
    @error_handler
    def load_model(self):
        if not self._is_loaded:
            self.log_info(f"Loading model: {self.model_name}")
            self.__pipeline = pipeline("image-classification", model=self.model_name)
            self._is_loaded = True
            self.log_info("Model loaded successfully")
    
    @timing_decorator
    @error_handler
    def process(self, input_data):
        if not self._is_loaded:
            self.load_model()
        
        if isinstance(input_data, str):
            image = Image.open(input_data)
        else:
            image = input_data
        
        self.log_info("Processing image classification...")
        results = self.__pipeline(image)
        top_results = results[:3]
        
        return {
            "predictions": [
                {"label": r["label"], "confidence": f"{r['score']:.4f}"}
                for r in top_results
            ]
        }
    
    def get_model_info(self):
        return {
            "Model Name": self.model_name,
            "Category": "Computer Vision",
            "Task": "Image Classification",
            "Description": self.description,
            "Input": "Image (JPG, PNG, etc.)",
            "Output": "Top-3 class predictions with confidence scores",
            "Use Case": "Identify objects, animals, scenes in images",
            "Model Size": "Medium (~350MB)",
            "Classes": "1000 ImageNet classes",
            "Provider": "Hugging Face / Google"
        }
    
    def get_top_prediction(self, input_data):
        result = self.process(input_data)
        return result["predictions"][0]["label"]
