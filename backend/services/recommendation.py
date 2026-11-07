PRODUCTS = {
    "dictionary": {
        "name": "Mithila Dictionary",
        "description": "Learn and explore the Maithili language.",
        "url": "https://mithilastack.com/maithilidictionary"
    },
    "puja": {
        "name": "DevtaPittar",
        "description": "Explore puja services and connect with Vedic priests.",
        "url": "https://devtapittar.com/"
    },
    "books": {
        "name": "Gyan Changera",
        "description": "Discover Maithili books and literature.",
        "url": None
    }
}


def recommend_product(question: str):
    question = question.lower()

    dictionary_keywords = [
     "mithila ka language",
"mithila ki language",
"mithila ki bhasha",
"mithila ka bhasha"   
    "maithili language",
    "maithili word",
    "maithili",
    "maithli",
    "methli",
    "mithili",
    "mithila language",
    "meaning",
    "translation",
    "dictionary",
    "maithili sikhe",
    "maithili seekhe"
    "maithili language",
    "maithili word",
    "maithili",
    "maithli",
    "methli",
    "mithili",
    "mithila language",
    "meaning",
    "translation",
    "dictionary",
    "मैथिली",
    "मैथिली भाषा",
    "मिथिला भाषा",
    "मिथिला की भाषा",
    "भाषा सिख",
    "भाषा सीख",
    "भाषा सिखाइए",
    "शब्द का अर्थ",
    "शब्द का मतलब",
    "अनुवाद",
    "maithili sikhe",
    "maithili seekhe",
    "maithili sikhao",
    "maithili sikhna",
    "language sikhao",
    "language sikhna",
    "bhasha sikhao",
    "bhasha sikhna",
    "mithila ki language",
    "mithila ki bhasha"

]
    

    puja_keywords = [
        "puja",
        "pooja",
        "pandit",
        "priest",
        "worship",
        "vivah",
        "madhushravani",
        "religious service"
    ]

    book_keywords = [
        "book",
        "books",
        "literature",
        "maithili sahitya",
        "novel",
        "poetry",
        "poem"
    ]

    if any(word in question for word in dictionary_keywords):
        return PRODUCTS["dictionary"]

    elif any(word in question for word in puja_keywords):
        return PRODUCTS["puja"]

    elif any(word in question for word in book_keywords):
        return PRODUCTS["books"]

    return None
if __name__ == "__main__":

    test_questions = [
        "I want to learn Maithili language",
        "I need a pandit for puja",
        "Suggest some Maithili books",
        "Who was Vidyapati?"
    ]

    for question in test_questions:

        result = recommend_product(question)

        print("\nUser:", question)

        if result:
            print("Recommended:", result["name"])
            print("Description:", result["description"])
            print("Website:", result["url"])
        else:
            print("No product recommendation")