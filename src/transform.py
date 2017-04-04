import fileinput
import re
import itertools

DEBUG = 0

def isplit(iterable):
	return list(filter(lambda x: x, [list(g) for k,g in itertools.groupby(iterable,lambda x:x=="") if not k]))

def out_conds(lines):
	return ["!"+x for x in re.findall(r'\[.+?\|(.+?)\]', ' '.join(lines)) if (x[0] != '<')]

def debang(text):
	return text.replace("!","")

def generate_selector(xid, conds):
	return '~'.join([('#'+x+':checked' if x[0] != "!" else '#'+x[1:]+':not(:checked)') for x in sorted(conds, key=debang)]) + ' ~ #' + xid

def add_labels(text):
	label_template = '<label for="{name}">{text}</label>'
	return re.sub(r'\[(.+?)\|(.+?)\]',	lambda m: label_template.format(name=m.group(2) if m.group(2)[0] != '<' else m.group(2)[1:], text=m.group(1)), text)

clean_input = isplit([x.split('#')[0].strip() for x in fileinput.input()])

oc = out_conds(clean_input[0][1:])

blocks = [(set(conds.split() + out_conds(lines)), lines) for (conds, *lines) in clean_input]

blocks_xid = [(xid, conds, lines) for (xid, (conds, lines)) in zip(['x'+str(i) for i in range(len(blocks))], blocks)]

input_names = sorted(set([debang(cond) for (conds, lines) in blocks for cond in conds]))

input_template = ('{name}' if DEBUG else '') + '<input type="checkbox" name="{name}" id="{name}" {checked}>'
inputs = '\n'.join([input_template.format(name=name,checked=("checked" if name == "init" else "")) for name in sorted(input_names)])

css = """
body
{
	font-family: "Consolas", monospace;
	color: #222;
	background-color: #EEE; 
	max-width: 800px;
	margin: auto;
	padding: 10px;
	font-size: 15px;
}

input
{
	display: none;
}

h1
{
	margin: 10px 0 20px 0;
}

p
{
	margin: 0 0 1em 0;
}

div
{
	height: 0;
	opacity: 0;
	transition: all 0.3s;
	overflow: hidden;
}

label
{
	font-weight: bold;
	text-decoration: underline;
	cursor: pointer;
}


SELECTOR
{
	opacity: 1;
	height: auto;
}

""".replace("SELECTOR", ', '.join([generate_selector(xid, conds) for (xid, conds, lines) in blocks_xid]))



div_template = """
<div id="{xid}">
	{paragraphs}
</div>
"""
p_template = '<p>{line}</p>'

divs = '\r\n'.join([div_template.format(xid=xid, paragraphs='\n\t'.join([p_template.format(line=add_labels(line)) for line in lines])) for (xid, conds, lines) in blocks_xid])

html_template = """
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width,initial-scale=1">
	<title>When the Tiger Came</title>
	<style>
	{css}
	</style>
</head>

<!-- TOGGLES -->
{inputs}

<h1>When the Tiger Came</h1>

<!-- BLOCKS -->
{divs}
"""
print(html_template.format(css=css, inputs=inputs, divs=divs))