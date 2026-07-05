<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Money Line — Trend Flip Screener</title>
<style>
  :root{
    --ink:#0b0d12; --panel:#12151d; --panel2:#181c26; --hair:#252a37;
    --text:#e8eaf0; --dim:#8b93a7; --gold:#e8b64c;
    --bull:#22c55e; --bear:#ef4444; --warn:#f59e0b;
    --mono:"JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    --sans:"Space Grotesk", "Segoe UI", system-ui, sans-serif;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:var(--ink);color:var(--text);font-family:var(--sans);min-height:100vh}
  header{display:flex;align-items:baseline;gap:28px;flex-wrap:wrap;padding:22px 28px 16px;border-bottom:1px solid var(--hair)}
  .brand{display:flex;align-items:baseline;gap:10px}
  .brand h1{font-size:20px;letter-spacing:.5px;font-weight:600}
  .brand .tick{color:var(--gold);font-family:var(--mono);font-size:20px}
  .brand small{color:var(--dim);font-size:11px;font-family:var(--mono)}
  .stats{display:flex;gap:26px;margin-left:auto;flex-wrap:wrap}
  .stat{text-align:right}
  .stat .lab{font-size:10px;letter-spacing:1.4px;color:var(--dim);text-transform:uppercase}
  .stat .val{font-family:var(--mono);font-size:18px;font-weight:600}
  .stat .val.bull{color:var(--bull)} .stat .val.bear{color:var(--bear)}
  .controls{display:flex;gap:10px;align-items:center;flex-wrap:wrap;padding:14px 28px}
  .tabs{display:flex;border:1px solid var(--hair);border-radius:8px;overflow:hidden}
  .tabs button{background:transparent;color:var(--dim);border:0;padding:8px 18px;font-family:var(--sans);font-size:13px;cursor:pointer}
  .tabs button.on{background:var(--panel2);color:var(--text)}
  .chip{border:1px solid var(--hair);background:transparent;color:var(--dim);border-radius:20px;padding:6px 14px;font-size:12px;cursor:pointer;font-family:var(--mono)}
  .chip.on-bull{border-color:var(--bull);color:var(--bull);background:rgba(34,197,94,.08)}
  .chip.on-bear{border-color:var(--bear);color:var(--bear);background:rgba(239,68,68,.08)}
  input[type=text]{background:var(--panel2);border:1px solid var(--hair);border-radius:8px;color:var(--text);padding:8px 12px;font-family:var(--mono);font-size:13px;outline:none;width:210px}
  input:focus{border-color:var(--gold)}
  .statusbar{padding:0 28px 8px;color:var(--dim);font-family:var(--mono);font-size:12px;min-height:18px}
  .wrap{padding:0 28px 24px;overflow-x:auto}
  table{width:100%;border-collapse:collapse;font-size:13px}
  thead th{font-size:10px;letter-spacing:1.3px;text-transform:uppercase;color:var(--dim);text-align:left;padding:10px 12px;border-bottom:1px solid var(--hair);cursor:pointer;user-select:none;white-space:nowrap}
  thead th.sorted{color:var(--gold)}
  tbody td{padding:12px;border-bottom:1px solid var(--hair);font-family:var(--mono);white-space:nowrap;vertical-align:middle}
  tbody tr:hover{background:var(--panel)}
  td.name{font-family:var(--sans)}
  td.name .sym{font-weight:600;font-size:14px}
  td.name .full{color:var(--dim);font-size:11px}
  .badge{display:inline-block;padding:3px 10px;border-radius:5px;font-size:11px;font-weight:700;letter-spacing:.6px;font-family:var(--mono)}
  .badge.bull{color:var(--bull);background:rgba(34,197,94,.12);border:1px solid rgba(34,197,94,.35)}
  .badge.bear{color:var(--bear);background:rgba(239,68,68,.12);border:1px solid rgba(239,68,68,.35)}
  .pct.pos{color:var(--bull)} .pct.neg{color:var(--bear)}
  .dimtxt{color:var(--dim)}
  .gauge{width:120px;height:6px;background:var(--panel2);border-radius:3px;position:relative;display:inline-block;vertical-align:middle;margin-right:8px}
  .gauge i{position:absolute;left:0;top:0;bottom:0;border-radius:3px}
  .gauge i.bull{background:linear-gradient(90deg,rgba(34,197,94,.25),var(--bull))}
  .gauge i.bear{background:linear-gradient(90deg,rgba(239,68,68,.25),var(--bear))}
  .gauge .mark{position:absolute;right:-1px;top:-3px;bottom:-3px;width:2px;background:var(--gold)}
  .near{color:var(--warn);font-weight:700}
  .fliplog{padding:0 28px 30px}
  .fliplog h2{font-size:13px;letter-spacing:1.4px;text-transform:uppercase;color:var(--dim);margin-bottom:10px}
  .fliplog .row{font-family:var(--mono);font-size:12px;color:var(--dim);padding:5px 0;border-bottom:1px solid var(--hair)}
  .fliplog .row b{color:var(--text)}
  .fliplog .g{color:var(--bull)} .fliplog .r{color:var(--bear)}
  .foot{padding:6px 28px 30px;color:var(--dim);font-size:11px;font-family:var(--mono);line-height:1.7}
  @media (max-width:760px){ header,.controls,.wrap,.statusbar,.foot,.fliplog{padding-left:14px;padding-right:14px} }
</style>
</head>
<body>

<header>
  <div class="brand">
    <span class="tick">⟋</span><h1>Money&nbsp;Line</h1><small id="brandSub">loading…</small>
  </div>
  <div class="stats">
    <div class="stat"><div class="lab">Assets</div><div class="val" id="stAssets">—</div></div>
    <div class="stat"><div class="lab">Bullish</div><div class="val bull" id="stBull">—</div></div>
    <div class="stat"><div class="lab">Bearish</div><div class="val bear" id="stBear">—</div></div>
    <div class="stat"><div class="lab">Last update</div><div class="val" id="stTime" style="font-size:13px">—</div></div>
  </div>
</header>

<div class="controls">
  <div class="tabs">
    <button id="tabCrypto" class="on">Crypto</button>
    <button id="tabStocks">Stocks</button>
    <button id="tabAll">All</button>
  </div>
  <div class="tabs" id="tfTabs">
    <button data-tf="1w" class="on">Weekly</button>
    <button data-tf="1d">Daily</button>
    <button data-tf="4h">4H</button>
  </div>
  <button class="chip" id="fBull">↑ BULLISH</button>
  <button class="chip" id="fBear">↓ BEARISH</button>
  <input type="text" id="search" placeholder="Search name, symbol…">
</div>

<div class="statusbar" id="status">Loading data…</div>

<div class="wrap">
  <table>
    <thead><tr id="headRow"></tr></thead>
    <tbody id="tbody"></tbody>
  </table>
</div>

<div class="fliplog">
  <h2>Recent flips</h2>
  <div id="flips" class="dimtxt" style="font-family:var(--mono);font-size:12px">—</div>
</div>

<div class="foot">
  Money Line = Supertrend-style ATR trailing stop (Wilder ATR, hl2) computed server-side on closed candles only.
  Data refreshes 4x daily via GitHub Actions; this page re-checks every 5 minutes. A screener, not a signal service.
</div>

<script>
const TF_LABEL={"1w":"Weekly","1d":"Daily","4h":"4H"};
let DATA=null, FLIPS=[];
let tab="crypto", tf="1w", showBull=true, showBear=true, q="";
let sortKey="sinceFlip", sortDir=-1;

const COLS=[
  ["idx","#"],["name","Asset"],["trend","Trend"],["sinceFlip","Since Flip %"],
  ["timeSince","Time Since Flip"],["flipLevel","Flip Level"],["dist","Distance to Flip"],["price","Price"]
];
const keyFn={
  trend:(s)=>s.bull?1:0, sinceFlip:(s)=>s.sinceFlip==null?-1e9:s.sinceFlip,
  timeSince:(s)=>s.flipTime?-s.flipTime:1e18, flipLevel:(s)=>s.flipLevel,
  dist:(s)=>s.dist, price:(s)=>s.price
};

function fmtPrice(p){
  if(p>=1000) return p.toLocaleString(undefined,{maximumFractionDigits:0});
  if(p>=1)    return p.toLocaleString(undefined,{minimumFractionDigits:2,maximumFractionDigits:2});
  return p.toLocaleString(undefined,{maximumFractionDigits:4});
}
function fmtSince(ts){
  if(!ts) return "—";
  let mins=Math.floor((Date.now()-ts)/60000);
  const mo=Math.floor(mins/43200); mins-=mo*43200;
  const w=Math.floor(mins/10080);  mins-=w*10080;
  const d=Math.floor(mins/1440);   mins-=d*1440;
  const hh=Math.floor(mins/60);
  const parts=[]; if(mo)parts.push(mo+"M"); if(w)parts.push(w+"W"); if(d)parts.push(d+"D"); if(hh&&!mo)parts.push(hh+"h");
  return parts.length?parts.join(" "):"<1h";
}

function renderHead(){
  const tr=document.getElementById("headRow"); tr.innerHTML="";
  for(const [k,label] of COLS){
    const th=document.createElement("th"); th.textContent=label;
    if(k===sortKey){ th.classList.add("sorted"); th.textContent=label+(sortDir<0?" ▼":" ▲"); }
    if(keyFn[k]) th.onclick=()=>{ sortDir = sortKey===k ? -sortDir : -1; sortKey=k; render(); };
    tr.appendChild(th);
  }
}

function render(){
  if(!DATA) return;
  renderHead();
  const tb=document.getElementById("tbody"); tb.innerHTML="";
  let view=DATA.assets.filter(a=>a.tf[tf]).map(a=>({a,s:a.tf[tf]}));
  if(tab!=="all") view=view.filter(v=>v.a.kind===tab);
  view=view.filter(v=>{
    if(v.s.bull&&!showBull) return false;
    if(!v.s.bull&&!showBear) return false;
    if(q&&!(v.a.sym.toLowerCase().includes(q)||v.a.name.toLowerCase().includes(q))) return false;
    return true;
  });
  const kf=keyFn[sortKey];
  if(kf) view.sort((x,y)=>sortDir*((kf(x.s)>kf(y.s))?1:(kf(x.s)<kf(y.s))?-1:0));

  const inTab=DATA.assets.filter(a=>a.tf[tf]&&(tab==="all"||a.kind===tab));
  const bulls=inTab.filter(a=>a.tf[tf].bull).length;
  document.getElementById("stAssets").textContent=inTab.length;
  document.getElementById("stBull").textContent=bulls+(inTab.length?` (${Math.round(bulls/inTab.length*100)}%)`:"");
  document.getElementById("stBear").textContent=(inTab.length-bulls)+(inTab.length?` (${Math.round((inTab.length-bulls)/inTab.length*100)}%)`:"");
  document.getElementById("brandSub").textContent=`${TF_LABEL[tf]} · ST(${DATA.params.atrLen}, ${DATA.params.mult})`;
  document.getElementById("stTime").textContent=DATA.updated;

  let i=1;
  for(const {a,s} of view){
    const pctCls=s.sinceFlip==null?"dimtxt":(s.sinceFlip>=0?"pct pos":"pct neg");
    const pctTxt=s.sinceFlip==null?"—":(s.sinceFlip>=0?"+":"")+s.sinceFlip.toFixed(0)+"%";
    const near=s.dist<3;
    const gaugeW=Math.max(4, Math.min(100, 100 - s.dist*6));
    const tr=document.createElement("tr");
    tr.innerHTML=`
      <td class="dimtxt">${i++}</td>
      <td class="name"><div class="sym">${a.sym}</div><div class="full">${a.name}</div></td>
      <td><span class="badge ${s.bull?"bull":"bear"}">${s.bull?"↑ BULLISH":"↓ BEARISH"}</span></td>
      <td class="${pctCls}">${pctTxt}</td>
      <td class="dimtxt">${fmtSince(s.flipTime)}</td>
      <td>${fmtPrice(s.flipLevel)} <span class="dimtxt">${s.bull?"↓flip":"↑flip"}</span></td>
      <td><span class="gauge"><i class="${s.bull?"bull":"bear"}" style="width:${gaugeW}%"></i><span class="mark"></span></span><span class="${near?"near":"dimtxt"}">${s.dist.toFixed(1)}% away${near?" ⚠":""}</span></td>
      <td>$${fmtPrice(s.price)}</td>`;
    tb.appendChild(tr);
  }
  if(!view.length) tb.innerHTML=`<tr><td colspan="8" class="dimtxt" style="padding:26px;text-align:center;font-family:var(--sans)">Nothing matches the current filters.</td></tr>`;

  const fl=document.getElementById("flips");
  if(FLIPS.length){
    fl.innerHTML=FLIPS.slice(0,30).map(f=>{
      const when=new Date(f.t).toUTCString().slice(5,22);
      return `<div class="row"><span class="${f.bull?"g":"r"}">${f.bull?"🟢":"🔴"}</span> <b>${f.sym}</b> flipped ${f.bull?'<span class="g">BULLISH</span>':'<span class="r">BEARISH</span>'} (${TF_LABEL[f.tf]||f.tf}) at $${fmtPrice(f.price)} — ${when} UTC</div>`;
    }).join("");
  } else fl.textContent="No flips recorded yet — the log fills as the backend detects trend changes.";

  document.getElementById("status").textContent=`Showing ${view.length} assets · ${TF_LABEL[tf]} · sorted by ${sortKey} · ⚠ = within 3% of flip level`;
}

async function loadData(){
  try{
    const r=await fetch("data.json?t="+Date.now());
    DATA=await r.json();
    try{ FLIPS=await (await fetch("flips.json?t="+Date.now())).json(); }catch(e){ FLIPS=[]; }
    if(!DATA.assets||!DATA.assets.length){
      document.getElementById("status").textContent="No data yet — run the GitHub Action once (Actions tab → Money Line refresh → Run workflow).";
      return;
    }
    render();
  }catch(e){
    document.getElementById("status").textContent="Could not load data.json — has the Action run yet?";
  }
}

const setTab=(t)=>{tab=t;for(const [id,v] of [["tabCrypto","crypto"],["tabStocks","stocks"],["tabAll","all"]])document.getElementById(id).classList.toggle("on",v===t);render();};
document.getElementById("tabCrypto").onclick=()=>setTab("crypto");
document.getElementById("tabStocks").onclick=()=>setTab("stocks");
document.getElementById("tabAll").onclick=()=>setTab("all");
document.querySelectorAll("#tfTabs button").forEach(b=>{
  b.onclick=()=>{ tf=b.dataset.tf;
    document.querySelectorAll("#tfTabs button").forEach(x=>x.classList.toggle("on",x===b));
    render(); };
});
const fB=document.getElementById("fBull"), fR=document.getElementById("fBear");
const paintChips=()=>{fB.classList.toggle("on-bull",showBull);fR.classList.toggle("on-bear",showBear);};
fB.onclick=()=>{showBull=!showBull;paintChips();render();};
fR.onclick=()=>{showBear=!showBear;paintChips();render();};
document.getElementById("search").oninput=(e)=>{q=e.target.value.trim().toLowerCase();render();};
paintChips(); loadData();
setInterval(loadData, 5*60*1000);   // re-check the static JSON every 5 minutes
</script>
</body>
</html>
