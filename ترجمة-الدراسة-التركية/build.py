import re,subprocess,os
B=os.path.dirname(os.path.abspath(__file__))
src=open(f'{B}/src/study.md').read().split('\n')
front='\n'.join(src[:193])   # title pages .. Arabic abstract (unchanged, already Turkish/English/Arabic)
# wrap title pages (before BEYAN) in Title Page style
i=front.index('# BEYAN')
tp=front[:i]; rest=front[i:]
PB='\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n'
k=tp.index('**T.C.**',5); tp=tp[:k]+PB+tp[k:]
k=tp.index('**[جامعة'); tp=tp[:k]+PB+tp[k:]
tp=tp.replace('**TEZ ONAY SAYFASI**',PB+'**TEZ ONAY SAYFASI**')
tp='::: {custom-style="Title Page"}\n'+tp+'\n:::\n'
parts=[]
for c in ['01','02','03','04a','04b','05','06','07']:
    t=open(f'{B}/tr/chunk_{c}.md').read()
    t=re.sub(r'<!--\s*NOTLAR.*?-->','',t,flags=re.S)
    parts.append(t.strip())
body='\n\n'.join(parts)
# place TOC after Önsöz (before KISALTMALAR)
toc='```{=openxml}\n<w:p><w:pPr><w:pStyle w:val="TOCHeading"/></w:pPr><w:r><w:t>İÇİNDEKİLER</w:t></w:r></w:p><w:p><w:r><w:fldChar w:fldCharType="begin" w:dirty="true"/></w:r><w:r><w:instrText xml:space="preserve"> TOC \\o "1-4" \\h \\z \\u </w:instrText></w:r><w:r><w:fldChar w:fldCharType="separate"/></w:r><w:r><w:t>(İçindekiler tablosunu güncellemek için sağ tıklayıp "Alanı Güncelleştir"i seçiniz.)</w:t></w:r><w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>\n```\n'
body=body.replace('# KISALTMALAR', toc+'\n# KISALTMALAR',1)
md=tp+'\n'+rest+'\n\n'+body+'\n'
open(f'{B}/build/tez_tr.md','w').write(md)
r=subprocess.run(['pandoc',f'{B}/build/tez_tr.md','-f','markdown+footnotes+pipe_tables+grid_tables+simple_tables','-o',f'{B}/build/tez_tr.docx',f'--reference-doc={B}/reference.docx',f'--resource-path={B}/build'],capture_output=True,text=True)
print(r.returncode,r.stderr[:2000])
