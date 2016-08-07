import csv
import time
from bs4 import BeautifulSoup
import requests


def get_task_links():
    url = 'http://rosettacode.org/wiki/Category:Programming_Tasks'
    r = requests.get(url)
    content = r.content
    soup = BeautifulSoup(content, 'html.parser')
    category_div = soup.find("div", class_="mw-category")
    task_links = []

    for link in category_div.find_all('a'):
        task_links.append(link['href'])

    return task_links


def get_task_data(url_extension, languages):
    """Returns the a list of the Task, Language, and Code
    Limitations:
    1. Will only get the code from the first highlighted source.
    So if a language has multiple version, e.g. optimized and unoptimized, it
    will only grab the first version.
    2. RCRPG data is ommitted, as it was contained on seperate pages.
    """
    task_data = []
    url = 'http://rosettacode.org' + url_extension
    r = requests.get(url)
    content = r.content
    soup = BeautifulSoup(content, "html.parser", from_encoding="UTF-8")
    headers = soup.find_all("h2")

    for row in headers:
        headlines = row.find_all(class_="mw-headline")

        for headline in headlines:
            try:
                language = headline.find('a').contents[0]
            except AttributeError:
                continue
            else:
                if language in languages:
                    code = headline.find_next("pre")
                    task_formatted = url_extension[6:]
                    language_formatted = headline.find('a').contents[0]
                    try:
                        code_formatted = code.get_text()
                    except AttributeError:
                        code_formatted = '`PARSER ERROR'
                    task_data.append([language_formatted,
                                      task_formatted, code_formatted])
                    # print("Task: {}".format(url_extension[6:]))
                    # print("Language: {}".format(language_formatted))
                    # print("Code: {}".format(code_formatted))
                    # print("")
    return task_data


def get_all_task_data(languages, task_links):
    with open('coding_data.csv', 'a') as f:
        code_writer = csv.writer(f, delimiter=',')
        all_task_data = []
        for task_link in task_links:
            task_data = get_task_data(task_link, languages)
            for lang in task_data:
                code_writer.writerow(lang)
            all_task_data += task_data
        return all_task_data


def main():
    t0 = time.time()

    languages = ['C', 'C#', 'Common Lisp', 'Clojure',
                 'Haskell', 'Java', 'JavaScript', 'OCaml',
                 'Perl', 'PHP', 'Python', 'Ruby', 'Scala', 'Scheme', 'Tcl']

    all_task_data = get_all_task_data(languages, get_task_links())
    print(len(all_task_data))

    t1 = time.time()
    total = t1-t0
    print(total)


if __name__ in "__main__":
    main()
