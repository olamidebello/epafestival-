/* Community language packs: text only; no dialect wording is invented. */
(() => {
  const sources={
    adventure:'The adventure',activities:'Activities',playerSettings:'Player & settings',culturalPromise:'Our cultural promise ↗',
    install:'Install app ↗',begin:'Begin your adventure ↗',square:'Step into the square.',
    character:'Your character',designer:'Square designer',drumWorkshop:'Drum workshop',danceStudio:'Dance studio',
    playSettings:'Play settings',greet:'Greet 👋',clap:'Clap 👏',walk:'Walk / run',photo:'Save photo',
    talkSade:'Talk to Sade',talkTunde:'Talk to Tunde',talkBisi:'Talk to Bisi',
    prepareSquare:'Bring the square to life.',reset:'Reset adventure',stars:'Heritage Stars',unity:'Community Unity',
    explore:'Explore',drum:'Drum',dance:'Dance',prepare:'Prepare',workshop:'Workshop',
    terms:'Terms and Conditions',privacy:'Privacy Policy',copyright:'Copyright',
    startDrum:'Start drum challenge',startDance:'Start dance challenge',
    savePlayer:'Save player',tutorial:'How to play',exportSave:'Export save',
    solo:'Solo · device save',offline:'Offline · solo'
  };
  const selectors={adventure:'nav a[href="#adventure"]',activities:'nav a[href="#activities"]',playerSettings:'#settings',
    culturalPromise:'#about',install:'.install-nav',begin:'#start',square:'#living-town h2',character:'#wardrobe',designer:'#layout',
    drumWorkshop:'#composer',danceStudio:'#studio',playSettings:'#advanced-settings',greet:'#greet',clap:'#clap',walk:'#run',photo:'#photo',
    talkSade:'[data-neighbor="0"]',talkTunde:'[data-neighbor="1"]',talkBisi:'[data-neighbor="2"]',prepareSquare:'#adventure h2',reset:'#reset',
    explore:'[data-tab="explore"]',drum:'[data-tab="drum"]',dance:'[data-tab="dance"]',prepare:'[data-tab="prepare"]',workshop:'[data-tab="workshop"]',
    terms:'.legal-links a[href="terms.html"]',privacy:'.legal-links a[href="privacy.html"]',copyright:'.legal-links a[href="copyright.html"]',
    savePlayer:'#savesettings',tutorial:'#tutorial',exportSave:'#backup'};
  let locale='oro-ago',pack=null;
  try{locale=localStorage.getItem('epa-language')||'oro-ago';const raw=localStorage.getItem('epa-language-pack');if(raw)pack=validate(JSON.parse(raw));}catch{}
  function validate(v){
    if(!v||v.locale!=='oro-ago'||!v.strings||typeof v.strings!=='object'||Array.isArray(v.strings))throw Error('Use an Ìgbómìnà (Oro-Ago) language pack.');
    if(v.review?.status!=='approved'||typeof v.review?.reviewer!=='string'||!v.review.reviewer.trim())throw Error('A local speaker must supply their name and mark the translation reviewed before importing.');
    const strings={};for(const key of Object.keys(sources)){const s=v.strings[key];if(typeof s==='string'&&s.trim()&&s.length<=500)strings[key]=s.trim();}
    if(!Object.keys(strings).length)throw Error('The pack has no translated interface text.');
    return {locale:'oro-ago',strings,review:{status:'approved',reviewer:v.review.reviewer.slice(0,100),notes:typeof v.review.notes==='string'?v.review.notes.slice(0,500):''}};
  }
  const b=document.createElement('button');b.id='language';b.type='button';document.querySelector('nav').append(b);
  const notice=document.createElement('p');notice.id='language-notice';notice.className='language-notice';notice.setAttribute('role','status');document.querySelector('.intro').before(notice);
  function apply(){
    const active=locale==='oro-ago';b.textContent=active?'Language: Ìgbómìnà (Oro-Ago)':'Language: English';
    notice.hidden=!active;const noticeText=pack?'Ìgbómìnà (Oro-Ago) community language pack · '+Object.keys(pack.strings).length+' translated labels · unprovided text remains in English. Reviewer supplied in this local file; not independently authenticated.':'Ìgbómìnà (Oro-Ago) selected. Reviewed local-dialect wording is not yet available; English fallback is shown.';if(notice.textContent!==noticeText)notice.textContent=noticeText;
    // Do not change document lang: untranslated sections still remain English.
    document.documentElement.dataset.language=locale;
    for(const [key,selector] of Object.entries(selectors)){const el=document.querySelector(selector);if(!el)continue;const desired=active&&pack?.strings[key]?pack.strings[key]:sources[key];if(el.textContent!==desired)el.textContent=desired;}
    const play=document.querySelector('#play');if(play){const key=tab==='dance'?'startDance':'startDrum';const desired=active&&pack?.strings[key]?pack.strings[key]:sources[key];if(play.textContent!==desired)play.textContent=desired;}
  }
  b.onclick=()=>{
    modal('<p class="eyebrow">COMMUNITY LANGUAGE</p><h2>Ìgbómìnà (Oro-Ago).</h2><p>Use English now, or select the Ìgbómìnà (Oro-Ago) translation workspace. No local-dialect wording is represented as verified until a community speaker supplies and reviews it. Standard Yoruba is not silently substituted.</p><div class="world-tools"><button id="lang-en">English</button><button id="lang-oro">Ìgbómìnà (Oro-Ago) · '+(pack?'local pack':'English fallback')+'</button></div><p>Help complete the language option: download the template, fill in the local wording with a fluent Ìgbómìnà speaker from Oro-Ago, and include the reviewer’s name. Translation files stay on this device.</p><button id="lang-template">Download translation template</button><p><label>Import reviewed text pack <input type="file" id="lang-file" accept="application/json,.json"></label></p><p id="lang-result" role="status"></p><p>Approval in an imported file is supplied by that file’s author; the game does not independently authenticate the reviewer. Partial packs retain English for missing text.</p>');
    document.querySelector('#lang-en').onclick=()=>{locale='en';localStorage.setItem('epa-language',locale);document.querySelector('#modal').close();apply();};
    document.querySelector('#lang-oro').onclick=()=>{locale='oro-ago';localStorage.setItem('epa-language',locale);document.querySelector('#modal').close();apply();};
    document.querySelector('#lang-template').onclick=()=>{const data={locale:'oro-ago',displayName:'Ìgbómìnà (Oro-Ago)',review:{status:'draft',reviewer:'',notes:'Review pronunciation, tone marks and local usage with a fluent Ìgbómìnà speaker from Oro-Ago.'},sourceText:sources,strings:Object.fromEntries(Object.keys(sources).map(k=>[k,'']))};const u=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=u;a.download='epa-oro-ago-translation-template.json';a.click();setTimeout(()=>URL.revokeObjectURL(u),1000);};
    document.querySelector('#lang-file').onchange=async e=>{try{const f=e.target.files[0];if(!f||f.size>50000)throw Error('Choose a JSON pack smaller than 50 KB.');pack=validate(JSON.parse(await f.text()));localStorage.setItem('epa-language-pack',JSON.stringify(pack));locale='oro-ago';localStorage.setItem('epa-language',locale);document.querySelector('#lang-result').textContent='Loaded '+Object.keys(pack.strings).length+' community labels. Missing text uses English.';apply();}catch(error){document.querySelector('#lang-result').textContent=error.message;}};
  };
  let queued=false;new MutationObserver(()=>{if(queued)return;queued=true;queueMicrotask(()=>{queued=false;apply();});}).observe(document.querySelector('main'),{childList:true,subtree:true});
  apply();
})();
