from bs4 import BeautifulSoup
import requests
import argparse
import json

def get_response(url):
    """ Get the response object """
    if url is None:
        print("URL not provided")
    else:
        response = requests.get(url)
        if response.status_code != 200:
            print(f'Error {response.status_code}: Request Failed!')
        return response


def convert_to_json(rsp, flag=True):
    """Convert the data to JSON format"""
    quiz_list = []
    with open("index.html", 'r') as file:
        soup = BeautifulSoup(file.read(), "html.parser")
    for mainDiv in soup.find_all("div", class_="SetPageTerm-content"):
        # Removing <span>
        for matched in mainDiv.findAll('span'):
            matched.unwrap()
        # Replacing <br> with line break
        for breaks in mainDiv.findAll('br'):
            breaks.replace_with('\n')
        json_data = {}
        definition = mainDiv.find(
            'a', attrs={'class': 'SetPageTerm-definitionText'})
        answer = mainDiv.find('a', attrs={'class': 'SetPageTerm-wordText'})
        if flag is True:
            json_data['Question'] = answer.text
            json_data['Answer'] = definition.text
        else:
            json_data['Question'] = definition.text
            json_data['Answer'] = answer.text
        quiz_list.append(json_data)
    # Exporting to a JSON file
    json_data = json.dumps(quiz_list)
    data = json.loads(json_data)
    with open('data.json', 'w') as f:
        json.dump(data, f)


def convert_to_text(flag=True):
    """ Convert the data to Text file format """
    with open("index.html", encoding='utf-8') as file:
        soup = BeautifulSoup(file, "html.parser")
    count = 1
    with open('data1.txt', 'w', encoding='utf-8') as f:
        for mainDiv in soup.find_all("div", class_="SetPageTerm-content"):
            for matched in mainDiv.findAll('span'):
                matched.unwrap()
            for breaks in mainDiv.findAll('br'):
                breaks.replace_with('\n')
            answer = mainDiv.find('a', attrs={'class': 'SetPageTerm-wordText'})
            definition = mainDiv.find(
                'a', attrs={'class': 'SetPageTerm-definitionText'})
            if flag is True:
                f.write(f'Question {count}\n')
                f.write(f'{answer.text}\n')
                f.write(f'\tAnswer: {definition.text}\n\n')
            else:
                f.write(f'Question {count}\n')
                f.write(f'{definition.text}\n')
                f.write(f'\tAnswer: {answer.text}\n\n')
            count = count + 1
// amandyk
convert_to_text()
