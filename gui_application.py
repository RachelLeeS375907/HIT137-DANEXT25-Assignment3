import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from PIL import Image, ImageTk
from sentiment_model import SentimentAnalysisModel
from image_classification_model import ImageClassificationModel


class AIModelGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("HIT137 Assignment 3 - Group DAN/EXT25")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f0f0")
        
        # Private attributes (encapsulation)
        self.__models = {
            "Sentiment Analysis": SentimentAnalysisModel(),
            "Image Classification": ImageClassificationModel()
        }
        self.__current_model = None
        self.__selected_image_path = None
        
        # Setup GUI layout
        self.__setup_gui()
    
    def __setup_gui(self):
        # Title
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = tk.Label(
            title_frame,
            text="HIT137 Assignment 3 Group: DAN/EXT25",
            font=("Arial", 24, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=20)
        
        # Main container
        main_container = tk.Frame(self.root, bg="#f0f0f0")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left panel - Model selection and input
        left_panel = tk.Frame(main_container, bg="white", relief=tk.RIDGE, bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.__setup_model_selection(left_panel)
        self.__setup_input_section(left_panel)
        self.__setup_output_section(left_panel)
        
        # Right panel - Information
        right_panel = tk.Frame(main_container, bg="white", relief=tk.RIDGE, bd=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.__setup_info_section(right_panel)
    
    def __setup_model_selection(self, parent):
        #Setup model selection section
        frame = tk.LabelFrame(
            parent,
            text="Select AI Model",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.model_var = tk.StringVar(value="Sentiment Analysis")
        
        for model_name in self.__models.keys():
            rb = tk.Radiobutton(
                frame,
                text=model_name,
                variable=self.model_var,
                value=model_name,
                font=("Arial", 11),
                bg="white",
                command=self.__on_model_change
            )
            rb.pack(anchor=tk.W, padx=20, pady=5)
    
    def __setup_input_section(self, parent):
    #Setup input section
        frame = tk.LabelFrame(
            parent,
            text="Input Data",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Input type selection
        input_frame = tk.Frame(frame, bg="white")
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(
            input_frame,
            text="Input Type:",
            font=("Arial", 10, "bold"),
            bg="white"
        ).pack(side=tk.LEFT, padx=5)
        
        self.input_type_var = tk.StringVar(value="Text")
        self.input_dropdown = ttk.Combobox(
            input_frame,
            textvariable=self.input_type_var,
            values=["Text", "Image"],
            state="readonly",
            width=15
        )
        self.input_dropdown.pack(side=tk.LEFT, padx=5)
        self.input_dropdown.bind("<<ComboboxSelected>>", self.__on_input_type_change)
        
        # Text input
        self.text_input_frame = tk.Frame(frame, bg="white")
        self.text_input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        tk.Label(
            self.text_input_frame,
            text="Enter text:",
            font=("Arial", 10),
            bg="white"
        ).pack(anchor=tk.W, pady=5)
        
        self.text_input = scrolledtext.ScrolledText(
            self.text_input_frame,
            height=6,
            font=("Arial", 10),
            wrap=tk.WORD
        )
        self.text_input.pack(fill=tk.BOTH, expand=True)
        self.text_input.insert(1.0, "This product is amazing! I love it!")
        
        # Image input
        self.image_input_frame = tk.Frame(frame, bg="white")
        
        tk.Label(
            self.image_input_frame,
            text="Select an image:",
            font=("Arial", 10),
            bg="white"
        ).pack(anchor=tk.W, pady=5)
        
        btn_frame = tk.Frame(self.image_input_frame, bg="white")
        btn_frame.pack(fill=tk.X, pady=5)
        
        self.select_image_btn = tk.Button(
            btn_frame,
            text="Browse Image",
            command=self.__select_image,
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2"
        )
        self.select_image_btn.pack(side=tk.LEFT, padx=5)
        
        self.image_label = tk.Label(
            btn_frame,
            text="No image selected",
            font=("Arial", 9),
            bg="white",
            fg="#7f8c8d"
        )
        self.image_label.pack(side=tk.LEFT, padx=10)
        
        # Image preview
        self.image_preview_label = tk.Label(self.image_input_frame, bg="white")
        self.image_preview_label.pack(pady=10)
        
        # Process button
        self.process_btn = tk.Button(
            frame,
            text="Process Input",
            command=self.__process_input,
            bg="#59ff00",
            fg="white",
            font=("Arial", 12, "bold"),
            cursor="hand2",
            height=2
        )
        self.process_btn.pack(fill=tk.X, padx=10, pady=10)
    
    def __setup_output_section(self, parent):
        """Setup output section"""
        frame = tk.LabelFrame(
            parent,
            text="Output Results",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.output_text = scrolledtext.ScrolledText(
            frame,
            height=8,
            font=("Courier", 10),
            wrap=tk.WORD,
            bg="#ecf0f1"
        )
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.output_text.insert(1.0, "Results will appear here...")
    
    def __setup_info_section(self, parent):
        # Create notebook for tabs
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Model Info Tab
        model_info_frame = tk.Frame(notebook, bg="white")
        notebook.add(model_info_frame, text="Model Information")
        
        self.model_info_text = scrolledtext.ScrolledText(
            model_info_frame,
            font=("Arial", 10),
            wrap=tk.WORD,
            bg="#fefefe"
        )
        self.model_info_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # OOP Concepts Tab
        oop_frame = tk.Frame(notebook, bg="white")
        notebook.add(oop_frame, text="OOP Concepts")
        
        oop_text = scrolledtext.ScrolledText(
            oop_frame,
            font=("Arial", 10),
            wrap=tk.WORD,
            bg="#fefefe"
        )
        oop_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        #Text area for OOP Content
        oop_content = """
        OBJECT-ORIENTED PROGRAMMING CONCEPTS USED:
1. MULTIPLE INHERITANCE:
   - SentimentAnalysisModel and ImageClassificationModel both inherit from:
     * AIModel (abstract base class)
     * LoggerMixin (mixin class for logging)
   - Location: sentiment_model.py and image_classification_model.py
   - Why: To combine abstract model behavior with logging functionality

2. ENCAPSULATION:
   - Private attributes: __model_name, __description, __pipeline
   - Protected attributes: _is_loaded
   - Property decorators for controlled access
   - Location: base_models.py (AIModel class)
   - Why: To hide internal implementation and provide controlled access

3. ABSTRACTION:
   - AIModel is an abstract base class (ABC)
   - Abstract methods: load_model(), process(), get_model_info()
   - Location: base_models.py
   - Why: To define a contract that all model classes must follow

4. POLYMORPHISM:
   - Each model implements process() differently:
     * Sentiment model processes text
     * Image model processes images
   - Location: Both model files
   - Why: Same interface, different behavior based on object type

5. METHOD OVERRIDING:
   - Child classes override abstract methods from AIModel
   - load_model(), process(), get_model_info() are overridden
   - Location: sentiment_model.py and image_classification_model.py
   - Why: To provide specific implementation for each model type

6. MULTIPLE DECORATORS:
   - @timing_decorator: Measures execution time
   - @error_handler: Handles exceptions gracefully
   - Applied to load_model() and process() methods
   - Location: base_models.py (defined), applied in model classes
   - Why: To add cross-cutting concerns without modifying core logic

7. COMPOSITION:
   - AIModelGUI contains instances of model classes
   - Models are stored in __models dictionary
   - Location: gui_application.py
   - Why: "Has-a" relationship - GUI has models, doesn't inherit from them
        """
        
        oop_text.insert(1.0, oop_content)
        oop_text.config(state=tk.DISABLED)
        
        # Update model info
        self.__update_model_info()
    
    def __update_model_info(self):
        model_name = self.model_var.get()
        model = self.__models[model_name]
        info = model.get_model_info()
        
        self.model_info_text.delete(1.0, tk.END)
        self.model_info_text.insert(tk.END, f"  {model_name.upper()}\n")

        
        for key, value in info.items():
            self.model_info_text.insert(tk.END, f"▸ {key}:\n  {value}\n\n")
    
    def __on_model_change(self):
        """Handle model selection change"""
        self.__update_model_info()
        model_name = self.model_var.get()
        
        # Update input type based on model
        if model_name == "Sentiment Analysis":
            self.input_type_var.set("Text")
            self.input_dropdown.config(values=["Text"])
        else:
            self.input_type_var.set("Image")
            self.input_dropdown.config(values=["Image"])
        
        self.__on_input_type_change()
    
    def __on_input_type_change(self, event=None):
        """Handle input type change"""
        input_type = self.input_type_var.get()
        
        if input_type == "Text":
            self.image_input_frame.pack_forget()
            self.text_input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        else:
            self.text_input_frame.pack_forget()
            self.image_input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    def __select_image(self):
        filepath = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"),
                ("All files", "*.*")
            ]
        )
        
        if filepath:
            self.__selected_image_path = filepath
            self.image_label.config(text=filepath.split("/")[-1])
            
            # Show preview
            try:
                img = Image.open(filepath)
                img.thumbnail((200, 200))
                photo = ImageTk.PhotoImage(img)
                self.image_preview_label.config(image=photo)
                self.image_preview_label.image = photo
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def __process_input(self):
        model_name = self.model_var.get()
        model = self.__models[model_name]
        
        try:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(1.0, "Processing... Please wait...\n")
            self.root.update()
            
            if model_name == "Sentiment Analysis":
                text = self.text_input.get(1.0, tk.END).strip()
                if not text:
                    messagebox.showwarning("Warning", "Please enter some text!")
                    return

                result = model.process(text)

                output = ""
                output += f"SENTIMENT ANALYSIS RESULTS\n"
                output += f"Input Text:\n{result['input_text']}\n\n"
                output += f"Sentiment: {result['label']}\n"
                output += f"Confidence: {result['confidence']}\n"
                
            else:  # Image Classification
                if not self.__selected_image_path:
                    messagebox.showwarning("Warning", "Please select an image!")
                    return

                result = model.process(self.__selected_image_path)

                output = ""
                output += f"IMAGE CLASSIFICATION RESULTS\n"
                output += f"Top Predictions:\n\n"
                
                for i, pred in enumerate(result['predictions'], 1):
                    output += f"{i}. {pred['label']}\n"
                    output += f"   Confidence: {pred['confidence']}\n\n"
            
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(1.0, output)
            
        except Exception as e:
            messagebox.showerror("Error", f"Processing failed: {str(e)}")
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(1.0, f"Error: {str(e)}")
