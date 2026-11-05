# -*- coding: utf-8 -*-
import re,json,sys
sys.path.insert(0,'.')
from ep_quotes2 import Q, DISP
from ep_tr2 import TR2
body=open('ep_body2.md',encoding='utf8').read()
app=open('ep_appendix2.md',encoding='utf8').read()
res=json.load(open(sys.argv[1]))
OUT=sys.argv[2]
AD=str.maketrans('0123456789','٠١٢٣٤٥٦٧٨٩')
used=[]
def card(m):
    kind,id=m.group(1),m.group(2); q=Q[id]; used.append(id)
    assert res[id]['st'].startswith('OK'),id
    if kind=='A':
        return f"> **بطاقة اقتباس** — {q['cite']}\n>\n> «{q['text']}»"
    t=DISP.get(id,q['text']); lead='…' if t[0].islower() else ''
    return (f"> **بطاقة اقتباس (ترجمتي)**\n>\n> <span dir=\"ltr\">{q['cite']}</span>\n>\n> {TR2[id]}\n>\n"
            f"> <span dir=\"ltr\">*Original:* “{lead}{t}”</span>")
body=re.sub(r'\{\{([AE]):([AE]\d+)\}\}',card,body)
# أرقام الترويسات وأزمنة المقاطع هندية
body='\n'.join(l.translate(AD) if (l.startswith('## ') or l.startswith('`✂`')) else l for l in body.split('\n'))
def ver(id):
    r=res[id]; q=Q[id]
    if q['lang']=='ar':
        return f"الشاملة، كتاب {q['book']}: مطابقة آلية على الصفحة المنسوبة — {r['st']}"
    return f"archive.org/{q['book'][3:] if q['book'].startswith('or:') and q['book'][3:] not in ('schachtU','gibb','hallaqU') else {'schachtU':'INTRODUCTIONISLAMICLAWSchacht','gibb':'mohammedanismanh027895mbp','hallaqU':'HallaqOriginsEvolutionIslamicLawHallaq'}[q['book'][3:]]}: تطابق {r['cov']:.3f} بعد تصحيح أخطاء OCR الواضحة"
seen=[]; [seen.append(i) for i in used if i not in seen]
rows=['| الرمز | النص الأصلي | المصدر والصفحة | التحقق |','|---|---|---|---|']
for id in seen:
    q=Q[id]; rows.append(f"| {id} | {q['text'].replace('|','/')} | {q['cite']} | {ver(id)} |")
app=app.replace('{{TABLE}}','\n'.join(rows))
body=body.replace('{{APPENDIX}}',app)
open(OUT,'w',encoding='utf8').write(body)
print(len(seen),'cards;',len(body.split()),'words')
