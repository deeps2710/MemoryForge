// Requires the Codex Artifact Tool presentation runtime; see docs/PRESENTATION.md.
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createRequire} from 'node:module';
const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const MODULES=process.env.ARTIFACT_NODE_MODULES;
const SKILL=process.env.PRESENTATIONS_SKILL_DIR;
const PYTHON=process.env.ARTIFACT_PYTHON;
if(!MODULES||!SKILL||!PYTHON) throw Error('Set ARTIFACT_NODE_MODULES, PRESENTATIONS_SKILL_DIR and ARTIFACT_PYTHON.');
process.env.RUNTIME_NODE_MODULES=MODULES;
process.env.RUNTIME_NODE=process.execPath;
process.env.RUNTIME_PYTHON=PYTHON;
const {Presentation,PresentationFile,FileBlob}=await import(pathToFileURL(createRequire(import.meta.url).resolve('@oai/artifact-tool',{paths:[MODULES]})).href);
const {finalizePresentation,applyPresentationChartFont}=await import(pathToFileURL(path.join(SKILL,'container_tools/artifact_tool_utils.mjs')).href);
const TMP=path.join(ROOT,'.local/presentation-build');
await fs.mkdir(TMP,{recursive:true});
const revision=process.env.DECK_REVISION||'v1';
await fs.mkdir(path.join(TMP,'final'),{recursive:true});
const finalPath=path.join(TMP,'final',`MemoryForge_BitWise_DataForge_${revision}.pptx`);
const P=Presentation.create({slideSize:{width:1280,height:720}});
const C={bg:'#F5F5EE',ink:'#153F35',body:'#263C35',muted:'#556B61',green:'#37684B',lime:'#D5E5A9',orange:'#925528',white:'#FFFFFF',line:'#A4B8A5'};
const FONT='Arial';
const repo='https://github.com/deeps2710/MemoryForge';
const source=(p)=>`${repo}/blob/main/${p}`;
let slideNo=0;
function text(s,t,x,y,w,h,size=28,color=C.body,bold=false,align='left'){
 const q=s.shapes.add({geometry:'textbox',name:`text-${slideNo}-${s.shapes.items?.length??t.slice(0,15)}`,position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 q.text=t;q.text.style={typeface:FONT,fontSize:size,color,bold,alignment:align,verticalAlignment:'top',autoFit:'none',insets:{top:0,bottom:0,left:0,right:0}};return q;
}
function base(title,{dark=false,notes='',foot=''}={}){
 let s=P.slides.add();slideNo++;s.background.fill=dark?C.ink:C.bg;
 if(title)text(s,title,62,46,1150,64,43,dark?C.white:C.ink,true);
 text(s,`DataForge 2026   /   BitWise   /   ${String(slideNo).padStart(2,'0')}`,62,680,750,22,16,dark?C.lime:C.muted);
 if(foot)text(s,foot,62,634,1150,36,17,dark?C.lime:C.muted);
 s.speakerNotes.textFrame.setText(notes);return s;
}
async function img(s,file,x,y,w,h,alt){s.images.add({blob:new Uint8Array(await fs.readFile(path.join(ROOT,file))),contentType:'image/png',position:{left:x,top:y,width:w,height:h},fit:'contain',alt});}
function rows(s,arr,x=70,y=175,w=1130,gap=110){arr.forEach(([h,b],i)=>{text(s,h,x,y+i*gap,w,38,29,C.ink,true);text(s,b,x,y+i*gap+42,w,60,25,C.body);});}
function node(s,id,label,x,y,w=260,h=100,kind='process'){
 if(kind==='store') h+=20;
 const q=s.shapes.add({geometry:kind==='store'?'can':kind==='external'?'rect':'roundRect',name:id,position:{left:x,top:y,width:w,height:h},fill:kind==='store'?C.lime:kind==='external'?C.white:'#E7EDE1',line:{fill:C.green,width:2}});
 q.text=`${id}\n${label}`;q.text.style={typeface:FONT,fontSize:kind==='store'?22:23,color:C.ink,bold:false,alignment:'center',verticalAlignment:'middle',autoFit:'none',insets:{top:kind==='store'?30:9,left:9,right:9,bottom:7}};return q;
}
function edge(s,a,b,from='right',to='left'){return s.shapes.connect(a,b,{kind:'straight',fromSide:from,toSide:to,line:{fill:C.green,width:2},tail:{type:'triangle',width:'med',length:'med'}});}
function label(s,t,x,y,w=200,mask=false){const q=text(s,t,x,y,w,44,19,C.muted,false,'center');if(mask)q.fill=C.bg;return q;}
function table(s,vals,widths,y=175,h=365,size=24){
 const t=s.tables.add({rows:vals.length,columns:vals[0].length,left:62,top:y,width:1156,height:h,columnWidths:widths,values:vals});
 for(let r=0;r<vals.length;r++)for(let c=0;c<vals[0].length;c++){const cell=t.getCell(r,c);cell.fill=r===0?C.ink:(r%2?C.white:'#E9EEDF');cell.text.style={typeface:FONT,fontSize:size,color:r===0?C.white:C.body,bold:r===0,verticalAlignment:'middle',insets:{top:12,left:14,bottom:12,right:14}};}
 t.borders.assign({fill:C.line,width:1,style:'solid'});return t;
}
async function screenshotSlide(title,file,caption,notes){const s=base(title,{foot:caption,notes});await img(s,file,165,124,950,500,title);return s;}


function route(s,a,b,points,from,to){
 let previous=a;
 points.forEach((xy,i)=>{const bend=s.shapes.add({geometry:'rect',position:{left:xy[0]-.5,top:xy[1]-.5,width:1,height:1},fill:'none',line:{fill:'none',width:0}});s.shapes.connect(previous,bend,{kind:'straight',...(i===0?{fromSide:from}:{}),line:{fill:C.green,width:2}});previous=bend;});
 s.shapes.connect(previous,b,{kind:'straight',toSide:to,line:{fill:C.green,width:2},tail:{type:'triangle',width:'med',length:'med'}});
}
// 1
let s=base('',{dark:true,notes:'DataForge 2026, Pathway track. Team BitWise: Deepshikha Rani and Ved Patel. Team names and optional contact details supplied by the user. Logo supplied by the user, used without modifying its original PNG bytes.'});
text(s,'MemoryForge',64,172,780,110,78,C.white,true);
text(s,'Interactive learning with\nfast-weight associative memory',68,302,790,112,36,C.lime);
text(s,'DataForge 2026\nTeam BitWise',68,475,720,85,28,C.white);
text(s,'Deepshikha Rani  and  Ved Patel',68,580,790,48,27,C.white);
await img(s,'assets/memoryforge-logo.png',890,214,300,300,'User-supplied MemoryForge logo');
// 2
await screenshotSlide('New associations with unchanged encoder weights','assets/screenshots/guided-lab.png','Public app capture, seed 1000: 3 writes, encoder delta 0, prediction beside truth.',`Screenshot captured from https://memoryforge.streamlit.app/ on 2026-09-08. Original screenshot bytes included in assets/screenshots. Source: ${source('src/ui.py')}. The opening preset has 23/30 correct held-out queries.`);
// 3
s=base('DFD: offline model preparation',{foot:'Training rows update weights. Held-out rows evaluate them. Application startup never invokes this path.',notes:`Sources: ${source('src/data.py')}, ${source('src/training.py')}, ${source('scripts/train_encoder.py')}, ${source('artifacts/encoder.training.json')}. All 1797 original row IDs are stratified once with seed 42. Encoder and training-only head learn from 1347 rows. 450 held-out rows provide sanity evaluation and later episode pools, never optimizer updates.`});
let a,b,c,d,e,f;
a=node(s,'E3','Bundled digit images\nand original labels',62,160,285,110,'external');b=node(s,'P1','Normalize /16\nand stratify IDs',500,160,280,110);c=node(s,'D1','Training split\n1,347 original IDs',937,160,280,110,'store');d=node(s,'D2','Held-out split\n450 original IDs',500,448,280,110,'store');e=node(s,'P2','Train encoder + head\n100 fixed epochs',937,448,280,110);f=node(s,'D3','encoder.pt + metadata\nweights, split, fingerprint',62,448,310,110,'store');
edge(s,a,b);label(s,'Features and labels',350,158,145);edge(s,b,c);label(s,'Training partition',786,158,145);edge(s,b,d,'bottom','top');label(s,'Held-out partition',502,330,275,true);edge(s,c,e,'bottom','top');label(s,'Optimizer inputs',963,330,226,true);route(s,e,f,[[1077,594],[217,594]],'bottom','bottom');label(s,'Saved weights and training report',390,601,530);edge(s,d,e);label(s,'Sanity evaluation\n(no updates)',786,451,145);
// 4
s=base('DFD: session memory, retrieval and audit',{foot:'D6 is volatile session state. Reset zeros sums/counts. Next Query changes the cursor without a memory write.',notes:`Detailed session path: ${source('src/ui.py')} dispatch, ${source('src/lab.py')} _begin/_write_rows/_finish/state_view, ${source('src/fast_memory.py')}. Teach appends one support per class. Set shots rebuilds nested clean prefixes. Conflict appends support[0] under its next cyclic label while truth remains unchanged. Before/after actions audit exact frozen weights and query all 30 images. D6 stores S (3x16) and c (3); M is derived. D7 captures before/after snapshots, scores and measurements. Rendering cannot backpropagate into encoder weights.`});
a=node(s,'D5','Episode support/query\nkeys and true labels',62,161,287,109,'store');b=node(s,'P5','Validate action\nand select support writes',495,161,288,109);c=node(s,'D6','Session fast memory\nS, c and derived M',931,161,287,109,'store');d=node(s,'P7','Audit exact weights\nand render feedback',62,455,287,116);e=node(s,'P6','Read Mq, choose label\ncompare with true label',495,455,288,116);f=node(s,'D7','Before/after snapshots\nand query outcomes',931,455,287,116,'store');
edge(s,a,b);label(s,'k, one-hot v',353,175,137);edge(s,b,c);label(s,'Teach / conflict\nreset / set shots',787,158,139);edge(s,c,e,'bottom','top');label(s,'Current M',815,337,140,true);edge(s,a,e,'bottom','top');label(s,'Query q and\nground truth',300,336,160,true);edge(s,e,f);label(s,'Scores and\npredictions',787,460,138);route(s,f,d,[[1074,603],[205,603]],'bottom','bottom');label(s,'Snapshots, deltas, predictions, truth',397,607,530);edge(s,e,d,'left','right');label(s,'Live result',352,480,140);
text(s,'Write: S += v kᵀ, c += v. M[i] = S[i]/c[i] if c[i]>0, else 0. Read: scores = Mq.',65,113,1144,35,22,C.orange);

// 5: real screenshots and measured interference
s=base('Memory changes, and a wrong label has a cost',{foot:'Actual public app captures, seed 1000. The query set stays fixed. Original screenshots are included in the ZIP.',notes:`Source: ${source('artifacts/phase4_deployment.json')} and ${source('src/lab.py')}. Left: after two support examples per class, 6 writes, 27/30 correct. Right: Inject Conflict writes digit 1 as BETA while true association remains ALPHA. The same 30 queries give 26/30 correct and five predictions change. Encoder delta remains zero. Reset clears S and c and abstains. Screenshot files: assets/screenshots/memory-and-retrieval.png and conflict-outcome.png.`});
await img(s,'assets/screenshots/memory-and-retrieval.png',62,159,565,318,'Live retrieval matrix and query scores after six writes');
await img(s,'assets/screenshots/conflict-outcome.png',653,159,565,318,'Measured conflict feedback with original truth preserved');
text(s,'6 writes / 27 of 30 correct',68,509,558,47,30,C.ink,true);
text(s,'7 writes / 26 of 30 correct',657,509,558,47,30,C.orange,true);
text(s,'The heatmap contains the actual matrix.\nRetrieval scores equal memory-row dot products.',68,566,554,63,23);
text(s,'Five predictions change after one wrong label.\nReset clears memory and restores abstention.',657,566,554,63,23);
// 6: native evidence chart and research distinctions
const evidence=JSON.parse(await fs.readFile(path.join(ROOT,'artifacts/phase3_evidence.json'),'utf8'));
const shots=[1,2,5,10];const series=[0,3].map(n=>({name:n===0?'Clean':'3 wrong-label writes',values:shots.map(k=>Number((evidence.summary.find(r=>r.shots===k&&r.conflicts===n).mean_accuracy*100).toFixed(2))),valuesFormatCode:'0.0',fill:n===0?C.green:C.orange}));
s=base('Measured evidence and the research connection',{foot:'Local developer evaluation, 50 fixed seeds. Papers: BDH 2509.26507v1; CQ 2608.09888v1; DeltaNet 2406.06484v3; Titans 2501.00663v1.',notes:`Source: ${source('artifacts/phase3_evidence.json')}. Native chart uses rounded mean accuracy percentages at 1,2,5,10 shots, conflicts 0 or 3. Query sets are paired within each seed. 650 total conditions and 19,500 outcomes share images; no independent evaluation claim. Primary citations adjacent to slide claims: BDH https://arxiv.org/html/2509.26507v1 §§1.2–1.3,2.2,3; CQ https://arxiv.org/html/2608.09888v1 §§3.1–3.3; DeltaNet https://arxiv.org/html/2406.06484v3 §§2.1–2.2,3; Titans https://arxiv.org/html/2501.00663v1 §§3.1–3.3. CQ exact updates/dimensions remain proprietary. This toy implements neither BDH nor CQ. No architecture accuracy ranking or external reproduction.`});
text(s,'Mean query accuracy (%)',65,139,610,45,26,C.ink,true);
const chart=s.charts.add('bar',{position:{left:60,top:193,width:625,height:342},categories:shots.map(n=>`${n} shots`),series,barOptions:{direction:'column',grouping:'clustered',gapWidth:110},hasLegend:true,legend:{position:'bottom',textStyle:{fontSize:19,typeface:FONT}},xAxis:{textStyle:{fontSize:19,typeface:FONT}},yAxis:{min:0,max:100,majorUnit:20,numberFormatCode:'0',textStyle:{fontSize:18,typeface:FONT}},dataLabels:{showValue:true,position:'outEnd',textStyle:{fontSize:16,typeface:FONT}},chartFill:C.bg,plotAreaFill:C.bg});applyPresentationChartFont(chart,{fontFamily:FONT});
text(s,'650 conditions / 19,500 query outcomes\nEncoder delta = 0 throughout\nShared images limit statistical inference.',70,546,609,86,24);
text(s,'BDH [2025]',728,147,480,33,25,C.ink,true);text(s,'Fixed connections, dynamic Hebbian state.\nThe lab isolates that state distinction.',728,183,480,67,23);
text(s,'BDH-CQ [2026]',728,269,480,33,25,C.ink,true);text(s,'Context memory plus iterative workspace.\nWorkspace details remain proprietary.',728,305,480,67,23);
text(s,'DeltaNet [2024] / Titans [2024–25]',728,390,480,36,24,C.ink,true);text(s,'DeltaNet uses retrieval-and-correction.\nTitans optimizes neural memory at test time.',728,431,480,73,23);
text(s,'MemoryForge uses supervised class means.\nIt implements neither BDH nor CQ reasoning.',728,550,480,76,24,C.orange);
// 7: evidence, operation and honest scope
s=base('Deployment, reproducibility and limits',{notes:`Sources: ${source('artifacts/phase4_final_robustness.json')}, ${source('artifacts/phase4_deployment.json')}, ${source('docs/LIMITATIONS.md')}. 124 tests passed on final Windows Python 3.12 configuration. Independent fresh retraining matches checkpoint tensors and full numerical Phase 1 report. Cloud Linux received install/browser verification. One measurement/action includes automation and network overhead. 130 seconds is an upper bound covering fresh provisioning and dependencies. No learner study or concurrent load study. User-provided team names/contacts do not establish role division or completed technical defense.`});
rows(s,[['124 tests pass','Exact checkpoint regeneration and numerical core replay support reproducibility.'],['Public CPU application','Python 3.12.14. Observed actions: 952–1,017 ms. Fresh rebuild: within 130 seconds.'],['The claim stays narrow','Pretrained digit identities, temporary symbols, simple memory and overlapping episodes.'],['Team ownership','Codex assisted code and writing. BitWise must explain and defend the implementation.']],70,146,1135,109);
text(s,'Live: memoryforge.streamlit.app     Source: github.com/deeps2710/MemoryForge',70,602,1135,37,25,C.green,true);
// 8: final THANK YOU slide
s=base('',{dark:true,notes:'DataForge 2026, Team BitWise. Deepshikha Rani and Ved Patel. The user supplied both names and email addresses and authorized optional inclusion in this presentation and its submission ZIP. Scoped MIT applies to original project code/docs/weights; logo and third-party notices remain separate. See docs/AI_ASSISTANCE.md and docs/PROVENANCE.md.'});
text(s,'THANK YOU',65,139,1150,115,84,C.white,true);
text(s,'DataForge 2026 / Team BitWise',70,289,1120,59,37,C.lime);
text(s,'Deepshikha Rani',70,409,565,45,30,C.white,true);text(s,'deepshikharani297@gmail.com',70,463,565,45,25,C.lime);
text(s,'Ved Patel',720,409,490,45,30,C.white,true);text(s,'ved2032patel@gmail.com',720,463,490,45,25,C.lime);
text(s,'Questions and live demonstration',70,587,1130,51,30,C.white);
await fs.writeFile(path.join(TMP,'presentation.json'),JSON.stringify(P.toProto()));
const candidate=path.join(TMP,`candidate-${revision}.pptx`);
await (await PresentationFile.exportPptx(P)).save(candidate);
console.log('Exported candidate',candidate);
await finalizePresentation({workspaceDir:ROOT,candidatePath:candidate,finalPath,pythonExecutable:PYTHON,integrityValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit',],explicitTotalSlideCount:8,requiredNativeTableOwnerSlides:[],requiredNativeChartOwnerSlides:[6],materializeLiteralChartWorkbooks:true,fontPolicy:{basis:'design',families:[FONT]},verifyArtifactToolImport:true,receiptPath:path.join(TMP,`validation-${revision}.json`)});
console.log('Finalized',finalPath);
const rendered=await PresentationFile.importPptx(await FileBlob.load(finalPath));
for(let i=0;i<rendered.slides.items.length;i++){
 const slide=rendered.slides.items[i];const blob=await rendered.export({slide,format:'png',scale:1});
 await fs.writeFile(path.join(TMP,`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await blob.arrayBuffer()));
 console.log('Rendered',i+1);
}
