import re
import locale
locale.setlocale(locale.LC_ALL)

text = "SSAš, valgiau ir dabar 'nebevalgauųųų \n fdsfdsa'"

text = text.lower()
text = re.sub(r'[^a-ž\n ]', '', text)
print(text)