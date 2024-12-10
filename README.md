# Text Analysis and Quiz Generator

A Streamlit application that analyzes text and generates quizzes using OpenAI's GPT-3.5.

## Demo

[![Watch the video](https://res.cloudinary.com/rh-demo/video/upload/q_auto,f_auto/Text_fary4w.jpg)](https://res.cloudinary.com/rh-demo/video/upload/q_auto,f_auto/Text_fary4w.mp4)


## Features

- Text classification (educational, operational, or procedural)
- Automatic quiz generation
- Multiple choice questions with instant feedback
- File upload support

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/text-analyzer-quiz
cd text-analyzer-quiz
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.streamlit/secrets.toml` file with your OpenAI API key:
```toml
OPENAI_API_KEY = "your-api-key-here"
```

## Usage

Run the Streamlit app:
```bash
streamlit run text_analyzer_app.py
```

## License

MIT License
