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
  const languages={"yo":{"name":"Yorùbá","strings":{"adventure":"Ìrìn àjò","activities":"Àwọn ìgbòkègbodò","begin":"Bẹ̀rẹ̀ ìrìn àjò rẹ","character":"Ẹni ìṣeré rẹ","drumWorkshop":"Ilé iṣẹ́ ìlù","danceStudio":"Ilé ijó","playSettings":"Ètò ìṣeré","photo":"Ya fọ́tò","explore":"Ṣàwárí","drum":"Ìlù","dance":"Ijó","prepare":"Múra sílẹ̀","workshop":"Ilé iṣẹ́","privacy":"Ìlànà àṣírí","copyright":"Ẹ̀tọ́ àdàkọ"}},"ha":{"name":"Hausa","strings":{"adventure":"Kasada","activities":"Ayyuka","begin":"Fara kasadarka","character":"Halin wasanka","playSettings":"Saitunan wasa","greet":"Gaisuwa 👋","photo":"Ɗauki hoto","explore":"Bincika","drum":"Ganga","dance":"Rawa","prepare":"Shirya","workshop":"Bitar sana’a","tutorial":"Yadda ake wasa","privacy":"Manufar sirri","copyright":"Haƙƙin mallaka"}},"ig":{"name":"Igbo","strings":{"activities":"Ihe omume","begin":"Malite njem gị","playSettings":"Ntọala egwuregwu","greet":"Kele 👋","photo":"See foto","explore":"Nyochaa","drum":"Ịgbà","dance":"Egwu","prepare":"Kwadebe","tutorial":"Otu esi egwu egwu","privacy":"Iwu nzuzo","copyright":"Ikike nwebisiinka"}},"sw":{"name":"Kiswahili","strings":{"adventure":"Matukio","activities":"Shughuli","begin":"Anza safari yako","character":"Mhusika wako","designer":"Pamba uwanja","drumWorkshop":"Warsha ya ngoma","danceStudio":"Studio ya dansi","playSettings":"Mipangilio ya mchezo","greet":"Salimia 👋","clap":"Piga makofi 👏","photo":"Piga picha","explore":"Chunguza","drum":"Ngoma","dance":"Dansi","prepare":"Jiandae","workshop":"Warsha","tutorial":"Jinsi ya kucheza","exportSave":"Hamisha hifadhi","terms":"Sheria na masharti","privacy":"Sera ya faragha","copyright":"Hakimiliki"}},"ar":{"name":"العربية","rtl":true,"strings":{"adventure":"المغامرة","activities":"الأنشطة","begin":"ابدأ مغامرتك","character":"شخصيتك","designer":"تصميم الساحة","drumWorkshop":"ورشة الطبول","danceStudio":"استوديو الرقص","playSettings":"إعدادات اللعبة","greet":"إلقاء التحية 👋","clap":"تصفيق 👏","photo":"التقاط صورة","explore":"استكشاف","drum":"الطبول","dance":"الرقص","prepare":"الاستعداد","workshop":"الورشة","tutorial":"طريقة اللعب","exportSave":"تصدير الحفظ","terms":"الشروط والأحكام","privacy":"سياسة الخصوصية","copyright":"حقوق النشر"}},"af":{"name":"Afrikaans","strings":{"adventure":"Die avontuur","activities":"Aktiwiteite","begin":"Begin jou avontuur","character":"Jou karakter","designer":"Ontwerp die plein","drumWorkshop":"Tromwerkswinkel","danceStudio":"Dansateljee","playSettings":"Spelinstellings","greet":"Groet 👋","clap":"Klap hande 👏","photo":"Neem foto","explore":"Verken","drum":"Trom","dance":"Dans","prepare":"Berei voor","workshop":"Werkswinkel","tutorial":"Hoe om te speel","exportSave":"Voer stoorlêer uit","terms":"Bepalings en voorwaardes","privacy":"Privaatheidsbeleid","copyright":"Kopiereg"}},"fr":{"name":"Français","strings":{"adventure":"L’aventure","activities":"Activités","begin":"Commencer l’aventure","character":"Votre personnage","designer":"Décorer la place","drumWorkshop":"Atelier de percussions","danceStudio":"Studio de danse","playSettings":"Paramètres du jeu","greet":"Saluer 👋","clap":"Applaudir 👏","photo":"Prendre une photo","explore":"Explorer","drum":"Tambour","dance":"Danse","prepare":"Préparer","workshop":"Atelier","tutorial":"Comment jouer","exportSave":"Exporter la sauvegarde","terms":"Conditions générales","privacy":"Politique de confidentialité","copyright":"Droits d’auteur"}},"pt":{"name":"Português","strings":{"adventure":"A aventura","activities":"Atividades","begin":"Começar a aventura","character":"Sua personagem","designer":"Decorar a praça","drumWorkshop":"Oficina de tambores","danceStudio":"Estúdio de dança","playSettings":"Configurações do jogo","greet":"Cumprimentar 👋","clap":"Aplaudir 👏","photo":"Tirar foto","explore":"Explorar","drum":"Tambor","dance":"Dança","prepare":"Preparar","workshop":"Oficina","tutorial":"Como jogar","exportSave":"Exportar progresso","terms":"Termos e condições","privacy":"Política de privacidade","copyright":"Direitos autorais"}}};
  const languageName=value=>value==='oro-ago'?'Ìgbómìnà (Oro-Ago)':value==='en'?'English':languages[value]?.name||'Ìgbómìnà (Oro-Ago)';
  const available=value=>value==='en'||value==='oro-ago'||Object.hasOwn(languages,value);
  let locale='oro-ago',pack=null;
  try{const saved=localStorage.getItem('epa-language');locale=available(saved)?saved:'oro-ago';const raw=localStorage.getItem('epa-language-pack');if(raw)pack=validate(JSON.parse(raw));}catch{}
  function validate(v){
    if(!v||(!available(v.locale)||v.locale==='en')||!v.strings||typeof v.strings!=='object'||Array.isArray(v.strings))throw Error('Use a supported community language pack.');
    if(v.review?.status!=='approved'||typeof v.review?.reviewer!=='string'||!v.review.reviewer.trim())throw Error('A local speaker must supply their name and mark the translation reviewed before importing.');
    const strings={};for(const key of Object.keys(sources)){const s=v.strings[key];if(typeof s==='string'&&s.trim()&&s.length<=500)strings[key]=s.trim();}
    if(!Object.keys(strings).length)throw Error('The pack has no translated interface text.');
    return {locale:v.locale,strings,review:{status:'approved',reviewer:v.review.reviewer.slice(0,100),notes:typeof v.review.notes==='string'?v.review.notes.slice(0,500):''}};
  }
  const languageLabel=document.createElement('label');languageLabel.className='language-picker';languageLabel.textContent='Language ';
  const picker=document.createElement('select');picker.id='language-choice';picker.setAttribute('aria-label','Choose your language');
  for(const [value,name] of [['oro-ago','Ìgbómìnà (Oro-Ago) — default'],['en','English'],...Object.entries(languages).map(([code,v])=>[code,v.name+' · starter'])]){const option=document.createElement('option');option.value=value;option.textContent=name;picker.append(option);}
  languageLabel.append(picker);document.querySelector('nav').append(languageLabel);
  const b=document.createElement('button');b.id='language';b.type='button';document.querySelector('nav').append(b);
  function choose(value){
    locale=available(value)?value:'oro-ago';
    try{localStorage.setItem('epa-language',locale);}catch{toast('Language applied for this visit; browser storage is unavailable.');}
    apply();
  }
  picker.onchange=()=>choose(picker.value);
  window.addEventListener('storage',event=>{if(event.key==='epa-language'){locale=available(event.newValue)?event.newValue:'oro-ago';apply();}});
  const notice=document.createElement('p');notice.id='language-notice';notice.className='language-notice';notice.setAttribute('role','status');document.querySelector('.intro').before(notice);
  function apply(){
    const active=locale!=='en';const reviewed=pack?.locale===locale?pack:null;const strings=reviewed?.strings||languages[locale]?.strings||{};
    picker.value=locale;b.textContent='Language settings';b.setAttribute('aria-label','Language settings: '+languageName(locale));
    notice.hidden=!active;
    const noticeText=reviewed?languageName(locale)+' community pack · '+Object.keys(strings).length+' translated labels · missing text uses English. Reviewer named in the local file; not independently authenticated.':locale==='oro-ago'?'Ìgbómìnà (Oro-Ago) selected. Reviewed dialect wording is not yet available; English fallback is shown.':languageName(locale)+' starter translation · review pending · missing text uses English.';
    if(notice.textContent!==noticeText)notice.textContent=noticeText;
    // Do not change document lang: untranslated sections still remain English.
    document.documentElement.dataset.language=locale;
    for(const [key,selector] of Object.entries(selectors)){const el=document.querySelector(selector);if(!el)continue;const desired=active&&strings[key]?strings[key]:sources[key];if(el.textContent!==desired)el.textContent=desired;el.dir=languages[locale]?.rtl&&strings[key]?'rtl':'auto';el.lang=strings[key]?(locale==='oro-ago'?'yo':locale):'en';}
    const play=document.querySelector('#play');if(play){const key=tab==='dance'?'startDance':'startDrum';const desired=active&&strings[key]?strings[key]:sources[key];if(play.textContent!==desired)play.textContent=desired;}
  }
  b.onclick=()=>{
    modal('<p class="eyebrow">COMMUNITY LANGUAGE</p><h2>Choose your language.</h2><p>The header dropdown offers Ìgbómìnà (the default), English, Yorùbá, Hausa, Igbo, Kiswahili, Arabic, Afrikaans, French, and Portuguese. Starter interface translations await fluent-speaker review. Use the community translation workspace to contribute reviewed wording. No local-dialect wording is represented as verified until a community speaker supplies and reviews it. Standard Yoruba is not silently substituted.</p><div class="world-tools"><button id="lang-en">English</button><button id="lang-oro">Ìgbómìnà (Oro-Ago) · '+(pack?.locale==='oro-ago'?'local pack':'English fallback')+'</button></div><p>Help complete the language option: download the template, fill in the local wording with a fluent Ìgbómìnà speaker from Oro-Ago, and include the reviewer’s name. Translation files stay on this device.</p><button id="lang-template">Download translation template</button><p><label>Import reviewed text pack <input type="file" id="lang-file" accept="application/json,.json"></label></p><p id="lang-result" role="status"></p><p>Approval in an imported file is supplied by that file’s author; the game does not independently authenticate the reviewer. Partial packs retain English for missing text.</p>');
    document.querySelector('#lang-en').onclick=()=>{choose('en');document.querySelector('#modal').close();};
    document.querySelector('#lang-oro').onclick=()=>{choose('oro-ago');document.querySelector('#modal').close();};
    document.querySelector('#lang-template').onclick=()=>{const data={locale:locale==='en'?'oro-ago':locale,displayName:languageName(locale==='en'?'oro-ago':locale),review:{status:'draft',reviewer:'',notes:'Review pronunciation, tone marks and local usage with a fluent Ìgbómìnà speaker from Oro-Ago.'},sourceText:sources,strings:Object.fromEntries(Object.keys(sources).map(k=>[k,'']))};const u=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=u;a.download='epa-'+data.locale+'-translation-template.json';a.click();setTimeout(()=>URL.revokeObjectURL(u),1000);};
    document.querySelector('#lang-file').onchange=async e=>{try{const f=e.target.files[0];if(!f||f.size>50000)throw Error('Choose a JSON pack smaller than 50 KB.');pack=validate(JSON.parse(await f.text()));localStorage.setItem('epa-language-pack',JSON.stringify(pack));locale=pack.locale;localStorage.setItem('epa-language',locale);document.querySelector('#lang-result').textContent='Loaded '+Object.keys(pack.strings).length+' community labels. Missing text uses English.';apply();}catch(error){document.querySelector('#lang-result').textContent=error.message;}};
  };
  let queued=false;new MutationObserver(()=>{if(queued)return;queued=true;queueMicrotask(()=>{queued=false;apply();});}).observe(document.querySelector('main'),{childList:true,subtree:true});
  apply();
})();
