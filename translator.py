import sys
import requests
from bs4 import BeautifulSoup

url = 'https://context.reverso.net/translation/'
user_agent = 'Mozilla/5.0'
headers = {'User-Agent': user_agent}

lang_list = ['arabic', 'german', 'english', 'spanish', 'french', 'hebrew', 'japanese',
             'dutch', 'polish', 'portuguese', 'romanian', 'russian', 'turkish']


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

    if trans_tags and examples_tags:
        translations = [t.text for t in trans_tags]
        examples = [e.text.strip() for e in examples_tags]
        i = 2
        while i < len(examples):
            examples.insert(i, ' ')
            i += 3
        return translations, examples


def translation(from_, to_, word):
    language_1 = from_
    languages_2 = []
    if to_ != 'all':
        languages_2.append(to_)
    else:
        for lang in lang_list:
            if lang != from_:
                languages_2.append(lang)
    for language_2 in languages_2:
        trans_page = f'{url}{language_1}-{language_2}/{word}'
        if parsing(trans_page):
            translations, examples = parsing(trans_page)

            output_num = 1

            output(language_2, translations, examples, output_num)
            export_to_file(word, language_2, translations, examples, output_num)
        else:
            print(f'Sorry, unable to find {word}')
            break


def check_input(from_, to_):
    if from_ not in lang_list:
        print(f"Sorry, the program doesn't support {from_}")
        return False
    elif to_ not in lang_list and to_ != 'all':
        print(f"Sorry, the program doesn't support {to_}.")
        return False
    return True


def main():
    from_, to_ = sys.argv[1].lower(), sys.argv[2].lower()
    word = sys.argv[3]

    if check_input(from_, to_):
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            translation(from_, to_, word)
        else:
            print('Something wrong with your internet connection')


if __name__ == "__main__":
    main()
