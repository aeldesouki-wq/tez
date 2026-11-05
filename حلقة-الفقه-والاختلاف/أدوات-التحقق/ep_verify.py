# -*- coding: utf-8 -*-
import json,re,sys,unicodedata,difflib
sys.path.insert(0,'.')
from ep_quotes import Q
PARTS={'A50':'2','A49':'10'}
def norm_ar(s):
    s=re.sub(r'[ً-ْٰـ]','',s)
    s=s.replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ى','ي').replace('ة','ه').replace('ٱ','ا')
    return ' '.join(re.sub(r'[^ء-ي ]',' ',s).split())
def load(book):
    return [r for r in map(json.loads,open(f'books/{book}.jsonl',encoding='utf8')) if 'fail' not in r]

def paged(recs,part=None):
    pieces=[]  # (page, text)
    for r in recs:
        if part is not None and str(r['part'])!=part: continue
        t=r['text'] or ''
        cur=r['page']
        last=0
        for m in re.finditer(r'⦗([٠-٩0-9]+)⦘',t):
            pieces.append((cur,t[last:m.start()]))
            cur=int(m.group(1).translate(str.maketrans('٠١٢٣٤٥٦٧٨٩','0123456789'))); last=m.end()
        pieces.append((cur,t[last:]))
    return pieces

def norm_en(s):
    s=unicodedata.normalize('NFKD',s)
    s=''.join(c for c in s if not unicodedata.combining(c))
    s=s.lower().replace('islande','islamic').replace('islam ic','islamic').replace('mohammedan law','muhammadan law')
    s=re.sub(r'(\w)- (\w)',r'\1\2',s)           # hyphenation breaks
    s=re.sub(r'[^a-z ]',' ',s)
    return ' '.join(s.split())
res=[]; bad=0
cache={}
for k,q in Q.items():
    if q['lang']=='ar':
        b=q['book']; recs=cache[b] if b in cache else cache.setdefault(b,load(b))
        p=q['page']; part=PARTS.get(k)
        pcs=paged(recs,part)
        nq=norm_ar(q['text'])
        on=norm_ar(' '.join(t for pg,t in pcs if pg==p))
        near=norm_ar(' '.join(t for pg,t in pcs if pg in (p,p+1)))
        ok=nq in near
        only='x'
        res.append((k,'OK' if ok else 'MISSING', 'p' if nq in on else ('span' if ok else '-')))
        if not ok: bad+=1
    else:
        f=q['book'][3:]; raw=open('or/'+f+'.txt',encoding='utf8').read()
        t=norm_en(raw); nq=norm_en(q['text'])
        anc=norm_en(q['anchor'])
        best=0; pos=None
        for m in re.finditer(re.escape(anc),t):
            w=t[max(0,m.start()-len(nq)):m.start()+len(nq)+len(nq)]
            sm=difflib.SequenceMatcher(None,nq,w,autojunk=False)
            blk=sm.find_longest_match(0,len(nq),0,len(w))
            # use ratio over best aligned window
            for off in range(max(0,m.start()-len(nq)-40)-max(0,m.start()-len(nq)), 1):
                pass
            r=sm.ratio()*len(w)/max(len(nq),1)  # approx
            cov=sum(b.size for b in sm.get_matching_blocks())/len(nq)
            if cov>best: best=cov; pos=m.start()
        ok=best>=0.93
        res.append((k,'OK' if ok else 'LOW',f'{best:.3f}'))
        if not ok: bad+=1
for r in res: print(*r)
print('bad',bad,'of',len(res))
