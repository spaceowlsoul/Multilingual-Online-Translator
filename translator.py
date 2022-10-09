import requests
from bs4 import BeautifulSoup

url = 'https://context.reverso.net/translation/'
user_agent = 'Mozilla/5.0'
headers = {'User-Agent': user_agent}

lang_dict = {'1': 'arabic', '2': 'german', '3': 'english', '4': 'spanish', '5': 'french',
             '6': 'hebrew', '7': 'japanese', '8': 'dutch', '9': 'polish', '10': 'portuguese',
             '11': 'romanian', '12': 'russian', '13': 'turkish'}


def translation(from_, to_, word):
    language_1 = lang_dict[from_]
    language_2 = lang_dict[to_]
    trans_page = f'{url}{language_1}-{language_2}/{word}'

    r = requests.get(trans_page, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')

    trans_tags = soup.find_all('span', {'class': 'display-term'})
    examples_tags = soup.find('section', id="examples-content").find_all('span', class_="text")

    translations = [t.text for t in trans_tags]
    examples = [e.text.strip() for e in examples_tags]
    i = 2
    while i < len(examples):
        examples.insert(i, ' ')
        i += 3

    output_num = 5

    print(f'\n{language_2.title()} Translations:')
    print(*translations[:output_num], sep='\n')

    print(f'\n{language_2.title()} Examples:')
    print(*examples[:10 + output_num], sep='\n')


def main():
    print('Hello, welcome to the translator. Translator supports:')
    for num, lang in lang_dict.items():
        print('{}. {}'.format(num, lang.title()))

    from_ = input('Type the number of your language:\n').lower()
    to_ = input('Type the number of language you want to translate to:\n').lower()
    word = input('Type the word you want to translate:\n').lower()

    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        print(r.status_code, "OK")
        translation(from_, to_, word)


if __name__ == "__main__":
    main()
