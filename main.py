import pandas as pd
import requests
from bs4 import BeautifulSoup

input_file = 'input.xlsx'
data = pd.read_excel(input_file)



def extract_content(url):
    try:

        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')


        header = soup.find('header')
        if header:
            header.extract()
        footer = soup.find('footer')
        if footer:
            footer.extract()


        title = soup.title.string if soup.title else "No Title Found"
        content = ' '.join([p.text for p in soup.find_all('p')])

        return title, content
    except Exception as e:
        print(f"Error extracting content from {url}: {str(e)}")
        return None, None


# for multiple urls
for index, row in data.iterrows():
    # Extract URL and URL_ID from the DataFrame
    url = row['URL']
    url_id = row['URL_ID']


    try:

        title, content = extract_content(url)
    except requests.exceptions.HTTPError as e:
        print(f"Error extracting content from {url}: {str(e)}")
        title, content = None, None


    text_filename = f"{url_id}.txt"


    with open(text_filename, 'w', encoding='utf-8') as text_file:
        text_file.write(f"Title: {title}\n\n")
        if content is not None:
            text_file.write(content)

    print(f"Saved {text_filename}")

print("Extraction and saving completed.")
