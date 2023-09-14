import PyPDF2
import openai
import os
import json

paper_directory = './'

# Set up OpenAI API key
def get_api_key_from_file(filename='apikey.txt'):
    with open(filename, 'r') as file:
        return file.readline().strip()

openai.api_key = get_api_key_from_file()

# File to keep track of perviously renamed pdfs
RENAMED_PDFS_FILE = "renamed_pdfs.json"

# function to extract pdf contents until desired number of pages or character count is reached. 
def extract_text_from_pdf(pdf_path, pages_to_extract=3, min_chars=1000):
    """Extract text from the first few pages of a PDF or until min_chars is reached."""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        extracted_text = ""
        for page_num in range(min(pages_to_extract, len(reader.pages))):
            page_text = reader.pages[page_num].extract_text()
            extracted_text += page_text
            # Check if the cumulative extracted text has reached min_chars
            if len(extracted_text) >= min_chars:
                break
        return extracted_text[:min_chars]  # Return only up to min_chars characters

# function to send prompt to gpt-4
def get_filename_from_openai(text):
    messages = [
        {
            "role": "system",
            "content": "You are an assistant that suggests PDF filenames based on content. Suggest a filename in the format where you identify the first author's surname, the year of publication, and one or two relevant key phrases. The format should be: \n surname_year_keyphrase1_keyphrase2.pdf \n Include no extraneous text. 'pdf' shouldn't be used anywhere except in the file extension. Responses should only be in the forms like: \n Ramkumar_2023_Mascara1b_CRIRES.pdf \n Troutman_2011_βPICTORIS_rovibrational.pdf \n If there is an issue finding any of the info mentioned, with no additional text simply return: \nERROR\n"
        },
        {
            "role": "user",
            "content": f"Content:\n{text}"
        }
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4", 
        messages=messages
    )

    new_filename_raw = response['choices'][0]['message']['content'].strip()
    return new_filename_raw

# Creates file tracking json if one doesn't exist, otherwise loads it
def load_renamed_pdfs():
    if os.path.exists(RENAMED_PDFS_FILE):
        with open(RENAMED_PDFS_FILE, 'r') as f:
            return json.load(f)
    else:
        with open(RENAMED_PDFS_FILE, 'w') as f:
            json.dump([], f)  # Creating an empty JSON array
        return []

def save_renamed_pdfs(renamed_list):
    with open(RENAMED_PDFS_FILE, 'w') as f:
        json.dump(renamed_list, f)

def main():
    directory = paper_directory
    
    renamed_pdfs = load_renamed_pdfs()

    for filename in os.listdir(directory):
        if filename.endswith('.pdf') and filename not in renamed_pdfs:
            text = extract_text_from_pdf(os.path.join(directory, filename))
            new_filename_raw = get_filename_from_openai(text)

            # Add condition for same name scenario (prevent duplicate rename and save)
            if filename == new_filename_raw:
                print(f"Filename: {filename} already in desired format.")
                renamed_pdfs.append(new_filename_raw)
                save_renamed_pdfs(renamed_pdfs)
                continue

            if new_filename_raw == "ERROR":
                print("Error processing file: " + filename)
                save_renamed_pdfs(renamed_pdfs)
            else:
                os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename_raw))
                print("Old Filename: " + filename, "\nNew Filename: " + new_filename_raw)
                renamed_pdfs.append(new_filename_raw)
                save_renamed_pdfs(renamed_pdfs)  # Save the renamed files list after every rename

if __name__ == "__main__":
    main()

