# Text-Analysis
Extract textual data articles from the given URL and perform text analysis to compute variables.

Approach to the Solution:
Textual Analysis: I began by understanding the requirements outlined in the problem statement. Then, I identified the key tasks involved in performing textual analysis, such as cleaning the text, computing sentiment scores, analyzing readability, and calculating various derived variables.

Implementation: I implemented the solution in Python using the pandas library for data manipulation, nltk for natural language processing tasks such as tokenization and stopwords removal, and regular expressions for pattern matching. I also used file I/O operations to read the input text files and write the output to an Excel file.

How to Run the .py File to Generate Output:
Save the provided Python script in a file with a .py extension, for example, text_analysis.py.
Make sure you have all the dependencies installed. See the next point for details.
Place your input text files in a directory named extracted_articles in the same directory where your Python script is located.
Open a terminal or command prompt and navigate to the directory where your Python script is located.
Run the script by executing the command python text_analysis.py. This will execute the script and generate the output Excel file named Output.xlsx.

Dependencies:
The script requires the following dependencies:
Python (version 3.x recommended)
pandas: pip install pandas
nltk (Natural Language Toolkit): pip install nltk
Additionally, you need to download the NLTK resources. After installing NLTK, run Python and execute the following commands:

import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('cmudict')

Regular expressions module is included in the Python standard library, so no additional installation is required.
By following these steps, you should be able to run the Python script and generate the desired output. Make sure to provide the input files in the specified format and ensure that the dependencies are installed correctly.
