import requests

from bs4 import BeautifulSoup

url = 'https://context.reverso.net/translation/'
user_agent = 'Mozilla/5.0'
headers = {'User-Agent': user_agent}

lang_dict = {'en': 'english', 'fr': 'french'}
trans_dict = {'en': 'french', 'fr': 'english'}


def translation(language_choice, word):
    language_1 = lang_dict[language_choice]
    language_2 = trans_dict[language_choice]
    trans_page = f'{url}{language_2}-{language_1}/{word}'

    r = requests.get(trans_page, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')

    trans_tags = soup.find_all('span', {'class': 'display-term'})
    examples_tags = soup.find('section', id="examples-content").find_all('span', class_="text")

    translations = [t.text for t in trans_tags]
    examples = [e.text.strip() for e in examples_tags]

    print("Translations")
    print(translations)
    print(examples)


def main():
    r = requests.get(url, headers=headers)

    language_choice = input('''Type "en" if you want to translate from French into English, 
or "fr" if you want to translate from English into French:\n''')
    word = input('Type the word you want to translate:\n')
    print(f'You chose "{language_choice}" as the language to translate "{word}".')

    if r.status_code == 200:
        print(r.status_code, "OK")
        translation(language_choice, word)


if __name__ == "__main__":
    main()

