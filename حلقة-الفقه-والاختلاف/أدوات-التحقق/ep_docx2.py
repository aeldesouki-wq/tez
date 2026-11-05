# -*- coding: utf-8 -*-
"""md -> docx (عربي من اليمين إلى اليسار). الاستعمال: python3 ep_docx2.py in.md out.docx"""
import sys,subprocess,zipfile,re,shutil,os,tempfile
src,out=sys.argv[1:3]
tmp=tempfile.mkdtemp()
raw=os.path.join(tmp,'raw.docx')
subprocess.run(['pandoc',src,'-f','markdown+raw_html','-o',raw],check=True)
zin=zipfile.ZipFile(raw)
zout=zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED)
for it in zin.infolist():
    data=zin.read(it.filename)
    if it.filename=='word/document.xml':
        x=data.decode('utf8')
        # فقرات: اتجاه RTL
        def para(m):
            p=m.group(0)
            txt=''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>',p))
            ltr = ('Original:' in p) or (not re.search(r'[؀-ۿ]',txt) and re.search(r'[A-Za-z]{4}',txt) is not None)
            if '<w:pPr>' in p:
                p=p.replace('<w:pPr>','<w:pPr><w:bidi w:val="0"/>' if ltr else '<w:pPr><w:bidi/>',1)
            else:
                p=p.replace('<w:p>','<w:p><w:pPr>'+('<w:bidi w:val="0"/>' if ltr else '<w:bidi/>')+'</w:pPr>',1)
            return p
        x=re.sub(r'<w:p>.*?</w:p>|<w:p [^>]*>.*?</w:p>',para,x,flags=re.S)
        # خلايا الجداول بلا ترتيب خاص؛ جداول من اليمين
        x=x.replace('<w:tblPr>','<w:tblPr><w:bidiVisual/>')
        # الأوساط: rtl على الأجزاء العربية
        def run(m):
            r=m.group(0)
            if re.search(r'[؀-ۿ]',r) and '<w:rtl/>' not in r:
                if '<w:rPr>' in r: r=r.replace('<w:rPr>','<w:rPr><w:rtl/>',1)
                else: r=r.replace('<w:r>','<w:r><w:rPr><w:rtl/></w:rPr>',1)
            return r
        x=re.sub(r'<w:r>.*?</w:r>|<w:r [^>]*>.*?</w:r>',run,x,flags=re.S)
        data=x.encode('utf8')
    if it.filename=='word/styles.xml':
        x=data.decode('utf8')
        x=re.sub(r'<w:rPrDefault>.*?</w:rPrDefault>','<w:rPrDefault><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman" w:eastAsia="Times New Roman"/><w:sz w:val="26"/><w:szCs w:val="28"/><w:lang w:val="ar-SA" w:bidi="ar-SA"/></w:rPr></w:rPrDefault>',x,flags=re.S)
        data=x.encode('utf8')
    zout.writestr(it,data)
zout.close(); shutil.rmtree(tmp)
print('ok',out)
