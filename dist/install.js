(() => {
  let promptEvent;
  const button=document.querySelector('#install-button');
  const status=document.querySelector('#install-status');
  const standalone=()=>window.matchMedia('(display-mode: standalone)').matches||navigator.standalone===true;
  function options(){
    if(standalone()){button.hidden=true;status.textContent='You are using the installed Epa app.';return;}
    if(!window.isSecureContext){status.textContent='Open the HTTPS version of this site after its certificate is configured to enable installation.';return;}
    status.textContent=promptEvent?'Ready to install.':'Use your browser’s install menu, or follow the instructions below. If already installed, open Epa from your home screen.';
  }
  window.addEventListener('beforeinstallprompt',event=>{event.preventDefault();promptEvent=event;button.hidden=false;options();});
  button.onclick=async()=>{
    if(!promptEvent)return options();
    const deferred=promptEvent;promptEvent=null;button.hidden=true;
    try{await deferred.prompt();const choice=await deferred.userChoice;status.textContent=choice.outcome==='accepted'?'Installation requested. Complete your browser’s confirmation.':'Installation dismissed. You can keep playing in the browser.';}catch{status.textContent='Use your browser’s install menu or the instructions below.';}
  };
  window.addEventListener('appinstalled',()=>{promptEvent=null;button.hidden=true;status.textContent='Epa is installed. Launch it from your home screen.';});
  options();
  if('serviceWorker' in navigator&&window.isSecureContext){navigator.serviceWorker.register('sw.js').then(()=>navigator.serviceWorker.ready).then(()=>{document.querySelector('#offline-status').textContent='Offline game assets are ready for this installation.';}).catch(()=>{document.querySelector('#offline-status').textContent='Offline setup could not complete. Stay online and reopen the app to try again.';});}
})();
