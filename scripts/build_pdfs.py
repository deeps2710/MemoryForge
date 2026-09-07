"""Build the separately requested blog and one-page concept summary.

Use requirements-pdf.txt in a document-authoring environment, not the app venv.
Optional --font-dir selects LiberationSans TTFs; otherwise standard PDF fonts
are used. Markdown in docs/ is the editable writing source. No ML is rerun.
"""
import argparse
from datetime import datetime, timezone
from html import escape
import importlib.metadata
import json
from pathlib import Path
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pypdf import PdfReader, PdfWriter, Transformation
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle, Preformatted

ROOT = Path(__file__).resolve().parents[1]
W, H = A4
INK = colors.HexColor("#18382F")
LEAF = colors.HexColor("#365C44")
MUTED = colors.HexColor("#53625B")
PALE = colors.HexColor("#EDF2E8")
LINE = colors.HexColor("#CFDACE")
COMMIT = "f3ec52e60c999d60f8ea89c2f7c243eaa89c1bac"
REPO = f"https://github.com/deeps2710/MemoryForge/tree/{COMMIT}"
SOURCES = {
    "1":"https://arxiv.org/html/1706.03762v7",
    "2":"https://arxiv.org/html/2406.06484v3",
    "3":"https://arxiv.org/html/2509.26507v1",
    "4":"https://arxiv.org/html/2608.09888v1",
    "5":REPO,
    "6":"https://arxiv.org/html/2501.00663v1",
}
FONT = "Helvetica"
FONT_BOLD = "Helvetica-Bold"
BOXES = []
CHART_BOX = None


def register_fonts(directory):
    global FONT, FONT_BOLD
    if directory is None:
        return
    for suffix, file in [("","Regular"),("-Bold","Bold"),("-Italic","Italic"),("-BoldItalic","BoldItalic")]:
        pdfmetrics.registerFont(TTFont("MF" + suffix, str(directory / f"LiberationSans-{file}.ttf")))
    pdfmetrics.registerFontFamily("MF", normal="MF", bold="MF-Bold", italic="MF-Italic", boldItalic="MF-BoldItalic")
    FONT, FONT_BOLD = "MF", "MF-Bold"


def inline(text):
    text = escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*(.+?)\*", r"<i>\1</i>", text)
    def cite(match):
        prefix = "&nbsp;" if match.group(1) else ""
        return prefix + "&nbsp;".join(f'<a href="{SOURCES[n.strip()]}" color="#365C44">[{n.strip()}]</a>'
                        for n in match.group(2).split(","))
    return re.sub(r"(\s*)\[([1-6](?:,\s*[1-6])*)\]", cite, text)


def para(text, size=11, leading=None, bold=False, color=INK):
    return Paragraph(inline(text), ParagraphStyle("p", fontName=FONT_BOLD if bold else FONT,
                     fontSize=size, leading=leading or size*1.36, textColor=color, alignment=TA_LEFT,
                     spaceAfter=0, splitLongWords=False, allowWidows=0, allowOrphans=0))


def blocks(text):
    """Parse the small explicit Markdown subset used by the two source files."""
    lines = text.strip().splitlines()
    result, i = [], 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if re.match(r"^\[[1-6]\]:\s+https://", line):
            i += 1
        elif line.startswith("<!--"):
            result.append((line[4:-3].strip(), None)); i += 1
        elif line.startswith("```"):
            label, body = line[3:], []
            i += 1
            while not lines[i].startswith("```"):
                body.append(lines[i]); i += 1
            result.append((label,"\n".join(body))); i += 1
        elif line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                row = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r"[-:]+", c) for c in row):
                    rows.append(row)
                i += 1
            result.append(("table", rows))
        elif line.startswith("## "):
            result.append(("heading",line[3:])); i += 1
        elif line.startswith("# "):
            result.append(("title",line[2:])); i += 1
        else:
            body = [line]; i += 1
            while i < len(lines) and lines[i].strip() and not lines[i].startswith(("#", "|", "```", "<!--")):
                body.append(lines[i].strip()); i += 1
            result.append(("paragraph"," ".join(body)))
    return result


def table(rows, width, compact=False):
    size, leading = (9.05, 11.2) if compact else (9.6, 12.8)
    ratios = ([.275,.725] if len(rows[0]) == 2 else
              ([.23,.375,.395] if rows[0][0].startswith("Clean shots") else [.56,.15,.29]))
    content = [[para(cell, size, leading, bold=(r==0)) for cell in row] for r,row in enumerate(rows)]
    t = Table(content, colWidths=[width*r for r in ratios], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),PALE), ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("LINEBELOW",(0,0),(-1,0),.7,LINE),
        ("LINEBELOW",(0,1),(-1,-1),.35,LINE),
        ("LEFTPADDING",(0,0),(-1,-1),6), ("RIGHTPADDING",(0,0),(-1,-1),6),
        ("TOPPADDING",(0,0),(-1,-1),5), ("BOTTOMPADDING",(0,0),(-1,-1),5),
    ]))
    return t


def equation(text, width, compact=False):
    s = ParagraphStyle("code",fontName="Courier",fontSize=9.0 if compact else 10.0,leading=13 if compact else 15,textColor=INK)
    t = Table([[Preformatted(text,s)]],colWidths=[width])
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),PALE),
                          ("LEFTPADDING",(0,0),(-1,-1),9),("RIGHTPADDING",(0,0),(-1,-1),9),
                          ("TOPPADDING",(0,0),(-1,-1),9),("BOTTOMPADDING",(0,0),(-1,-1),9)]))
    return t


def place(c, obj, x, y, width, bottom, label):
    _, h = obj.wrap(width, H)
    if y-h < bottom:
        raise ValueError(f"Layout overflow on page {c.getPageNumber()} at {label[:60]}: need {bottom-(y-h):.1f} more points")
    obj.drawOn(c,x,y-h)
    BOXES.append({"page":c.getPageNumber(),"label":label[:60],"x":x,"y":y-h,"width":width,"height":h})
    return y-h


def diagram(c,x,y,width):
    h = 93
    top = y-15
    bw, gap = (width-32)/3, 16
    items = [("FROZEN ENCODER","image -> unit key"), ("WRITABLE MEMORY","key + symbol -> S, c"), ("QUERY READOUT","q + M -> scores")]
    for i,(title,body) in enumerate(items):
        bx=x+i*(bw+gap)
        c.setFillColor(PALE); c.roundRect(bx,top-54,bw,54,7,stroke=0,fill=1)
        c.setFillColor(LEAF); c.setFont(FONT_BOLD,8.4); c.drawCentredString(bx+bw/2,top-18,title)
        c.setFillColor(INK); c.setFont(FONT,9); c.drawCentredString(bx+bw/2,top-36,body)
        if i < 2:
            c.setStrokeColor(LEAF); c.line(bx+bw+3,top-27,bx+bw+gap-3,top-27)
            c.line(bx+bw+gap-6,top-24,bx+bw+gap-3,top-27)
            c.line(bx+bw+gap-6,top-30,bx+bw+gap-3,top-27)
    c.setFont(FONT,8.3); c.setFillColor(MUTED)
    c.drawString(x,y-h+5,"Keys and queries share the encoder. Only demonstrations write to memory.")
    return y-h


def flow(c, content, x, y, width, bottom, compact=False):
    global CHART_BOX
    references = False
    for kind, text in blocks(content):
        if kind in ("title","column","references","page"):
            continue
        if kind == "heading":
            references = text in ("Sources and technical ownership", "Primary sources and continuation")
            y -= 2 if compact else 6
            y = place(c, para(text,11.0 if compact else 15.0,13.4 if compact else 18,bold=True),x,y,width,bottom,text)
            y -= 4 if compact else 7
        elif kind == "paragraph":
            size = 10.0 if compact else (8.35 if references else 11.0)
            leading = 12.2 if compact else (10.5 if size < 9 else 15.0)
            y = place(c,para(text,size,leading),x,y,width,bottom,text)
            y -= 5 if compact else (4 if size < 9 else 8)
        elif kind == "table":
            y = place(c,table(text,width,compact),x,y,width,bottom,"table") - (7 if compact else 10)
        elif kind in ("equation","command"):
            y = place(c,equation(text,width,compact),x,y,width,bottom,kind) - (7 if compact else 10)
        elif kind == "diagram":
            y = diagram(c,x,y,width)
        elif kind == "chart":
            h = 211
            if y-h < bottom:
                raise ValueError("Chart does not fit")
            CHART_BOX = (c.getPageNumber()-1,x,y-h,width,h)
            y -= h+7
    return y


def base(c,page,total,summary=False):
    c.setFillColor(colors.white); c.rect(0,0,W,H,stroke=0,fill=1)
    c.setStrokeColor(LINE); c.setLineWidth(.6); c.line(36,37,W-36,37)
    c.setFillColor(MUTED); c.setFont(FONT,7.5)
    c.drawString(36,24,"MemoryForge | Evidence: 07 Sep 2026 | Codex-assisted writing; team review required")
    c.drawRightString(W-36,24,f"{page} / {total}")
    c.linkURL(REPO,(36,20,W-74,33),relative=0,thickness=0)


def make_chart(report,path):
    plt.rcParams.update({"font.family":"DejaVu Sans","font.size":9,"pdf.fonttype":42})
    fig,ax=plt.subplots(figsize=(7.3,3.1),layout="constrained")
    for conflict,color,style,label in [(0,"#365C44","-","Clean"),(1,"#9C5F30","--","1 wrong-label write"),(3,"#5962A0",":","3 wrong-label writes")]:
        rows=[r for r in report["summary"] if r["conflicts"]==conflict]
        ax.errorbar([r["shots"] for r in rows],[100*r["mean_accuracy"] for r in rows],
                    yerr=[100*r["std_accuracy_population"] for r in rows],color=color,
                    linestyle=style,marker="o",markersize=3.4,capsize=2.5,linewidth=1.5,label=label)
    ax.axhline(100/3,color="#758078",linestyle="--",linewidth=.8)
    ax.text(9.9,36,"Chance 33.33%",ha="right",fontsize=8,color="#53625B")
    ax.set(xlabel="Clean demonstrations per class",ylabel="Mean query accuracy (%)",ylim=(-4,113),xticks=[0,1,2,5,10])
    ax.spines[["top","right"]].set_visible(False)
    ax.grid(axis="y",alpha=.17)
    ax.legend(loc="upper center",bbox_to_anchor=(.5,1.19),ncol=3,frameon=False,fontsize=8)
    fig.savefig(path,format="pdf",metadata={"Title":"MemoryForge: observed mean accuracy and population standard deviation"})
    plt.close(fig)


def build_summary(output,source):
    c=canvas.Canvas(str(output),pagesize=A4,pageCompression=1)
    c.setTitle("MemoryForge - One-page concept summary"); c.setAuthor("MemoryForge")
    base(c,1,1,True)
    c.drawImage(str(ROOT/"assets/memoryforge-logo.png"),W-86,H-85,50,50,mask="auto")
    c.setFillColor(LEAF); c.setFont(FONT_BOLD,8.7); c.drawString(36,H-41,"CONCEPT BRIEF / ASSOCIATIVE MEMORY AND FAST WEIGHTS")
    c.setFillColor(INK); c.setFont(FONT_BOLD,24); c.drawString(36,H-70,"Fast-weight associative memory")
    c.setFont(FONT,10); c.setFillColor(MUTED); c.drawString(36,H-88,"MemoryForge | Learning associations without retraining")
    c.setStrokeColor(LINE); c.line(36,H-101,W-36,H-101)
    main,refs=source.split("<!-- references -->")
    main=re.sub(r"^# .+?\n\n.+?\n\n","",main, count=1, flags=re.S)
    left,right=main.split("<!-- column -->")
    cw=(W-72-18)/2
    yleft=flow(c,left,36,H-111,cw,146,True)
    yright=flow(c,right,36+cw+18,H-111,cw,146,True)
    c.setStrokeColor(LINE); c.line(36,137,W-36,137)
    c.setFillColor(LEAF); c.setFont(FONT_BOLD,8.4); c.drawString(36,124,"PRIMARY SOURCES AND CONTINUATION | citation numbers are clickable")
    entries=[text for kind,text in blocks(refs) if kind=="paragraph"]
    y=114
    for entry in entries[:2]:
        y=place(c,para(entry,8.0,9.5),36,y,cw,43,"reference")-3
    y=114
    for entry in entries[2:]:
        y=place(c,para(entry,8.0,9.5),36+cw+18,y,cw,43,"reference")-3
    c.save()
    return {"left_column_bottom":yleft,"right_column_bottom":yright}


def build_blog(output,source,scratch,report):
    global CHART_BOX
    pages=source.split("<!-- page -->")
    intermediate=scratch/"blog-typeset.pdf"
    c=canvas.Canvas(str(intermediate),pagesize=A4,pageCompression=1)
    c.setTitle("MemoryForge - Teaching a memory without retraining a network"); c.setAuthor("MemoryForge")
    labels=["THE EXPERIMENT","THE MEMORY RULE","THE EVIDENCE","THE RESEARCH CONNECTION"]
    bottoms=[]
    for i,text in enumerate(pages):
        base(c,i+1,len(pages))
        c.setFillColor(LEAF); c.setFont(FONT_BOLD,8.5); c.drawString(42,H-39,f"MEMORYFORGE / {labels[i]}")
        if i==0:
            c.drawImage(str(ROOT/"assets/memoryforge-logo.png"),W-100,H-110,57,57,mask="auto")
            y=place(c,para("Teaching a memory without retraining a network",26,29,bold=True),42,H-55,W-147,50,"title")
            text=re.sub(r"^\s*# .+?\n\n.+?\n\n","",text,count=1,flags=re.S)
            y-=10
        else:
            c.setStrokeColor(LINE); c.line(42,H-49,W-42,H-49)
            y=H-64
        bottoms.append(flow(c,text,42,y,W-84,48))
        c.showPage()
    c.save()
    chart=scratch/"evidence-chart.pdf"
    make_chart(report,chart)
    writer=PdfWriter(clone_from=intermediate)
    page_index,x,y,w,h=CHART_BOX
    chart_reader=PdfReader(chart)
    cp=chart_reader.pages[0]
    transform=Transformation().scale(w/float(cp.mediabox.width),h/float(cp.mediabox.height)).translate(x,y)
    writer.pages[page_index].merge_transformed_page(cp,transform)
    with output.open("wb") as stream:
        writer.write(stream)
    return bottoms


def check_output(path,expected_pages):
    r=PdfReader(path)
    assert len(r.pages)==expected_pages,(path,len(r.pages))
    texts=[p.extract_text() for p in r.pages]
    assert all("\ufffd" not in t and "<!--" not in t and "<br/>" not in t for t in texts)
    links=sum(1 for p in r.pages for a in p.get("/Annots",[]) if a.get_object().get("/A",{}).get("/URI"))
    words=len(re.findall(r"\b[\w]+(?:[.-][\w]+)*\b"," ".join(texts)))
    if expected_pages==1:
        assert 500<=words<=950,words
    return {"pages":len(r.pages),"words_in_extracted_pdf":words,"hyperlinks":links,"bytes":path.stat().st_size}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--font-dir",type=Path)
    parser.add_argument("--output-dir",type=Path,default=ROOT/"output/pdf")
    parser.add_argument("--scratch-dir",type=Path,default=ROOT/"tmp/pdfs")
    args=parser.parse_args()
    args.output_dir.mkdir(parents=True,exist_ok=True); args.scratch_dir.mkdir(parents=True,exist_ok=True)
    register_fonts(args.font_dir)
    report=json.loads((ROOT/"artifacts/phase3_evidence.json").read_text())
    summary=(ROOT/"docs/CONCEPT_SUMMARY.md").read_text(encoding="utf-8")
    blog=(ROOT/"docs/BLOG.md").read_text(encoding="utf-8")
    for shots in (1,2,5,10):
        for conflicts in (0,3):
            r=next(r for r in report["summary"] if r["shots"]==shots and r["conflicts"]==conflicts)
            values=np.array([row["accuracy"] for e in report["episodes"] for row in e["conditions"] if row["shots"]==shots and row["conflicts"]==conflicts])
            assert float(values.mean())==r["mean_accuracy"]
            assert float(values.std(ddof=0))==r["std_accuracy_population"]
            assert f'{100*r["mean_accuracy"]:.2f}% +/- {100*r["std_accuracy_population"]:.2f} pp' in blog
    concept_path=args.output_dir/"MemoryForge_Concept_Summary.pdf"
    blog_path=args.output_dir/"MemoryForge_Blog.pdf"
    summary_layout=build_summary(concept_path,summary)
    blog_bottoms=build_blog(blog_path,blog,args.scratch_dir,report)
    result={"created_at_utc":datetime.now(timezone.utc).isoformat(),"implementation_commit":COMMIT,
            "phase4_started":False,"font":FONT,"concept_summary":check_output(concept_path,1),
            "blog":check_output(blog_path,4),"summary_layout":summary_layout,"blog_content_bottoms":blog_bottoms,
            "chart_source":"artifacts/phase3_evidence.json","chart_is_vector":True,
            "packages":{n:importlib.metadata.version(n) for n in ("reportlab","matplotlib","pypdf")},
            "visual_review":"pending rendered-page inspection"}
    (args.scratch_dir/"build_check.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()
