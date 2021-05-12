import csv, os, glob, google_trans_new
from tqdm import tqdm # sweet progress bar

#==============================================================================

def get_lang():
    """
    Purpose:
        gets language to translate to from user
    Dependencies: 
        google_trans_new
    Argument:
        None
    Returns:
        None
    """
    # dict of language short code(key) and name(value)
    langs = google_trans_new.LANGUAGES
       
    # enumerate and print each language name 
    for i in range(len(langs)):
        key = list(langs.keys())[i]
        print(str(i +1) + ": " + langs[key])

    selection = int(input("Select target language: ")) - 1

    # get short code
    lang = list(langs.keys())[selection]
    read_file(lang)

    return None

#==============================================================================

def read_file(lang):
    """
    Purpose:
        reads through each line of xml file
    Dependencies: 
        glob, os, tqdm
    Argument:
        lang- a language short code
    Returns:
        None
    """

    # requires just one xml file be in the folder
    with open(glob.glob("./*.xml")[0], 'r', encoding="utf8") as open_f:
        lines = open_f.readlines()
        open_f.close()
        
        try:
            os.remove("config.xml")
        except:
            pass
        try:
            os.remove("text.csv")
        except:
            pass
                
        for line in tqdm(lines):
            write_to_xml(line)
            if "<rdf:li xml:lang=\"en-US\">" in line and "</rdf:Bag>" not in line:
                english = clean_english(line)
                translation = translate(english, lang)
                write_to_csv(english,translation)
                formatted = add_formatting(translation, lang)
                write_to_xml(formatted)
        
    return None

#==============================================================================

def clean_english(line):
    """
    Purpose:
        removes formatting from a line with english text in it
    Dependencies: 
        None
    Argument:
        line - a string with xml markup and english subtitle text
    Returns:
        a cleaned line of english text
    """
    line = line.split("rtf1")
    line = line[1].split("}")
    line = line[0].split(" \\par ")
    return " ".join(line).strip()

#==============================================================================

def translate(eng, lang):
    """
    Purpose:
        Uses Google API to get translation
    Dependencies: 
        google_trans_new
    Argument:
        eng - a string of cleaned english text
        lang - short code for target language
    Returns:
        english translation of target language
    """
    translator = google_trans_new.google_translator()
    return translator.translate(eng, lang_tgt=lang, lang_src='en').strip()

#==============================================================================

def add_formatting(text, lang):
    """
    Purpose:
        adds xml markup to translation
    Dependencies: 
        None
    Argument:
        text - a string of translated text
        lang- a language short code
    Returns:
        translated text with xml formatting 
    """
    words = text.split()
    new_line = ""
    count = 0
    for word in words:
        word_length = len(word)
        if count + word_length > 45:
            new_line = new_line[:-1] + " \\par "
            count = 0
        new_line += word + " "
        count += word_length + 1
    new_line = new_line.strip()
    return "<rdf:li xml:lang=\"" + lang + "\">{\\rtf1 "+ new_line + "</rdf:li>"

#==============================================================================

def write_to_csv(eng,trns):
    """
    Purpose:
        writes the english and translated text in a row in a csv file
    Dependencies: 
        csv
    Argument:
        eng - a string of english text
        trns - a string of translated text
    Returns:
        None
    """
    with open("text.csv",'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([eng,trns])
        csv_file.close()
    return None

#==============================================================================

def write_to_xml(line):
    """
    Purpose:
        writes a line of xml to the xml file
    Dependencies: 
        None
    Argument:
        line - a string with xml mark up
    Returns:
        None
    """
    with open("config.xml", 'a', encoding="utf8") as open_f:
        open_f.write(line)
        open_f.close()
    return None

#==============================================================================

def main():
    get_lang()

#==============================================================================

if __name__ == '__main__':
    main()