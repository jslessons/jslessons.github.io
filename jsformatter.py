import re
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
methods = ['left', 'forward', 'right', 'penup', 'setpos', 'pendown', 'color','let', 'str','capitalize', 'casefold', 'center', 'count', 'encode', 'endswith', 'expandtabs', 'find', 'format', 'format_map', 'index', 'isalnum', 'isalpha', 'isascii', 'isdecimal', 
'isdigit', 'isidentifier', 'islower', 'isnumeric', 'isprintable', 'isspace',
 'istitle', 'isupper', 'join', 'ljust', 'lower', 'lstrip', 'maketrans', 'partition', 'replace', 'rfind', 'rindex', 'rjust', 'rpartition', 'rsplit', 
'rstrip', 'split', 'splitlines', 'startswith', 'strip', 'swapcase', 'title', 'translate', 'upper', 'zfill', 'append', 'clear', 'copy', 'count', 'extend', 'index', 'insert', 'pop', 
'remove', 'reverse', 'sort', 'clear', 'copy', 'fromkeys', 'items', 'keys', 'pop',
 'popitem', 'setdefault', 'update', 'values', 'dict', 'print', 
'len', 'float','bool', 'list', 'tupple', 'range', 'close', 'write', 'input', 'acos', 'acosh', 'asin', 'asinh', 'atan', 'atan2', 'atanh', 'ceil', 
'copysign', 'cos', 'cosh', 'degrees', 'erf', 'erfc', 'exp', 'expm1', 'fabs', 'factorial', 'floor', 'fmod', 'frexp', 
'fsum', 'gamma', 'gcd', 'hypot', 'inf', 'isclose', 'isfinite', 'isinf', 'isnan', 'ldexp', 'lgamma', 'log', 'log10', 'log1p', 'log2', 'modf', 'nan', 
'pow', 'random', 'const', 'alert', 'prompt', 'parseInt', 'radians', 'typeof', 'remainder', 'sin', 'sinh', 'sqrt', 'tan', 'tanh', 'tau', 'trunc', 'randint', 'pprint', 'open', 'log', 'console']
operations = ['>=', '<=', '+=','-', '**','+', '*', '//',   '!=', 'and', 'for', 'or']
orange_words = [r'stream<', r'end<', r'sep<', r'text<']
system_words = ['%', '==','assert ',' as ','with ','from ','elif ', 'if ','while ', 'for ', 'return ', 'else',  'break'	,'continue']
def repl(m): 
	
	return '<span class="purple">' + m[0] + '</span>'
def purple(m):
	t = m[0]
	t = re.sub(r'[-+]?\d+\.?\d*', repl, t)
	return t
def yellow(m):
	t = m[0]
	t = t.replace('<span class="purple">', '')
	t = t.replace('<span class="red">', '')
	t = t.replace('</span>', '')
	return '<span class="yellow">' + t + '</span>'
def red(m):
	return '<span class="red">' + m[0] + '</span>'
def f_name(m):
	d, n = m[0].split(' ')
	return f'<span class="blue">{d}</span> <span class="green">{n}</span>'
def reddy(m):
	s = m[0].split('=')
	return f'{s[0]}<span class="red">=</span>{s[1]}'
def orange(m):
	s = m[0][:-1]
	return f'<span class="orange">{s}</span><'


class Formatter:
	def __init__(self, input_file, output_file):
		with open(input_file, 'r', encoding='utf-8') as file:
			content = file.read()
		self.content = content
		self.output = output_file
		self.data = ''


	def create_html(self):
		begin = """<!DOCTYPE html>
<html lang="ru">
<head>
	<meta charset="UTF-8">
	<meta content="width=device-width" name='viewport'>
	<title>Условный оператор</title>
	<link rel="stylesheet" href="style.css">
	<link href="https://fonts.googleapis.com/css2?family=Source+Code+Pro&display=swap" rel="stylesheet">
	<link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;700&display=swap" rel="stylesheet">
</head>
<body>
	<div class="container">
	<a href="index.html" class="link special" ><span>Назад в начало</span></a>"""
		end = f"""\n{self.data}\n\t\t</div>\n\t</body>
</html>"""
		with open(self.output, 'w', encoding='utf-8') as f:
			f.write(begin + end)

	def make_title(self, code):
		t = '\t\t\t'
		# start = self.content.find('№ ')
		# end = self.content[start+2:].find('\n')
		title = '<h2 class="title">' + code[2:-1] + '</h2>'
		self.content = self.content.replace(code, '')
		self.data += t + title + '\n'

	def make_code_p(self, code):
		lines = [el.rstrip()  for el in code[2:-2].split('\n') if el]
		# make colors	
		for ind, text in enumerate(lines):
			if text.find('//') != -1:
				comment = '<span class="grey">' + text[text.find('//'):]+'</span>'
				text = text[:text.find('// ')]
			else:
				comment = ''
			text = re.sub(r'\w{1}=\S', reddy, text)
			# text = re.sub(r'\S{1}<\', reddy, text)



			
			for o in operations:
				text = text.replace(f'{o} ', f'<span class="red">{o} </span>')
			for o in system_words:
				text = text.replace(f'{o}', f'<span class="red">{o}</span>')
			for m in methods:
				text = text.replace(f'{m}(', f'<span class="blue">{m}</span>(')
			# text = re.sub(r'[-+]?\d+\.?\d*', repl, text)
			text = re.sub(r'\W{1}[-+]?\d+\.?\d*\W?', purple, text)
			text = text.replace('int(', f'<span class="blue">int</span>(')
			text = text.replace('str(', f'<span class="blue">int</span>(')
			text = text.replace(' <<', f'<span class="red"> <</span><')
			text = text.replace('let ', f'<span class="blue">let </span>')

			text = re.sub(r'\s{1}=\s{1}', red, text)
			text = re.sub(r'\s{1}>\s{1}', red, text)
			text = re.sub(r'\s{1}<\s{1}', red, text)
			text = re.sub(r'(\x20\x20\x20\x20)', r'&nbsp;&nbsp;&nbsp;&nbsp;', text)
			
			text = re.sub(r'(def \w+)', f_name, text)
			text = re.sub(r'true|false', repl, text)
			text = re.sub(r' / ', red, text)
			text = re.sub(r'from ', red, text)
			text = re.sub(r' in ', red, text)
			text = re.sub(r'import ', red, text)
			text = re.sub(r'(\'.*?\')', yellow, text)
			text = re.sub(r'(`.*?`)', yellow, text)

			text = text.replace('var', '<span class="blue">var</span>')
			text = text.replace('console', '<span class="blue">console</span>')
			for o in orange_words:
				text = re.sub(o, orange, text)
			text = text + comment
			lines[ind] = text


		text = '<p class="code">\n\t\t\t\t' + '\n\t\t\t\t<br>\n\t\t\t\t'.join(lines) + '\n\t\t\t</p>'
		self.content = self.content.replace(code, '')
		self.data += f'\t\t\t{text}\n'

	def make_text(self, code):
		t = '\t\t\t'
		# start = self.content.find('№ ')
		# end = self.content[start+2:].find('\n')
		title = '<p class="text">' + code[2:-1] + '</p>'
		self.content = self.content.replace(code, '')
		self.data += t + title + '\n'

	def make_subtitle(self, code):
		t = '\t\t\t'
		# start = self.content.find('№ ')
		# end = self.content[start+2:].find('\n')
		title = '<h2 class="title">' + code[2:-1] + '</h2>'
		self.content = self.content.replace(code, '')
		self.data += t + title + '\n'

	def format(self):
		while self.content:
			symbol = self.content[0]
			if symbol == '№':
				end = self.content.find('\n')
				self.make_title(self.content[0:end+1])
			elif symbol == '\\':
				end = self.content.find('\n')
				self.make_subtitle(self.content[0:end+1])
			elif symbol == '@':
				end = self.content[1:].find('@\n') 
				self.make_code_p(self.content[0:end+3])
				# print(self.content)
			elif symbol == '!':
				end = self.content.find('\n')
				self.make_text(self.content[0:end+1])
			else:
				break

		self.create_html()
# formatter = Formatter('test.txt', 'test.html')
formatter = Formatter('while.txt', 'while.html')
formatter.format()
