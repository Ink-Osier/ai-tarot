if(!self.define){let e,i={};const s=(s,n)=>(s=new URL(s+".js",n).href,i[s]||new Promise((i=>{if("document"in self){const e=document.createElement("script");e.src=s,e.onload=i,document.head.appendChild(e)}else e=s,importScripts(s),i()})).then((()=>{let e=i[s];if(!e)throw new Error(`Module ${s} didn’t register its module`);return e})));self.define=(n,r)=>{const o=e||("document"in self?document.currentScript.src:"")||location.href;if(i[o])return;let d={};const t=e=>s(e,o),l={module:{uri:o},exports:d,require:t};i[o]=Promise.all(n.map((e=>l[e]||t(e)))).then((e=>(r(...e),d)))}}define(["./workbox-3e911b1d"],(function(e){"use strict";self.skipWaiting(),e.clientsClaim(),e.precacheAndRoute([{url:"assets/index-BEaatdCi.js",revision:null},{url:"assets/index-D_h8E8sY.css",revision:null},{url:"assets/workbox-window.prod.es5-D5gOYdM7.js",revision:null},{url:"index.html",revision:"150ed75759e5bed50b0ff3ad42b47065"},{url:"android-chrome-192x192.png",revision:"36dc543284d58a544d3491d1611904c5"},{url:"android-chrome-512x512.png",revision:"4ca7804449a443123bdcbf9590de8353"},{url:"manifest.webmanifest",revision:"e97a21c2a4ca082c526e9f03b70d9de2"}],{}),e.cleanupOutdatedCaches(),e.registerRoute(new e.NavigationRoute(e.createHandlerBoundToURL("index.html")))}));
