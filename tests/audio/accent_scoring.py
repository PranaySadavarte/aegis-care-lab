"""Literal transcription and explicit numeral-equivalence scores, kept separate."""
import re
import jiwer
WORDS=dict(zip('zero one two three four five six seven eight nine'.split(),'0123456789'))
def normalize(text):
    return ' '.join(re.sub(r'[^a-z0-9\s]',' ',text.lower()).split())
def numeric(text):
    tokens=[WORDS.get(word,word) for word in normalize(text).split()]
    return re.sub(r'(?<!\w)(?:\d\s+)+\d(?!\w)',lambda m:re.sub(r'\s','',m.group()),' '.join(tokens))
def score(reference,hypothesis):
    if not hypothesis.strip():return {'scoring_status':'NO_SPEECH_EVENT','literal_wer':None,'cer':None,'numeral_wer':None,'exact_test_sequences':False}
    ref=normalize(reference);hyp=normalize(hypothesis)
    words=jiwer.process_words(ref,hyp)
    sequences=re.findall(r'\b\d+\b',numeric(hypothesis))
    return {'scoring_status':'OBSERVED','literal_wer':words.wer,'cer':jiwer.cer(ref,hyp),'numeral_wer':jiwer.wer(numeric(reference),numeric(hypothesis)),
            'word_substitutions':words.substitutions,'word_deletions':words.deletions,'word_insertions':words.insertions,'reference_words':len(ref.split()),
            'test_sequences_observed':sequences,'exact_test_sequences':sequences==['1234','5678'],
            'negative_word_observed':bool(re.search(r'\b(not|dont|don t)\b',normalize(hypothesis))),
            'negation_scope':'Lexical cue only; not semantic consent or reminder-policy grading.'}
