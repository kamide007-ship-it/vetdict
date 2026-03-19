const SPECIES_ICONS={dog:"\u{1F415}",cat:"\u{1F408}",horse:"\u{1F434}",rabbit:"\u{1F407}",hamster:"\u{1F439}",guinea_pig:"\u{1F439}",chinchilla:"\u{1F43F}\uFE0F",ferret:"\u{1F9A1}",hedgehog:"\u{1F994}",sugar_glider:"\u{1F43F}\uFE0F",degu:"\u{1F42D}",bird:"\u{1F426}",parakeet:"\u{1F99C}",parrot:"\u{1F99C}",reptile:"\u{1F98E}",tortoise:"\u{1F422}",snake:"\u{1F40D}",lizard:"\u{1F98E}",amphibian:"\u{1F438}",exotic_other:"\u{1F999}"};

/* ===== Bilingual i18n system ===== */
let currentLang="ja";
const I18N={
  ja:{
    skipLink:"メインコンテンツへスキップ",
    logoSub:"多動物種対応 獣医学疾患データベース",
    navChecker:"症状チェッカー",navDatabase:"疾患データベース",navChat:"症状相談",navDrugs:"薬品辞書",
    landingChatTitle:"症状をすぐに相談",
    landingChatHint:'症状を入力すると、考えられる疾患をお伝えします。<br/><span style="font-size:.76rem;color:var(--gray-500)">例: 「犬が嘔吐して元気がない」「cat vomiting and lethargic」</span>',
    heroBadge:"獣医師が開発 &mdash; 臨床現場をサポート",
    heroLead:"症状から鑑別疾患リストを即座に表示。<br/>疾患データベース・薬品辞書を搭載した獣医学総合プラットフォーム。",
    heroCta:"動物種を選んで始める",
    statDiseases:"疾患数",statSpecies:"対応動物種",statSymptoms:"症状項目",statDrugs:"薬品数",
    heroCredit:'開発: <a href="https://www.minamisoma-vet.com/" target="_blank" rel="noopener">南相馬アニマルクリニック</a> 獣医師 上手 健太郎',
    sponsorDesc:"獣医師考案・国内製造・競走馬理化学研究所検査合格",
    sponsorCta:"詳細 &rarr;",
    selectSpecies:"動物種を選択",
    cardSymptoms:"&#9745; 症状を選択",cardResults:"&#128202; 検索結果",
    breedLabel:"品種を選択（任意）",breedNone:"品種を選択しない",
    symptomSearchPh:"症状を検索... (例: 咳, vomiting, 下痢)",
    analyzeBtn:"鑑別疾患を検索",
    resultsEmpty:'動物種を選択し、症状にチェックを入れて<br/>「鑑別疾患を検索」を押してください',
    resultsSelectSymptom:"症状を選択してください",
    cardDiseaseDb:"&#128218; 疾患データベース",
    diseaseSearchPh:"疾患名で検索... (例: 腎臓, colic, 感染)",
    cardChat:"&#128172; 症状相談",
    chatWelcome:'こんにちは。気になる症状を日本語または英語で入力してください。<br/>例: 「うちの猫が嘔吐して食欲がない」「my dog is limping and has a fever」<br/><br/><em style="font-size:.76rem;color:var(--gray-500)">※ 本ツールは疾患についての参考情報を提供するものです。診断・治療は必ず獣医師にご相談ください。</em>',
    chatInputPh:"症状を入力してください...",chatSend:"送信",
    cardDrugs:"&#128138; 薬品辞書",
    drugSearchPh:"薬品名で検索... (例: amoxicillin, メロキシカム)",
    allCategories:"全カテゴリ",allSpecies:"全動物種",
    sponsorTagline:"獣医師が考案・国内製造 &mdash; 競走馬理化学研究所の検査合格",
    sponsorSpecies:"対応動物種: 馬・犬・猫",
    sponsorEquine:"馬用サプリメント",sponsorCanine:"犬用サプリメント",
    footerDisclaimer:"※ 本サービスは疾患に関する参考情報の提供を目的としています。診断・治療は必ず獣医師にご相談ください。",
    footerCredit:'開発: <a href="https://www.minamisoma-vet.com/" target="_blank" rel="noopener">南相馬アニマルクリニック</a> 獣医師 上手 健太郎 (Kentaro Kamide, DVM)',
    refTitle1:"引用文献・参考資料 ― 疾患データベース",
    refTitle2:"品種疾患リスク・遺伝疾患",
    refTitle3:"症状の臨床的重み付け・尤度比",
    refTitle4:"エキゾチック動物・鳥類・爬虫類",
    refTitle5:"馬疾患データベース",
    refTitle6:"関連サービス・データベース",refTitle7:"薬品辞書",
    // Dynamic UI strings
    analyzing:"解析中...",
    noSymptomData:"症状データを読み込めませんでした",
    noMatchingSymptom:"該当する症状がありません",
    noSymptomsSelected:"症状が選択されていません",
    noDiseasesFound:"一致する疾患は見つかりませんでした",
    loadFailed:"読み込みに失敗しました",
    noDiseaseMatch:"該当する疾患がありません",
    noDrugMatch:"該当する薬品がありません",
    errorPrefix:"エラー: ",
    overallAssessment:"総合評価: ",
    commError:"通信エラーが発生しました。",
    noResponse:"応答を取得できませんでした",
    diseaseCount:"%filtered% / %total% 件表示",
    catLabels:{respiratory:"呼吸器",digestive:"消化器",neurological:"神経",musculoskeletal:"運動器",dermatological:"皮膚",urinary:"泌尿器",ophthalmological:"眼",cardiovascular:"循環器",behavioral:"行動",general:"全身",other:"その他"},
    sevLabels:{low:"軽度",moderate:"中等度",high:"重度",emergency:"緊急"},
    dtDescription:"説明",dtPathophysiology:"病態生理",dtCauses:"原因",dtPrevention:"予防",dtTreatment:"治療",dtPrognosis:"予後",
    dtMatchedSymptoms:"一致した症状",dtRecommendedTests:"推奨検査",dtRecTestList:"推奨検査一覧:",
    dtSymptoms:"症状",
    dtContraindications:"禁忌事項",dtRoutes:"投与経路",dtFormulations:"製剤",dtInteractions:"薬物相互作用",dtSpeciesInfo:"動物種別情報:",
    safe:"安全",contraindicated:"禁忌",dosageLabel:"投与量: ",
    sponsorVetLabel:"獣医師考案・国内製造・競走馬理化学研究所検査合格",
    productDetails:"製品詳細 &rarr;",
    speciesCardDisease:"疾患",speciesCardDrug:"薬品",
    menuOpen:"メニューを開く",menuClose:"メニューを閉じる",
    removeLabel:"%s%を削除",
    metabSupport:"代謝サポート",aminoAcid:"アミノ酸",digestSupport:"消化管サポート",jointSupport:"関節・運動器",
  },
  en:{
    skipLink:"Skip to main content",
    logoSub:"Multi-Species Veterinary Disease Database",
    navChecker:"Symptom Checker",navDatabase:"Disease Database",navChat:"Symptom Chat",navDrugs:"Drug Dictionary",
    landingChatTitle:"Quick Symptom Chat",
    landingChatHint:'Describe symptoms and we\'ll suggest possible conditions.<br/><span style="font-size:.76rem;color:var(--gray-500)">e.g. "my dog is vomiting and lethargic" "cat not eating for 2 days"</span>',
    heroBadge:"Developed by a veterinarian &mdash; Supporting clinical practice",
    heroLead:"Instantly display differential diagnosis lists from symptoms.<br/>A comprehensive veterinary platform with disease database &amp; drug dictionary.",
    heroCta:"Select a species to start",
    statDiseases:"Diseases",statSpecies:"Species",statSymptoms:"Symptoms",statDrugs:"Drugs",
    heroCredit:'Developed by: <a href="https://www.minamisoma-vet.com/" target="_blank" rel="noopener">Minamisoma Animal Clinic</a> — Kentaro Kamide, DVM',
    sponsorDesc:"Formulated by a veterinarian — Made in Japan — Passed racing lab tests",
    sponsorCta:"Details &rarr;",
    selectSpecies:"Select Species",
    cardSymptoms:"&#9745; Select Symptoms",cardResults:"&#128202; Results",
    breedLabel:"Select breed (optional)",breedNone:"No breed selected",
    symptomSearchPh:"Search symptoms... (e.g. cough, vomiting, diarrhea)",
    analyzeBtn:"Search Differential Diagnoses",
    resultsEmpty:'Select a species, check symptoms, and<br/>press "Search Differential Diagnoses"',
    resultsSelectSymptom:"Please select symptoms",
    cardDiseaseDb:"&#128218; Disease Database",
    diseaseSearchPh:"Search diseases... (e.g. renal, colic, infection)",
    cardChat:"&#128172; Symptom Chat",
    chatWelcome:'Hello! Please describe the symptoms in Japanese or English.<br/>Examples: "my cat is vomiting and has no appetite" "my dog is limping and has a fever"<br/><br/><em style="font-size:.76rem;color:var(--gray-500)">Note: This tool provides reference information about diseases. Always consult a veterinarian for diagnosis and treatment.</em>',
    chatInputPh:"Describe symptoms...",chatSend:"Send",
    cardDrugs:"&#128138; Drug Dictionary",
    drugSearchPh:"Search drugs... (e.g. amoxicillin, meloxicam)",
    allCategories:"All Categories",allSpecies:"All Species",
    sponsorTagline:"Formulated by a veterinarian — Made in Japan — Passed racing lab tests",
    sponsorSpecies:"Supported species: Horse, Dog, Cat",
    sponsorEquine:"Equine Supplements",sponsorCanine:"Canine Supplements",
    footerDisclaimer:"Note: This service provides reference information about diseases. Always consult a veterinarian for diagnosis and treatment.",
    footerCredit:'Developed by: <a href="https://www.minamisoma-vet.com/" target="_blank" rel="noopener">Minamisoma Animal Clinic</a> — Kentaro Kamide, DVM',
    refTitle1:"References — Disease Database",
    refTitle2:"Breed Disease Risks & Genetic Disorders",
    refTitle3:"Clinical Symptom Weighting & Likelihood Ratios",
    refTitle4:"Exotic Animals, Birds & Reptiles",
    refTitle5:"Equine Disease Database",
    refTitle6:"Related Services & Databases",refTitle7:"Drug Dictionary",
    analyzing:"Analyzing...",
    noSymptomData:"Failed to load symptom data",
    noMatchingSymptom:"No matching symptoms",
    noSymptomsSelected:"No symptoms selected",
    noDiseasesFound:"No matching diseases found",
    loadFailed:"Failed to load",
    noDiseaseMatch:"No matching diseases",
    noDrugMatch:"No matching drugs",
    errorPrefix:"Error: ",
    overallAssessment:"Overall: ",
    commError:"A communication error occurred.",
    noResponse:"Could not retrieve response",
    diseaseCount:"%filtered% / %total% shown",
    catLabels:{respiratory:"Respiratory",digestive:"Digestive",neurological:"Neurological",musculoskeletal:"Musculoskeletal",dermatological:"Dermatological",urinary:"Urinary",ophthalmological:"Ophthalmological",cardiovascular:"Cardiovascular",behavioral:"Behavioral",general:"General",other:"Other"},
    sevLabels:{low:"Mild",moderate:"Moderate",high:"Severe",emergency:"Emergency"},
    dtDescription:"Description",dtPathophysiology:"Pathophysiology",dtCauses:"Causes",dtPrevention:"Prevention",dtTreatment:"Treatment",dtPrognosis:"Prognosis",
    dtMatchedSymptoms:"Matched Symptoms",dtRecommendedTests:"Recommended Tests",dtRecTestList:"Recommended Tests:",
    dtSymptoms:"Symptoms",
    dtContraindications:"Contraindications",dtRoutes:"Routes",dtFormulations:"Formulations",dtInteractions:"Drug Interactions",dtSpeciesInfo:"Species Information:",
    safe:"Safe",contraindicated:"Contraindicated",dosageLabel:"Dosage: ",
    sponsorVetLabel:"Formulated by a veterinarian — Made in Japan — Passed racing lab tests",
    productDetails:"Product details &rarr;",
    speciesCardDisease:"diseases",speciesCardDrug:"drugs",
    menuOpen:"Open menu",menuClose:"Close menu",
    removeLabel:"Remove %s%",
    metabSupport:"Metabolic Support",aminoAcid:"Amino Acids",digestSupport:"Digestive Support",jointSupport:"Joint & Mobility",
  }
};

function t(key){return (I18N[currentLang]&&I18N[currentLang][key])||key;}

function applyLanguage(){
  document.documentElement.lang=currentLang;
  document.title=currentLang==="ja"?"Vet Dict — 多動物種対応 獣医学疾患データベース":"Vet Dict — Multi-Species Veterinary Disease Database";
  // Update data-i18n (textContent)
  document.querySelectorAll("[data-i18n]").forEach(el=>{
    const key=el.getAttribute("data-i18n");
    const val=t(key);
    if(val&&val!==key)el.textContent=val;
  });
  // Update data-i18n-html (innerHTML)
  document.querySelectorAll("[data-i18n-html]").forEach(el=>{
    const key=el.getAttribute("data-i18n-html");
    const val=t(key);
    if(val&&val!==key)el.innerHTML=val;
  });
  // Update data-i18n-ph (placeholder)
  document.querySelectorAll("[data-i18n-ph]").forEach(el=>{
    const key=el.getAttribute("data-i18n-ph");
    const val=t(key);
    if(val&&val!==key)el.placeholder=val;
  });
  // Update lang toggle active state
  document.querySelectorAll(".lang-toggle button").forEach(b=>{
    const isActive=b.dataset.lang===currentLang;
    b.classList.toggle("active",isActive);
    b.setAttribute("aria-checked",isActive);
  });
  // Re-render dynamic content
  renderSpeciesGrid();
  if(symptomData.length)renderSymptomList(symptomData);
  renderSelectedSymptoms();
  if(allDiseases.length)renderDiseaseDb();
  if(drugsLoaded)renderDrugList();
}

function setupLanguageToggle(){
  const toggle=document.querySelector(".lang-toggle");
  if(!toggle){console.warn(".lang-toggle element not found");return;}
  toggle.addEventListener("click",e=>{
    const btn=e.target.closest("[data-lang]");
    if(!btn||btn.dataset.lang===currentLang)return;
    currentLang=btn.dataset.lang;
    try{localStorage.setItem("vetdict-lang",currentLang);}catch(e){}
    applyLanguage();
  });
  // Restore saved language preference
  try{const saved=localStorage.getItem("vetdict-lang");if(saved&&I18N[saved]){currentLang=saved;applyLanguage();}}catch(e){}
}
/* ===== End i18n system ===== */

let SPECIES=[];

let currentSpecies=null,selectedSymptoms=new Set(),symptomData=[],allDiseases=[],diseaseFilter="",currentBreed="";
let symptomRequestId=0,diseaseRequestId=0,breedRequestId=0;

document.addEventListener("DOMContentLoaded",()=>{
  try{
    loadSpeciesStats();
    setupNavigation();
    setupChat();
    setupHamburger();
    setupLanguageToggle();
    const symptomSearch=document.getElementById("symptomSearch");
    const analyzeBtn=document.getElementById("analyzeBtn");
    const diseaseSearch=document.getElementById("diseaseSearch");
    if(symptomSearch)symptomSearch.addEventListener("input",()=>renderSymptomList(symptomData));
    if(analyzeBtn)analyzeBtn.addEventListener("click",doAnalyze);
    if(diseaseSearch)diseaseSearch.addEventListener("input",()=>{diseaseDisplayLimit=100;renderDiseaseDb();});
    // Restore view from URL hash
    const hash=location.hash.replace("#","");
    if(hash&&["checker","database","chat","drugs"].includes(hash))switchView(hash);
  }catch(e){
    console.error("Error in DOMContentLoaded:",e);
  }
});

/* --- Hamburger menu --- */
function setupHamburger(){
  const btn=document.getElementById("hamburgerBtn");
  const nav=document.getElementById("mainNav");
  if(!btn||!nav){console.warn("hamburgerBtn or mainNav not found");return;}
  btn.addEventListener("click",()=>{
    const open=nav.classList.toggle("open");
    btn.setAttribute("aria-expanded",open);
    btn.setAttribute("aria-label",open?t("menuClose"):t("menuOpen"));
  });
  // Close on tab selection (mobile)
  nav.addEventListener("click",e=>{if(e.target.closest("[role=tab]")){nav.classList.remove("open");btn.setAttribute("aria-expanded","false");}});
}

/* --- Animate count with Intersection Observer --- */
let statsAnimated=false;
function initStatsObserver(){
  const stats=document.querySelector(".hero-stats");
  if(!stats||statsAnimated)return;
  const prefersReduced=matchMedia("(prefers-reduced-motion:reduce)").matches;
  const observer=new IntersectionObserver(entries=>{
    entries.forEach(entry=>{
      if(entry.isIntersecting&&!statsAnimated){
        statsAnimated=true;
        triggerStatsAnimation(prefersReduced);
        observer.disconnect();
      }
    });
  },{threshold:0.3});
  observer.observe(stats);
}

let pendingStats={};
function triggerStatsAnimation(instant){
  const dur=instant?0:undefined;
  if(pendingStats.diseases!==undefined)animateCount(document.getElementById("statDiseases"),pendingStats.diseases,dur||1200);
  if(pendingStats.species!==undefined)animateCount(document.getElementById("statSpecies"),pendingStats.species,dur||800);
  if(pendingStats.symptoms!==undefined)animateCount(document.getElementById("statSymptoms"),pendingStats.symptoms,dur||1000);
  if(pendingStats.drugs!==undefined)animateCount(document.getElementById("statDrugs"),pendingStats.drugs,dur||1000);
}

function animateCount(el,target,duration){
  if(!el||target<=0){if(el)el.textContent="0";return;}
  if(duration===0){el.textContent=target.toLocaleString();return;}
  const start=performance.now();
  const fmt=n=>n.toLocaleString();
  (function step(now){
    const t=Math.min((now-start)/duration,1);
    const ease=1-Math.pow(1-t,3);
    el.textContent=fmt(Math.round(target*ease));
    if(t<1)requestAnimationFrame(step);
  })(start);
}

/* --- Load stats with Promise.all --- */
function loadSpeciesStats(){
  Promise.all([
    fetch("/api/species-stats").then(r=>r.json()),
    fetch("/api/health-check/symptoms").then(r=>r.json())
  ]).then(([data,sd])=>{
    try{
      // Check if API returned an error response
      if(!data.species||!Array.isArray(data.species)){
        throw new Error("Invalid species data structure from API");
      }
      SPECIES=data.species.map(sp=>({...sp,icon:SPECIES_ICONS[sp.id]||"\u{1F43E}"}));
      pendingStats={
        diseases:data.total_diseases||0,
        species:data.total_species||SPECIES.length,
        drugs:data.total_drugs||0,
        symptoms:sd.symptoms?sd.symptoms.length:0
      };
      renderSpeciesGrid();
      initStatsObserver();
      // If hero is already in view (most cases), trigger immediately
      if(!statsAnimated){
        const rect=document.querySelector(".hero-stats");
        if(rect&&rect.getBoundingClientRect().top<window.innerHeight){
          statsAnimated=true;
          triggerStatsAnimation(matchMedia("(prefers-reduced-motion:reduce)").matches);
        }
      }
    }catch(e){
      console.error("Error processing species stats:",e);
      setDefaultStats();
    }
  }).catch(err=>{
    console.error("Error loading species stats:",err);
    setDefaultStats();
  });
}

function setDefaultStats(){
  SPECIES=[
    {id:"dog",name:"犬",nameEn:"Dog",icon:"\u{1F415}",diseases:575,drugs:0},
    {id:"cat",name:"猫",nameEn:"Cat",icon:"\u{1F408}",diseases:530,drugs:0},
    {id:"horse",name:"馬",nameEn:"Horse",icon:"\u{1F434}",diseases:656,drugs:0},
    {id:"rabbit",name:"うさぎ",nameEn:"Rabbit",icon:"\u{1F407}",diseases:414,drugs:0},
    {id:"hamster",name:"ハムスター",nameEn:"Hamster",icon:"\u{1F439}",diseases:285,drugs:0},
    {id:"guinea_pig",name:"モルモット",nameEn:"Guinea Pig",icon:"\u{1F439}",diseases:308,drugs:0},
    {id:"chinchilla",name:"チンチラ",nameEn:"Chinchilla",icon:"\u{1F43F}\uFE0F",diseases:246,drugs:0},
    {id:"ferret",name:"フェレット",nameEn:"Ferret",icon:"\u{1F9A1}",diseases:241,drugs:0},
    {id:"hedgehog",name:"ハリネズミ",nameEn:"Hedgehog",icon:"\u{1F994}",diseases:210,drugs:0},
    {id:"sugar_glider",name:"フクロモモンガ",nameEn:"Sugar Glider",icon:"\u{1F43F}\uFE0F",diseases:188,drugs:0},
    {id:"degu",name:"デグー",nameEn:"Degu",icon:"\u{1F42D}",diseases:178,drugs:0},
    {id:"bird",name:"鳥",nameEn:"Bird",icon:"\u{1F426}",diseases:479,drugs:0},
    {id:"parakeet",name:"インコ",nameEn:"Parakeet",icon:"\u{1F99C}",diseases:402,drugs:0},
    {id:"parrot",name:"オウム",nameEn:"Parrot",icon:"\u{1F99C}",diseases:251,drugs:0},
    {id:"reptile",name:"爬虫類",nameEn:"Reptile",icon:"\u{1F98E}",diseases:250,drugs:0},
    {id:"tortoise",name:"リクガメ",nameEn:"Tortoise",icon:"\u{1F422}",diseases:256,drugs:0},
    {id:"snake",name:"ヘビ",nameEn:"Snake",icon:"\u{1F40D}",diseases:214,drugs:0},
    {id:"lizard",name:"トカゲ",nameEn:"Lizard",icon:"\u{1F98E}",diseases:218,drugs:0},
    {id:"amphibian",name:"両生類",nameEn:"Amphibian",icon:"\u{1F438}",diseases:215,drugs:0},
    {id:"exotic_other",name:"その他エキゾチック",nameEn:"Exotic Other",icon:"\u{1F999}",diseases:250,drugs:0},
  ];
  pendingStats={
    diseases:6393,
    species:20,
    drugs:175,
    symptoms:52
  };
  renderSpeciesGrid();
  initStatsObserver();
  if(!statsAnimated){
    const rect=document.querySelector(".hero-stats");
    if(rect&&rect.getBoundingClientRect().top<window.innerHeight){
      statsAnimated=true;
      triggerStatsAnimation(matchMedia("(prefers-reduced-motion:reduce)").matches);
    }
  }
}

function renderSpeciesGrid(){
  const grid=document.getElementById("speciesGrid");
  if(!grid){console.warn("speciesGrid element not found");return;}
  grid.innerHTML=SPECIES.map(sp=>{
    const primary=currentLang==="ja"?sp.name:sp.nameEn;
    const secondary=currentLang==="ja"?sp.nameEn:sp.name;
    const dLabel=t("speciesCardDisease"),drLabel=t("speciesCardDrug");
    return`<div class="species-card" role="button" tabindex="0" aria-pressed="${currentSpecies===sp.id}" data-species="${sp.id}">
      <span class="icon" aria-hidden="true">${sp.icon}</span>
      <div class="name">${primary}</div>
      <div class="count">${secondary}</div>
      <div class="count" style="margin-top:2px">${sp.diseases}${dLabel}${sp.drugs?' · '+sp.drugs+drLabel:''}</div>
    </div>`}).join("");
  // Event delegation for species cards
  if(grid.dataset.bound==="1")return;
  grid.dataset.bound="1";
  grid.addEventListener("click",e=>{
    const card=e.target.closest(".species-card");
    if(card)selectSpecies(card.dataset.species);
  });
  grid.addEventListener("keydown",e=>{
    const card=e.target.closest(".species-card");
    if(card&&(e.key==="Enter"||e.key===" ")){e.preventDefault();selectSpecies(card.dataset.species);}
  });
}

function selectSpecies(id){
  currentSpecies=id;selectedSymptoms.clear();currentBreed="";
  document.querySelectorAll(".species-card").forEach(c=>{
    const sel=c.dataset.species===id;
    c.setAttribute("aria-pressed",sel);
  });
  renderSelectedSymptoms();loadSymptoms(id);loadDiseaseDb(id);loadBreeds(id);
  resetSpeciesChat(id);
  const resultsArea=document.getElementById("resultsArea");
  if(resultsArea)resultsArea.innerHTML=`<div class="results-empty"><span class="big-icon" aria-hidden="true">\u{1F50D}</span><p>${t("resultsSelectSymptom")}</p></div>`;
}

function resetSpeciesChat(species){
  const sp=SPECIES.find(s=>s.id===species);
  const spLabel=sp?(currentLang==="ja"?sp.name:sp.nameEn):(species||"dog");
  const hint=currentLang==="ja"?`${spLabel}の症状を入力してください。`:`Please describe ${spLabel} symptoms.`;
  ["chatMessages","landingChatMessages"].forEach(id=>{
    const el=document.getElementById(id);
    if(el){el.innerHTML=`<div class="chat-msg bot">${hint}</div>`;}
  });
}

function loadBreeds(species){
  const requestId=++breedRequestId;
  const area=document.getElementById("breedSelectArea");
  const select=document.getElementById("breedSelect");
  select.innerHTML=`<option value="">${t("breedNone")}</option>`;
  currentBreed="";
  fetch("/api/breeds/"+species).then(r=>r.json()).then(data=>{
    if(requestId!==breedRequestId||species!==currentSpecies)return;
    if(data.breeds&&data.breeds.length>0){
      data.breeds.forEach(b=>{select.innerHTML+=`<option value="${b.id}">${b.name_ja} (${b.name})</option>`;});
      area.classList.remove("hidden");
    }else{area.classList.add("hidden");}
  }).catch(()=>{if(requestId===breedRequestId)area.classList.add("hidden");});
  select.onchange=function(){currentBreed=this.value;};
}

function loadSymptoms(species){
  const requestId=++symptomRequestId;
  fetch(`/api/species/${species}/symptoms`).then(r=>r.json()).then(data=>{
    if(requestId!==symptomRequestId||species!==currentSpecies)return;
    if(data.symptoms&&data.symptoms.length){
      symptomData=data.symptoms;
      renderSymptomList(symptomData);
      return;
    }
    return fetch("/api/health-check/symptoms").then(r=>r.json()).then(data=>{
      if(requestId!==symptomRequestId||species!==currentSpecies)return;
      symptomData=data.symptoms||[];
      renderSymptomList(symptomData);
    });
  }).catch(()=>{
    if(requestId!==symptomRequestId)return;
    document.getElementById("symptomList").innerHTML=`<div style="padding:20px;text-align:center;color:var(--gray-500)">${t("loadFailed")}</div>`;
  });
}

function renderSymptomList(symptoms){
  const symptomSearch=document.getElementById("symptomSearch");
  const list=document.getElementById("symptomList");
  if(!list){console.warn("symptomList element not found");return;}
  const search=(symptomSearch?.value||"").toLowerCase();
  const categories={};
  symptoms.forEach(s=>{const cat=s.category||"other";if(!categories[cat])categories[cat]=[];categories[cat].push(s);});
  const catLabels=t("catLabels");
  let html="";
  for(const[cat,items]of Object.entries(categories)){
    const filtered=items.filter(s=>{if(!search)return true;return(s.name_ja||"").toLowerCase().includes(search)||(s.name_en||"").toLowerCase().includes(search)||(s.id||"").toLowerCase().includes(search);});
    if(!filtered.length)continue;
    html+=`<div class="symptom-cat" role="heading" aria-level="4">${catLabels[cat]||cat}</div>`;
    for(const s of filtered){const sel=selectedSymptoms.has(s.id);const primary=currentLang==="ja"?s.name_ja:s.name_en;const secondary=currentLang==="ja"?s.name_en:s.name_ja;html+=`<div class="symptom-item" role="checkbox" aria-checked="${sel}" tabindex="0" data-id="${s.id}"><span class="sym-icon" aria-hidden="true">${sel?"\u2713":"+"}</span><span>${primary} <span style="color:var(--gray-600)">${secondary}</span></span></div>`;}
  }
  list.innerHTML=html||`<div style="padding:20px;text-align:center;color:var(--gray-500)">${t("noMatchingSymptom")}</div>`;
  // Event delegation for symptom items
  list.onclick=e=>{const item=e.target.closest(".symptom-item");if(item)toggleSymptom(item.dataset.id);};
  list.onkeydown=e=>{const item=e.target.closest(".symptom-item");if(item&&(e.key==="Enter"||e.key===" ")){e.preventDefault();toggleSymptom(item.dataset.id);}};
}

function toggleSymptom(id){if(selectedSymptoms.has(id))selectedSymptoms.delete(id);else selectedSymptoms.add(id);renderSelectedSymptoms();renderSymptomList(symptomData);}

function renderSelectedSymptoms(){
  const area=document.getElementById("selectedSymptoms"),btn=document.getElementById("analyzeBtn");
  if(selectedSymptoms.size===0){area.innerHTML=`<span style="color:var(--gray-500);font-size:.78rem">${t("noSymptomsSelected")}</span>`;btn.disabled=true;return;}
  btn.disabled=false;
  area.innerHTML=[...selectedSymptoms].map(id=>{const sym=symptomData.find(s=>s.id===id);const label=sym?(currentLang==="ja"?sym.name_ja:sym.name_en):id;const ariaLabel=t("removeLabel").replace("%s%",label);return`<span class="selected-tag">${label} <button class="remove" type="button" aria-label="${ariaLabel}" data-id="${id}">&times;</button></span>`;}).join("");
  area.querySelectorAll(".remove").forEach(b=>b.addEventListener("click",e=>{e.stopPropagation();toggleSymptom(b.dataset.id);}));
}

function collectLabValues(){
  const vals={};
  document.querySelectorAll("#labValuesGrid input[data-lab]").forEach(el=>{
    if(el.value.trim()!==""){const v=parseFloat(el.value);if(!isNaN(v))vals[el.dataset.lab]=v;}
  });
  return Object.keys(vals).length>0?vals:null;
}
function highlightLabAbnormals(){
  let filled=0,abnormal=0;
  document.querySelectorAll("#labValuesGrid input[data-lab]").forEach(el=>{
    const v=parseFloat(el.value),lo=parseFloat(el.dataset.lo),hi=parseFloat(el.dataset.hi);
    const flag=el.nextElementSibling;
    el.classList.remove("lab-high","lab-low");
    if(flag)flag.textContent="";
    if(isNaN(v)||el.value.trim()==="")return;
    filled++;
    if(v>hi){el.classList.add("lab-high");if(flag){flag.textContent="\u2191";flag.style.color="#e74c3c";}abnormal++;}
    else if(v<lo){el.classList.add("lab-low");if(flag){flag.textContent="\u2193";flag.style.color="#2980b9";}abnormal++;}
  });
  const badge=document.getElementById("labSummaryBadge");
  if(filled>0){badge.style.display="inline";badge.textContent=abnormal>0?`${filled}\u9805\u76ee\u5165\u529b / ${abnormal}\u7570\u5e38`:`${filled}\u9805\u76ee\u5165\u529b`;badge.style.background=abnormal>0?"#e74c3c":"var(--green)";}
  else{badge.style.display="none";}
}
function clearLabValues(){
  document.querySelectorAll("#labValuesGrid input[data-lab]").forEach(el=>{el.value="";});
  highlightLabAbnormals();
}
document.addEventListener("input",e=>{if(e.target.matches("#labValuesGrid input"))highlightLabAbnormals();});


function buildFieldFallback(label,name){
  if(currentLang==="ja")return `${label}: ${name}について一般的な獣医学情報を確認し、個体の状態に合わせて獣医師が評価してください。`;
  return `${label}: Review standard veterinary references for ${name} and individualize by clinical assessment.`;
}


function escapeHtml(value){
  return String(value??"").replace(/[&<>"']/g,ch=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[ch]));
}

function sanitizeUrl(value){
  try{
    const url=new URL(String(value??""),window.location.origin);
    return ["http:","https:"].includes(url.protocol)?url.href:"#";
  }catch{
    return "#";
  }
}

function renderReferenceLinks(item){
  const refs=(item&&Array.isArray(item.evidence_sources))?item.evidence_sources:[];
  if(!refs.length)return "";
  return `<div class="missing-note">References: ${refs.map(r=>`<a href="${r&&r.url?sanitizeUrl(r.url):"#"}" target="_blank" rel="noopener noreferrer">${escapeHtml(r&&r.name)}</a>`).join(" | ")}</div>`;
}

function renderCitationMap(item){
  const cmap=(item&&item.citation_map&&typeof item.citation_map==="object")?item.citation_map:{};
  const refs=(item&&Array.isArray(item.evidence_sources))?item.evidence_sources:[];
  const idToNumber={};
  refs.forEach(ref=>{
    if(ref&&ref.id){
      if(ref.number)idToNumber[ref.id]=String(ref.number);
      else{
        const m=String(ref.id).match(/^ref-(\d+)$/);
        if(m)idToNumber[ref.id]=m[1];
      }
    }
  });
  const entries=Object.entries(cmap).filter(([,ids])=>Array.isArray(ids)&&ids.length>0);
  if(!entries.length)return "";
  return `<div class="missing-note">Citation map: ${entries.map(([k,ids])=>`${escapeHtml(k)} → ${ids.map(id=>idToNumber[id]?`[${escapeHtml(idToNumber[id])}]`:escapeHtml(id)).join(", ")}`).join(" / ")}</div>`;
}

function doAnalyze(){
  if(!currentSpecies||selectedSymptoms.size===0)return;
  const btn=document.getElementById("analyzeBtn");btn.disabled=true;btn.innerHTML=`<span class="spinner"></span> ${t("analyzing")}`;
  const payload={species:currentSpecies,symptoms:[...selectedSymptoms]};
  if(currentBreed)payload.breed=currentBreed;
  const labVals=collectLabValues();
  if(labVals)payload.lab_values=labVals;
  fetch("/api/analyze-symptoms",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)})
  .then(r=>r.json()).then(data=>renderResults(data))
  .catch(err=>{document.getElementById("resultsArea").innerHTML=`<div class="severity-bar high">${t("errorPrefix")}${err.message}</div>`;})
  .finally(()=>{btn.disabled=false;btn.textContent=t("analyzeBtn");});
}

function renderResults(data){
  const area=document.getElementById("resultsArea");
  const diseases=data.suspected_diseases||data.possible_conditions||[];
  const diseasesByPhase=data.suspected_diseases_by_phase||{};
  const tests=data.recommended_tests||[];
  const severity=data.severity||"low";
  const adviceJa=data.general_advice_ja||"";
  if(diseases.length===0){area.innerHTML=`<div class="results-empty"><span class="big-icon">\u2705</span><p>${t("noDiseasesFound")}</p></div>`;return;}
  const sevLabels=t("sevLabels");
  let html=`<div class="severity-bar ${severity}">${t("overallAssessment")}${sevLabels[severity]||severity}</div>`;
  if(data.lab_boost_applied){
    const labNames={bun:"BUN",creatinine:"Cre",sdma:"SDMA",alt:"ALT",alp:"ALP",ggt:"GGT",tbil:"T-Bil",albumin:"Alb",glucose:"Glu",lipase:"Lipase",potassium:"K",sodium:"Na",calcium:"Ca",phosphorus:"P",wbc:"WBC",pcv:"PCV",platelets:"PLT",t4:"T4",crp:"CRP",usg:"USG"};
    const labRanges={bun:[7,27],creatinine:[0.5,1.8],sdma:[0,14],alt:[10,125],alp:[23,212],ggt:[0,11],tbil:[0,0.5],albumin:[2.3,4],glucose:[74,143],lipase:[10,160],potassium:[3.5,5.8],sodium:[140,155],calcium:[7.9,12],phosphorus:[2.5,6.8],wbc:[5.5,16.9],pcv:[37,55],platelets:[175,500],t4:[1,4],crp:[0,10],usg:[1.03,99]};
    let abnList=[];
    if(data.lab_values){for(const[k,v]of Object.entries(data.lab_values)){const r=labRanges[k];if(r){if(v>r[1])abnList.push(`<span style="color:#e74c3c;font-weight:700">${labNames[k]||k} ${v}\u2191</span>`);else if(v<r[0])abnList.push(`<span style="color:#2980b9;font-weight:700">${labNames[k]||k} ${v}\u2193</span>`);}}}
    html+=`<div style="font-size:.8rem;color:#2980b9;margin-bottom:8px;padding:8px 12px;background:#ebf5fb;border-radius:var(--radius)">&#128300; ${currentLang==="ja"?"検査値異常":"Lab abnormalities"}: ${abnList.length?abnList.join("&ensp;"):(currentLang==="ja"?"（基準値内）":"(within range)")}</div>`;
  }
  const adviceText=currentLang==="ja"?adviceJa:(data.general_advice||adviceJa);
  if(adviceText)html+=`<div style="font-size:.82rem;color:var(--gray-700);margin-bottom:12px;padding:8px 12px;background:var(--gray-50);border-radius:var(--radius)">${adviceText}</div>`;

  // Stepwise differential diagnosis: Phase 1 (common) vs Phase 2 (rare)
  const phase1=diseasesByPhase.phase_1_common||[];
  const phase2=diseasesByPhase.phase_2_rare||[];

  // Render Phase 1 (Common/Very Common)
  if(phase1.length>0){
    html+=`<div style="margin-bottom:16px"><div style="font-size:.86rem;font-weight:700;color:var(--green);padding:8px 12px;background:rgba(34,168,79,.08);border-left:4px solid var(--green);border-radius:var(--radius);margin-bottom:10px">🎯 ${currentLang==="ja"?"最初に検討すべき疾患（よくある疾患）":"Primary Differential (Common diseases)"}</div>`;
    phase1.forEach(d=>{html+=renderDiseaseCard(d,data);});
    html+=`</div>`;
  }

  // Render Phase 2 (Uncommon/Rare)
  if(phase2.length>0){
    html+=`<div style="margin-bottom:16px"><div style="font-size:.86rem;font-weight:700;color:var(--orange);padding:8px 12px;background:rgba(240,133,14,.08);border-left:4px solid var(--orange);border-radius:var(--radius);margin-bottom:10px">🔍 ${currentLang==="ja"?"さらに検討すべき疾患（稀な疾患）":"Secondary Differential (Rare/Uncommon diseases)"}</div>`;
    phase2.forEach(d=>{html+=renderDiseaseCard(d,data);});
    html+=`</div>`;
  }

  // Fallback: render all diseases if no phase info
  if(phase1.length===0&&phase2.length===0){
    diseases.forEach(d=>{
    const name=d.name||d.name_ja||"",nameJa=d.name_ja||"",pct=d.match_percent||d.confidence||0;
    const likelihood=d.likelihood||(pct>=50?"high":pct>=30?"moderate":"low");
    const desc=currentLang==="ja"?(d.description_ja||d.description||""):(d.description||d.description_ja||"");
    const diseaseName=nameJa||name||"Disease";
    const matchSymptoms=d.matching_symptoms||[],recTests=d.recommended_tests||[];
    const lf=currentLang==="ja"?"_ja":"";const lf2=currentLang==="ja"?"":"_ja";
    const pick=(ja,en)=>currentLang==="ja"?(ja||en||""):(en||ja||"");
    const symNames=data.symptom_names||{};
    const patho=pick(d.pathophysiology_ja,d.pathophysiology)||buildFieldFallback(t("dtPathophysiology"),diseaseName);
    const causes=pick(d.causes_ja,d.causes)||buildFieldFallback(t("dtCauses"),diseaseName);
    const prevention=pick(d.prevention_ja,d.prevention)||buildFieldFallback(t("dtPrevention"),diseaseName);
    const treatment=pick(d.treatment_ja,d.treatment)||buildFieldFallback(t("dtTreatment"),diseaseName);
    const prognosis=pick(d.prognosis_ja,d.prognosis)||buildFieldFallback(t("dtPrognosis"),diseaseName);
    const matchDisplay=matchSymptoms.map(s=>{const n=symNames[s];if(!n)return s;return currentLang==="ja"?`${n.ja} <span style="color:var(--gray-500);font-size:.78rem">${n.en}</span>`:`${n.en} <span style="color:var(--gray-500);font-size:.78rem">${n.ja}</span>`;}).join("&ensp;|&ensp;");
      html+=renderDiseaseCard(d,data);
    });
  }

  if(tests.length){html+=`<div style="margin-top:16px"><strong style="font-size:.86rem">${t("dtRecTestList")}</strong><ul class="test-list">${tests.map(x=>{const label=typeof x==="string"?x:(currentLang==="ja"?(x.name_ja||x.name):(x.name||x.name_ja));const priority=x.priority?` <span style="color:var(--gray-500);font-size:.75rem">[${x.priority}]</span>`:"";return`<li>\u{1F52C} ${label}${priority}</li>`;}).join("")}</ul></div>`;}
  area.innerHTML=html;
}

function renderDiseaseCard(d,data){
  const name=d.name||d.name_ja||"",nameJa=d.name_ja||"",pct=d.match_percent||d.confidence||0;
  const likelihood=d.likelihood||(pct>=50?"high":pct>=30?"moderate":"low");
  const desc=currentLang==="ja"?(d.description_ja||d.description||""):(d.description||d.description_ja||"");
  const diseaseName=nameJa||name||"Disease";
  const matchSymptoms=d.matching_symptoms||[],recTests=d.recommended_tests||[];
  const lf=currentLang==="ja"?"_ja":"";const lf2=currentLang==="ja"?"":"_ja";
  const pick=(ja,en)=>currentLang==="ja"?(ja||en||""):(en||ja||"");
  const symNames=data.symptom_names||{};
  const patho=pick(d.pathophysiology_ja,d.pathophysiology)||buildFieldFallback(t("dtPathophysiology"),diseaseName);
  const causes=pick(d.causes_ja,d.causes)||buildFieldFallback(t("dtCauses"),diseaseName);
  const prevention=pick(d.prevention_ja,d.prevention)||buildFieldFallback(t("dtPrevention"),diseaseName);
  const treatment=pick(d.treatment_ja,d.treatment)||buildFieldFallback(t("dtTreatment"),diseaseName);
  const prognosis=pick(d.prognosis_ja,d.prognosis)||buildFieldFallback(t("dtPrognosis"),diseaseName);
  const matchDisplay=matchSymptoms.map(s=>{const n=symNames[s];if(!n)return s;return currentLang==="ja"?`${n.ja} <span style="color:var(--gray-500);font-size:.78rem">${n.en}</span>`:`${n.en} <span style="color:var(--gray-500);font-size:.78rem">${n.ja}</span>`;}).join("&ensp;|&ensp;");
  const completeness=Number(d.completeness_score||100);
  const missing=(d.missing_fields||[]);
  const qualityClass=completeness>=90?"quality-ok":"quality-warn";
  const prevalenceTier=d.prevalence_tier||"unknown";
  const prevalenceLabel={very_common:(currentLang==="ja"?"非常に一般的":"Very Common"),common:(currentLang==="ja"?"一般的":"Common"),uncommon:(currentLang==="ja"?"稀":"Uncommon"),rare:(currentLang==="ja"?"非常に稀":"Rare"),unknown:(currentLang==="ja"?"不明":"Unknown")}[prevalenceTier]||"";

  let html=`<div class="disease-result"><div class="disease-head" onclick="this.nextElementSibling.classList.toggle('open')"><div><span class="disease-name">${name}</span>${nameJa&&nameJa!==name?`<span class="disease-name-ja">${nameJa}</span>`:""}<span class="quality-badge ${qualityClass}">${completeness}%</span>${prevalenceLabel?`<span style="font-size:.7rem;color:var(--gray-500);margin-left:8px;padding:2px 6px;background:var(--gray-100);border-radius:6px">${prevalenceLabel}</span>`:""}  </div><span class="match-badge ${likelihood}">${pct}%</span></div><div class="disease-detail"><dl><dt>${t("dtDescription")}</dt><dd>${desc||buildFieldFallback(t("dtDescription"),diseaseName)}</dd><dt>${t("dtPathophysiology")}</dt><dd>${patho}</dd><dt>${t("dtCauses")}</dt><dd>${causes}</dd><dt>${t("dtPrevention")}</dt><dd>${prevention}</dd><dt>${t("dtTreatment")}</dt><dd>${treatment}</dd><dt>${t("dtPrognosis")}</dt><dd>${prognosis}</dd>${matchSymptoms.length?`<dt>${t("dtMatchedSymptoms")}</dt><dd>${matchDisplay}</dd>`:""} ${recTests.length?`<dt>${t("dtRecommendedTests")}</dt><dd>${recTests.join(", ")}</dd>`:""}</dl>${d.content_origin?`<div class="missing-note">Content source: ${d.content_origin}</div>`:""}${renderCitationMap(d)}${renderReferenceLinks(d)}${missing.length?`<div class="missing-note">Data needs review: ${missing.join(", ")}</div>`:""}</div></div>`;
  return html;
}

function loadDiseaseDb(species){
  const requestId=++diseaseRequestId;
  const list=document.getElementById("diseaseDbList");
  if(!list){console.warn("diseaseDbList element not found");return;}
  list.innerHTML='<div style="padding:20px;text-align:center"><span class="spinner"></span></div>';
  fetch(`/api/health-check/diseases?species=${encodeURIComponent(species)}`).then(r=>r.json()).then(data=>{if(requestId!==diseaseRequestId||species!==currentSpecies)return;if(data.diseases){allDiseases=data.diseases;renderAzNav();renderDiseaseDb();}})
  .catch(()=>{if(requestId===diseaseRequestId&&list)list.innerHTML=`<div style="padding:20px;text-align:center;color:var(--gray-500)">${t("loadFailed")}</div>`;});
}

function renderAzNav(){
  const azNav=document.getElementById("azNav");
  if(!azNav){console.warn("azNav element not found");return;}
  azNav.innerHTML=`<button class="active" onclick="filterDiseaseDb('')">ALL</button>`+"ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("").map(l=>`<button onclick="filterDiseaseDb('${l}')">${l}</button>`).join("");
}

function filterDiseaseDb(letter){
  diseaseFilter=letter;
  diseaseDisplayLimit=100;
  document.querySelectorAll(".az-nav button").forEach(b=>b.classList.toggle("active",b.textContent===letter||(letter===""&&b.textContent==="ALL")));
  renderDiseaseDb();
}

let diseaseDisplayLimit=100;
function renderDiseaseDb(){
  const list=document.getElementById("diseaseDbList");
  const search=(document.getElementById("diseaseSearch").value||"").toLowerCase();
  let filtered=allDiseases;
  if(diseaseFilter)filtered=filtered.filter(d=>(d.name||"").toUpperCase().startsWith(diseaseFilter));
  if(search)filtered=filtered.filter(d=>(d.name||"").toLowerCase().includes(search)||(d.name_ja||"").toLowerCase().includes(search)||(d.description||"").toLowerCase().includes(search)||(d.description_ja||"").toLowerCase().includes(search));
  document.getElementById("diseaseDbCount").textContent=t("diseaseCount").replace("%filtered%",filtered.length).replace("%total%",allDiseases.length);
  if(filtered.length===0){list.innerHTML=`<div style="padding:20px;text-align:center;color:var(--gray-500)">${t("noDiseaseMatch")}</div>`;return;}
  const pk=(ja,en)=>currentLang==="ja"?(ja||en||""):(en||ja||"");
  const shown=filtered.slice(0,diseaseDisplayLimit);
  list.innerHTML=shown.map(d=>{
    const diseaseName=d.name_ja||d.name||"Disease";
    const desc=pk(d.description_ja,d.description)||buildFieldFallback(t("dtDescription"),diseaseName);
    const patho=pk(d.pathophysiology_ja,d.pathophysiology)||buildFieldFallback(t("dtPathophysiology"),diseaseName);
    const causes=pk(d.causes_ja,d.causes)||buildFieldFallback(t("dtCauses"),diseaseName);
    const prevention=pk(d.prevention_ja,d.prevention)||buildFieldFallback(t("dtPrevention"),diseaseName);
    const treatment=pk(d.treatment_ja,d.treatment)||buildFieldFallback(t("dtTreatment"),diseaseName);
    const prognosis=pk(d.prognosis_ja,d.prognosis)||buildFieldFallback(t("dtPrognosis"),diseaseName);
    return`<div class="disease-db-item" onclick="this.querySelector('.disease-detail').classList.toggle('open')">
      <div class="d-name">${d.name||""} <span class="d-name-ja">${d.name_ja||""}</span><span class="quality-badge ${(Number(d.completeness_score||100)>=90)?"quality-ok":"quality-warn"}">${Number(d.completeness_score||100)}%</span></div>
      <div class="d-desc">${desc.substring(0,80)}${desc.length>80?"...":""}</div>
      <div class="disease-detail"><dl>
        <dt>${t("dtDescription")}</dt><dd>${desc}</dd>
        <dt>${t("dtPathophysiology")}</dt><dd>${patho}</dd>
        <dt>${t("dtCauses")}</dt><dd>${causes}</dd>
        <dt>${t("dtPrevention")}</dt><dd>${prevention}</dd>
        <dt>${t("dtTreatment")}</dt><dd>${treatment}</dd>
        <dt>${t("dtPrognosis")}</dt><dd>${prognosis}</dd>
        ${d.symptoms?`<dt>${t("dtSymptoms")}</dt><dd>${Array.isArray(d.symptoms)?d.symptoms.join(", "):(typeof d.symptoms==="object"?Object.keys(d.symptoms).join(", "):d.symptoms)}</dd>`:""}
        ${d.recommended_tests?`<dt>${t("dtRecommendedTests")}</dt><dd>${d.recommended_tests.join(", ")}</dd>`:""}
      </dl>${d.content_origin?`<div class="missing-note">Content source: ${d.content_origin}</div>`:""}${renderCitationMap(d)}${renderReferenceLinks(d)}${(d.missing_fields&&d.missing_fields.length)?`<div class="missing-note">Data needs review: ${d.missing_fields.join(", ")}</div>`:""}</div>
    </div>`}).join("");
  if(filtered.length>diseaseDisplayLimit){
    list.innerHTML+=`<button class="show-more-btn" onclick="diseaseDisplayLimit+=100;renderDiseaseDb();" style="display:block;margin:16px auto;padding:8px 24px;border:1px solid var(--gray-300);border-radius:6px;background:var(--white);cursor:pointer">${currentLang==="ja"?`さらに表示 (残り${filtered.length-diseaseDisplayLimit}件)`:`Show more (${filtered.length-diseaseDisplayLimit} remaining)`}</button>`;
  }
}

function switchView(view){
  const views=["checker","database","chat","drugs"];
  views.forEach(v=>{
    const tab=document.getElementById("tab-"+v);
    const panel=document.getElementById("view"+v.charAt(0).toUpperCase()+v.slice(1));
    if(tab)tab.setAttribute("aria-selected",v===view);
    if(panel)panel.classList.toggle("hidden",v!==view);
  });
  history.replaceState(null,null,"#"+view);
  if(view==="drugs"&&!drugsLoaded)loadDrugDictionary();
}

function setupNavigation(){
  const nav=document.getElementById("mainNav");
  if(!nav){console.warn("mainNav element not found");return;}
  nav.addEventListener("click",e=>{
    const tab=e.target.closest("[role=tab]");
    if(tab)switchView(tab.dataset.view);
  });
  // Keyboard navigation: arrow keys between tabs
  nav.addEventListener("keydown",e=>{
    const tabs=[...nav.querySelectorAll("[role=tab]")];
    const idx=tabs.indexOf(document.activeElement);
    if(idx<0)return;
    let next=-1;
    if(e.key==="ArrowRight")next=(idx+1)%tabs.length;
    else if(e.key==="ArrowLeft")next=(idx-1+tabs.length)%tabs.length;
    if(next>=0){e.preventDefault();tabs[next].focus();switchView(tabs[next].dataset.view);}
  });
  // Listen for hash changes (browser back/forward)
  window.addEventListener("hashchange",()=>{
    const hash=location.hash.replace("#","");
    if(["checker","database","chat","drugs"].includes(hash))switchView(hash);
  });
}

function setupChat(){
  const chatSend=document.getElementById("chatSend");
  const chatInput=document.getElementById("chatInput");
  const landingChatSend=document.getElementById("landingChatSend");
  const landingChatInput=document.getElementById("landingChatInput");
  if(chatSend)chatSend.addEventListener("click",()=>sendChatMessage());
  if(chatInput)chatInput.addEventListener("keydown",e=>{if(e.key==="Enter")sendChatMessage();});
  if(landingChatSend)landingChatSend.addEventListener("click",()=>sendLandingChat());
  if(landingChatInput)landingChatInput.addEventListener("keydown",e=>{if(e.key==="Enter")sendLandingChat();});
}
function stripGuidanceFromResponse(response,guidance){
  if(!response||!guidance)return response||"";
  return response.startsWith(guidance)?response.slice(guidance.length).trimStart():response;
}

function renderSpeciesGuidance(containerId,guidance){
  if(!guidance)return;
  const msgs=document.getElementById(containerId);
  if(!msgs)return;
  const div=document.createElement("div");
  div.className="species-guidance";
  div.textContent=guidance;
  msgs.appendChild(div);
  msgs.scrollTop=msgs.scrollHeight;
}

function sendLandingChat(){
  const input=document.getElementById("landingChatInput"),text=input.value.trim();if(!text)return;input.value="";
  const msgs=document.getElementById("landingChatMessages");
  const userDiv=document.createElement("div");userDiv.className="chat-msg user";userDiv.textContent=text;msgs.appendChild(userDiv);msgs.scrollTop=msgs.scrollHeight;
  const species=currentSpecies||"dog";
  const loading=document.createElement("div");loading.className="chat-msg bot";loading.innerHTML='<span class="spinner" style="width:16px;height:16px"></span>';msgs.appendChild(loading);msgs.scrollTop=msgs.scrollHeight;
  fetch("/api/diagnostic-chat/chat",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message:text,species:species})})
  .then(r=>{if(!r.ok)throw new Error(`HTTP ${r.status}`);return r.json();})
  .then(data=>{
    if(!data){loading.textContent="No response data";return;}
    const base=(data.response||data.message||data.error||t("noResponse"));
    if(!base){loading.textContent="No base response";return;}
    loading.textContent=stripGuidanceFromResponse(base,data.species_guidance);
    renderSpeciesGuidance("landingChatMessages",data.species_guidance);
    msgs.scrollTop=msgs.scrollHeight;
  })
  .catch(err=>{
    console.error("Chat error:",err);
    loading.textContent=t("commError")+" ("+err.message+")";
    msgs.scrollTop=msgs.scrollHeight;
  });
}

function sendChatMessage(){
  const input=document.getElementById("chatInput"),text=input.value.trim();if(!text)return;input.value="";
  addChatMsg(text,"user");const species=currentSpecies||"dog";
  fetch("/api/diagnostic-chat/chat",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message:text,species:species})})
  .then(r=>{if(!r.ok)throw new Error(`HTTP ${r.status}`);return r.json();})
  .then(data=>{
    if(!data){addChatMsg("No response data","bot");return;}
    if(data.species_guidance) addChatMsg(`[Species] ${data.species_guidance}`,"bot");
    const base=(data.response||data.message||data.error||t("noResponse"));
    if(base) addChatMsg(stripGuidanceFromResponse(base,data.species_guidance),"bot");
    else addChatMsg(t("noResponse"),"bot");
  })
  .catch(err=>{
    console.error("Chat error:",err);
    addChatMsg(t("commError")+" ("+err.message+")","bot");
  });
}

function addChatMsg(text,type){
  const msgs=document.getElementById("chatMessages"),div=document.createElement("div");
  div.className=`chat-msg ${type}`;div.textContent=text;
  msgs.appendChild(div);msgs.scrollTop=msgs.scrollHeight;
}

let drugsLoaded=false,allDrugs=[],drugCategories={};

function loadDrugDictionary(){
  const list=document.getElementById("drugList");
  list.innerHTML='<div style="padding:20px;text-align:center"><span class="spinner"></span></div>';
  Promise.all([fetch("/api/drugs").then(r=>r.json()),fetch("/api/drug-categories").then(r=>r.json())])
  .then(([drugsData,catData])=>{
    allDrugs=drugsData.drugs||[];drugCategories=drugsData.categories||{};
    pendingStats.drugs=allDrugs.length;animateCount(document.getElementById("statDrugs"),allDrugs.length,800);
    const catSelect=document.getElementById("drugCategoryFilter");
    catSelect.innerHTML=`<option value="">${t("allCategories")}</option>`;
    (catData.categories||[]).forEach(c=>{if(c.count>0){const cName=currentLang==="ja"?(c.name_ja||c.name_en):(c.name_en||c.name_ja);catSelect.innerHTML+=`<option value="${c.id}">${cName} (${c.count})</option>`;}});
    const spSelect=document.getElementById("drugSpeciesFilter");
    spSelect.innerHTML=`<option value="">${t("allSpecies")}</option>`;
    SPECIES.forEach(sp=>{const primary=currentLang==="ja"?sp.name:sp.nameEn;const secondary=currentLang==="ja"?sp.nameEn:sp.name;spSelect.innerHTML+=`<option value="${sp.id}">${primary} ${secondary}</option>`;});
    drugsLoaded=true;renderDrugList();
  }).catch(()=>{list.innerHTML=`<div style="padding:20px;text-align:center;color:var(--gray-500)">${t("loadFailed")}</div>`;});
  document.getElementById("drugSearch").addEventListener("input",renderDrugList);
  document.getElementById("drugCategoryFilter").addEventListener("change",renderDrugList);
  document.getElementById("drugSpeciesFilter").addEventListener("change",renderDrugList);
}

function renderDrugList(){
  const list=document.getElementById("drugList");
  const search=(document.getElementById("drugSearch").value||"").toLowerCase();
  const cat=document.getElementById("drugCategoryFilter").value;
  const species=document.getElementById("drugSpeciesFilter").value;
  let filtered=allDrugs;
  if(cat)filtered=filtered.filter(d=>d.category===cat);
  if(species)filtered=filtered.filter(d=>d.species_info&&d.species_info[species]);
  if(search)filtered=filtered.filter(d=>(d.name||"").toLowerCase().includes(search)||(d.name_ja||"").toLowerCase().includes(search)||(d.category_ja||"").toLowerCase().includes(search));
  document.getElementById("drugCount").textContent=t("diseaseCount").replace("%filtered%",filtered.length).replace("%total%",allDrugs.length);
  if(filtered.length===0){list.innerHTML=`<div style="padding:20px;text-align:center;color:var(--gray-500)">${t("noDrugMatch")}</div>`;return;}
  filtered=[...filtered].sort((a,b)=>(b.sponsor?1:0)-(a.sponsor?1:0));
  list.innerHTML=filtered.map(d=>{
    const speciesFilter=document.getElementById("drugSpeciesFilter").value;
    let dosageHtml="";
    if(speciesFilter&&d.species_info&&d.species_info[speciesFilter]){
      const si=d.species_info[speciesFilter];
      const safeLabel=si.safe?`<span style="color:var(--green);font-weight:700">\u2713 ${t("safe")}</span>`:`<span style="color:var(--red);font-weight:700">\u2717 ${t("contraindicated")}</span>`;
      const doseText=currentLang==="ja"?(si.dosage_ja||si.dosage||"N/A"):(si.dosage||si.dosage_ja||"N/A");
      const noteText=currentLang==="ja"?(si.notes_ja||si.notes||""):(si.notes||si.notes_ja||"");
      dosageHtml=`<div style="margin-top:4px;font-size:.8rem;padding:6px 10px;background:${si.safe?'#f0fdf4':'#fef2f2'};border-radius:6px">${safeLabel} | ${t("dosageLabel")}${doseText}<br/><span style="color:var(--gray-500)">${noteText}</span></div>`;
    }
    const catLabel=drugCategories[d.category]?(currentLang==="ja"?(drugCategories[d.category].ja||drugCategories[d.category].en):(drugCategories[d.category].en||drugCategories[d.category].ja)):(currentLang==="ja"?(d.category_ja||d.category):(d.category||d.category_ja));
    const sponsorBadge=d.sponsor?'<span style="font-size:.65rem;padding:2px 8px;background:var(--green);color:#fff;border-radius:10px;margin-left:6px;font-weight:600">Sponsor</span>':"";
    const sponsorLink=d.sponsor?`<div style="margin-top:8px;padding:8px 12px;background:var(--green-light);border:1px solid rgba(34,168,79,.3);border-radius:6px;font-size:.8rem"><strong style="color:var(--green-dark)">${d.sponsor_name||"Equine & Canine Vet Nutrition"}</strong><br/><span style="color:var(--gray-600)">${t("sponsorVetLabel")}</span><br/><a href="${d.sponsor_url||d.sponsor_url_dog||'https://www.caninevet.jp/'}" target="_blank" onclick="event.stopPropagation()" style="color:var(--navy);font-weight:600">${t("productDetails")}</a></div>`:"";
    return`<div class="disease-db-item" onclick="this.querySelector('.disease-detail')&&this.querySelector('.disease-detail').classList.toggle('open')" style="${d.sponsor?'border-left:3px solid var(--green)':''}">
      <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:4px">
        <div class="d-name">${d.name} <span class="d-name-ja">${d.name_ja}</span>${sponsorBadge}</div>
        <span style="font-size:.7rem;padding:2px 8px;background:var(--gray-100);color:var(--navy);border-radius:10px;font-weight:600">${catLabel}</span>
      </div>${dosageHtml}
      <div class="disease-detail">${sponsorLink}
        <dl><dt>${t("dtContraindications")}</dt><dd>${currentLang==="ja"?(d.contraindications_ja||d.contraindications||""):(d.contraindications||d.contraindications_ja||"")}</dd></dl>
        ${d.routes_ja||d.routes?`<dl><dt>${t("dtRoutes")}</dt><dd>${currentLang==="ja"?(d.routes_ja||[]).join(", "):(d.routes||[]).join(", ")}</dd></dl>`:""}
        ${d.formulations_ja||d.formulations?`<dl><dt>${t("dtFormulations")}</dt><dd>${currentLang==="ja"?(d.formulations_ja||d.formulations||[]).join(", "):(d.formulations||d.formulations_ja||[]).join(", ")}</dd></dl>`:""}
        ${d.drug_interactions&&d.drug_interactions.length?`<dl><dt>${t("dtInteractions")}</dt><dd>${d.drug_interactions.map(di=>`<span style="display:inline-block;margin:2px 4px 2px 0;padding:2px 6px;background:#fef2f2;border-radius:4px;font-size:.76rem">${di.drug}: ${currentLang==="ja"?(di.effect_ja||di.effect):(di.effect||di.effect_ja)}</span>`).join("")}</dd></dl>`:""}
        <div style="margin-top:8px"><strong style="font-size:.8rem">${t("dtSpeciesInfo")}</strong>
          <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:6px;margin-top:4px">
            ${Object.entries(d.species_info||{}).map(([sp,info])=>{const spName=SPECIES.find(s=>s.id===sp);const label=spName?(currentLang==="ja"?spName.name:spName.nameEn):sp;const dose=currentLang==="ja"?(info.dosage_ja||info.dosage||""):(info.dosage||info.dosage_ja||"");const note=currentLang==="ja"?(info.notes_ja||info.notes||""):(info.notes||info.notes_ja||"");return`<div style="font-size:.76rem;padding:4px 8px;background:${info.safe?'#f0fdf4':'#fef2f2'};border-radius:4px;border:1px solid ${info.safe?'#bbf7d0':'#fecaca'}"><strong>${label}</strong>: ${info.safe?'\u2713':'\u2717'} ${dose}${note?'<br/><span style="color:var(--gray-500)">'+note+'</span>':''}</div>`;}).join("")}
          </div>
        </div>
      </div>
    </div>`;
  }).join("");
}
