import re
import unicodedata
import htmlentitydefs

# Remueve acentos
def strip_accents(s):
   return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

# Normaliza strings:
# - Borra espacios del comienzo y finla
# - Pasa a mayusculas
# - Convierte en representacion ASCII mas cercana
def normalize(text):
    text = text.decode('utf-8').upper()
    text = strip_accents(unicode(text))
    text = re.sub("[^A-Z0-9]+", " ", text)
    text = re.sub("[\s]+", " ", text) 
    text = text.strip()
    return text.encode('utf-8')

##
# Removes HTML or XML character references and entities from a text string.
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.

def unescape_html(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

def clean_url(text, replace = ""):
    return re.sub("http:\/\/[\w.\/]+", replace, text)

def clean_users(text, replace = ""):
    return re.sub("@\w+", replace, text)


if __name__=="__main__":
    from sys import argv
    print normalize(argv[1])
