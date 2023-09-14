# Paper Renamer GPT

Paper Renamer is a script that automatically renames PDF files based on their content. Using OpenAI's GPT-4, the script extracts the first author's surname, the year of publication, and relevant key phrases to generate a meaningful filename. The advantage of this approach is that it can handle arbitrarily formatted pdfs. 

### Examples
[Ramkumar_2023_Mascara1b_CRIRES.pdf](https://arxiv.org/pdf/2308.07157.pdf)

[Leigh_2021_uniForest_MicrobiomeStudies.pdf](https://www.biorxiv.org/content/10.1101/2021.05.17.444491v1.full.pdf)

[Melo-Vega-Angeles_2023_COVID-19_CopperFuturesVolatility.pdf](https://www.mdpi.com/2227-7099/11/7/200)
## Installation
Download repo:
```
git clone https://github.com/ksmith9/paper_renamer_gpt/
```
Install relevant python modules:
```
pip install openai PyPDF2
```
## Usage
Create a file: apikey.txt with your openai api key.

Navigate to the directory containing the script and run:

```
python pdf_renamer.py
```

The script will process PDFs in the current directory and rename them. It will also create and update a json file with papers already processed to ensure the same info isn't sent multiple times. 

## Note
I've tested this on a few papers from fields that aren't my own, but I lack the relevant domain knowledge to tell you whether they're any good. Hopefully it's enough to know what paper you're looking at, assuming you've read them already. If not, I'd reccomend tweaking the prompt in the function get_filename_from_openai.

### License

[MIT License](https://choosealicense.com/licenses/mit/)
