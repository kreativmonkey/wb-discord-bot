import re


class Extensions:
    """
    There is no reason to create an instance of this class, 
    all methods are static and can be called with "Extensions.[methodname]"
    """
    @staticmethod
    def EscapeUrlsInText(text):
        return re.sub(r"((?:http|https)://[\w+?\.\w+]+(?:[a-zA-Z0-9\~\!\@\#\$\%\^\&\*\(\)_\-\=\+\\\/\?\.\:\;\'\,]*)?)", r'<\1>', text)
