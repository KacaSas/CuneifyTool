import csv
import pandas as pd
import re
import streamlit as st
import base64

st.set_page_config(page_title='CuneifyTool', page_icon='resources/icon/icon.png', layout='wide')  # change favicon and page title

# load cuneiform fonts
def load_font_css(font_name, font_path):
	with open(font_path, "rb") as f:
		font_data = f.read()
		b64_font = base64.b64encode(font_data).decode()
		return f"""
		@font-face {{
			font-family: '{font_name}';
			src: url(data:font/ttf;base64,{b64_font}) format('truetype');
		}}
		"""
fonts_css = ""
fonts_css += load_font_css("Sinacherib", "resources/fonts/Sinacherib.ttf")
fonts_css += load_font_css("Santakku", "resources/fonts/Santakku.ttf")
fonts_css += load_font_css("SantakkuM", "resources/fonts/SantakkuM.ttf")
fonts_css += load_font_css("Assurbanipal", "resources/fonts/Assurbanipal.ttf")
fonts_css += load_font_css("OB Freie", "resources/fonts/OBFreie-Regular.ttf")
fonts_css += load_font_css("CuneiformComposite", "resources/fonts/CuneiformComposite.ttf")
fonts_css += load_font_css("Esagil", "resources/fonts/Esagil.ttf")
fonts_css += load_font_css("Nabu-ninua-ihsus", "resources/fonts/Nabuninuaihsus.ttf")
fonts_css += load_font_css("Gudea", "resources/fonts/Oracc-gudea.ttf")
fonts_css += load_font_css("Oracc LAK", "resources/fonts/Oracc-LAK.ttf")
fonts_css += load_font_css("Oracc RSP", "resources/fonts/Oracc-RSP.ttf")

st.markdown(f"<style>{fonts_css}</style>", unsafe_allow_html=True)  # insert fonts into the app page

def clearTextArea():
	st.session_state['translitInput'] = ''

st.header('CuneifyTool')
st.write('<br><br><font style="font-size: 19px">This app is inspired by <i>Cuneify</i> by S. Tinney, <i>Cuneify REPL</i> by J. Knowles, and other similar tools for converting transliterations into cuneiform script. The cuneiform fonts used in this app are available thanks to the efforts of S. Vanséveren, S. Tinney, and others. Individual cuneiform signs are mapped according to my <i>Cuneiform Sign List</i> (http://home.zcu.cz/~ksaskova/Sign_List.html). For details on the fonts used, related tools, and cuneiform sign lists, see <i>Sources and references</i> below.<br></font>', unsafe_allow_html=True)

signList = pd.read_csv('resources/signList/SignList.csv', keep_default_na=False, na_values=[])

st.sidebar.write('<p style="margin-top: 17em;"><b><font style="font-size: 19px">Options</b></font></p>', unsafe_allow_html=True)
selectedCuneiFont = st.sidebar.selectbox('Cuneiform font', ('Assurbanipal', 'Nabu-ninua-ihsus', 'Sinacherib', 'Esagil', 'Santakku', 'SantakkuM', 'OB Freie', 'CuneiformComposite', 'Gudea', 'Oracc RSP', 'Oracc LAK'), index=0, key='selectedCuneiFont', label_visibility='visible')
selectedCuneiFontSize = st.sidebar.selectbox('Font size', ('10', '15', '17', '19', '20', '21', '22', '23', '24', '25', '27', '30', '32', '35', '37', '40', '42', '45', '47'), index=5, key='selectedCuneiFontSize', label_visibility='visible')

columna1, columna2 = st.columns([1, 1], gap='small')
with columna1:
	st.markdown(f"""
	<style>
	div[data-testid="stTextArea"] textarea {{
		font-size: {selectedCuneiFontSize}px !important; background-color: #0e1117 !important;}}
	</style>""", unsafe_allow_html=True)

	translitInput = st.text_area('Write/paste transliteration', height=500, key='translitInput', placeholder='Write or paste transliteration...', label_visibility='collapsed')
	applyCuneify = st.button('Apply', use_container_width=True, key='applyCuneify')
with columna2:
	st.write('')
	with st.container(border=True, height=501):
		if translitInput != '' or applyCuneify:
			replacementsInput = {'1': '₁', '2': '₂', '3': '₃', '4': '₄', '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉', '0': '₀', 'Sh': 'Š', 'sh': 'š', 'kh': 'ḫ', 'H': 'Ḫ', 'h': 'ḫ', 'ŋ': 'g', 'Ŋ': 'G', r',s': r'ṣ', r',S': r'Ṣ', r',t': r'ṭ', r',T': r'Ṭ', r's,': r'ṣ', r'S,': r'Ṣ', r't,': r'ṭ', r'T,': r'Ṭ', r'.': r'-', r'<br>': r'\n', ' ': '-###-', '\n': '-\n&&&\n-', r'\b(\w∗)(á)(\w∗)\b': r'$1a$3₂'}
			for x,y in replacementsInput.items():
				translitInput = translitInput.replace(x, y)

			replacementsInputRegExp = {r'\b(\w*)(á)(\w*)\b': r'\1a\3₂', r'\b(\w*)(é)(\w*)\b': r'\1e\3₂', r'\b(\w*)(í)(\w*)\b': r'\1i\3₂', r'\b(\w*)(ú)(\w*)\b': r'\1u\3₂', r'\b(\w*)(à)(\w*)\b': r'\1a\3₃', r'\b(\w*)(è)(\w*)\b': r'\1e\3₃', r'\b(\w*)(ì)(\w*)\b': r'\1i\3₃', r'\b(\w*)(ù)(\w*)\b': r'\1u\3₃'}
			for pattern, replacement in replacementsInputRegExp.items():
				translitInput = re.sub(pattern, replacement, translitInput)

			translitInput = translitInput.split('-')

			cuneiformText = []
			for entry in translitInput:
				if entry != '':
					searchEntry = r'\b' + entry + r'\b'
				else:
					searchEntry = r'\b' + '' + r'\b'

				foundSignRow1 = signList.loc[signList['NamesForCuenify'].str.contains(searchEntry, case=False, regex=True)]
				if len(foundSignRow1) == 0:
					foundSignRow2 = signList.loc[signList['ValuesForCuenify'].str.contains(searchEntry, case=False, regex=True)]
					foundSignRow = pd.concat([foundSignRow1, foundSignRow2], axis=0, join='outer', ignore_index=False, keys=None)
				else:
					foundSignRow = foundSignRow1
				foundSignRow = foundSignRow.drop_duplicates(inplace=False)

				if len(foundSignRow.columns) != 0 and len(foundSignRow) == 1:
					foundSign = entry.replace(entry, str(foundSignRow['Sign'].values[0]))
				else:
					foundSign = entry
				cuneiformText.append(foundSign)

				finalCuneiformText = ''
				for signs in cuneiformText:
					finalCuneiformText = finalCuneiformText + signs

			finalCuneiformText = '<font style="font-family: ' + str(selectedCuneiFont) + '; font-size:' + str(selectedCuneiFontSize) + 'pt; color: #ffffab;">' + finalCuneiformText + '</font>'
			finalCuneiformText = finalCuneiformText.replace('&&&', '<br>')
			finalCuneiformText = finalCuneiformText.replace('###', ' ')
			st.write(finalCuneiformText, unsafe_allow_html=True)


	clearTextArea = st.button('Clear the text area contents', key='clearTextArea', on_click=clearTextArea, use_container_width=True)

st.write('<p style="margin-top: 3em;"><b><font style="font-size: 19px">Sources and references</font></b></p>', unsafe_allow_html=True)

with st.expander('Sources and references', expanded=False):
	st.markdown('**Fonts**', unsafe_allow_html=True)
	st.markdown(
		'– *Oracc-LAK.ttf* (by S. Tinney and V. Kethana). https://oracc.museum.upenn.edu/osl/OraccCuneiformFonts/index.html and https://github.com/oracc/oracc2/tree/main/msc/fonts.<br>'
		'– *Oracc-RSP.ttf* (by S. Tinney). https://oracc.museum.upenn.edu/osl/OraccCuneiformFonts/index.html and https://github.com/oracc/oracc2/tree/main/msc/fonts.<br>'
		'– *Oracc-gudea.ttf* (by S. Tinney). https://oracc.museum.upenn.edu/osl/OraccCuneiformFonts/index.html and https://github.com/oracc/oracc2/tree/main/msc/fonts.<br>'
		'– *CuneiformComposite.ttf* (by S. Tinney). http://oracc.museum.upenn.edu/doc/help/visitingoracc/fonts/.<br>'
		'– *SantakkuM.ttf* (by S. Vanséveren). https://www.hethport.uni-wuerzburg.de/cuneifont/.<br>'
		'– *Old Babylonian Freie* (by C. R. Ziegeler). https://refubium.fu-berlin.de/handle/fub188/45271 and https://github.com/crzfub/OB-Freie.<br>'
		'– *Santakku.ttf* (by S. Vanséveren). https://www.hethport.uni-wuerzburg.de/cuneifont/.<br>'
		'– *Assurbanipal.ttf* (by S. Vanséveren). https://www.hethport.uni-wuerzburg.de/cuneifont/.<br>'
		'– *Nabuninuaihsus.ttf* (by R. Leroy). https://github.com/eggrobin/Nabu-ninua-ihsus, https://oracc.museum.upenn.edu/osl/OraccCuneiformFonts/index.html and https://github.com/oracc/oracc2/tree/main/msc/fonts.<br>'
		'– *Sinacherib.ttf* (by K. Šašková). http://home.zcu.cz/~ksaskova/.<br>'
		'– *Esagil.ttf* (by S. Vanséveren). https://www.hethport.uni-wuerzburg.de/cuneifont/.', unsafe_allow_html=True)
	st.markdown('**Tools**', unsafe_allow_html=True)
	st.markdown('– Cuneify REPL (by Jon Knowles). https://amazing-chandrasekhar-e6c92b.netlify.app/index.html.<br>'
		'– CuneifyPlus (by Tom Gillam). https://cuneify.herokuapp.com/.<br>'
		'– Cuneify (by Andrew Senior). https://andrewsenior.com/cuneify/index.html and https://github.com/asenior/cuneify.<br>'
		'– Cuneify (by Steve Tinney). http://oracc.museum.upenn.edu/saao/knpp/cuneiformrevealed/cuneify/.<br>'
		'– eBL: Cuneiform converter. electronic Babylonian Library (eBL). München: Ludwig-Maximilians-Universität München – Bayerische Akademie der Wissenschaften. https://www.ebl.uni-muenchen.de/tools/cuneiform-converter.<br>'
		'– KUR.NU.GI4.A – Cuneiform Script Analyzer (by uyum). https://kurnugia.web.app/.<br>'
		'– GI-DUB – Sumerian Cuneiform Input Aid (by uyum). https://qantuppi.web.app/.', unsafe_allow_html=True)
	st.markdown('**Sign lists**', unsafe_allow_html=True)
	st.markdown(
		'– Borger, R. (2004): *Mesopotamisches Zeichenlexikon* (AOAT 305). Münster: Ugarit-Verlag.<br>'
		'– Borger, R. (1981): *Assyrisch-babylonische Zeichenliste* (AOAT 1981). Neukirchen-Vluyn.<br>'
		'– *Catalogue of Old Babylonian Signs*. Old Babylonian Text Corpus (OBTC). Pilsen: University of West Bohemia. https://klinopis.zcu.cz/utf/signs.html.<br>'
		'– *eBL: Signs*. electronic Babylonian Library (eBL). München: Ludwig-Maximilians-Universität München – Bayerische Akademie der Wissenschaften. https://www.ebl.uni-muenchen.de/signs.<br>'
		'– Labat, R. (1994): *Manuel d’épigraphie akkadienne*. Paris.<br>'
		'– *PCSL: Proto-Cuneiform Sign List*. Philadelphia: The Open Richly Annotated Cuneiform Corpus. https://oracc.museum.upenn.edu/pcsl/.<br>'
		'– Šašková, K. (2021): *Cuneiform Sign List*. http://home.zcu.cz/~ksaskova/Sign_List.html.<br>'
		'– Tinney, S. et al. (2017–): *ePSD2 Sign List*. The Pennsylvania Sumerian Dictionary Project 2 (ePSD2). Philadelphia: University of Pennsylvania Museum of Anthropology and Archaeology. https://oracc.museum.upenn.edu/epsd2/signlist/.<br>'
		'– Veldhuis, N., Tinney, S. et al. (2014–): *OSL: Oracc Sign List*. Philadelphia: The Open Richly Annotated Cuneiform Corpus. https://oracc.museum.upenn.edu/osl/.<br>'
		'', unsafe_allow_html=True)

# footer
footer = """<style>
background-color: transparent;
text-decoration: underline;
}

a:hover, a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0.1;
bottom: 0;
width: 99%;
background-color: transparent;
color: #575656;
text-align: left;
}
</style>
<div class="footer">
<p>KacaSas 2025</p>
</div>
"""
st.sidebar.markdown(footer, unsafe_allow_html=True)

