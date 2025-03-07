from rapidfuzz import fuzz, process
import pytesseract
from pdf2image import convert_from_path

court_mapping = {
    'Court of Appeals of Ohio, Tenth District, Franklin County.': 'Ohio Supreme Court',
    'Court of Criminal Appeals of Alabama.': 'Court of Criminal Appeals of Alabama',
    'Supreme Court of the United States': 'Supreme Court of the United States',
    'Supreme Court of the United States.': 'Supreme Court of the United States',
    'United States Court of Appeals, District of Columbia Circuit.': 'Court of Appeals for the D.C. Circuit',
    'United States Court of Appeals, Eighth Circuit.': 'Court of Appeals for the Eighth Circuit',
    'United States Court of Appeals, Eleventh Circuit.': 'Court of Appeals for the Eleventh Circuit',
    'United States Court of Appeals, Federal Circuit.': 'Court of Appeals for the Federal Circuit',
    'United States Court of Appeals, Fifth Circuit.': 'Court of Appeals for the Fifth Circuit',
    'United States Court of Appeals, First Circuit.': 'Court of Appeals for the First Circuit',
    'United States Court of Appeals, Fourth Circuit.': 'Court of Appeals for the Fourth Circuit',
    'United States Court of Appeals, Ninth Circuit.': 'Court of Appeals for the Ninth Circuit',
    'United States Court of Appeals, Second Circuit.': 'Court of Appeals for the Second Circuit',
    'United States Court of Appeals, Seventh Circuit.': 'Court of Appeals for the Seventh Circuit',
    'United States Court of Appeals, Sixth Circuit.': 'Court of Appeals for the Sixth Circuit',
    'United States Court of Appeals, Tenth Circuit.': 'Court of Appeals for the Tenth Circuit',
    'United States Court of Appeals, Third Circuit.': 'Court of Appeals for the Third Circuit',
    'United States Court of Federal Claims.': 'United States Court of Federal Claims',
    'United States District Court, District of Columbia.': 'District Court, District of Columbia',
    'United States District Court, C.D. California, Western Division.': 'District Court, C.D. California',
    'United States District Court, C.D. California.': 'District Court, C.D. California',
    'United States District Court, D. Arizona.': 'District Court, D. Arizona',
    'United States District Court, D. Colorado.': 'District Court, D. Colorado',
    'United States District Court, D. Delaware.': 'District Court, D. Delaware',
    'United States District Court, D. Kansas.': 'District Court, D. Kansas',
    'United States District Court, D. Maryland.': 'District Court, D. Maryland',
    'United States District Court, D. Massachusetts.': 'District Court, D. Massachusetts',
    'United States District Court, D. Montana, Missoula Division.': 'District Court, D. Montana',
    'United States District Court, D. Nevada.': 'District Court, D. Nevada',
    'United States District Court, D. New Jersey.': 'District Court, D. New Jersey',
    'United States District Court, D. Puerto Rico.': 'District Court, D. Puerto Rico',
    'United States District Court, E.D. Louisiana.': 'District Court, E.D. Louisiana',
    'United States District Court, E.D. Michigan, Southern Division.': 'District Court, E.D. Michigan',
    'United States District Court, E.D. Missouri, Eastern Division.': 'District Court, E.D. Missouri',
    'United States District Court, E.D. New York.': 'District Court, E.D. New York',
    'United States District Court, E.D. Pennsylvania.': 'District Court, E.D. Pennsylvania',
    'United States District Court, E.D. Texas, Texarkana Division.': 'District Court, E.D. Texas',
    'United States District Court, E.D. Virginia.': 'District Court, E.D. Virginia',
    'United States District Court, E.D. Wisconsin.': 'District Court, E.D. Wisconsin',
    'United States District Court, M.D. Florida, Tampa Division.': 'District Court, M.D. Florida',
    'United States District Court, M.D. North Carolina.': 'District Court, M.D. North Carolina',
    'United States District Court, N.D. California, San Jose Division.': 'District Court, N.D. California',
    'United States District Court, N.D. California.': 'District Court, N.D. California',
    'United States District Court, N.D. Florida, Gainesville Division.': 'District Court, N.D. Florida',
    'United States District Court, N.D. Georgia, Atlanta Division.': 'District Court, N.D. Georgia',
    'United States District Court, N.D. Illinois, Eastern Division.': 'District Court, N.D. Illinois',
    'United States District Court, N.D. Indiana,': 'District Court, N.D. Indiana',
    'United States District Court, N.D. Mississippi.': 'District Court, N.D. Mississippi',
    'United States District Court, N.D. New York.': 'District Court, N.D. New York',
    'United States District Court, N.D. Ohio, Eastern Division.': 'District Court, N.D. Ohio',
    'United States District Court, N.D. Texas, Dallas Division.': 'District Court, N.D. Texas',
    'United States District Court, N.D. Texas, Fort Worth Division.': 'District Court, N.D. Texas',
    'United States District Court, S.D. California.': 'District Court, S.D. California',
    'United States District Court, S.D. Florida.': 'District Court, S.D. Florida',
    'United States District Court, S.D. Illinois.': 'District Court, S.D. Illinois',
    'United States District Court, S.D. Indiana, Indianapolis Division.': 'District Court, S.D. Indiana',
    'United States District Court, S.D. New York.': 'District Court, S.D. New York',
    'United States District Court, S.D. Texas, Houston Division.': 'District Court, S.D. Texas',
    'United States District Court, W.D. Missouri, Saint Joseph Division.': 'District Court, W.D. Missouri',
    'United States District Court, W.D. North Carolina, Charlotte Division.': 'District Court, W.D. North Carolina',
    'United States District Court, W.D. Oklahoma.': 'District Court, W.D. Oklahoma',
    'United States District Court, W.D. Pennsylvania.': 'District Court, W.D. Pennsylvania',
    'United States District Court, W.D. Texas, Austin Division.': 'District Court, W.D. Texas',
    'United States District Court, W.D. Virginia, Lynchburg Division.': 'District Court, W.D. Virginia',
    'United States District Court, W.D. Washington, at Tacoma.': 'District Court, W.D. Washington',
    'United States District Court, W.D. Wisconsin.': 'District Court, W.D. Wisconsin',
    'United States District court, D. Maryland, Northern Division.': 'District Court, D. Maryland',
    'District of Columbia Court of Appeals': 'District of Columbia Court of Appeals',
    'New York Court of Appeals': 'New York Court of Appeals',
    'Ohio Supreme Court': 'Ohio Supreme Court',
    'Supreme Court of Louisiana': 'Supreme Court of Louisiana'
}

def pdf_to_text(pdf_path, output_txt=None, lang='eng'):
    text = ""
    
    # Convert PDF pages to images
    images = convert_from_path(pdf_path)

    for i, img in enumerate(images):
        page_text = pytesseract.image_to_string(img, lang=lang)
        text += f"\n--- Page {i+1} ---\n{page_text}\n"

    # Save to file if output path is provided
    if output_txt:
        with open(output_txt, "w", encoding="utf-8") as f:
            f.write(text)

    return text

def best_fuzzy_match(query, choices):

    query_cleaned = query.lower().replace(" ", "")  # Normalize query
    choices_cleaned = {c: c.lower().replace(" ", "") for c in choices}  # Normalize choices

    best_match, score, _ = process.extractOne(query_cleaned, choices_cleaned.values(), scorer=fuzz.ratio)

    # Get the original string from the dictionary
    best_original = next(orig for orig, cleaned in choices_cleaned.items() if cleaned == best_match)

    return best_original, score


import re

def simple_sent_tokenize(text):
    """
    A simple sentence tokenizer that splits text on punctuation
    (., !, or ?) followed by whitespace. This heuristic might not
    cover every edge case but works well for many texts.
    """
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return sentences

def chunk_text(text, chunk_size=200, overlap=20):
    """
    Splits the input text into chunks with a target word count per chunk
    and overlapping sentences to maintain context.

    Args:
        text (str): The text to be chunked.
        chunk_size (int): Approximate target number of words per chunk.
        overlap (int): Minimum number of words to include as overlap in subsequent chunks.

    Returns:
        list[str]: List of text chunks.
    """
    sentences = simple_sent_tokenize(text)
    chunks = []
    current_chunk = []
    current_words = 0

    for sentence in sentences:
        sentence_word_count = len(sentence.split())
        
        # If adding this sentence would exceed the chunk size and the current chunk isn't empty,
        # finalize the current chunk.
        if current_words + sentence_word_count > chunk_size and current_chunk:
            chunks.append(" ".join(current_chunk))
            
            # Prepare the overlap for the next chunk: backtrack through the current chunk
            # and collect sentences until the overlap word count is reached.
            new_chunk = []
            new_words = 0
            for sent in reversed(current_chunk):
                words_in_sent = len(sent.split())
                if new_words + words_in_sent <= overlap:
                    new_chunk.insert(0, sent)
                    new_words += words_in_sent
                else:
                    break
            
            # Start a new chunk with the overlapping sentences.
            current_chunk = new_chunk.copy()
            current_words = new_words
        
        # Add the current sentence to the chunk.
        current_chunk.append(sentence)
        current_words += sentence_word_count

    # Add any remaining sentences as a final chunk.
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks