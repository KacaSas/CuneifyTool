import csv
import pandas as pd
import re
import streamlit as st
import base64
from st_copy_to_clipboard import st_copy_to_clipboard

st.set_page_config(page_title='CuneifyTool', page_icon='resources/icon/icon.png', layout='wide')  # change favicon and page title

# load cuneiform fonts
def loadFontCSS(fontName, fontPath):
	with open(fontPath, "rb") as f:
		fontData = f.read()
		b64Font = base64.b64encode(fontData).decode()
		return f"""
		@font-face {{
			font-family: '{fontName}';
			src: url(data:font/ttf;base64,{b64Font}) format('truetype');
		}}
		"""
fontsCSS = ""
fontsCSS += loadFontCSS("Sinacherib", "resources/fonts/Sinacherib.ttf")
fontsCSS += loadFontCSS("Santakku", "resources/fonts/Santakku.ttf")
fontsCSS += loadFontCSS("SantakkuM", "resources/fonts/SantakkuM.ttf")
fontsCSS += loadFontCSS("Assurbanipal", "resources/fonts/Assurbanipal.ttf")
fontsCSS += loadFontCSS("OB Freie", "resources/fonts/OBFreie-Regular.ttf")
fontsCSS += loadFontCSS("CuneiformComposite", "resources/fonts/CuneiformComposite.ttf")
fontsCSS += loadFontCSS("Esagil", "resources/fonts/Esagil.ttf")
fontsCSS += loadFontCSS("Nabu-ninua-ihsus", "resources/fonts/Nabuninuaihsus.ttf")
fontsCSS += loadFontCSS("Gudea", "resources/fonts/Oracc-gudea.ttf")
fontsCSS += loadFontCSS("Oracc LAK", "resources/fonts/Oracc-LAK.ttf")
fontsCSS += loadFontCSS("Oracc RSP", "resources/fonts/Oracc-RSP.ttf")

st.markdown(f"<style>{fontsCSS}</style>", unsafe_allow_html=True)  # insert fonts into the app page

def clearTextArea():
	st.session_state['translitInput'] = ''

st.header('CuneifyTool')
st.write('<br><br><font style="font-size: 19px; color: #2e9aff">This app is inspired by <i>Cuneify</i> by S. Tinney, <i>Cuneify REPL</i> by J. Knowles, and other similar tools for converting transliterations into cuneiform script. The cuneiform fonts used in this app are available thanks to the efforts of S. Vanséveren, S. Tinney, C. R. Ziegeler, R. Leroy, and others. Individual cuneiform signs are mapped according to my <i>Cuneiform Sign List</i> (http://home.zcu.cz/~ksaskova/Sign_List.html). For details on the fonts used, related tools, and cuneiform sign lists, see <i>Sources and references</i> below.<br></font>', unsafe_allow_html=True)

signList = pd.read_csv('resources/signList/SignList.csv', keep_default_na=False, na_values=[])

st.sidebar.write('<p style="margin-top: 17em;"><b><font style="font-size: 19px">Font options</b></font></p>', unsafe_allow_html=True)

selectedCuneiFont = st.sidebar.selectbox('Cuneiform font', ('Oracc LAK', 'Oracc RSP', 'Gudea', 'CuneiformComposite', 'SantakkuM', 'OB Freie', 'Santakku', 'Assurbanipal', 'Nabu-ninua-ihsus', 'Sinacherib', 'Esagil'), index=7, key='selectedCuneiFont', label_visibility='collapsed')

selectedCuneiFontSizePT = st.sidebar.selectbox('Font size', ('10 pt', '15 pt', '17 pt', '19 pt', '20 pt', '21 pt', '22 pt', '23 pt', '24 pt', '25 pt', '27 pt', '30 pt', '32 pt', '35 pt', '37 pt', '40 pt', '42 pt', '45 pt', '47 pt', '50 pt', '52 pt', '55 pt', '57 pt', '60 pt'), index=7, key='selectedCuneiFontSize', label_visibility='collapsed')

selectedCuneiFontSize = selectedCuneiFontSizePT.replace(' pt', '')

selectedCuneiFontSizePT2PX = round(int(selectedCuneiFontSize) * 1.333)

st.sidebar.divider()

with st.sidebar.expander('Font details', expanded=False):
	st.write("""
		<b>Oracc LAK</b><br><font style="color: #969799; font-size: 0.9em;">– Early Dynastic / 3<sup>rd</sup> millennium</font><br>
		<b>Oracc RSP</b><br><font style="color: #969799; font-size: 0.9em;">– Early Dynastic IIIb</font><br>
		<b>Gudea</b><br><font style="color: #969799; font-size: 0.9em;">– Gudea signs</font><br>
		<b>CuneiformComposite</b><br><font style="color: #969799; font-size: 0.9em;">– end of the 3<sup>rd</sup> millennium</font><br>
		<b>SantakkuM</b><br><font style="color: #969799; font-size: 0.9em;">– Old Babylonian monumental</font><br>
		<b>OB Freie</b><br><font style="color: #969799; font-size: 0.9em;">– Old Babylonian literature</font><br>
		<b>Santakku</b><br><font style="color: #969799; font-size: 0.9em;">– Old Babylonian cursive</font><br>
		<b>Assurbanipal</b><br><font style="color: #969799; font-size: 0.9em;">– Neo-Assyrian</font><br>
		<b>Nabu-ninua-ihsus</b><br><font style="color: #969799; font-size: 0.9em;">– Neo-Assyrian</font><br>
		<b>Sinacherib</b><br><font style="color: #969799; font-size: 0.9em;">– Neo-Assyrian</font><br>
		<b>Esagil</b><br><font style="color: #969799; font-size: 0.9em;">– Neo-Babylonian</font><br>
		""", unsafe_allow_html=True)

columna1, columna2 = st.columns([1, 1], gap='small')
with columna1:
	st.markdown(f"""
	<style>
	div[data-testid="stTextArea"] textarea {{
		font-size: {selectedCuneiFontSizePT2PX}px !important; background-color: #0e1117 !important;}}
	</style>""", unsafe_allow_html=True)

	translitInput = st.text_area('Write/paste transliteration', height=500, key='translitInput', placeholder='Write or paste a transliteration...', label_visibility='collapsed')
	applyCuneify = st.button('Apply', use_container_width=True, key='applyCuneify')
	translitInput = translitInput.lower()
with columna2:
	st.write('')
	with st.container(border=True, height=501):
		if translitInput != '' or applyCuneify:
			replacementsInput = {'1': '₁', '2': '₂', '3': '₃', '4': '₄', '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉', '0': '₀', 'Sh': 'Š', 'sh': 'š', 'Sz': 'Š', 'sz': 'š', 'kh': 'ḫ', 'H': 'Ḫ', 'h': 'ḫ', 'ŋ': 'g', 'Ŋ': 'G', 'v': 'w', 'V': 'W', r',s': r'ṣ', r',S': r'Ṣ', r',t': r'ṭ', r',T': r'Ṭ', r's,': r'ṣ', r'S,': r'Ṣ', r't,': r'ṭ', r'T,': r'Ṭ', r'.': r'-', r'<br>': r'\n', ' ': '-###-', '<': '-<-', '>': '->-', r'?': r'-\?-', '!': '-!-', r'[': r'-\[-', r'(': r'-\(-', r']': r'-\]-', r')': r'-\)-', ':': '-:-', ';': '-;@@@-', '⸢': '-⸢-', '⸣': '-⸣-', ',': '-,@@@-', '\n': '-\n&&&\n-', r'\b(\w∗)(á)(\w∗)\b': r'$1a$3₂'}
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

				cuneifiedText = ''
				for signs in cuneiformText:
					cuneifiedText = cuneifiedText + signs

			finalCuneiformText = '<font style="font-family: ' + str(selectedCuneiFont) + '; font-size:' + str(selectedCuneiFontSize) + 'pt; color: #ffffab;">' + cuneifiedText + '</font>'
			finalCuneiformText = finalCuneiformText.replace('&&&', '<br>').replace('###', ' ').replace('@@@', '').replace('\\', '')
			st.write(finalCuneiformText, unsafe_allow_html=True)

			cuneifiedTextToCopy = cuneifiedText.replace('&&&', '\n').replace('###', ' ').replace('\n\n', '\n').replace('\\', '').replace('@@@', '')
			cuneifiedTextToCopy = re.sub(r'\n\s*\n', '\n', cuneifiedTextToCopy.strip())

	col1, col2, col3 = st.columns([1, 0.7, 1], gap='small')
	with col1:
		if translitInput != '':
			st_copy_to_clipboard(cuneifiedTextToCopy, before_copy_label='Copy cunified text (as plain text)', after_copy_label='Copied successfully!', show_text=False)
	with col3:
		clearTextArea = st.button('Clear', key='clearTextArea', on_click=clearTextArea, use_container_width=True)

st.write('<p style="margin-top: 3em;"><b><font style="font-size: 19px">Sources and references</font></b></p>', unsafe_allow_html=True)

with st.expander('↕', expanded=False):
	st.markdown('**Fonts used**', unsafe_allow_html=True)
	st.markdown(
		'– *Oracc-LAK.ttf* (by S. Tinney and V. Kethana). https://oracc.museum.upenn.edu/osl/OraccCuneiformFonts/index.html and https://github.com/oracc/oracc2/tree/main/msc/fonts.<br>'
		'– *Oracc-RSP.ttf* (by S. Tinney). https://oracc.museum.upenn.edu/osl/OraccCuneiformFonts/index.html and https://github.com/oracc/oracc2/tree/main/msc/fonts.<br>'
		'– *Oracc-gudea.ttf* (by S. Tinney). https://oracc.museum.upenn.edu/osl/OraccCuneiformFonts/index.html and https://github.com/oracc/oracc2/tree/main/msc/fonts.<br>'
		'– *CuneiformComposite.ttf* (by S. Tinney). http://oracc.museum.upenn.edu/doc/help/visitingoracc/fonts/.<br>'
		'– *SantakkuM.ttf* (by S. Vanséveren). https://hethport.net/cuneifont/.<br>'
		'– *Old Babylonian Freie* (by C. R. Ziegeler). https://refubium.fu-berlin.de/handle/fub188/45271 and https://github.com/crzfub/OB-Freie.<br>'
		'– *Santakku.ttf* (by S. Vanséveren). https://hethport.net/cuneifont/.<br>'
		'– *Assurbanipal.ttf* (by S. Vanséveren). https://hethport.net/cuneifont/.<br>'
		'– *Nabuninuaihsus.ttf* (by R. Leroy). https://github.com/eggrobin/Nabu-ninua-ihsus, https://oracc.museum.upenn.edu/osl/OraccCuneiformFonts/index.html and https://github.com/oracc/oracc2/tree/main/msc/fonts.<br>'
		'– *Sinacherib.ttf* (by K. Šašková). http://home.zcu.cz/~ksaskova/.<br>'
		'– *Esagil.ttf* (by S. Vanséveren). https://hethport.net/cuneifont/.', unsafe_allow_html=True)
	st.markdown('**Similar tools**', unsafe_allow_html=True)
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
.footer a:link, .footer a:visited {
color: #575656;
text-decoration: none;
}

.footer a:hover, .footer a:active {
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
<p><a href="https://zcu.academia.edu/Kate%C5%99ina%C5%A0a%C5%A1kov%C3%A1" target="_blank">KacaSas</a> 2025</p>
</div>
"""
st.sidebar.markdown(footer, unsafe_allow_html=True)

