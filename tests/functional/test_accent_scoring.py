import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tests/audio'))
from accent_scoring import score,numeric
class AccentScoring(unittest.TestCase):
    reference='The first test reference is one two three four. The second test reference is five six seven eight. I do not want a reminder.'
    def test_digit_format_difference_not_hidden_in_literal_wer(self):
        result=score(self.reference,'The first test reference is 1234. The second test reference is 5678. I do not want a reminder.')
        self.assertGreater(result['literal_wer'],0);self.assertEqual(result['numeral_wer'],0);self.assertTrue(result['exact_test_sequences'])
    def test_extra_or_wrong_digit_is_failure(self):
        for digits in ('12345','1233','91234'):
            self.assertFalse(score(self.reference,'The first test reference is '+digits+' and the second is 5678')['exact_test_sequences'])
    def test_missing_speech_has_no_fabricated_error_score(self):
        result=score(self.reference,'');self.assertIsNone(result['literal_wer']);self.assertEqual(result['scoring_status'],'NO_SPEECH_EVENT')
    def test_negation_loss_visible(self):
        result=score(self.reference,self.reference.replace('do not','do'))
        self.assertFalse(result['negative_word_observed']);self.assertGreater(result['literal_wer'],0)
    def test_individual_digits_join_without_merging_separate_numbers(self):
        self.assertEqual(numeric('one two three four and five six seven eight'),'1234 and 5678')
