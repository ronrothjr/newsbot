from newsbot import Newsbot
from email import send_email

if __name__ == '__main__':
    search_results = Newsbot.article_search([
        (['Artificial Intelligence', '_AI_', '"Brian Green"'], 3),
        (['Artificial Intelligence', '_AI_', '"Mark Graves"'], 3),
        (['Artificial Intelligence', '_AI_', '"Jason Thacker"'], 3),
        (['Artificial Intelligence', '_AI_', '"Michael Sacasas"'], 3),
        (['Artificial Intelligence', '_AI_', '"Nicoleta Acatrinei"'], 3),
        (['Artificial Intelligence', '_AI_', '"Gretchen Huizinga"'], 3),
        (['Artificial Intelligence', '_AI_', '"Mois Navon"'], 3),
        (['Artificial Intelligence', '_AI_', '"Michael Paulus"'], 3),
        (['Artificial Intelligence', '_AI_', '"Cory Labrecque"'], 3),
        (['Artificial Intelligence', '_AI_', '"Elias Kruger"'], 3),
        (['Artificial Intelligence', '_AI_', '"Trish Shaw"'], 3),
        (['Artificial Intelligence', '_AI_', '"Joanna Ng"'], 3),
        (['moral or religious impact of', '_AI_', '"generative AI"'], None)
    ])
    send_email(search_results.replace('\n', '<br>'))
