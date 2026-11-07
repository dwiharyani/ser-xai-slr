import {Fragment, useMemo, useState} from 'react';
export type Row = Record<string, any>;
export type Field = {key:string; label:string; split?:boolean};
const value=(v:unknown):string => v==null?'Not supplied':Array.isArray(v)?v.join('; '):typeof v==='object'?Object.entries(v).map(([k,x])=>`${k}: ${x}`).join(' · '):String(v);
export function exportCSV(rows:Row[],filename:string){
 if(!rows.length)return;const keys=Object.keys(rows[0]);
 const cell=(x:unknown)=>{let s=x==null?'':typeof x==='object'?JSON.stringify(x):String(x);if(/^[=+@-]/.test(s))s="'"+s;return '"'+s.replaceAll('"','""')+'"'};
 const blob=new Blob(['\ufeff'+[keys,...rows.map(r=>keys.map(k=>r[k]))].map(r=>r.map(cell).join(',')).join('\r\n')],{type:'text/csv;charset=utf-8'});
 const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=filename;a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);
}
export function DOI({doi}:{doi?:string}){return doi?<a href={`https://doi.org/${encodeURI(doi.replace(/^https?:\/\/doi.org\//,''))}`} target="_blank" rel="noreferrer">DOI ↗</a>:<span className="muted">Not supplied</span>}
export default function DataTable({rows,columns,filters=[],name,detailKeys}:{rows:Row[];columns:Field[];filters?:Field[];name:string;detailKeys?:Field[]}){
 const [query,setQuery]=useState(''),[chosen,setChosen]=useState<Record<string,string>>({}),[sort,setSort]=useState({key:'id',asc:true}),[page,setPage]=useState(0),[size,setSize]=useState(20);
 const options=useMemo(()=>Object.fromEntries(filters.map(f=>[f.key,[...new Set(rows.flatMap(r=>Array.isArray(r[f.key])?r[f.key]:f.split?String(r[f.key]??'Not supplied').split(';').map(x=>x.trim()):[value(r[f.key])]))].sort()])),[rows,filters]);
 const result=useMemo(()=>rows.filter(r=>Object.values(r).map(value).join(' ').toLocaleLowerCase().includes(query.toLocaleLowerCase())&&Object.entries(chosen).every(([k,v])=>!v||(Array.isArray(r[k])?r[k].includes(v):filters.find(f=>f.key===k)?.split?String(r[k]??'Not supplied').split(';').map(s=>s.trim()).includes(v):value(r[k])===v))).sort((a,b)=>value(a[sort.key]).localeCompare(value(b[sort.key]),undefined,{numeric:true})*(sort.asc?1:-1)),[rows,query,chosen,sort,filters]);
 const maxPage=Math.max(0,Math.ceil(result.length/size)-1),current=Math.min(page,maxPage);
 const change=(key:string,v:string)=>{setChosen({...chosen,[key]:v});setPage(0)};
 return <div className="data-explorer">
  <div className="table-toolbar"><label className="search-label">Search {name}<input type="search" placeholder="Study ID, title, DOI or metadata…" value={query} onChange={e=>{setQuery(e.target.value);setPage(0)}}/></label><button className="outline" onClick={()=>exportCSV(result,`${name}-filtered.csv`)} disabled={!result.length}>Download filtered CSV ↓</button></div>
  <div className="filters">{filters.map(f=><label key={f.key}>{f.label}<select value={chosen[f.key]||''} onChange={e=>change(f.key,e.target.value)}><option value="">All</option>{options[f.key]?.map((v:string)=><option key={v}>{v}</option>)}</select></label>)}<button className="text-button" onClick={()=>{setChosen({});setQuery('');setPage(0)}}>Reset filters</button></div>
  <div className="table-meta"><span role="status">{result.length} of {rows.length} records</span><span>Click a heading to sort · Expand a title for details</span></div>
  <div className="table-scroll" role="region" aria-label={`${name} data table`} tabIndex={0}><table><caption className="sr-only">{name}, searchable and sortable, {result.length} matching records</caption><thead><tr>{columns.map(c=><th key={c.key} scope="col" aria-sort={sort.key===c.key?sort.asc?'ascending':'descending':'none'}><button onClick={()=>setSort({key:c.key,asc:sort.key===c.key?!sort.asc:true})}>{c.label} <span aria-hidden="true">{sort.key===c.key?(sort.asc?'↑':'↓'):'↕'}</span></button></th>)}</tr></thead><tbody>
   {result.slice(current*size,(current+1)*size).map(r=><tr key={r.id}>{columns.map(c=><td key={c.key} className={c.key==='title'?'title-cell':c.key==='id'?'id-cell':''}>{c.key==='doi'?<DOI doi={r[c.key]}/>:c.key==='title'?<details><summary>{r.title}</summary><dl className="record-details">{(detailKeys||Object.keys(r).filter(k=>k!=='title').map(k=>({key:k,label:k}))).map(f=><Fragment key={f.key}><dt>{f.label}</dt><dd>{f.key==='doi'?<DOI doi={r[f.key]}/>:value(r[f.key])}</dd></Fragment>)}</dl></details>:c.key==='state'||c.key==='fullTextState'?<span className={`badge ${String(r[c.key]).startsWith('Included')?'green':''}`}>{value(r[c.key])}</span>:value(r[c.key])}</td>)}</tr>)}
   {!result.length&&<tr><td colSpan={columns.length} className="empty">No records match these filters. Try a broader search or reset filters.</td></tr>}
  </tbody></table></div>
  <div className="pagination"><label>Rows per page <select value={size} onChange={e=>{setSize(Number(e.target.value));setPage(0)}}>{[20,50,100].map(n=><option key={n}>{n}</option>)}</select></label><div><button onClick={()=>setPage(current-1)} disabled={!current}>← Previous</button><span>Page {current+1} of {maxPage+1}</span><button onClick={()=>setPage(current+1)} disabled={current>=maxPage}>Next →</button></div></div>
 </div>
}
