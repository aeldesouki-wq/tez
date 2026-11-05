# -*- coding: utf-8 -*-
"""التحقق من سجل النسخة الثانية.
الاستعمال: python3 ep_verify2.py <مجلد صفحات الشاملة المخزَّنة> <مجلد نصوص archive.org> <ملف نتائج json>
صفحات الشاملة مخزَّنة بصيغة  <كتاب>_<معرّف>.txt  وأول سطر فيها  #رقم_الصفحة_المطبوعة|العنوان
والنصوص العربية تُقابَل بعد حذف التشكيل وتوحيد الألف والياء والتاء المربوطة، على الصفحة المنسوبة نفسها
(مع مراعاة علامات الصفحات الداخلية ⦗N⦘). النص الإنجليزي يُقابَل تقريبياً (تغطية ≥ 0.93) بعد تصحيح أخطاء OCR الواضحة.
"""
import sys,re,glob,json,difflib,unicodedata
sys.path.insert(0,'.')
from ep_quotes2 import Q
CACHE,OR,OUT=sys.argv[1:4]
AD=str.maketrans('٠١٢٣٤٥٦٧٨٩','0123456789')
def norm_ar(s):
    s=s.replace('ﷺ',' ')
    s=re.sub(r'[ً-ْٰـ]','',s)
    s=s.replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ى','ي').replace('ة','ه').replace('ٱ','ا')
    return ' '.join(re.sub(r'[^ء-ي ]',' ',s).split())
def pieces(book):
    out=[]
    for f in glob.glob(f'{CACHE}/{book}_*.txt'):
        t=open(f,encoding='utf8').read()
        m=re.match(r'#(\d+)\|[^\n]*\n',t)
        cur=int(m.group(1)); body=t[m.end():]; last=0
        for mm in re.finditer(r'⦗([٠-٩0-9]+)⦘',body):
            out.append((cur,norm_ar(body[last:mm.start()]))); cur=int(mm.group(1).translate(AD)); last=mm.end()
        out.append((cur,norm_ar(body[last:])))
    return out
def norm_en(s):
    s=unicodedata.normalize('NFKD',s); s=''.join(c for c in s if not unicodedata.combining(c))
    s=s.lower().replace('islande','islamic').replace('islam ic','islamic')
    s=re.sub(r'(\w)[-¬] (\w)',r'\1\2',s)
    s=re.sub(r'[^a-z ]',' ',s); return ' '.join(s.split())
ENF={'or:schachtU':'INTRODUCTIONISLAMICLAWSchacht','or:gibb':'gibb','or:hallaqU':'HallaqOriginsEvolutionIslamicLawHallaq',
     'or:HallaqOriginsEvolutionIslamicLawHallaq':'HallaqOriginsEvolutionIslamicLawHallaq'}
cache={}; res={}; bad=0
for k,q in sorted(Q.items()):
    if q['lang']=='ar':
        b=q['book']; pcs=cache.setdefault(b,pieces(b)); nq=norm_ar(q['text']); p=q['page']
        pages=sorted({pg for pg,t in pcs if nq in t})
        if p in pages: st='OK'
        elif any(abs(pg-p)<=1 for pg in pages):   # مقطع يمتد على حدّ صفحتين
            st='OK-span'
        else: st='MISSING'
        # مقطع يمتد عبر صفحتين متجاورتين
        if st=='MISSING':
            ps=sorted(pcs,key=lambda x:x[0]); 
            for i in range(len(ps)-1):
                if ps[i][0]==p and nq in ps[i][1]+' '+ps[i+1][1]: st='OK-span'
        res[k]=dict(st=st,pages=pages)
    else:
        f=ENF.get(q['book']); 
        try: raw=open(f'{OR}/{f}.txt',encoding='utf8').read()
        except Exception: res[k]=dict(st='NOFILE'); continue
        t=norm_en(raw); nq=norm_en(q['text']); anc=norm_en(q['anchor']); best=0
        for m in re.finditer(re.escape(anc),t):
            w=t[max(0,m.start()-len(nq)):m.start()+2*len(nq)]
            sm=difflib.SequenceMatcher(None,nq,w,autojunk=False)
            cov=sum(b.size for b in sm.get_matching_blocks())/len(nq); best=max(best,cov)
        res[k]=dict(st='OK' if best>=0.93 else 'LOW',cov=round(best,3))
    if not res[k]['st'].startswith('OK'): bad+=1
json.dump(res,open(OUT,'w'),ensure_ascii=False,indent=1)
for k,v in res.items():
    if not v['st'].startswith('OK') or k in ('A45','A57','A58','A56'): print(k,v)
print('bad',bad,'of',len(res))
