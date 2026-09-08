// Editable DataForge deck. Authoring runtime and evidence: docs/PRESENTATION.md.
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createRequire} from 'node:module';
const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const MODULES=process.env.ARTIFACT_NODE_MODULES,SKILL=process.env.PRESENTATIONS_SKILL_DIR,PYTHON=process.env.ARTIFACT_PYTHON;
if(!MODULES||!SKILL||!PYTHON)throw Error('Set ARTIFACT_NODE_MODULES, PRESENTATIONS_SKILL_DIR and ARTIFACT_PYTHON.');
process.env.RUNTIME_NODE_MODULES=MODULES;process.env.RUNTIME_NODE=process.execPath;process.env.RUNTIME_PYTHON=PYTHON;
const {Presentation,PresentationFile,FileBlob}=await import(pathToFileURL(createRequire(import.meta.url).resolve('@oai/artifact-tool',{paths:[MODULES]})).href);
const {finalizePresentation,applyPresentationChartFont}=await import(pathToFileURL(path.join(SKILL,'container_tools/artifact_tool_utils.mjs')).href);
const TMP=path.join(ROOT,'.local/redesign'),rev=process.env.DECK_REVISION||'r1';
await fs.mkdir(path.join(TMP,'final'),{recursive:true});await fs.mkdir(path.join(TMP,'slides'),{recursive:true});
const finalPath=path.join(TMP,'final',`MemoryForge_DataForge2026_Presentation_${rev}.pptx`);
const P=Presentation.create({slideSize:{width:1280,height:720}});
const C={bg:'#F5F3E9',ink:'#173E35',body:'#263F35',muted:'#586754',sage:'#DDE5D0',green:'#456C4C',amber:'#996027',white:'#FFFFFF',line:'#B9C7AE'};
const FONT='Arial';const REF='https://github.com/deeps2710/MemoryForge/blob/3751264ac4eef1c5561692e67999c1d639ec658f/';
let number=0;
function tx(s,t,x,y,w,h,size=29,color=C.body,bold=false,align='left'){
 const q=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});q.text=t;q.text.style={typeface:FONT,fontSize:size,color,bold,alignment:align,verticalAlignment:'top',autoFit:'none',insets:{top:0,left:0,bottom:0,right:0}};return q;
}
function rect(s,x,y,w,h,fill=C.sage){return s.shapes.add({geometry:'rect',position:{left:x,top:y,width:w,height:h},fill,line:{fill:'none',width:0}});}
function base(title,notes,foot='',dark=false){const s=P.slides.add();number++;s.background.fill=dark?C.ink:C.bg;if(title)tx(s,title,60,49,1160,70,43,dark?C.white:C.ink,true);tx(s,`MemoryForge  /  DataForge 2026                                      ${String(number).padStart(2,'0')}`,60,680,1150,24,20,dark?C.sage:C.muted);if(foot)tx(s,foot,60,627,1160,42,20,dark?C.sage:C.muted);s.speakerNotes.textFrame.setText(notes);return s;}
async function img(s,f,x,y,w,h,alt){s.images.add({blob:new Uint8Array(await fs.readFile(path.join(ROOT,f))),contentType:'image/png',position:{left:x,top:y,width:w,height:h},fit:'contain',alt});}
function block(s,title,body,x,y,w,size=28){tx(s,title,x,y,w,44,30,C.ink,true);tx(s,body,x,y+48,w,number===9?260:(number===5?(y>480?80:110):(number===7&&y>480?80:150)),size);}
function box(s,id,t,x,y,w,h=95,color=C.sage){const q=rect(s,x,y,w,h,color);q.name=id;q.text=t;q.text.style={typeface:FONT,fontSize:26,color:C.ink,alignment:'center',verticalAlignment:'middle',insets:{top:10,bottom:10,left:10,right:10},autoFit:'none'};return q;}
function arrow(s,a,b,from='right',to='left'){s.shapes.connect(a,b,{kind:'straight',fromSide:from,toSide:to,line:{fill:C.green,width:2},tail:{type:'triangle',width:'med',length:'med'}});}
// 1. User-directed cover hierarchy, with newly assigned responsibilities.
let s=base('', 'Team names and contacts supplied by the user. The user authorized role allocation for this submission on 2026-09-08. See docs/TEAM.md. Assigned roles do not certify completed contribution history. Original supplied logo retained.');
tx(s,'DataForge 2026',60,44,1070,61,43,C.green,true);
tx(s,'MemoryForge',60,132,1000,113,86,C.ink,true);
tx(s,'Associative Memory & Fast Weights',64,262,1100,55,37,C.body);
tx(s,'PS-1 — Pathway Track',65,327,1070,47,31,C.green);
tx(s,'Team BitWise',65,408,700,46,33,C.ink,true);
tx(s,'MEMBER',65,480,430,27,19,C.muted,true);tx(s,'ASSIGNED RESPONSIBILITIES',550,480,665,27,19,C.muted,true);
tx(s,'Ved Patel',65,523,430,52,31,C.ink,true);tx(s,'ML engineering, application development,\nevaluation',550,520,665,65,27);
tx(s,'Deepshikha Rani',65,602,430,51,31,C.ink,true);tx(s,'Research, technical writing, presentation',550,604,665,46,27);
await img(s,'assets/memoryforge-logo.png',1075,141,145,145,'MemoryForge supplied logo');
// 2. Problem, solution, stage and measured distinction.
s=base('Learning an association without retraining',`Sources: ${REF}src/encoder.py, ${REF}src/lab.py, ${REF}artifacts/phase4_deployment.json. Public app inspected again on 2026-09-08 and shows the same preset. Screenshot captured earlier that date. Memory delta is Frobenius distance from the empty retrieval matrix. No claim of novel visual categories or learner outcomes.`, 'Working CPU prototype. Seed 1000 preset: 3 writes and 23/30 fixed queries correct.');
tx(s,'The problem',60,143,360,40,29,C.ink,true);tx(s,'A changed prediction does not\nshow what the model learned.\nMemoryForge exposes the\nstate that changed.',60,190,405,158,28);
tx(s,'Encoder parameter delta',60,382,395,35,26,C.ink);tx(s,'0',60,423,370,71,67,C.green,true);
tx(s,'Fast-memory delta',60,505,395,34,26,C.ink);tx(s,'1.73205 > 0',60,543,410,71,53,C.amber,true);
await img(s,'assets/screenshots/guided-lab.png',472,164,748,421,'Actual preset: frozen encoder audit, nonzero fast memory, taught symbols and held-out prediction');
// 3. Equations verified against code.
s=base('The write rule and the retrieval rule',`Source of truth: ${REF}src/fast_memory.py (_sums, _counts, _matrix, query). The toy uses class-wise averages of additive Hebbian sums, not direct additive updates to its displayed M. M rows are not renormalized. query computes row-major Q @ M.T. Only written labels can win. Exact ties use first index, flagged.`, 'Empty memory abstains. Scores are similarities, not calibrated probabilities.');
tx(s,'WRITE A DEMONSTRATION',60,152,660,32,22,C.green,true);
tx(s,'S ← S + v kᵀ',60,203,640,63,45,C.ink,true);tx(s,'c ← c + v',60,274,640,61,43,C.ink,true);
tx(s,'M[i] = S[i] / c[i]',60,355,640,60,41,C.ink,true);tx(s,'Zero row when c[i] = 0',62,419,640,40,26,C.muted);
tx(s,'READ A QUERY',60,490,640,31,22,C.green,true);tx(s,'scores = Mq',60,532,640,64,45,C.ink,true);
block(s,'What the symbols mean','k and q: unit 16-D embeddings\nv: one-hot temporary label\nS: key sums, c: write counts',760,154,461,28);
block(s,'What changes','S and c change when taught.\nM holds one mean per label.\nEncoder tensors remain fixed.',760,381,461,28);
// 4. Actual architecture and stack.
s=base('Architecture of the working prototype',`Sources: ${REF}app.py, ${REF}src/data.py, ${REF}src/training.py, ${REF}src/lab.py. 1797 rows split 1347/450 using seed42. Encoder64-32-16 + 10-class head, trained100epochs. Classifier head is training/sanity only. Cache stores frozen encoder, heldout keys and original tensor snapshots. Each browser has its own LabSession. All image data are bundled scikit-learn digits.`, 'No model API or database. Session reload clears memory. Detailed DFD: docs/DATA_FLOW.md.');
tx(s,'Offline preparation',60,144,1160,37,28,C.green,true);
let a=box(s,'train','1,347 training images',60,200,337),b=box(s,'learn','Train 64–32–16 encoder',471,200,337),c=box(s,'checkpoint','Save checkpoint + freeze',882,200,338);arrow(s,a,b);arrow(s,b,c);
tx(s,'Runtime on CPU: 450 held-out images',60,333,1160,37,28,C.green,true);
a=box(s,'heldout','Disjoint supports\nand queries',60,392,247,109);b=box(s,'embed','Frozen encoder\nunit embeddings',364,392,247,109);c=box(s,'memory','Session memory\nS, c and Mq',670,392,247,109);let d=box(s,'ui','Streamlit UI\naudit + feedback',974,392,246,109);arrow(s,a,b);arrow(s,b,c);arrow(s,c,d);
tx(s,'Python 3.12 / PyTorch / scikit-learn / NumPy / Streamlit / Plotly',60,549,1160,47,28,C.ink,true);
// 5. Prototype actions and features.
s=base('A learner can inspect each state change',`Sources: ${REF}src/ui.py and ${REF}src/lab.py. Actual screenshot after Teach to2shots/class,6writes27/30. Query advances through fixed30images without write. Clear zeros memory and abstains. Features also include0-10shot slider, saved research/evidence and3-question60-second check. No user learning study has been run.`, 'Guided lab, Playground, sourced research, and a 60-second concept check are implemented.');
await img(s,'assets/screenshots/memory-and-retrieval.png',60,158,775,436,'Actual fast-memory matrix and similarity scores after teaching two supports per class');
block(s,'1  Teach','Add one support per class.\nS, c and M update.',875,166,347,28);
block(s,'2  Test Query','Read Mq on a held-out image.\nMemory stays unchanged.',875,327,347,28);
block(s,'3  Clear Memory','Zero the memory.\nThe predictor abstains.',875,493,347,28);
// 6. Native measured evidence chart.
const report=JSON.parse(await fs.readFile(path.join(ROOT,'artifacts/phase3_evidence.json'),'utf8'));
const shots=[1,2,5,10],series=[0,3].map(n=>({name:n?'3 wrong-label writes':'Clean',values:shots.map(k=>Number((report.summary.find(r=>r.shots===k&&r.conflicts===n).mean_accuracy*100).toFixed(2))),fill:n?C.amber:C.green,valuesFormatCode:'0.0'}));
s=base('More support reduces average conflict damage',`Source: ${REF}artifacts/phase3_evidence.json. Developer-produced paired suite:50seeds1000-1049,0/1/2/5/10shots;0/1/3wrongwrites atnonzero shots.650conditions19500outcomes. Bar values rounded0.01percentage point, labels0.1. Clean means94.07,95.67,96.93,98.07. Corrupt3means84.47,86.87,94.20,97.27. Clean-minus-corrupt gaps9.60,8.80,2.73,0.80pp. Fixed corruption count means different noise fractions. No independent replication.`, 'Developer evaluation. Shared images and unequal corruption fractions limit the comparison.');
tx(s,'Mean query accuracy (%)',64,143,750,38,26,C.ink,true);
const ch=s.charts.add('bar',{position:{left:53,top:203,width:771,height:384},categories:shots.map(x=>`${x} shot${x>1?'s':''}`),series,barOptions:{direction:'column',grouping:'clustered',gapWidth:115},hasLegend:true,legend:{position:'bottom',textStyle:{fontSize:23,typeface:FONT}},xAxis:{textStyle:{fontSize:24,typeface:FONT}},yAxis:{min:0,max:100,majorUnit:20,numberFormatCode:'0',textStyle:{fontSize:23,typeface:FONT}},dataLabels:{showValue:true,position:'outEnd',textStyle:{fontSize:22,typeface:FONT}},chartFill:C.bg,plotAreaFill:C.bg});applyPresentationChartFont(ch,{fontFamily:FONT});
block(s,'50 fixed seeds','650 conditions\n19,500 query outcomes\nEncoder delta = 0 throughout',874,165,348,27);
block(s,'A limit worth testing','More shots can hurt one seed.\nNo novel-category or\nconcurrent-load evaluation.',874,402,348,27);
// 7. Failure analysis using real screenshot.
s=base('A wrong label changes the answer',`Sources: ${REF}artifacts/phase2_demo.json, ${REF}artifacts/phase4_deployment.json, ${REF}src/lab.py. Conflict appends first taught digit1key toBETA, whiletrueALPHAunchanged. At2shots/class6writes27/30; conflict7writes26/30. Five predictions change, netonefewer correct. It can improve or worsen a different seed. Reset actually zeros S,c. Screenshot is the actual UI warning and measured outcomes.`, 'Seed 1000, the same 30 queries. One mislabeled write; the original ground truth is preserved.');
await img(s,'assets/screenshots/conflict-outcome.png',60,168,773,435,'Actual wrong-label write and measured accuracy/prediction changes');
tx(s,'27/30 → 26/30',870,166,350,68,42,C.amber,true);tx(s,'correct after the conflict',872,232,348,42,26,C.body);
block(s,'5 predictions change','The mean for BETA now\nincludes an ALPHA key.',872,330,348,28);
block(s,'The lesson','A writable memory also\naccepts contradictory input.',872,497,348,28);
// 8. Research boundaries and PS-1 connection.
s=base('The research connection is about changing state',`Primary sources, rechecked2026-09-08: BDH https://arxiv.org/html/2509.26507v1 §§1.2,2.2; CQ https://arxiv.org/html/2608.09888v1 §§3.2-3.3; DeltaNet https://arxiv.org/html/2406.06484v3 §§2.1-2.2; Titans https://arxiv.org/html/2501.00663v1 §3. Published mechanisms only. MemoryForge implements none of these architectures. User-specified PS-1/Pathway; organizer audited docs/SUBMISSION_INSTRUCTIONS_AUDIT.md.`, 'PS-1 / Pathway: a real state-changing experiment, inspectable evidence, and sourced BDH explanation.');
block(s,'BDH [1]','Fixed connections coexist with\nHebbian synaptic state.\nThis motivates the teaching distinction.',60,157,545,28);
block(s,'BDH-CQ [2]','Context memory feeds an iterative\nquery workspace. Exact updates\nand dimensions remain proprietary.',675,157,545,28);
block(s,'Alternative update rules','DeltaNet [3]: retrieval-error correction.\nTitans [4]: neural memory optimized\nat test time.',60,387,545,28);
block(s,'MemoryForge’s boundary','Class-mean label memory only.\nNo BDH graph or CQ workspace.\nNo claim of general reasoning.',675,387,545,28);
tx(s,'[1] 2509.26507v1   [2] 2608.09888v1   [3] 2406.06484v3   [4] 2501.00663v1',60,583,1160,32,22,C.muted);
// 9. Honest future, scale and sustainability.
s=base('What it can support, and what needs validation',`Current core-state arithmetic is derived from src/fast_memory.py:3*16+3=51float64values=408bytes, excludingencoder,derivedM,snapshots,history,keysandPythonoverhead. Dense updates/readO(Cd) forC labels,d features. No capacity orconcurrentloadstudy. Future work and sustainability are proposals requested for this presentation, not implementation commitments or current revenue. See docs/FUTURE_SCOPE.md. No pricing, customer orpartner claim.`, 'Proposals only. No current revenue, paying users, learning-outcome study, or production-readiness claim.');
block(s,'Reuse and scale','An inspectable CPU teaching lab.\nCore S+c state: 408 bytes.\nDense reads grow with labels\nand embedding width.\nTotal app memory is larger.',60,162,351,27);
block(s,'Next experiments','Hold the noise fraction fixed.\nCompare memory update rules.\nTest unfamiliar categories.\nMeasure learner understanding\nand concurrent-session behavior.',466,162,351,27);
block(s,'Sustainability option','Keep the teaching core open.\nExplore paid workshops or\nmanaged classroom hosting.\nValidate demand and support\ncosts before offering a service.',872,162,351,27);
tx(s,'Functional prototype today',60,474,1160,43,32,C.green,true);tx(s,'Public CPU app, 124 tests passed, reproducible evidence.\nLearner outcomes and production capacity remain unmeasured.',60,527,1160,77,29);
// 10. Final thank you, as requested in the previous deck scope.
s=base('', 'Team names/contacts supplied by the user. Roles newly allocated on user authorization. MIT covers original code/docs/weights, with separate logo, dataset and dependency terms. Codex assistance disclosed. Public preset read again2026-09-08. Prototype verified, competition upload not performed.','',true);
tx(s,'DataForge 2026',60,74,1150,61,41,C.sage,true);tx(s,'THANK YOU',60,189,1150,111,83,C.white,true);
tx(s,'MemoryForge / Team BitWise',65,330,1120,57,36,C.sage);tx(s,'Ved Patel',65,438,535,45,31,C.white,true);tx(s,'Deepshikha Rani',685,438,535,45,31,C.white,true);tx(s,'ved2032patel@gmail.com',65,493,540,42,26,C.sage);tx(s,'deepshikharani297@gmail.com',685,493,540,42,26,C.sage);
tx(s,'Live demonstration: memoryforge.streamlit.app',65,581,1140,49,32,C.white);
const candidate=path.join(TMP,`candidate-${rev}.pptx`);await(await PresentationFile.exportPptx(P)).save(candidate);
await finalizePresentation({workspaceDir:ROOT,candidatePath:candidate,finalPath,pythonExecutable:PYTHON,integrityValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit'],explicitTotalSlideCount:10,requiredNativeTableOwnerSlides:[],requiredNativeChartOwnerSlides:[6],materializeLiteralChartWorkbooks:true,fontPolicy:{basis:'design',families:[FONT]},verifyArtifactToolImport:true,receiptPath:path.join(TMP,`validation-${rev}.json`)});
const final=await PresentationFile.importPptx(await FileBlob.load(finalPath));
for(let i=0;i<10;i++){const blob=await final.export({slide:final.slides.items[i],format:'png',scale:2});await fs.writeFile(path.join(TMP,'slides',`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await blob.arrayBuffer()));console.log('Rendered',i+1);}
console.log('Finalized',finalPath);
