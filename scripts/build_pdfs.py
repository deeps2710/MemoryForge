"""Typeset the edited MemoryForge blog and exactly one-page concept briefing.

Editable writing: docs/BLOG.md and docs/CONCEPT_SUMMARY.md. No ML code is run.
Uses the separate requirements-pdf.txt environment. See docs/PDF_DELIVERY.md.
"""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
from html import escape
import json
from pathlib import Path
import re
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Table, TableStyle
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
W,H=A4
BG=colors.HexColor('#F5F3E9'); INK=colors.HexColor('#173E35')
GREEN=colors.HexColor('#456C4C'); MUTED=colors.HexColor('#586754')
SAGE=colors.HexColor('#DDE5D0'); AMBER=colors.HexColor('#996027'); LINE=colors.HexColor('#B9C7AE')
REV='3751264ac4eef1c5561692e67999c1d639ec658f'
SOURCES={'1':'https://arxiv.org/html/2509.26507v1','2':'https://arxiv.org/html/2608.09888v1','3':'https://arxiv.org/html/2406.06484v3','4':'https://arxiv.org/html/2501.00663v1','5':f'https://github.com/deeps2710/MemoryForge/tree/{REV}'}
F='Helvetica'; FB='Helvetica-Bold'; BOXES=[]

def fonts(folder):
    global F,FB
    if folder:
        for suffix in ['Regular','Bold','Italic','BoldItalic']:
            pdfmetrics.registerFont(TTFont('MF-'+suffix,str(folder/f'LiberationSans-{suffix}.ttf')))
        pdfmetrics.registerFontFamily('MF-Regular',normal='MF-Regular',bold='MF-Bold',italic='MF-Italic',boldItalic='MF-BoldItalic')
        F,FB='MF-Regular','MF-Bold'

def inline(t):
    t=escape(t).replace("&lt;br/&gt;", "<br/>").replace("&lt;-", "←").replace("k^T", "k<super>T</super>")
    t=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',t)
    t=re.sub(r'\*(.+?)\*',r'<i>\1</i>',t)
    t=re.sub(r'\[([1-5])\]',lambda m:f'<a href="{SOURCES[m[1]]}" color="#456C4C">[{m[1]}]</a>',t)
    return t

def p(t,size=11.3,bold=False,color=INK,leading=None):
    return Paragraph(inline(t),ParagraphStyle('mf',fontName=FB if bold else F,fontSize=size,leading=leading or size*1.27,textColor=color,splitLongWords=False,allowWidows=0,allowOrphans=0))

def put(c,t,x,y,w,size=11.3,bold=False,color=INK,leading=None,floor=42):
    q=p(t,size,bold,color,leading);_,h=q.wrap(w,1000)
    if y-h<floor:raise ValueError(f'Page {c.getPageNumber()} overflow by {floor-(y-h):.1f}pt: {t[:85]}')
    q.drawOn(c,x,y-h);BOXES.append({'page':c.getPageNumber(),'x':x,'top':y,'width':w,'bottom':y-h,'text':t[:65]});return y-h

def base(c,n,total,summary=False):
    c.setFillColor(BG);c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(MUTED);c.setFont(F,8.5)
    c.drawString(40,23,'MemoryForge / Team BitWise / DataForge 2026')
    c.drawRightString(W-40,23,f'{n} / {total}')
    if not summary:
        c.setFont(FB,9);c.setFillColor(GREEN);c.drawString(40,H-30,'MEMORYFORGE / ASSOCIATIVE MEMORY & FAST WEIGHTS')

def blocks(t):
    # Controlled Markdown subset: paragraphs, headings, explicit page/figure markers, fenced code.
    return re.findall(r'```(?:equation|command)\n.*?```|<!--.*?-->|(?:[^\n]+\n?)+?(?=\n\s*\n|\Z)',t.strip(),re.S)

def arrow(c,x1,y1,x2,y2):
    c.setStrokeColor(GREEN);c.setFillColor(GREEN);c.setLineWidth(1);c.line(x1,y1,x2,y2)
    q=c.beginPath();q.moveTo(x2,y2);q.lineTo(x2-5,y2+3);q.lineTo(x2-5,y2-3);q.close();c.drawPath(q,fill=1,stroke=0)

def architecture(c,x,y,w):
    bw=(w-38)/3; h=58
    for row,labels in enumerate([['1,347 training rows','Train encoder\n64-32-16 + head','Save checkpoint\nfreeze encoder'],['450 held-out rows\nsupports and queries','Frozen encoder\nunit keys and q','Session memory\nsupports write; q reads']]):
        yy=y-row*94
        for j,t in enumerate(labels):
            xx=x+j*(bw+19);c.setFillColor(SAGE);c.rect(xx,yy-h,bw,h,fill=1,stroke=0)
            put(c,t.replace('\n','<br/>'),xx+9,yy-10,bw-18,10.7,leading=13)
            if j<2:arrow(c,xx+bw+2,yy-h/2,xx+bw+17,yy-h/2)
    return y-159

def chart(c,x,y,w,report):
    h=224;left=x+36;bottom=y-h+36;pw=w-50;ph=h-77
    c.setFont(F,9);c.setFillColor(MUTED)
    for v in range(0,101,20):
        yy=bottom+ph*v/100;c.setStrokeColor(LINE);c.setLineWidth(.35);c.line(left,yy,left+pw,yy);c.drawRightString(left-7,yy-3,str(v))
    c.drawString(x,y-10,'Mean query accuracy (%)')
    c.setFillColor(GREEN);c.rect(x+200,y-11,8,8,fill=1,stroke=0);c.setFillColor(INK);c.drawString(x+213,y-10,'Clean')
    c.setFillColor(AMBER);c.rect(x+280,y-11,8,8,fill=1,stroke=0);c.setFillColor(INK);c.drawString(x+293,y-10,'3 wrong-label writes')
    for i,k in enumerate([1,2,5,10]):
        center=left+(i+.5)*pw/4
        for j,n in enumerate([0,3]):
            v=next(r['mean_accuracy']*100 for r in report['summary'] if r['shots']==k and r['conflicts']==n)
            xx=center-25+j*27;c.setFillColor(GREEN if n==0 else AMBER);c.rect(xx,bottom,23,ph*v/100,fill=1,stroke=0)
            c.setFont(FB,9);c.setFillColor(INK);c.drawCentredString(xx+11.5,bottom+ph*v/100+5,f'{v:.1f}')
        c.setFont(F,10);c.drawCentredString(center,bottom-19,f'{k} shot'+('s' if k>1 else ''))
    return y-h

def table(c,rows,x,y,w,widths=None):
    contents=[[p(str(v),10.2,bold=(i==0),leading=12.7) for v in row] for i,row in enumerate(rows)]
    t=Table(contents,colWidths=widths or [w/len(rows[0])]*len(rows[0]))
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),SAGE),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,-1),.4,LINE)]))
    _,h=t.wrap(w,1000)
    if y-h<42:raise ValueError('Table overflows')
    t.drawOn(c,x,y-h);return y-h

def flow(c,source,x,y,w,report,size=11.3,floor=43):
    for b in blocks(source):
        b=b.strip()
        if not b:continue
        if b.startswith('<!-- screenshot:'):
            name=re.search(r'screenshot:(.*?) -->',b)[1];ih=w*720/1280
            c.drawImage(str(ROOT/'assets/screenshots'/name),x,y-ih,w,ih,mask='auto');y-=ih+10
        elif b=='<!-- architecture -->':y=architecture(c,x,y,w)-8
        elif b=='<!-- chart -->':y=chart(c,x,y,w,report)-6
        elif b=='<!-- transitions -->':
            y=table(c,[['Seed 1000 state','Writes','Correct / 30'],['One support per class','3','23'],['Two supports per class','6','27'],['One wrong-label write','7','26'],['Clear Memory','0','0 (abstention)']],x,y,w,[w*.56,w*.17,w*.27])-12
        elif b=='<!-- evidence-table -->':
            rows=[['Supports / class','Clean mean +/- SD','3 wrong writes: mean +/- SD']]
            for k in [1,2,5,10]:
                rr=[next(r for r in report['summary'] if r['shots']==k and r['conflicts']==n) for n in [0,3]]
                rows.append([k]+[f"{100*r['mean_accuracy']:.2f}% +/- {100*r['std_accuracy_population']:.2f} pp" for r in rr])
            y=table(c,rows,x,y,w,[w*.23,w*.35,w*.42])-12
        elif b.startswith('```'):
            lines=b.splitlines()[1:-1];h=len(lines)*(size*1.43)+20
            if y-h<floor:raise ValueError('Equation/code overflow')
            c.setFillColor(SAGE);c.rect(x,y-h,w,h,fill=1,stroke=0)
            for i,line in enumerate(lines):put(c,line,x+11,y-9-i*size*1.43,w-22,size-.3,leading=size*1.4,floor=floor)
            y-=h+10
        elif b.startswith('<!--'):continue
        elif b.startswith('# '):y=put(c,b[2:],x,y,w,25,True,leading=28,floor=floor)-14
        elif b.startswith('## '):y=put(c,b[3:],x,y-4,w,13.3 if size<11.1 else 16,True,leading=16.5 if size<11.1 else 19,floor=floor)-7
        else:
            is_ref=bool(re.match(r'^\[[1-5]\]',b));ss=8.7 if is_ref else (10.2 if b.startswith('**Figure') else size)
            y=put(c,b.replace('\n',' '),x,y,w,ss,color=MUTED if b.startswith('**Figure') else INK,leading=ss*(1.24 if size<11.1 and not is_ref else 1.32),floor=floor)- (5 if is_ref or size<11.1 else 10)
    return y

def metadata(c,title):
    c.setTitle(title);c.setAuthor('Team BitWise: Ved Patel and Deepshikha Rani');c.setSubject('DataForge 2026 / PS-1 - Pathway / Associative Memory and Fast Weights')

def blog(output,source,report):
    c=canvas.Canvas(str(output),pagesize=A4,pageCompression=1);metadata(c,'MemoryForge - Project Blog')
    pages=source.split('<!-- page -->');assert len(pages)==6;bottoms=[]
    for i,body in enumerate(pages):
        base(c,i+1,6)
        if i==0:
            y=put(c,'MemoryForge',40,H-54,W-140,40,True,leading=44)-6
            y=put(c,'Associative Memory & Fast Weights',42,y,W-130,15,color=GREEN)-7
            y=put(c,'DataForge 2026 / PS-1 - Pathway / Team BitWise',42,y,W-84,10.3,color=MUTED)-15
            c.drawImage(str(ROOT/'assets/memoryforge-logo.png'),W-102,H-122,60,60,mask='auto')
            body=re.sub(r'^\s*# MemoryForge\s+Associative Memory & Fast Weights\s+DataForge 2026 / PS-1 - Pathway / Team BitWise\s*','',body)
        else:y=H-56
        bottoms.append(flow(c,body,42,y,W-84,report,11.3));c.showPage()
    c.save();return bottoms

def summary(output,source,report):
    c=canvas.Canvas(str(output),pagesize=A4,pageCompression=1);metadata(c,'MemoryForge - One-page Concept Summary');base(c,1,1,True)
    put(c,'MemoryForge',38,H-30,W-130,34,True,leading=39)
    put(c,'Associative Memory & Fast Weights',40,H-76,W-100,14.3,color=GREEN)
    put(c,'ONE-PAGE CONCEPT SUMMARY / DataForge 2026 / PS-1 - Pathway',40,H-99,W-80,8.9,color=MUTED)
    c.drawImage(str(ROOT/'assets/memoryforge-logo.png'),W-89,H-83,47,47,mask='auto')
    body,refs=source.split('<!-- references -->')
    body=re.sub(r'^\s*# MemoryForge\s+Associative Memory & Fast Weights\s+DataForge 2026 / PS-1 - Pathway / Team BitWise\s*','',body)
    columns=body.split('<!-- column -->');cw=(W-96)/2
    bottoms=[flow(c,col,40+i*(cw+16),H-128,cw,report,10.8,144) for i,col in enumerate(columns)]
    c.setStrokeColor(LINE);c.line(40,137,W-40,137)
    put(c,'PRIMARY SOURCES / numbered citations are clickable',40,130,W-80,8.5,True,color=GREEN)
    rr=[line for line in refs.strip().splitlines() if line.strip()]
    for x,items in [(40,rr[:3]),(40+cw+16,rr[3:])]:
        yy=114
        for item in items:yy=put(c,item,x,yy,cw,7.9,leading=9.7,floor=34)-4
    c.showPage();c.save();return bottoms

def check(file,n):
    r=PdfReader(file);assert len(r.pages)==n
    text='\n'.join(p.extract_text() or '' for p in r.pages)
    assert 'MemoryForge' in text and not any(t in text for t in ['\ufffd','<!--','```','<br/>'])
    uris=[str(a.get_object().get('/A',{}).get('/URI','')) for p in r.pages for a in p.get('/Annots',[])]
    assert all(u in uris for u in SOURCES.values())
    words=len(re.findall(r'\b[\w]+(?:[.-][\w]+)*\b',text))
    if n==1:assert 500<=words<=950,words
    return {'pages':n,'words':words,'bytes':file.stat().st_size,'sha256':sha256(file.read_bytes()).hexdigest(),'citation_targets':sorted(set(uris))}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--font-dir',type=Path);ap.add_argument('--output-dir',type=Path,default=ROOT/'output/pdf');ap.add_argument('--scratch-dir',type=Path,default=ROOT/'tmp/pdfs/redesign');ap.add_argument('--slide-render-dir',type=Path)
    args=ap.parse_args();fonts(args.font_dir);args.output_dir.mkdir(parents=True,exist_ok=True);args.scratch_dir.mkdir(parents=True,exist_ok=True)
    report=json.loads((ROOT/'artifacts/phase3_evidence.json').read_text())
    for row in report['summary']:
        values=[c['accuracy'] for e in report['episodes'] for c in e['conditions'] if c['shots']==row['shots'] and c['conflicts']==row['conflicts']]
        assert abs(sum(values)/len(values)-row['mean_accuracy'])<1e-12
    bpath=args.output_dir/'MemoryForge_Blog.pdf';spath=args.output_dir/'MemoryForge_OnePage_Summary.pdf'
    bottoms=blog(bpath,(ROOT/'docs/BLOG.md').read_text(encoding='utf-8-sig'),report)
    cols=summary(spath,(ROOT/'docs/CONCEPT_SUMMARY.md').read_text(encoding='utf-8-sig'),report)
    result={'created_at_utc':datetime.now(timezone.utc).isoformat(),'implementation_commit':REV,'font':F,'blog':check(bpath,6),'summary':check(spath,1),'blog_bottoms':bottoms,'summary_bottoms':cols,'chart':'Vector bars from actual JSON; full precision retained in evidence.','visual_review':'Pending render inspection'}
    if args.slide_render_dir:
        pp=args.output_dir/'MemoryForge_DataForge2026_Presentation.pdf';c=canvas.Canvas(str(pp),pagesize=(960,540),pageCompression=1);metadata(c,'MemoryForge - DataForge 2026 Presentation')
        for n in range(1,11):c.drawImage(str(args.slide_render_dir/f'slide-{n:02}.png'),0,0,960,540);c.showPage()
        c.save();assert len(PdfReader(pp).pages)==10
        result['presentation_pdf']={'pages':10,'sha256':sha256(pp.read_bytes()).hexdigest(),'format':'192-dpi raster companion from finalized PPTX renders; editable content is in PPTX.'}
    (args.scratch_dir/'build_check.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');(args.scratch_dir/'text_boxes.json').write_text(json.dumps(BOXES),encoding='utf-8');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
