# 🏢 Company Brochure Generator

Company Brochure Generator is a Python-based application that scrapes relevant company website information and generates a short brochure in Markdown format for potential customers, investors, and recruits. The application supports **OpenAI GPT-4o** and **Ollama Llama3.2** for text generation.

## 📑 Table of Contents
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Required Libraries](#required-libraries)
- [Files](#files)
- [Contributing](#contributing)
- [License](#license)

## 📂 Project Structure

company-brochure-generator/ 
│── data/ # Folder for storing extracted website data (if applicable) 
│── create_brochure.py # Main script to generate the company brochure 
│── requirements.txt # List of required Python libraries 
│── README.md # Project documentation 
│── LICENSE # License information

## ⚙️ Installation

1. **Clone this repository:**

   ```bash
   git clone https://github.com/your-username/company-brochure-generator.git
   cd company-brochure-generator
   ```
2. **(Optional) Create a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the application:**

    ```bash
    python create_brochure.py
    ```

## 🚀 Usage

1. Enter the company name in the input field.

2. Provide the landing page URL of the company.

3. Select the AI model for brochure generation (GPT or Ollama).

4. The script will fetch relevant webpage information, extract key content, and generate a Markdown brochure.

## 📦 Required Libraries

Ensure you have the following Python libraries installed:

- requests
- beautifulsoup4
- openai
- gradio
- python-decouple
- IPython

Alternatively, install them using:

```bash
pip install -r requirements.txt
```

## 📄 Files
- create_brochure.py: Main script that:
    - Scrapes relevant company website content
    - Extracts useful information (company overview, careers, etc.)
    - Generates a Markdown brochure using GPT-4o or Llama3.2
- requirements.txt: List of required Python libraries.
- README.md: Project documentation.

## 🤝 Contributing
Contributions are welcome! Feel free to submit a pull request or open an issue if you find any bugs or have suggestions for improvements.


