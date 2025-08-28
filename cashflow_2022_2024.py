Here is the complete one-file `index.html` you can copy-paste into your computer, then upload to GitHub Pages or Netlify:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Cashflow Dashboard 2022–2024</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.3.2/papaparse.min.js"></script>
  <style>
    body { font-family: system-ui, sans-serif; margin:0; background:#f1f5f9; }
    .wrap { max-width:1200px; margin:auto; padding:24px; }
    .card { background:#fff; border-radius:12px; padding:20px; margin:12px 0; box-shadow:0 4px 16px rgba(0,0,0,.08); }
    .metrics { display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:16px; }
    .metric span { display:block; }
    .metric .label { font-size:12px; color:#64748b; text-transform:uppercase; }
    .metric .val { font-size:22px; font-weight:700; }
  </style>
</head>
<body>
<div class="wrap">
  <div class="card">
    <h2>💶 Cashflow Dashboard</h2>
    <input id="csv" type="file" accept=".csv">
    <p>Upload your cashflow CSV (with headers: Transaction Year, Income/Exp, Amount in EUR).</p>
  </div>

  <div class="card metrics">
    <div class="metric"><span class="label">Total Income</span><span class="val" id="m_income">€0,00</span></div>
    <div class="metric"><span class="label">Total Expenditure</span><span class="val" id="m_exp">€0,00</span></div>
    <div class="metric"><span class="label">Total Salary</span><span class="val" id="m_sal">€0,00</span></div>
    <div class="metric"><span class="label">Net Profit</span><span class="val" id="m_net">€0,00</span></div>
  </div>

  <div class="card"><canvas id="chart" height="120"></canvas></div>
</div>

<script>
const euro=n=>{if(!n||isNaN(n))n=0;return '€'+n.toFixed(2).replace('.',',').replace(/\B(?=(\d{3})+(?!\d))/g,'.')};
const parseAmt=v=>{if(!v)return 0;let s=(''+v).trim().replace(/\s/g,'');if(s.includes(',')&&s.lastIndexOf(',')>s.lastIndexOf('.')){s=s.replace(/\./g,'');s=s.replace(',', '.');}return parseFloat(s)||0};

let chart;
document.getElementById('csv').addEventListener('change',e=>{
  const f=e.target.files[0]; if(!f) return;
  Papa.parse(f,{header:true,skipEmptyLines:true,complete:res=>{
    const rows=res.data.map(r=>({year:+r['Transaction Year'],type:r['Income/Exp'],amt:parseAmt(r['Amount in EUR'])}));
    const inc=rows.filter(r=>r.type==='Income'||r.type==='Other Income').reduce((a,r)=>a+r.amt,0);
    const exp=rows.filter(r=>r.type==='Expenditure').reduce((a,r)=>a+Math.abs(r.amt),0);
    const sal=rows.filter(r=>r.type==='Salary').reduce((a,r)=>a+Math.abs(r.amt),0);
    const net=inc-exp-sal;
    document.getElementById('m_income').textContent=euro(inc);
    document.getElementById('m_exp').textContent=euro(exp);
    document.getElementById('m_sal').textContent=euro(sal);
    document.getElementById('m_net').textContent=euro(net);

    const years=[...new Set(rows.map(r=>r.year))].sort();
    const income=years.map(y=>rows.filter(r=>r.year===y&&(r.type==='Income'||r.type==='Other Income')).reduce((a,r)=>a+r.amt,0));
    const outgo=years.map(y=>rows.filter(r=>r.year===y&&(r.type==='Expenditure'||r.type==='Salary')).reduce((a,r)=>a+Math.abs(r.amt),0));

    if(chart) chart.destroy();
    chart=new Chart(document.getElementById('chart'),{type:'bar',data:{labels:years,datasets:[{label:'Income',data:income},{label:'Outgo',data:outgo}]},options:{responsive:true}});
  }});
});
</script>
</body>
</html>
```

Save as `index.html` on your computer. Open locally in the browser or push to GitHub Pages/Netlify for public use.
