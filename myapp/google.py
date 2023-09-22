from googlesearch import search

def search_on_google(query):
    results = list(search(query, num=5, stop=5))
    return results
