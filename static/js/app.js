const store={get:(k,d=null)=>{try{return JSON.parse(localStorage.getItem(k))??d}catch{return d}},set:(k,v)=>localStorage.setItem(k,JSON.stringify(v))};
async function api(url,body){const r=await fetch(url,body===undefined?{}:{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});if(!r.ok)throw Error((await r.json()).error||'Request failed');return r.json()}
const $=s=>document.querySelector(s); const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const selected=()=>new URLSearchParams(location.search).get('id')||store.get('career');
function choose(id){store.set('career',id);store.set('route',0);location.href='/career-details?id='+encodeURIComponent(id)}
if($('#profileForm')){let form=$('#profileForm'),p=store.get('profile',{});for(const el of form.elements){if(el.name)el.type==='checkbox'?el.checked=!!p[el.name]:el.value=p[el.name]??el.value}form.onsubmit=e=>{e.preventDefault();let data={};for(const el of form.elements)if(el.name)data[el.name]=el.type==='checkbox'?el.checked:el.value;store.set('profile',data);$('#saved').textContent='Saved on this browser.'}}
