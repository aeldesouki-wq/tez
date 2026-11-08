import docx
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH as A
from docx.oxml.ns import qn
d=docx.Document('ref_default.docx')
S={s.name:s for s in d.styles}
def font(st,size=12,bold=None,italic=False):
    f=st.font; f.name='Times New Roman'; f.size=Pt(size); f.bold=bold; f.italic=italic; f.color.rgb=RGBColor(0,0,0)
    rpr=st.element.get_or_add_rPr(); rf=rpr.find(qn('w:rFonts'))
    if rf is None: rf=rpr.makeelement(qn('w:rFonts'),{}); rpr.insert(0,rf)
    for a in ('w:ascii','w:hAnsi','w:cs','w:eastAsia'): rf.set(qn(a),'Times New Roman')
    for a in ('w:asciiTheme','w:hAnsiTheme','w:cstheme','w:eastAsiaTheme'):
        if rf.get(qn(a)) is not None: del rf.attrib[qn(a)]
for n in ['Normal','Body Text','First Paragraph','Compact','Block Text']:
    st=S[n]; font(st,12); pf=st.paragraph_format
    pf.line_spacing=1.5; pf.space_after=Pt(6); pf.space_before=Pt(0)
    if n!='Compact': pf.first_line_indent=Cm(1.0); pf.alignment=A.JUSTIFY
for n,sz,al in [('Heading 1',14,A.CENTER),('Heading 2',13,A.LEFT),('Heading 3',12,A.LEFT),('Heading 4',12,A.LEFT),('Title',14,A.CENTER)]:
    st=S[n]; font(st,sz,True, italic=(n=='Heading 4')); pf=st.paragraph_format; pf.alignment=al; pf.first_line_indent=Cm(0)
    pf.space_before=Pt(12); pf.space_after=Pt(12 if n=='Heading 1' else 6); pf.line_spacing=1.5; pf.keep_with_next=True
st=S['Footnote Text']; font(st,10); pf=st.paragraph_format; pf.line_spacing=1.0; pf.space_after=Pt(2); pf.first_line_indent=Cm(0); pf.alignment=A.JUSTIFY
for n in ['Image Caption','Table Caption','Caption']:
    st=S[n]; font(st,11,True); st.paragraph_format.alignment=A.CENTER; st.paragraph_format.line_spacing=1.0
font(S['TOC Heading'],14,True)
for s in d.sections:
    s.page_width=Cm(21); s.page_height=Cm(29.7); s.left_margin=Cm(4); s.top_margin=Cm(4); s.right_margin=Cm(2.5); s.bottom_margin=Cm(2.5)
d.save('reference.docx'); print('ok')
