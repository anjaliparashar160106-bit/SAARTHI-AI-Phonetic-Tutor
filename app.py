from flask import Flask, render_template

# Initialize the Flask web server application
app = Flask(__name__)


# LEVEL 1 DATABASE: Alphabet Identification (A to Z)
# Each key contains its Hindi sound representation and accent-forgiving arrays.
alphabets_data = {
    'A': {'hindi': 'अ', 'audio': 'ए', 'next': 'B', 'sounds': ['a', 'ay', 'eh', 'e', 'ah', 'uh']},
    'B': {'hindi': 'ब', 'audio': 'बी', 'next': 'C', 'sounds': ['b', 'bee', 'be', 'v', 'we', 'zee']},
    'C': {'hindi': 'स', 'audio': 'सी', 'next': 'D', 'sounds': ['c', 'see', 'sea', 'si', 'she', 'say']},
    'D': {'hindi': 'ड', 'audio': 'डी', 'next': 'E', 'sounds': ['d', 'dee', 'the', 'di', 'de', 'tee']},
    'E': {'hindi': 'इ', 'audio': 'ई', 'next': 'F', 'sounds': ['e', 'ee', 'he', 'yi', 'yea', 'i']},
    'F': {'hindi': 'फ़', 'audio': 'एफ', 'next': 'G', 'sounds': ['f', 'ef', 'eff', 'if', 'fa', 'off']},
    'G': {'hindi': 'ग', 'audio': 'जी', 'next': 'H', 'sounds': ['g', 'jee', 'zi', 'gee', 'j', 'ze']},
    'H': {'hindi': 'ह', 'audio': 'एच', 'next': 'I', 'sounds': ['h', 'ach', 'each', 'age', 'edge', 'is']},
    'I': {'hindi': 'आइ', 'audio': 'आई', 'next': 'J', 'sounds': ['i', 'eye', 'aye', 'hi', 'high', 'aai']},
    'J': {'hindi': 'ज', 'audio': 'जे', 'next': 'K', 'sounds': ['j', 'jay', 'je', 'zay', 'zee', 'g']},
    'K': {'hindi': 'क', 'audio': 'के', 'next': 'L', 'sounds': ['k', 'kay', 'okay', 'que', 'ca', 'ok']},
    'L': {'hindi': 'ल', 'audio': 'एल', 'next': 'M', 'sounds': ['l', 'el', 'ell', 'al', 'hell', 'all']},
    'M': {'hindi': 'म', 'audio': 'एम', 'next': 'N', 'sounds': ['m', 'em', 'am', 'aim', 'hmm', 'ham']},
    'N': {'hindi': 'न', 'audio': 'एन', 'next': 'O', 'sounds': ['n', 'en', 'an', 'and', 'in', 'end']},
    'O': {'hindi': 'ओ', 'audio': 'ओ', 'next': 'P', 'sounds': ['o', 'oh', 'owe', 'awe', 'ho', 'zero']},
    'P': {'hindi': 'प', 'audio': 'पी', 'next': 'Q', 'sounds': ['p', 'pee', 'pea', 'pi', 'be', 'fee']},
    'Q': {'hindi': 'क्व', 'audio': 'क्यू', 'next': 'R', 'sounds': ['q', 'cue', 'queue', 'kyu', 'kyo', 'few']},
    'R': {'hindi': 'र', 'audio': 'आर', 'next': 'S', 'sounds': ['r', 'ar', 'are', 'our', 'or', 'aur']},
    'S': {'hindi': 'स', 'audio': 'एस', 'next': 'T', 'sounds': ['s', 'es', 'ass', 'yes', 'ace', 'is']},
    'T': {'hindi': 'ट', 'audio': 'टी', 'next': 'U', 'sounds': ['t', 'tee', 'tea', 'ti', 'tree', 'd']},
    'U': {'hindi': 'अ', 'audio': 'यू', 'next': 'V', 'sounds': ['u', 'you', 'yu', 'yoo', 'yo', 'hue']},
    'V': {'hindi': 'व', 'audio': 'वी', 'next': 'W', 'sounds': ['v', 'vee', 'we', 'vi', 'b', 'me']},
    'W': {'hindi': 'व', 'audio': 'डब्लू', 'next': 'X', 'sounds': ['w', 'double u', 'dablu', 'double you', 'dummy']},
    'X': {'hindi': 'क्स', 'audio': 'एक्स', 'next': 'Y', 'sounds': ['x', 'ex', 'axe', 'eggs', 'ax', 'yes']},
    'Y': {'hindi': 'य', 'audio': 'वाय', 'next': 'Z', 'sounds': ['y', 'why', 'wai', 'bye', 'wae', 'my']},
    'Z': {'hindi': 'ज़', 'audio': 'ज़éd', 'next': 'DONE', 'sounds': ['z', 'zed', 'zee', 'head', 'said', 'g']}
}


# LEVEL 2 DATABASE: The 12 Hindi Matras (Vowel Markers)
# Maps visual symbols to accent frequencies for targeted local mapping.

matras_data = {
    'A_SOUND':  {'display': 'अ', 'english_map': 'A', 'audio_hint': 'अ', 'example': 'Bus (बस)', 'next': 'AA_MATRA', 'sounds': ['a', 'uh', 'ah', 'u', 'bas', 'bus']},
    'AA_MATRA': {'display': 'ा (आ)', 'english_map': 'AA / A', 'audio_hint': 'आ', 'example': 'Car (कार)', 'next': 'I_MATRA', 'sounds': ['aa', 'ah', 'a', 'car', 'ka', 'aar']},
    'I_MATRA':  {'display': 'ि (इ)', 'english_map': 'I', 'audio_hint': 'इ', 'example': 'Pin (पिन)', 'next': 'EE_MATRA', 'sounds': ['i', 'ee', 'e', 'pin', 'in', 'pi']},
    'EE_MATRA': {'display': 'ी (ई)', 'english_map': 'EE', 'audio_hint': 'ई', 'example': 'Deep (दीप)', 'next': 'U_MATRA', 'sounds': ['ee', 'ea', 'i', 'yi', 'deep', 'di']},
    'U_MATRA':  {'display': 'ु (उ)', 'english_map': 'U', 'audio_hint': 'उ', 'example': 'Pull (पुल)', 'next': 'OO_MATRA', 'sounds': ['u', 'oo', 'o', 'pull', 'pul', 'pur']},
    'OO_MATRA': {'display': 'ू (ऊ)', 'english_map': 'OO', 'audio_hint': 'ऊ', 'example': 'Moon (मून)', 'next': 'E_MATRA', 'sounds': ['oo', 'u', 'who', 'you', 'moon', 'mun']},
    'E_MATRA':  {'display': 'े (ए)', 'english_map': 'E', 'audio_hint': 'ए', 'example': 'Pen (पेन)', 'next': 'AI_MATRA', 'sounds': ['e', 'ay', 'eh', 'hey', 'pen', 'pay']},
    'AI_MATRA': {'display': 'ै (ऐ)', 'english_map': 'AI', 'audio_hint': 'ऐ', 'example': 'Bank (बैंक)', 'next': 'O_MATRA', 'sounds': ['ai', 'aye', 'ae', 'bank', 'ben', 'baank']},
    'O_MATRA':  {'display': 'ो (ओ)', 'english_map': 'O', 'audio_hint': 'ओ', 'example': 'Go (गो)', 'next': 'AU_MATRA', 'sounds': ['o', 'oh', 'owe', 'go', 'low', '0']},
    'AU_MATRA': {'display': 'ौ (औ)', 'english_map': 'AU / OU', 'audio_hint': 'औ', 'example': 'Call (कॉल)', 'next': 'AM_MATRA', 'sounds': ['au', 'ou', 'aw', 'call', 'on', 'gaw']},
    'AM_MATRA': {'display': 'ं (अं)', 'english_map': 'AN / AM', 'audio_hint': 'अं', 'example': 'Fund (फंड)', 'next': 'AHA_MATRA', 'sounds': ['am', 'an', 'un', 'and', 'fund', 'fan']},
    'AHA_MATRA':{'display': 'ः (अः)', 'english_map': 'AHA', 'audio_hint': 'अह', 'example': 'Namah (नमः)', 'next': 'L2_DONE', 'sounds': ['aha', 'ah', 'h', 'namah', 'haha', 'nama']}
}

# LEVEL 3 DATABASE: 40 Core Practical Words 
# Phase A contains Hinglish phonetic mappings; Phase B maps functional real English.

words_data = {
    # Phase A: Hinglish Sound Progression (20 Words)
    'H_BUS':     {'display': 'BUS', 'hindi': 'बस', 'audio_hint': 'बस', 'example': 'बिना मात्रा का शब्द', 'next': 'H_GHAR', 'sounds': ['bus', 'bas', 'bass', 'buzz', 'us', 'bath']},
    'H_GHAR':    {'display': 'GHAR', 'hindi': 'घर', 'audio_hint': 'घर', 'example': 'बिना मात्रा का शब्द', 'next': 'H_KAR', 'sounds': ['ghar', 'gar', 'gah', 'bar', 'dar', 'gaar']},
    'H_KAR':     {'display': 'KAR', 'hindi': 'कर', 'audio_hint': 'कर', 'example': 'बिना मात्रा का शब्द', 'next': 'H_JAL', 'sounds': ['kar', 'car', 'ka', 'par', 'sar', 'cur']},
    'H_JAL':     {'display': 'JAL', 'hindi': 'जल', 'audio_hint': 'जल', 'example': 'बिना मात्रा का शब्द', 'next': 'H_MAT', 'sounds': ['jal', 'jul', 'gel', 'jar', 'well', 'chal']},
    'H_MAT':     {'display': 'MAT', 'hindi': 'मत', 'audio_hint': 'मत', 'example': 'बिना मात्रा का शब्द', 'next': 'H_FAL', 'sounds': ['mat', 'mutt', 'met', 'mut', 'hat', 'bat']},
    'H_FAL':     {'display': 'FAL', 'hindi': 'फल', 'audio_hint': 'फल', 'example': 'बिना मात्रा का शब्द', 'next': 'H_CHAL', 'sounds': ['fal', 'phal', 'full', 'fall', 'pal', 'hal']},
    'H_CHAL':    {'display': 'CHAL', 'hindi': 'चल', 'audio_hint': 'चल', 'example': 'बिना मात्रा का शब्द', 'next': 'H_MAN', 'sounds': ['chal', 'chul', 'char', 'cell', 'chel', 'cal']},
    'H_MAN':     {'display': 'MAN', 'hindi': 'मन', 'audio_hint': 'मन', 'example': 'बिना मात्रा का शब्द', 'next': 'H_TAN', 'sounds': ['man', 'mun', 'mon', 'men', 'main', 'ban']},
    'H_TAN':     {'display': 'TAN', 'hindi': 'तन', 'audio_hint': 'तन', 'example': 'बिना मात्रा का शब्द', 'next': 'H_DHAN', 'sounds': ['tan', 'tun', 'ten', 'tin', 'than', 'pan']},
    'H_DHAN':    {'display': 'DHAN', 'hindi': 'धन', 'audio_hint': 'धन', 'example': 'बिना मात्रा का शब्द', 'next': 'H_NAAM', 'sounds': ['dhan', 'dan', 'dun', 'done', 'dha', 'van']},
    
    'H_NAAM':    {'display': 'NAAM', 'hindi': 'नाम', 'audio_hint': 'नाम', 'example': 'मात्रा वाले शब्द', 'next': 'H_KAAM', 'sounds': ['naam', 'nam', 'name', 'naham', 'kam', 'am']},
    'H_KAAM':    {'display': 'KAAM', 'hindi': 'काम', 'audio_hint': 'काम', 'example': 'मात्रा वाले शब्द', 'next': 'H_PAPA', 'sounds': ['kaam', 'kam', 'come', 'calm', 'kham', 'arm']},
    'H_PAPA':    {'display': 'PAPA', 'hindi': 'पापा', 'audio_hint': 'पापा', 'example': 'मात्रा वाले शब्द', 'next': 'H_PAANI', 'sounds': ['papa', 'paapa', 'pappa', 'pop', 'baba', 'puppa']},
    'H_PAANI':   {'display': 'PAANI', 'hindi': 'पानी', 'audio_hint': 'पानी', 'example': 'मात्रा वाले शब्द', 'next': 'H_GAADI', 'sounds': ['paani', 'pani', 'pan', 'puny', 'pany', 'panni']},
    'H_GAADI':   {'display': 'GAADI', 'hindi': 'गाड़ी', 'audio_hint': 'गाड़ी', 'example': 'मात्रा वाले शब्द', 'next': 'H_DOODH', 'sounds': ['gaadi', 'gadi', 'gari', 'gadhi', 'god', 'gadd']},
    'H_DOODH':   {'display': 'DOODH', 'hindi': 'दूध', 'audio_hint': 'दूध', 'example': 'मात्रा वाले शब्द', 'next': 'H_PHOOL', 'sounds': ['doodh', 'dudh', 'dude', 'dood', 'do', 'dhud']},
    'H_PHOOL':   {'display': 'PHOOL', 'hindi': 'फूल', 'audio_hint': 'फूल', 'example': 'मात्रा वाले शब्द', 'next': 'H_KHANA', 'sounds': ['phool', 'ful', 'fool', 'pool', 'phal', 'phul']},
    'H_KHANA':   {'display': 'KHANA', 'hindi': 'खाना', 'audio_hint': 'खाना', 'example': 'मात्रा वाले शब्द', 'next': 'H_CHAI', 'sounds': ['khana', 'khaana', 'kana', 'kanaa', 'gana', 'hana']},
    'H_CHAI':    {'display': 'CHAI', 'hindi': 'चाय', 'audio_hint': 'चाय', 'example': 'मात्रा वाले शब्द', 'next': 'H_PAISA', 'sounds': ['chai', 'chaye', 'chi', 'shy', 'tie', 'chaa']},
    'H_PAISA':   {'display': 'PAISA', 'hindi': 'पैसा', 'audio_hint': 'पैसा', 'example': 'भारी/कठिन शब्द', 'next': 'L3_PHASE_A_DONE', 'sounds': ['paisa', 'piesa', 'pisa', 'paesa', 'baisa', 'pasa']},

    # Phase B: Functional Real-World English (20 Words)
    'E_IN':      {'display': 'IN', 'hindi': 'इन', 'audio_hint': 'इन', 'example': 'छोटे इंग्लिश शब्द', 'next': 'E_ON', 'sounds': ['in', 'inn', 'een', 'an', 'en', 'is']},
    'E_ON':      {'display': 'ON', 'hindi': 'ऑन', 'audio_hint': 'ऑन', 'example': 'छोटे इंग्लिश शब्द', 'next': 'E_GO', 'sounds': ['on', 'own', 'an', 'one', 'un', 'or']},
    'E_GO':      {'display': 'GO', 'hindi': 'गो', 'audio_hint': 'गो', 'example': 'छोटे इंग्लिश शब्द', 'next': 'E_UP', 'sounds': ['go', 'gow', 'ko', 'no', 'so', 'oh']},
    'E_UP':      {'display': 'UP', 'hindi': 'अप', 'audio_hint': 'अप', 'example': 'छोटे इंग्लिश शब्द', 'next': 'E_NO', 'sounds': ['up', 'ap', 'app', 'op', 'ab', 'cup']},
    'E_NO':      {'display': 'NO', 'hindi': 'नो', 'audio_hint': 'नो', 'example': 'छोटे इंग्लिश शब्द', 'next': 'E_TO', 'sounds': ['no', 'know', 'now', 'low', 'go', 'noh']},
    'E_TO':      {'display': 'TO', 'hindi': 'टू', 'audio_hint': 'टू', 'example': 'छोटे इंग्लिश शब्द', 'next': 'E_MY', 'sounds': ['to', 'two', 'too', 'do', 'tu', 'top']},
    'E_MY':      {'display': 'MY', 'hindi': 'माय', 'audio_hint': 'माय', 'example': 'छोटे इंग्लिश शब्द', 'next': 'E_WE', 'sounds': ['my', 'mai', 'mai', 'by', 'me', 'me']},
    'E_WE':      {'display': 'WE', 'hindi': 'वी', 'audio_hint': 'वी', 'example': 'छोटे इंग्लिश शब्द', 'next': 'E_HE', 'sounds': ['we', 'wee', 'v', 'vi', 'wi', 'me']},
    'E_HE':      {'display': 'HE', 'hindi': 'ही', 'audio_hint': 'ही', 'example': 'छोटे इंग्लिश शब्द', 'next': 'E_YOU', 'sounds': ['he', 'hee', 'hi', 'the', 'she', 'me']},
    'E_YOU':     {'display': 'YOU', 'hindi': 'यू', 'audio_hint': 'यू', 'example': 'छोटे इंग्लिश शब्द', 'next': 'E_OPEN', 'sounds': ['you', 'u', 'yoo', 'yo', 'hue', 'ye']},
    
    'E_OPEN':    {'display': 'OPEN', 'hindi': 'ओपन', 'audio_hint': 'ओपन', 'example': 'मोबाइल/स्क्रीन के शब्द', 'next': 'E_STOP', 'sounds': ['open', 'opan', 'opin', 'hope', 'apen', 'upon']},
    'E_STOP':    {'display': 'STOP', 'hindi': 'स्टॉप', 'audio_hint': 'स्टॉप', 'example': 'मोबाइल/स्क्रीन के शब्द', 'next': 'E_HELP', 'sounds': ['stop', 'istop', 'top', 'shop', 'step', 'stump']},
    'E_HELP':    {'display': 'HELP', 'hindi': 'हेल्प', 'audio_hint': 'हेल्प', 'example': 'मोबाइल/स्क्रीन के शब्द', 'next': 'E_HOME', 'sounds': ['help', 'halp', 'kelp', 'alp', 'hell', 'hope']},
    'E_HOME':    {'display': 'HOME', 'hindi': 'होम', 'audio_hint': 'होम', 'example': 'मोबाइल/स्क्रीन के शब्द', 'next': 'E_LOCK', 'sounds': ['home', 'hom', 'hoom', 'whom', 'come', 'hope']},
    'E_LOCK':    {'display': 'LOCK', 'hindi': 'लॉक', 'audio_hint': 'लॉक', 'example': 'मोबाइल/स्क्रीन के शब्द', 'next': 'E_CALL', 'sounds': ['lock', 'lok', 'look', 'rock', 'block', 'luck']},
    'E_CALL':    {'display': 'CALL', 'hindi': 'कॉल', 'audio_hint': 'कॉल', 'example': 'मोबाइल/स्क्रीन के शब्द', 'next': 'E_BANK', 'sounds': ['call', 'col', 'kaal', 'all', 'ball', 'fall']},
    'E_BANK':    {'display': 'BANK', 'hindi': 'बैंक', 'audio_hint': 'बैंक', 'example': 'मोबाइल/स्क्रीन के शब्द', 'next': 'E_CASH', 'sounds': ['bank', 'benk', 'banc', 'baank', 'tank', 'blank']},
    'E_CASH':    {'display': 'CASH', 'hindi': 'कैश', 'audio_hint': 'कैश', 'example': 'मोबाइल/स्क्रीन के शब्द', 'next': 'E_SHOP', 'sounds': ['cash', 'caish', 'kesh', 'cas', 'crash', 'catch']},
    'E_SHOP':    {'display': 'SHOP', 'hindi': 'शॉप', 'audio_hint': 'शॉप', 'example': 'मोबाइल/स्क्रीन के शब्द', 'next': 'E_MENU', 'sounds': ['shop', 'sop', 'saap', 'chop', 'top', 'ship']},
    'E_MENU':    {'display': 'MENU', 'hindi': 'मेन्यू', 'audio_hint': 'मेन्यू', 'example': 'मोबाइल/स्क्रीन के शब्द', 'next': 'L3_COMPLETE', 'sounds': ['menu', 'manue', 'maynu', 'minu', 'many', 'money']}
}


# Route for the main dashboard index page

@app.route('/')
def home():
    return render_template('index.html')

# Route for Level 1 alphabet learning interface

@app.route('/level/<letter>')
def level(letter):
    letter = letter.upper() 
    if letter in alphabets_data:
        return render_template('learn.html', letter=letter, data=alphabets_data[letter], current_level="level1")
    return "<h1>Letter nahi mila!</h1>"


# Route for Level 2 Hindi vowel matra learning interface

@app.route('/matra/<matra_key>')
def matra_level(matra_key):
    matra_key = matra_key.upper()
    if matra_key in matras_data:
        return render_template('learn.html', letter=matra_key, data=matras_data[matra_key], current_level="level2")
    return "<h1>Matra nahi mili!</h1>"


# Route for Level 3 practical word learning interface

@app.route('/word/<word_key>')
def word_level(word_key):
    word_key = word_key.upper()
    if word_key in words_data:
        return render_template('learn.html', letter=word_key, data=words_data[word_key], current_level="level3")
    return "<h1>Shabd nahi mila!</h1>"


# Route for the milestone/completion animation screen

@app.route('/level/DONE')
def done():
    return render_template('done.html')

# Start the Flask development application in secure debugging mode
if __name__ == '__main__':
    app.run(debug=True)
