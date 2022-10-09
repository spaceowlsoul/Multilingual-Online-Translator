import requests
from bs4 import BeautifulSoup

url = 'https://context.reverso.net/translation/'
user_agent = 'Mozilla/5.0'
headers = {'User-Agent': user_agent}

lang_dict = {'1': 'arabic', '2': 'german', '3': 'english', '4': 'spanish', '5': 'french',
             '6': 'hebrew', '7': 'japanese', '8': 'dutch', '9': 'polish', '10': 'portuguese',
             '11': 'romanian', '12': 'russian', '13': 'turkish'}


def output(language_2, translations, examples, output_num):
    print(f'{language_2.title()} Translations:')
    print(*translations[:output_num], sep='\n')

    print(f'\n{language_2.title()} Examples:')
    print(*examples[:output_num * 3], sep='\n')


def export_to_file(word, language_2, translations, examples, output_num):
    file_name = f'{word}.txt'
    with open(file_name, 'a', encoding='utf-8') as file:
        print(f'{language_2.title()} Translations:', file=file)
        print(*translations[:output_num], file=file, sep='\n')

        print(f'\n{language_2.title()} Examples:', file=file)
        print(*examples[:output_num * 3], file=file, sep='\n')


def parsing(trans_page):
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
    return translations, examples


def translation(from_, to_, word):
    language_1 = lang_dict[from_]
    languages_2 = []
    if to_ != '0':
        languages_2.append(lang_dict[to_])
    else:
        for num in lang_dict.keys():
            if num != from_:
                languages_2.append(lang_dict[num])
    for language_2 in languages_2:
        trans_page = f'{url}{language_1}-{language_2}/{word}'
        translations, examples = parsing(trans_page)

        output_num = 1

        output(language_2, translations, examples, output_num)
        export_to_file(word, language_2, translations, examples, output_num)


def main():
    print('Hello, welcome to the translator. Translator supports:')
    for num, lang in lang_dict.items():
        print('{}. {}'.format(num, lang.title()))

    from_ = input('Type the number of your language:\n')
    to_ = input('''Type the number of a language you want to translate to
or '0' to translate to all languages:\n''')
    word = input('Type the word you want to translate:\n')

    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        print(r.status_code, 'OK\n')
        translation(from_, to_, word)


if __name__ == "__main__":
    main()
