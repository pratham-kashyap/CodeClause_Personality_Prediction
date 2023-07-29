# Personality Prediction System

The Personality Prediction System is a Python-based application that predicts personality traits based on user-provided information and an attached CV (PDF/DOCX) file. It employs a Logistic Regression model trained on a dataset to predict the Big Five Personality traits, namely Openness to Experience, Conscientiousness, Extraversion, Agreeableness, and Neuroticism.

## Requirements

Before running the Personality Prediction System, ensure that you have the following dependencies installed:

- Python 3.x
- pandas
- tkinter
- scikit-learn
- textract
- poppler

You can install the required Python libraries using pip:

`pip install pandas tkinter scikit-learn textract`

For text extraction from PDF files, you need to install Poppler, which is an essential dependency for the `textract` library. Here's how to install it on different operating systems:

### macOS

You can use Homebrew to install Poppler on macOS:

`brew install poppler`

### Ubuntu

Poppler can be installed on Ubuntu using the package manager:

`sudo apt-get install poppler-utils`

### Windows

For Windows, you can download the pre-built binaries of Poppler from the official GitHub repository: [Poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases)

After downloading, extract the contents, and add the `bin` directory to your system's PATH environment variable. This allows the `textract` library to work with PDF files.

## How to Use

1. Clone this repository to your local machine or download the files.

2. Install the required Python libraries and Poppler according to the instructions provided above.

3. Open a terminal or command prompt and navigate to the directory containing the project files.

4. Run the `personality_prediction.py` script: `python personality_prediction.py`

5. The GUI window will appear, prompting you to enter your name, age, gender, and attach your CV file (PDF/DOCX). Provide the necessary information and select your CV file.

6. Click on the "Analyze and Predict" button to start the analysis and prediction process.

7. The system will display the predicted personality traits based on the provided information and CV analysis.

## Note

- The dataset used to train the Logistic Regression model is stored in `training_dataset.csv`.

- The provided sample resumes (PDF/DOCX) in the repository are for testing purposes. You can replace them with actual CV files for personalized predictions.

- The CV analysis is based on specific keywords related to each personality trait to determine the trait scores.

- The system displays the predicted personality traits along with brief descriptions for each trait.

Feel free to experiment with the Personality Prediction System, modify the CV analysis logic, or integrate it into your own projects for personality trait predictions based on input data and CV files.
