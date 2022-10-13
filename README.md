# Summarizer
Requires model: `pl_nask-0.0.5.tar.gz` from http://mozart.ipipan.waw.pl/~rtuora/spacy/

Install:
```bash
python -m pip install path/to/pl_nask-0.0.5.tar.gz
python -m pip install path/to/summarizer-0.0.1-py3-none-any.whl 
```

Usage:
```python
from summarizer import Summarizer

summarizer = Summarizer()
text = "..."
limit = 300
unit = "words" # "words" or "chars"
out = summarizer.summarize(text, limit, unit)  # dict or KeyError
```
Alternatively use loaded model:
```python
import spacy
from summarizer import Summarizer

nlp = spacy.load('pl_nask')
summarizer = Summarizer(nlp_model=nlp)
```

Output dict:
```
{
    'status': str 'correct' or 'failed',
    'message': str,
    'summary': str,
    'event_id': int,
    'algorithm': str,
}
```

`alg_names` should be displayed in the dropdown

`out['message']` should be displayed in task results



| `event_id` | `message` | `status` |
|---|---|--- |
| 0 | None| `correct` |
| 1 | `Limit wyrazów jest zbyt wysoki. Utworzono podsumowanie zawierające {} wyrazów.` | `correct` |
| 2 | `Limit wyrazów jest zbyt niski. Utworzono podsumowanie zawierające {} wyrazów.` | `correct` |
| 10 | `Nie udało się przetworzyć tekstu.` | `failed` |
| 11 | `Przesłano zbyt krótki tekst.` | `failed` |
| 12 | `Limit liczby wyrazów jest zbyt wysoki. Nie udało się stworzyć podsumowania.` | `failed` |
| 13 | `Limit liczby wyrazów jest zbyt niski. Nie udało się stworzyć podsumowania.` | `failed` |


