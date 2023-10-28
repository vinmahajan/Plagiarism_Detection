# Plagiarism Detection

This is a Plagiarism Detection System, which allows you to detect and analyze plagiarism in text documents. Designed to identify similarities between a given text and existing online content. It consists of a backend implemented in Python with Flask, a frontend using HTML and CSS. 


## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Plagiarism Detection is a web application that allows users to check a piece of text for potential plagiarism by comparing it with various online sources. This repository provides the source code for the application, which can be easily customized and extended to suit your specific needs.

## Features

- Text input for plagiarism checking.
- Comparison of input text against multiple online sources.
- Display of plagiarism scores and source URLs for each sentence.
- Clean and user-friendly web interface.

## Installation

To get started with this project, follow these steps:

1. **Clone the repository to your local machine:**

   ```sh
   git clone https://github.com/vinmahajan/Plagiarism_Detection.git
   cd Plagiarism_Detection
   ```
   
2. **Create a virtual environment (recommended) to isolate project dependencies:**

   ```bash
   python -m venv venv
   venv/scripts/activate
   ```

3. **Install the required Python packages using `pip`:**
   
   Install packages using requirements file

   ```bash
   pip install -r requirements.txt
   ```
    OR

   **You Can Manually Install Minimal Dependencies:**

   Make sure you have Python installed. You can install packages using pip:

   ```sh
   pip install Flask requests beautifulsoup4 trafilatura
   ```

4. **Run the Application:**

   Start the Flask development server:

   ```sh
   python app.py
   ```

   The application should now be running locally at `http://localhost:5000`.

5. **Access the Application:**

   Open a web browser and navigate to `http://localhost:5000` to access the plagiarism detection web application.

## Usage

1. Enter the text you want to check for plagiarism in the provided text area.

2. Click the "Check Plagiarism" button to initiate the plagiarism check.

3. The application will compare your text with various online sources and display the plagiarism scores and source URLs.

4. Review the results to identify potential instances of plagiarism in your text.

## Contributing

Contributions are welcome! If you have ideas for improvements, feature requests, or find any issues, please open an issue or submit a pull request. We encourage a collaborative and open-source development environment.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

