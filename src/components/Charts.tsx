import {useState} from 'react';
import type {Row} from './DataTable';
export function BarChart({bars,label,onChoose,selected}:{bars:{label:string;count:number}[];label:string;onChoose?:(s:string)=>void;selected?:string}){
 const max=Math.max(1,...bars.map(x=>x.count));
 return <div className="bar-chart" role="group" aria-label={label}>{bars.map(b=><div className="bar-row" key={b.label}><div className="bar-label">{onChoose?<button className={selected===b.label?'selected':''} onClick={()=>onChoose(b.label)} aria-pressed={selected===b.label}>{b.label}</button>:b.label}</div><div className="bar-track"><div className="bar-fill" style={{width:`${b.count/max*100}%`}}/></div><strong>{b.count}</strong></div>)}</div>
}
export function CrossTable({studies}:{studies:Row[]}){
 const [row,setRow]=useState('d3'),[col,setCol]=useState('d2');const dims=[['d1','D1 · Relationship'],['d2','D2 · Temporal resolution'],['d3','D3 · Target'],['d4','D4 · Method family'],['speechInformation','Speech information'],['year','Year']];
 const values=(s:Row,k:string):string[]=>Array.isArray(s[k])?s[k]:[String(s[k])];
 const rs=[...new Set(studies.flatMap(s=>values(s,row)))].sort(),cs=[...new Set(studies.flatMap(s=>values(s,col)))].sort();
 return <section><div className="filters"><label>Rows<select value={row} onChange={e=>setRow(e.target.value)}>{dims.map(([k,l])=><option value={k} key={k}>{l}</option>)}</select></label><label>Columns<select value={col} onChange={e=>setCol(e.target.value)}>{dims.map(([k,l])=><option value={k} key={k}>{l}</option>)}</select></label></div><div className="table-scroll heatmap" tabIndex={0} role="region" aria-label="Cross-dimensional study counts"><table><caption>Unique study counts · N = {studies.length} · Method families overlap</caption><thead><tr><th scope="col">{dims.find(d=>d[0]===row)?.[1]}</th>{cs.map(c=><th scope="col" key={c}>{c}</th>)}</tr></thead><tbody>{rs.map(r=><tr key={r}><th scope="row">{r}</th>{cs.map(c=>{const n=studies.filter(s=>values(s,row).includes(r)&&values(s,col).includes(c)).length;return <td key={c} style={{background:`rgba(94,127,99,${n?0.08+n/Math.max(1,studies.length)*.55:0})`}}>{n}</td>})}</tr>)}</tbody></table></div></section>
}
