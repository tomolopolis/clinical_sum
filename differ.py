from typing import List, Any, Callable, Tuple, Union
from itertools import zip_longest
import re
import difflib


Token = str
TokenList = List[Token]
whitespace = re.compile('\s+')
end_sentence = re.compile('[.!?]\s+')

def tokenize(s:str) -> TokenList:
    '''Split a string into tokens'''
    return whitespace.split(s)


def untokenize(ts:TokenList) -> str:
    '''Join a list of tokens into a string'''
    return ' '.join(ts)


def sentencize(s:str) -> TokenList:
    '''Split a string into a list of sentences'''
    return end_sentence.split(s)


def unsentencise(ts:TokenList) -> str:
    '''Join a list of sentences into a string'''
    return '. '.join(ts)


def html_unsentencise(ts:TokenList) -> str:
    '''Joing a list of sentences into HTML for display'''
    return ''.join(f'<p>{t}</p>' for t in ts)


def mark_text(text:str) -> str:
    return f'<span style="color: red;">{text}</span>'


def mark_span(text:TokenList) -> TokenList:
    if len(text) > 0:
        text[0] = '<span style="background: #69E2FB;">' + text[0]
        text[-1] += '</span>'
    return text


def markup_diff(a:TokenList, b:TokenList,
                mark:Callable[[TokenList], TokenList]=mark_span,
                default_mark: Callable[[TokenList], TokenList] = lambda x: x,
                isjunk:Union[None, Callable[[Token], bool]]=None) -> Tuple[TokenList, TokenList]:
    """Returns a and b with any differences processed by mark

    Junk is ignored by the differ
    """
    seqmatcher = difflib.SequenceMatcher(isjunk=isjunk, a=a, b=b, autojunk=False)
    out_a, out_b = [], []
    for tag, a0, a1, b0, b1 in seqmatcher.get_opcodes():
        markup = default_mark if tag == 'equal' else mark
        out_a += markup(a[a0:a1])
        out_b += markup(b[b0:b1])
    assert len(out_a) == len(a)
    assert len(out_b) == len(b)
    return out_a, out_b


def align_seqs(a: TokenList, b: TokenList, fill:Token='') -> Tuple[TokenList, TokenList]:
    out_a, out_b = [], []
    seqmatcher = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    for tag, a0, a1, b0, b1 in seqmatcher.get_opcodes():
        delta = (a1 - a0) - (b1 - b0)
        out_a += a[a0:a1] + [fill] * max(-delta, 0)
        out_b += b[b0:b1] + [fill] * max(delta, 0)
    assert len(out_a) == len(out_b)
    return out_a, out_b


def diff_ratio(a: str, b: str, fill:Token='',       
               isjunk:Union[None, Callable[[Token], bool]]=None) -> float:
    ratios = []
    diffs = []
    for sent_a, sent_b in zip_longest(*align_seqs(sentencize(a), sentencize(b))):
        ratios.append(difflib.SequenceMatcher(isjunk=isjunk, a=tokenize(sent_a), 
                                              b=tokenize(b), autojunk=False).ratio())
        diffs.append(difflib.SequenceMatcher(isjunk=isjunk, a=tokenize(sent_a), 
                                              b=tokenize(b), autojunk=False).get_opcodes())
    return sum(ratios) / len(ratios)


def diff_quick_ratio(a: str, b: str, fill:Token='',       
               isjunk:Union[None, Callable[[Token], bool]]=None) -> float:
    ratios = []
    for sent_a, sent_b in zip_longest(*align_seqs(sentencize(a), sentencize(b))):
        ratios.append(difflib.SequenceMatcher(isjunk=isjunk, a=tokenize(sent_a), 
                                              b=tokenize(b), autojunk=False).quick_ratio())
    return sum(ratios) / len(ratios)


def html_sidebyside(a, b):
    # Set the panel display
    out = '<div>'
    for left, right in zip_longest(a, b, fillvalue=''):
        out += f'<div style="display: inline-block; width: calc(50% - 10px)">{left}</div>'
        out += '<div style="width: 20px; display: inline-block"></div>'
        out += f'<div style="display: inline-block; width: calc(50% - 10px)">{right}</div>'
    out += '</div>'
    return out

import html
def html_diffs(a, b):
    a = html.escape(a)
    b = html.escape(b)

    out_a, out_b = [], []
    for sent_a, sent_b in zip(*align_seqs(sentencize(a), sentencize(b))):
        mark_a, mark_b = markup_diff(tokenize(sent_a), tokenize(sent_b))
        out_a.append(untokenize(mark_a))
        out_b.append(untokenize(mark_b))

    return html_sidebyside(out_a, out_b)

