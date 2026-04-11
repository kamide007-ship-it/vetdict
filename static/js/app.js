const SPECIES_ICONS={dog:"\u{1F415}",cat:"\u{1F408}",horse:"\u{1F434}",rabbit:"\u{1F407}",hamster:"\u{1F439}",guinea_pig:"\u{1F43E}",chinchilla:"\u{1F43E}",ferret:"\u{1F43E}",hedgehog:"\u{1F994}",sugar_glider:"\u{1F43E}",degu:"\u{1F43E}",bird:"\u{1F426}",parakeet:"\u{1F424}",parrot:"\u{1F99C}",reptile:"\u{1F98E}",tortoise:"\u{1F422}",snake:"\u{1F40D}",lizard:"\u{1F98E}",amphibian:"\u{1F438}",fish:"\u{1F41F}",exotic_other:"\u{1F43E}"};

/* ===== Admin / Pro access control ===== */
// Admin verification handled server-side
// OPEN BETA: All users get Pro access for free.
// Set to false when launching paid plans.
const OPEN_BETA=true;
let isAdmin=false;
let isPro=false;

async function checkAccess(){
  const params=new URLSearchParams(location.search);
  if(OPEN_BETA) isPro=true;
  if(params.get("pro")==="activated"){
    localStorage.setItem("vetdict-pro","1");
    isPro=true;
    history.replaceState(null,"",location.pathname+location.hash);
  }
  const adminParam=params.get("admin");
  if(adminParam){
    try{
      const r=await fetchWithTimeout("/api/admin/verify",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({token:adminParam})},5000);
      const d=await r.json();
      if(d.valid){localStorage.setItem("vetdict-admin","1");isAdmin=true;isPro=true;}
      else{localStorage.removeItem("vetdict-admin");}
    }catch(e){/* network error — skip admin */}
    history.replaceState(null,"",location.pathname+location.hash);
  } else if(localStorage.getItem("vetdict-admin")==="1"){
    isAdmin=true;isPro=true;
  }
  if(!OPEN_BETA&&localStorage.getItem("vetdict-pro")==="1"){
    isPro=true;
    const subId=localStorage.getItem("vetdict-subscription-id");
    if(subId){
      fetchWithTimeout("/api/paypal/verify",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({subscription_id:subId})},5000)
      .then(function(r){return r.json();})
      .then(function(d){if(!d.active){localStorage.removeItem("vetdict-pro");localStorage.removeItem("vetdict-subscription-id");isPro=false;document.body.classList.remove("is-pro");}})
      .catch(function(){});
    }
  }
  document.body.classList.toggle("is-admin",isAdmin);
  document.body.classList.toggle("is-pro",isPro);
  if(isAdmin){
    const badge=document.createElement("div");
    badge.className="admin-badge";
    badge.textContent="Admin";
    badge.title="管理者モード — 全機能アンロック済み";
    document.body.appendChild(badge);
  }
}

/* ===== Bilingual i18n system ===== */
let currentLang="ja";
const I18N={
  ja:{
    skipLink:"メインコンテンツへスキップ",
    logoSub:"獣医師のための臨床意思決定支援",
    navChecker:"鑑別診断",navDatabase:"疾患データベース",navChat:"臨床相談",navDrugs:"薬品辞書",navAnesthesia:"鎮静・麻酔",
    landingChatTitle:"臨床症状から鑑別診断",
    heroTrustRef:"138学術文献に基づく",heroTrustTests:"2,700+自動テスト検証済み",heroTrustOss:"オープンソース開発",
    landingChatHint:'臨床症状を入力すると鑑別疾患リストを生成します。<br/><span style="font-size:.76rem;color:var(--gray-500)">例: 「嘔吐 食欲不振 体重減少」「polyuria polydipsia lethargy」</span>',
    heroBadge:"現役獣医師が開発 — 臨床現場の鑑別診断を支援",
    heroAudience:"獣医師・獣医学生のための臨床支援ツール",
    heroLead:"臨床症状から鑑別疾患リストを即座に生成。<br/>6,393疾患・194薬品・188麻酔プロトコル・21動物種対応の臨床意思決定支援プラットフォーム。",
    heroCta:"動物種を選択して鑑別診断を開始",heroCtaDb:"疾患データベースを見る",
    statDiseases:"疾患数",statSpecies:"対応動物種",statSymptoms:"症状項目",statDrugs:"薬品数",statProtocols:"麻酔プロトコル",
    heroCredit:'開発: <a href="https://www.minamisoma-vet.com/" target="_blank" rel="noopener">南相馬アニマルクリニック</a> 獣医師 上手 健太郎',
    sponsorDesc:"獣医師考案・国内製造・競走馬理化学研究所検査合格",
    sponsorCta:"詳細 →",
    selectSpecies:"動物種を選択",
    cardSymptoms:"&#9745; 症状を選択",cardResults:"&#128202; 検索結果",
    breedLabel:"品種を選択（任意）",breedNone:"品種を選択しない",
    symptomSearchPh:"症状を検索... (例: 咳, vomiting, 下痢)",
    analyzeBtn:"鑑別疾患を検索",checkerGuide:'💡 <strong>使い方:</strong> 上の症状リストからチェックを入れ、「鑑別疾患を検索」を押してください。<br/>症状が多いほど精度が向上します（3つ以上推奨）。',
    resultsEmpty:'動物種を選択し、症状にチェックを入れて<br/>「鑑別疾患を検索」を押してください',
    resultsSelectSymptom:"症状を選択してください",
    cardDiseaseDb:"&#128218; 疾患データベース",
    diseaseSearchPh:"疾患名で検索... (例: 腎臓, colic, 感染)",
    cardChat:"&#128172; 症状相談",
    chatWelcome:'臨床症状を日本語または英語で入力してください。<br/>例: 「3歳猫 嘔吐 食欲廃絶 黄疸」「5yo dog PU/PD weight loss」<br/><br/><em style="font-size:.76rem;color:var(--gray-500)">※ 本ツールは臨床意思決定支援を目的とした参考情報を提供するものです。確定診断には臨床所見・検査結果との総合判断が必要です。</em>',
    chatInputPh:"臨床症状を入力...",chatSend:"送信",
    chatModeFree:"自由入力",chatModeGuided:"問診モード",
    guidedStart:"問診を開始",guidedNext:"次へ",guidedFinish:"結果を見る",guidedMore:"他の症状もある",guidedRestart:"最初からやり直す",
    guidedSelectCategory:"カテゴリを選んでください",guidedSelectSymptoms:"当てはまる症状を選んでください",
    guidedInterimTitle:"現在の診断候補",guidedFinalTitle:"問診結果",
    cardDrugs:"&#128138; 薬品辞書",
    cardAnesthesia:"&#128137; 鎮静・麻酔プロトコル",
    anesthesiaSearchPh:"薬品名・プロトコルを検索... (例: propofol, ketamine, 鎮静)",
    noAnesthesiaMatch:"該当するプロトコルがありません",
    anesthesiaOverviewLabel:"概要",anesthesiaFastingLabel:"絶食指針",
    anesthesiaRiskLow:"低リスク",anesthesiaRiskModerate:"中リスク",anesthesiaRiskHigh:"高リスク",
    anesthesiaDose:"用量",anesthesiaRoute:"投与経路",anesthesiaOnset:"効果発現",anesthesiaDuration:"持続時間",
    anesthesiaMonitoring:"モニタリング項目",anesthesiaTarget:"目標値",
    anesthesiaBreedConsider:"品種別注意事項",anesthesiaSelectSpecies:"動物種を選択すると、種別の鎮静・麻酔プロトコルが表示されます",
    anesthesiaAsaTitle:"ASA身体状態分類",anesthesiaAsaGuidance:"麻酔管理指針",
    anesthesiaWeightLabel:"体重",anesthesiaEmergency:"緊急プロトコル",anesthesiaCalcDose:"計算投与量",anesthesiaCalcRange:"範囲",
    anesthesiaPrint:"麻酔チェックリスト印刷",anesthesiaPrintTitle:"麻酔チェックリスト",
    anesthesiaPrintPatient:"患者情報",anesthesiaPrintSpecies:"動物種",anesthesiaPrintWeight:"体重",anesthesiaPrintDate:"日付",
    anesthesiaPrintPreop:"術前チェック",anesthesiaPrintIntraop:"術中チェック",anesthesiaPrintPostop:"術後チェック",
    anesthesiaPrintPreopItems:"絶食確認,体重測定,血液検査,胸部X線,心電図,静脈カテーテル留置,輸液準備",
    anesthesiaPrintIntraopItems:"モニター装着（SpO2/ETCO2/ECG/BP）,気管チューブサイズ確認,緊急薬品準備（アトロピン/エピネフリン）,保温装置,輸液速度設定",
    anesthesiaPrintPostopItems:"抜管タイミング確認,体温モニタリング,疼痛評価,覚醒状態確認,飲水・食事再開時期",
    anesthesiaAsaFilter:"ASA分類",anesthesiaAsaAll:"全ASA",
    anesthesiaSafetyTitle:"安全性情報",
    anesthesiaContraindicated:"禁忌",anesthesiaCaution:"慎重投与",anesthesiaMonitorExtra:"要モニタリング",
    drugSearchPh:"薬品名で検索... (例: amoxicillin, メロキシカム)",
    allCategories:"全カテゴリ",allSpecies:"全動物種",
    sponsorTagline:"獣医師が考案・国内製造 — 競走馬理化学研究所の検査合格",
    sponsorSpecies:"対応動物種: 馬・犬・猫",
    sponsorEquine:"馬用サプリメント",sponsorCanine:"犬用サプリメント",
    footerDisclaimer:"※ 本サービスは獣医師の臨床意思決定を支援するための参考情報を提供するものであり、確定診断を代替するものではありません。",
    footerCredit:'開発: <a href="https://www.minamisoma-vet.com/" target="_blank" rel="noopener">南相馬アニマルクリニック</a> 獣医師 上手 健太郎 (Kentaro Kamide, DVM)',
    refTitle1:"引用文献・参考資料 ― 疾患データベース",
    refTitle2:"品種疾患リスク・遺伝疾患",
    refTitle3:"症状の臨床的重み付け・尤度比",
    refTitle4:"エキゾチック動物・鳥類・爬虫類",
    refTitle5:"馬疾患データベース",
    refTitle6:"関連サービス・データベース",refTitle7:"薬品辞書",refTitle8:"魚病・水産学",
    // Dynamic UI strings
    analyzing:"解析中...",
    noSymptomData:"症状データを読み込めませんでした",
    noMatchingSymptom:"該当する症状がありません",
    noSymptomsSelected:"症状が選択されていません",
    noDiseasesFound:"一致する疾患は見つかりませんでした",
    loadFailed:"読み込みに失敗しました",
    retry:"再試行",
    reload:"再読み込み",
    networkError:"サーバーとの通信に失敗しました。ネットワーク接続を確認してください。",
    noDiseaseMatch:"該当する疾患がありません",
    noDrugMatch:"該当する薬品がありません",
    errorPrefix:"エラー: ",
    overallAssessment:"総合評価: ",
    commError:"通信エラーが発生しました。",
    noResponse:"応答を取得できませんでした",
    diseaseCount:"%filtered% / %total% 件表示",
    catLabels:{respiratory:"呼吸器",digestive:"消化器",neurological:"神経",musculoskeletal:"運動器",dermatological:"皮膚",urinary:"泌尿器",ophthalmological:"眼",cardiovascular:"循環器",behavioral:"行動",general:"全身",skin:"体表・外観",fins:"鰭",gills:"鰓",eyes:"眼",body:"腹部・体型",parasites:"寄生虫",emergency:"急変",reproductive:"繁殖",behavior:"行動",other:"その他"},
    sevLabels:{low:"軽度",moderate:"中等度",high:"重度",emergency:"緊急"},
    dtDescription:"説明",dtPathophysiology:"病態生理",dtCauses:"原因",dtPrevention:"予防",dtTreatment:"治療",dtPrognosis:"予後",
    dtMatchedSymptoms:"一致した症状",dtRecommendedTests:"推奨検査",dtRecTestList:"推奨検査一覧:",
    dtSymptoms:"症状",
    dtContraindications:"禁忌事項",dtRoutes:"投与経路",dtFormulations:"製剤",dtInteractions:"薬物相互作用",dtSpeciesInfo:"動物種別情報:",
    safe:"安全",contraindicated:"禁忌",dosageLabel:"投与量: ",
    sponsorVetLabel:"獣医師考案・国内製造・競走馬理化学研究所検査合格",
    productDetails:"製品詳細 \u2192",
    speciesCardDisease:"疾患",speciesCardDrug:"薬品",
    menuOpen:"メニューを開く",menuClose:"メニューを閉じる",
    removeLabel:"%s%を削除",
    metabSupport:"代謝サポート",aminoAcid:"アミノ酸",digestSupport:"消化管サポート",jointSupport:"関節・運動器",
    mdCombinations:"疾患の組み合わせ候補",mdAmbiguous:"曖昧な症状が検出されました",mdConfidence:"信頼度分析",mdClarifying:"確認質問",mdGuidance:"診断ガイダンス",mdRecommendations:"推奨事項",mdActive:"複合疾患モード",mdAnalyzing:"複合疾患の組み合わせを分析中...",
    resultsDisclaimer:"本結果は鑑別診断の参考情報です。確定診断・治療方針は臨床所見・検査結果と併せて総合的にご判断ください。",
    feedbackQuestion:"この鑑別診断リストは臨床的に参考になりましたか？",
    feedbackYes:"参考になった",
    feedbackNo:"改善の余地あり",
    feedbackThanks:"フィードバックありがとうございます。",
    shareResults:"鑑別診断結果を共有",shareCopy:"コピー",shareCopied:"コピー済み",
    husbandryTitle:"飼育環境ガイド",husbandryTemp:"適正温度",husbandryHumidity:"適正湿度",husbandryHousing:"飼育環境",husbandryDiet:"食事",husbandryEnrichment:"エンリッチメント",husbandrySocial:"社会性",husbandryNotes:"その他の注意",husbandryLoading:"飼育環境情報を読み込み中...",husbandryError:"飼育環境情報の取得に失敗しました",
  },
  en:{
    skipLink:"Skip to main content",
    logoSub:"Clinical Decision Support for Veterinarians",
    navChecker:"Differential Dx",navDatabase:"Disease Database",navChat:"Clinical Chat",navDrugs:"Drug Dictionary",navAnesthesia:"Anesthesia",
    landingChatTitle:"Differential Diagnosis from Clinical Signs",
    heroTrustRef:"Based on 138 academic references",heroTrustTests:"Verified by 2,700+ automated tests",heroTrustOss:"Open-source development",
    landingChatHint:'Enter clinical signs to generate a differential diagnosis list.<br/><span style="font-size:.76rem;color:var(--gray-500)">e.g. "vomiting anorexia weight loss" "polyuria polydipsia lethargy"</span>',
    heroBadge:"Built by a practicing veterinarian — Clinical decision support",
    heroAudience:"A clinical tool for veterinarians and veterinary students",
    heroLead:"Instantly generate differential diagnosis lists from clinical signs.<br/>6,393 diseases \u00b7 194 drugs \u00b7 188 anesthesia protocols \u00b7 21 species \u2014 a clinical decision support platform for veterinary professionals.",
    heroCta:"Select a species to begin differential diagnosis",heroCtaDb:"Browse Disease Database",
    statDiseases:"Diseases",statSpecies:"Species",statSymptoms:"Symptoms",statDrugs:"Drugs",statProtocols:"Anesthesia",
    heroCredit:'Developed by: <a href="https://www.minamisoma-vet.com/" target="_blank" rel="noopener">Minamisoma Animal Clinic</a> — Kentaro Kamide, DVM',
    sponsorDesc:"Formulated by a veterinarian — Made in Japan — Passed racing lab tests",
    sponsorCta:"Details →",
    selectSpecies:"Select Species",
    cardSymptoms:"&#9745; Select Symptoms",cardResults:"&#128202; Results",
    breedLabel:"Select breed (optional)",breedNone:"No breed selected",
    symptomSearchPh:"Search symptoms... (e.g. cough, vomiting, diarrhea)",
    analyzeBtn:"Search Differential Diagnoses",checkerGuide:'💡 <strong>How to use:</strong> Check symptoms from the list above, then press "Search Differential Diagnoses".<br/>More symptoms = better accuracy (3+ recommended).',
    resultsEmpty:'Select a species, check symptoms, and<br/>press "Search Differential Diagnoses"',
    resultsSelectSymptom:"Please select symptoms",
    cardDiseaseDb:"&#128218; Disease Database",
    diseaseSearchPh:"Search diseases... (e.g. renal, colic, infection)",
    cardChat:"&#128172; Symptom Chat",
    chatWelcome:'Enter clinical signs in Japanese or English.<br/>Examples: "3yo cat vomiting anorexia icterus" "5yo dog PU/PD weight loss"<br/><br/><em style="font-size:.76rem;color:var(--gray-500)">Note: This tool provides clinical decision support. Definitive diagnosis requires integration with clinical findings and diagnostic results.</em>',
    chatInputPh:"Enter clinical signs...",chatSend:"Send",
    chatModeFree:"Free Text",chatModeGuided:"Guided",
    guidedStart:"Start Consultation",guidedNext:"Next",guidedFinish:"See Results",guidedMore:"More Symptoms",guidedRestart:"Start Over",
    guidedSelectCategory:"Select a category",guidedSelectSymptoms:"Select symptoms that apply",
    guidedInterimTitle:"Current Candidates",guidedFinalTitle:"Consultation Results",
    cardDrugs:"&#128138; Drug Dictionary",
    cardAnesthesia:"&#128137; Sedation & Anesthesia Protocols",
    anesthesiaSearchPh:"Search protocols... (e.g. propofol, ketamine, sedation)",
    noAnesthesiaMatch:"No matching protocols",
    anesthesiaOverviewLabel:"Overview",anesthesiaFastingLabel:"Fasting Guidelines",
    anesthesiaRiskLow:"Low Risk",anesthesiaRiskModerate:"Moderate Risk",anesthesiaRiskHigh:"High Risk",
    anesthesiaDose:"Dose",anesthesiaRoute:"Route",anesthesiaOnset:"Onset",anesthesiaDuration:"Duration",
    anesthesiaMonitoring:"Monitoring Parameters",anesthesiaTarget:"Target",
    anesthesiaBreedConsider:"Breed-Specific Considerations",anesthesiaSelectSpecies:"Select a species to view sedation & anesthesia protocols",
    anesthesiaAsaTitle:"ASA Physical Status Classification",anesthesiaAsaGuidance:"Anesthesia Management Guidance",
    anesthesiaWeightLabel:"Weight",anesthesiaEmergency:"Emergency",anesthesiaCalcDose:"Calculated Dose",anesthesiaCalcRange:"range",
    anesthesiaPrint:"Print Checklist",anesthesiaPrintTitle:"Anesthesia Checklist",
    anesthesiaPrintPatient:"Patient Information",anesthesiaPrintSpecies:"Species",anesthesiaPrintWeight:"Weight",anesthesiaPrintDate:"Date",
    anesthesiaPrintPreop:"Preoperative Checklist",anesthesiaPrintIntraop:"Intraoperative Checklist",anesthesiaPrintPostop:"Postoperative Checklist",
    anesthesiaPrintPreopItems:"Fasting confirmed,Body weight recorded,Blood work,Thoracic radiographs,ECG,IV catheter placed,Fluids prepared",
    anesthesiaPrintIntraopItems:"Monitors attached (SpO2/ETCO2/ECG/BP),ETT size confirmed,Emergency drugs ready (atropine/epinephrine),Warming device,Fluid rate set",
    anesthesiaPrintPostopItems:"Extubation timing confirmed,Temperature monitoring,Pain assessment,Recovery status,Water/food resumption timing",
    anesthesiaAsaFilter:"ASA Class",anesthesiaAsaAll:"All ASA",
    anesthesiaSafetyTitle:"Safety Information",
    anesthesiaContraindicated:"Contraindicated",anesthesiaCaution:"Use with Caution",anesthesiaMonitorExtra:"Extra Monitoring",
    drugSearchPh:"Search drugs... (e.g. amoxicillin, meloxicam)",
    allCategories:"All Categories",allSpecies:"All Species",
    sponsorTagline:"Formulated by a veterinarian — Made in Japan — Passed racing lab tests",
    sponsorSpecies:"Supported species: Horse, Dog, Cat",
    sponsorEquine:"Equine Supplements",sponsorCanine:"Canine Supplements",
    footerDisclaimer:"Note: This service provides clinical decision support for veterinary professionals. It does not replace definitive diagnosis.",
    footerCredit:'Developed by: <a href="https://www.minamisoma-vet.com/" target="_blank" rel="noopener">Minamisoma Animal Clinic</a> — Kentaro Kamide, DVM',
    refTitle1:"References — Disease Database",
    refTitle2:"Breed Disease Risks & Genetic Disorders",
    refTitle3:"Clinical Symptom Weighting & Likelihood Ratios",
    refTitle4:"Exotic Animals, Birds & Reptiles",
    refTitle5:"Equine Disease Database",
    refTitle6:"Related Services & Databases",refTitle7:"Drug Dictionary",refTitle8:"Fish Diseases & Aquatic Medicine",
    analyzing:"Analyzing...",
    noSymptomData:"Failed to load symptom data",
    noMatchingSymptom:"No matching symptoms",
    noSymptomsSelected:"No symptoms selected",
    noDiseasesFound:"No matching diseases found",
    loadFailed:"Failed to load",
    retry:"Retry",
    reload:"Reload",
    networkError:"Failed to connect to server. Please check your network.",
    noDiseaseMatch:"No matching diseases",
    noDrugMatch:"No matching drugs",
    errorPrefix:"Error: ",
    overallAssessment:"Overall: ",
    commError:"A communication error occurred.",
    noResponse:"Could not retrieve response",
    diseaseCount:"%filtered% / %total% shown",
    catLabels:{respiratory:"Respiratory",digestive:"Digestive",neurological:"Neurological",musculoskeletal:"Musculoskeletal",dermatological:"Dermatological",urinary:"Urinary",ophthalmological:"Ophthalmological",cardiovascular:"Cardiovascular",behavioral:"Behavioral",general:"General",skin:"Skin & Appearance",fins:"Fins",gills:"Gills",eyes:"Eyes",body:"Body & Shape",parasites:"Parasites",emergency:"Emergency",reproductive:"Reproductive",behavior:"Behavior",other:"Other"},
    sevLabels:{low:"Mild",moderate:"Moderate",high:"Severe",emergency:"Emergency"},
    dtDescription:"Description",dtPathophysiology:"Pathophysiology",dtCauses:"Causes",dtPrevention:"Prevention",dtTreatment:"Treatment",dtPrognosis:"Prognosis",
    dtMatchedSymptoms:"Matched Symptoms",dtRecommendedTests:"Recommended Tests",dtRecTestList:"Recommended Tests:",
    dtSymptoms:"Symptoms",
    dtContraindications:"Contraindications",dtRoutes:"Routes",dtFormulations:"Formulations",dtInteractions:"Drug Interactions",dtSpeciesInfo:"Species Information:",
    safe:"Safe",contraindicated:"Contraindicated",dosageLabel:"Dosage: ",
    sponsorVetLabel:"Formulated by a veterinarian — Made in Japan — Passed racing lab tests",
    productDetails:"Product details \u2192",
    speciesCardDisease:"diseases",speciesCardDrug:"drugs",
    menuOpen:"Open menu",menuClose:"Close menu",
    removeLabel:"Remove %s%",
    metabSupport:"Metabolic Support",aminoAcid:"Amino Acids",digestSupport:"Digestive Support",jointSupport:"Joint & Mobility",
    mdCombinations:"Possible Disease Combinations",mdAmbiguous:"Ambiguous Symptoms Detected",mdConfidence:"Confidence Analysis",mdClarifying:"Clarifying Questions",mdGuidance:"Diagnostic Guidance",mdRecommendations:"Recommendations",mdActive:"Multi-Disease Mode Active",mdAnalyzing:"Analyzing multi-disease combinations...",
    resultsDisclaimer:"These results are for clinical reference. Final diagnosis and treatment decisions should integrate clinical findings and diagnostic results.",
    feedbackQuestion:"Was this differential diagnosis list clinically useful?",
    feedbackYes:"Helpful",
    feedbackNo:"Could improve",
    feedbackThanks:"Thank you for your feedback.",
    shareResults:"Share results",shareCopy:"Copy",shareCopied:"Copied!",
    husbandryTitle:"Care Environment Guide",husbandryTemp:"Temperature",husbandryHumidity:"Humidity",husbandryHousing:"Housing",husbandryDiet:"Diet",husbandryEnrichment:"Enrichment",husbandrySocial:"Socialization",husbandryNotes:"Additional Notes",husbandryLoading:"Loading care information...",husbandryError:"Failed to load care information",
  }
};

function t(key){return (I18N[currentLang]&&I18N[currentLang][key])||key;}

function fetchWithTimeout(url,opts={},timeoutMs=10000){
  const ctrl=new AbortController();
  const timer=setTimeout(()=>ctrl.abort(),timeoutMs);
  return fetch(url,{...opts,signal:ctrl.signal}).finally(()=>clearTimeout(timer));
}

function applyLanguage(){
  document.documentElement.lang=currentLang;
  document.title=currentLang==="ja"?"Vet Dict — 多動物種対応 獣医学疾患データベース":"Vet Dict — Multi-Species Veterinary Disease Database";
  // Update data-i18n (textContent)
  document.querySelectorAll("[data-i18n]").forEach(el=>{
    const key=el.getAttribute("data-i18n");
    const val=t(key);
    if(val&&val!==key)el.textContent=val;
  });
  // Update data-i18n-html (innerHTML — sanitized to allow only safe tags)
  document.querySelectorAll("[data-i18n-html]").forEach(el=>{
    const key=el.getAttribute("data-i18n-html");
    const val=t(key);
    if(val&&val!==key){
      const tmp=document.createElement("div");tmp.innerHTML=val;
      // Allowlist: only keep safe elements and attributes
      const SAFE_TAGS=new Set(["a","br","strong","em","span","b","i","u","small","sub","sup"]);
      const SAFE_ATTRS=new Set(["href","target","rel","style","class"]);
      tmp.querySelectorAll("*").forEach(n=>{
        if(!SAFE_TAGS.has(n.tagName.toLowerCase())){n.remove();return;}
        for(const a of[...n.attributes]){if(!SAFE_ATTRS.has(a.name))n.removeAttribute(a.name);}
        if(n.tagName==="A"){const hr=n.getAttribute("href")||"";if(hr.startsWith("javascript:"))n.removeAttribute("href");}
      });
      el.innerHTML=tmp.innerHTML;
    }
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
  if(allDiseases.length){diseaseNavMode=currentLang==="ja"?"category":"az";diseaseFilter="";renderAzNav();renderDiseaseDb();}
  if(drugsLoaded)renderDrugList();
  if(anesthesiaLoaded)reloadAnesthesiaForSpecies();
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

/* ===== GA4 Analytics Helper ===== */
function trackEvent(name,params){
  if(typeof gtag==="function") gtag("event",name,params||{});
}

let currentSpecies=null,selectedSymptoms=new Set(),symptomData=[],allDiseases=[],diseaseFilter="",currentBreed="";
let symptomRequestId=0,diseaseRequestId=0,breedRequestId=0;
let symptomSortMode="category";

/* Session engagement tracking */
const _sessionStart=Date.now();
let _maxScrollPct=0;
window.addEventListener("scroll",function(){const h=document.documentElement;const pct=Math.round((h.scrollTop/(h.scrollHeight-h.clientHeight||1))*100);if(pct>_maxScrollPct)_maxScrollPct=pct;},{passive:true});
document.addEventListener("visibilitychange",function(){if(document.visibilityState==="hidden"){const dur=Math.round((Date.now()-_sessionStart)/1000);trackEvent("session_engagement",{duration_sec:dur,max_scroll_pct:_maxScrollPct,species_used:currentSpecies||"none",analyses_done:loadDiagnosisHistory().length});}});

document.addEventListener("DOMContentLoaded",async()=>{
  /* Funnel step 0: page load */
  trackEvent("funnel_page_load",{referrer:document.referrer.substring(0,100),lang:currentLang});
  try{
    await checkAccess();
    loadSpeciesStats();
    setupNavigation();
    setupChat();
    setupGuidedConsultation();
    setupHamburger();
    setupLanguageToggle();
    const symptomSearch=document.getElementById("symptomSearch");
    const analyzeBtn=document.getElementById("analyzeBtn");
    const diseaseSearch=document.getElementById("diseaseSearch");
    if(symptomSearch)symptomSearch.addEventListener("input",debounce(()=>{renderSymptomList(symptomData);if(symptomSearch.value.length>=2)trackEvent("symptom_search",{species:currentSpecies,query:symptomSearch.value.substring(0,50)});},300));
    if(analyzeBtn)analyzeBtn.addEventListener("click",doAnalyze);
    if(diseaseSearch)diseaseSearch.addEventListener("input",debounce(()=>{diseaseDisplayLimit=100;renderDiseaseDb();},200));
    // Restore view from URL hash
    const hash=location.hash.replace("#","");
    if(hash&&["checker","database","chat","drugs","anesthesia"].includes(hash))switchView(hash);
    // Handle ?species= query param (from sitemap/SEO links)
    const spParam=new URLSearchParams(location.search).get("species");
    if(spParam&&SPECIES_ICONS[spParam])selectSpecies(spParam);
    // Search clear buttons (replaces inline onclick)
    document.querySelectorAll('[data-action="clear-search"]').forEach(btn=>{
      btn.addEventListener("click",()=>{const inp=btn.previousElementSibling;inp.value='';inp.dispatchEvent(new Event('input'));inp.focus();});
    });
    // Clear lab values button
    const clearLabBtn=document.getElementById("clearLabBtn");
    if(clearLabBtn)clearLabBtn.addEventListener("click",clearLabValues);
    // References toggle (replaces inline onclick)
    const refHeader=document.querySelector(".ref-header");
    if(refHeader){
      refHeader.addEventListener("click",()=>{
        const expanded=refHeader.getAttribute("aria-expanded")==="false";
        refHeader.setAttribute("aria-expanded",expanded);
        document.getElementById("refContent").classList.toggle("ref-open");
      });
      refHeader.addEventListener("keydown",(e)=>{
        if(e.key==="Enter"||e.key===" "){e.preventDefault();refHeader.click();}
      });
    }
    /* Attach click/keyboard handlers to all DB list containers at init (event delegation).
       These containers exist in static HTML and never get replaced — only their innerHTML changes.
       Attaching once at init avoids timing issues with async data loading. */
    ["diseaseDbList","drugList","anesthesiaList"].forEach(id=>{
      const el=document.getElementById(id);
      if(el&&!el.dataset.handlersAttached){el.dataset.handlersAttached="1";_attachDbItemHandlers(el);}
    });
    /* Returning user welcome */
    showReturningUserBanner();
  }catch(e){
    console.error("Error in DOMContentLoaded:",e);
  }
});

function showReturningUserBanner(){
  const history=loadDiagnosisHistory();
  if(!history.length)return;
  const heroContent=document.querySelector(".hero-content");
  if(!heroContent)return;
  const lastEntry=history[0];
  const sp=SPECIES.find(s=>s.id===lastEntry.species);
  if(!sp)return;
  const spName=currentLang==="ja"?sp.name:sp.nameEn;
  const topDisease=lastEntry.topDiseases&&lastEntry.topDiseases[0]?(currentLang==="ja"?(lastEntry.topDiseases[0].name_ja||lastEntry.topDiseases[0].name):lastEntry.topDiseases[0].name):"";
  const date=new Date(lastEntry.date).toLocaleDateString(currentLang==="ja"?"ja-JP":"en-US",{month:"short",day:"numeric"});
  const banner=document.createElement("div");
  banner.style.cssText="margin-top:12px;padding:10px 16px;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.2);border-radius:8px;font-size:.82rem;color:rgba(255,255,255,.9);backdrop-filter:blur(4px)";
  banner.innerHTML=currentLang==="ja"
    ?`📋 前回の診断: <strong>${escapeHtml(spName)}</strong> — ${escapeHtml(topDisease)} (${date}) <a href="/?species=${lastEntry.species}#checker" style="color:var(--green);margin-left:8px;font-weight:600">続きを見る →</a>`
    :`📋 Last diagnosis: <strong>${escapeHtml(spName)}</strong> — ${escapeHtml(topDisease)} (${date}) <a href="/?species=${lastEntry.species}#checker" style="color:var(--green);margin-left:8px;font-weight:600">Continue →</a>`;
  heroContent.appendChild(banner);
}

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
  if(pendingStats.protocols!==undefined)animateCount(document.getElementById("statProtocols"),pendingStats.protocols,dur||900);
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
    fetchWithTimeout("/api/dashboard-stats").then(r=>r.json()),
    fetchWithTimeout("/api/species-stats").then(r=>r.json()),
    fetchWithTimeout("/api/health-check/symptoms").then(r=>r.json())
  ]).then(([dashStats,speciesData,sd])=>{
    try{
      // Check if API returned an error response
      if(!speciesData.species||!Array.isArray(speciesData.species)){
        throw new Error("Invalid species data structure from API");
      }
      SPECIES=speciesData.species.map(sp=>({...sp,icon:SPECIES_ICONS[sp.id]||"\u{1F43E}"}));
      // Use dashboard stats for all counts (fully dynamic, no hardcoded values)
      pendingStats={
        diseases:dashStats.total_diseases||0,
        species:dashStats.total_species||SPECIES.length,
        drugs:dashStats.total_drugs||0,
        symptoms:sd.symptoms?sd.symptoms.length:0,
        protocols:dashStats.total_protocols||0
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
    {id:"dog",name:"犬",nameEn:"Dog",icon:"\u{1F415}",diseases:575,drugs:0,description:"Comprehensive disease dictionary for dogs",description_ja:"最も一般的なペットの疾患辞典"},
    {id:"cat",name:"猫",nameEn:"Cat",icon:"\u{1F408}",diseases:530,drugs:0,description:"Feline-specific diseases and symptoms",description_ja:"猫特有の疾患と症状"},
    {id:"horse",name:"馬",nameEn:"Horse",icon:"\u{1F434}",diseases:656,drugs:0,description:"Equine diseases and musculoskeletal disorders",description_ja:"馬の疾患・運動器障害を網羅"},
    {id:"rabbit",name:"うさぎ",nameEn:"Rabbit",icon:"\u{1F407}",diseases:414,drugs:0,description:"Common rabbit digestive and dental diseases",description_ja:"うさぎに多い消化器・歯科疾患"},
    {id:"hamster",name:"ハムスター",nameEn:"Hamster",icon:"\u{1F439}",diseases:285,drugs:0,description:"Hamster tumors, skin conditions, and more",description_ja:"ハムスターの腫瘍・皮膚疾患など"},
    {id:"guinea_pig",name:"モルモット",nameEn:"Guinea Pig",icon:"\u{1F43E}",diseases:308,drugs:0,description:"Vitamin C deficiency and respiratory diseases",description_ja:"ビタミンC欠乏症や呼吸器疾患"},
    {id:"chinchilla",name:"チンチラ",nameEn:"Chinchilla",icon:"\u{1F43E}",diseases:246,drugs:0,description:"Chinchilla dental and digestive conditions",description_ja:"チンチラの歯科・消化器疾患"},
    {id:"ferret",name:"フェレット",nameEn:"Ferret",icon:"\u{1F43E}",diseases:241,drugs:0,description:"Ferret endocrine and neoplastic diseases",description_ja:"フェレットの内分泌・腫瘍疾患"},
    {id:"hedgehog",name:"ハリネズミ",nameEn:"Hedgehog",icon:"\u{1F994}",diseases:210,drugs:0,description:"Hedgehog skin and neurological conditions",description_ja:"ハリネズミの皮膚・神経疾患"},
    {id:"sugar_glider",name:"フクロモモンガ",nameEn:"Sugar Glider",icon:"\u{1F43E}",diseases:188,drugs:0,description:"Nutritional diseases and stress-related conditions",description_ja:"栄養性疾患やストレス関連症状"},
    {id:"degu",name:"デグー",nameEn:"Degu",icon:"\u{1F43E}",diseases:178,drugs:0,description:"Degu diabetes and dental diseases",description_ja:"デグーの糖尿病・歯科疾患"},
    {id:"bird",name:"鳥",nameEn:"Bird",icon:"\u{1F426}",diseases:479,drugs:0,description:"Avian infections and nutritional diseases",description_ja:"鳥類全般の感染症・栄養疾患"},
    {id:"parakeet",name:"インコ",nameEn:"Parakeet",icon:"\u{1F99C}",diseases:402,drugs:0,description:"Parakeet respiratory and feather disorders",description_ja:"インコの呼吸器・羽毛疾患"},
    {id:"parrot",name:"オウム",nameEn:"Parrot",icon:"\u{1F99C}",diseases:251,drugs:0,description:"Psittacosis, PBFD, and large parrot diseases",description_ja:"オウム病やPBFDなど大型鳥の疾患"},
    {id:"reptile",name:"爬虫類",nameEn:"Reptile",icon:"\u{1F98E}",diseases:250,drugs:0,description:"Metabolic bone disease and general reptile conditions",description_ja:"爬虫類全般の代謝性骨疾患など"},
    {id:"tortoise",name:"リクガメ",nameEn:"Tortoise",icon:"\u{1F422}",diseases:256,drugs:0,description:"Tortoise shell and respiratory disorders",description_ja:"リクガメの甲羅・呼吸器疾患"},
    {id:"snake",name:"ヘビ",nameEn:"Snake",icon:"\u{1F40D}",diseases:214,drugs:0,description:"Snake respiratory infections and dysecdysis",description_ja:"ヘビの呼吸器感染症・脱皮異常"},
    {id:"lizard",name:"トカゲ",nameEn:"Lizard",icon:"\u{1F98E}",diseases:218,drugs:0,description:"Lizard parasitic and metabolic diseases",description_ja:"トカゲの寄生虫症・代謝疾患"},
    {id:"amphibian",name:"両生類",nameEn:"Amphibian",icon:"\u{1F438}",diseases:215,drugs:0,description:"Chytrid fungus and amphibian diseases",description_ja:"カエル・イモリのツボカビ症など"},
    {id:"fish",name:"魚",nameEn:"Fish",icon:"\u{1F41F}",diseases:25,drugs:23,description:"Ich, fin rot, dropsy and aquarium fish diseases",description_ja:"白点病・尾ぐされ病・松かさ病など観賞魚の疾患"},
    {id:"exotic_other",name:"その他エキゾチック",nameEn:"Exotic Other",icon:"\u{1F43E}",diseases:250,drugs:0,description:"Diseases of other exotic animals",description_ja:"その他のエキゾチックアニマルの疾患"},
  ];
  pendingStats={
    diseases:6393,
    species:21,
    drugs:194,
    symptoms:52,
    protocols:188
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
  const groups=currentLang==="ja"?{
    "犬・猫":["dog","cat"],
    "小動物":["rabbit","hamster","guinea_pig","chinchilla","ferret","hedgehog","sugar_glider","degu"],
    "鳥類":["bird","parakeet","parrot"],
    "爬虫類・両生類・魚":["reptile","tortoise","snake","lizard","amphibian","fish"],
    "馬・その他":["horse","exotic_other"],
  }:{
    "Dogs & Cats":["dog","cat"],
    "Small Animals":["rabbit","hamster","guinea_pig","chinchilla","ferret","hedgehog","sugar_glider","degu"],
    "Birds":["bird","parakeet","parrot"],
    "Reptiles, Amphibians & Fish":["reptile","tortoise","snake","lizard","amphibian","fish"],
    "Equine & Other":["horse","exotic_other"],
  };
  let html="";
  for(const[groupName,ids] of Object.entries(groups)){
    const members=ids.map(id=>SPECIES.find(s=>s.id===id)).filter(Boolean);
    if(!members.length)continue;
    html+=`<div class="species-group-label">${groupName}</div>`;
    html+=members.map(sp=>{
      const primary=currentLang==="ja"?sp.name:sp.nameEn;
      const secondary=currentLang==="ja"?sp.nameEn:sp.name;
      const desc=currentLang==="ja"?(sp.description_ja||sp.description||""):(sp.description||sp.description_ja||"");
      const dLabel=t("speciesCardDisease"),drLabel=t("speciesCardDrug");
      return`<div class="species-card" role="button" tabindex="0" aria-pressed="${currentSpecies===sp.id}" data-species="${sp.id}">
        <span class="icon" aria-hidden="true">${sp.icon}</span>
        <div class="name">${primary}</div>
        <div class="count">${secondary}</div>
        ${desc?`<div class="species-desc">${desc}</div>`:""}
        <div class="count" style="margin-top:2px">${sp.diseases}${dLabel}${sp.drugs?' · '+sp.drugs+drLabel:''}</div>
      </div>`}).join("");
  }
  grid.innerHTML=html;
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
  trackEvent("select_species",{species:id});
  currentSpecies=id;selectedSymptoms.clear();currentBreed="";
  document.querySelectorAll(".species-card").forEach(c=>{
    const sel=c.dataset.species===id;
    c.setAttribute("aria-pressed",sel);
  });
  renderSelectedSymptoms();loadSymptoms(id);loadDiseaseDb(id);loadBreeds(id);updateLabRangesForSpecies(id);updatePainScaleVisibility();loadHusbandry(id);reloadAnesthesiaForSpecies();
  resetSpeciesChat(id);
  // Reset guided consultation if active
  const guidedCont=document.getElementById("chatGuidedContainer");
  if(guidedCont&&!guidedCont.classList.contains("hidden")){startGuidedConsultation();}
  else{guidedState.species=id;}
  const sp=SPECIES.find(s=>s.id===id);
  if(sp&&typeof showToast==="function"){const label=currentLang==="ja"?sp.name:sp.nameEn;showToast(currentLang==="ja"?`${label}を選択しました`:`${label} selected`,"success");}
  const resultsArea=document.getElementById("resultsArea");
  if(resultsArea)resultsArea.innerHTML=`<div class="results-empty"><span class="big-icon" aria-hidden="true">\u{1F50D}</span><p>${t("resultsSelectSymptom")}</p></div>${renderHistoryPanel()}`;
}

function resetSpeciesChat(species){
  chatAccumulatedSymptoms=[];
  const sp=SPECIES.find(s=>s.id===species);
  const spLabel=sp?(currentLang==="ja"?sp.name:sp.nameEn):(species||"dog");
  const hint=currentLang==="ja"?`${spLabel}の症状を入力してください。`:`Please describe ${spLabel} symptoms.`;
  /* Quick symptom buttons per species */
  const quickSymptoms=currentLang==="ja"?{
    dog:["嘔吐している","元気がない","下痢している","咳が出る","足を引きずる","皮膚が痒い"],
    cat:["食べない","吐いた","くしゃみ","目やにが出る","おしっこが出ない","毛が抜ける"],
    rabbit:["糞が小さい","食べない","歯ぎしり","首が傾いている","お腹が張っている","鼻水"],
    chinchilla:["よだれが出る","毛が抜ける","食べない","糞が出ない","歯が伸びている","砂浴びしない"],
    hamster:["下痢","元気がない","毛が抜ける","目が開かない","お腹が膨れている","食べない"],
    guinea_pig:["食べない","鼻水","足を引きずる","脱毛","下痢","くしゃみ"],
    ferret:["ぐったり","脱毛","下痢","後ろ足がふらつく","嘔吐","食べない"],
    hedgehog:["針が抜ける","フケ","ふらつく","食べない","目が出ている","体重が減った"],
    bird:["羽を膨らませている","食べない","下痢","鼻水","羽が抜ける","くしゃみ"],
  }:{
    dog:["vomiting","lethargic","diarrhea","coughing","limping","itchy skin"],
    cat:["not eating","vomiting","sneezing","eye discharge","can't urinate","hair loss"],
    rabbit:["small feces","not eating","teeth grinding","head tilt","bloated","nasal discharge"],
  };
  const btns=(quickSymptoms[species]||[]).map(s=>
    `<button class="quick-sym-btn" style="display:inline-block;padding:4px 10px;margin:2px;background:var(--gray-50);border:1px solid var(--gray-200);border-radius:12px;font-size:.76rem;cursor:pointer;color:var(--navy);transition:all .15s" data-symptom="${escapeHtml(s)}">${s}</button>`
  ).join("");
  const quickHtml=btns?`<div style="margin-top:6px;font-size:.72rem;color:var(--gray-400)">${currentLang==="ja"?"💬 タップで入力:":"💬 Quick input:"}</div><div style="margin-top:4px">${btns}</div>`:"";
  ["chatMessages","landingChatMessages"].forEach(id=>{
    const el=document.getElementById(id);
    if(el){
      el.innerHTML=`<div class="chat-msg bot">${escapeHtml(hint)}${quickHtml}</div>`;
      el.querySelectorAll(".quick-sym-btn").forEach(btn=>{
        btn.addEventListener("click",function(){
          const input=document.getElementById("chatInput")||document.getElementById("landingChatInput");
          const send=document.getElementById("chatSend")||document.getElementById("landingChatSend");
          if(input){input.value=this.dataset.symptom||this.textContent;}
          if(send)send.click();
        });
      });
    }
  });
}

let cachedBreeds=[];
function loadBreeds(species){
  const requestId=++breedRequestId;
  const area=document.getElementById("breedSelectArea");
  const select=document.getElementById("breedSelect");
  select.innerHTML=`<option value="">${t("breedNone")}</option>`;
  currentBreed="";cachedBreeds=[];
  const ecoPanel=document.getElementById("breedEcologyPanel");
  if(ecoPanel)ecoPanel.innerHTML="";
  fetchWithTimeout("/api/breeds/"+species).then(r=>r.json()).then(data=>{
    if(requestId!==breedRequestId||species!==currentSpecies)return;
    if(data.breeds&&data.breeds.length>0){
      cachedBreeds=data.breeds;
      data.breeds.forEach(b=>{select.insertAdjacentHTML("beforeend",`<option value="${escapeHtml(b.id)}">${escapeHtml(b.name_ja)} (${escapeHtml(b.name)})</option>`);});
      area.classList.remove("hidden");
    }else{area.classList.add("hidden");}
  }).catch(()=>{if(requestId===breedRequestId)area.classList.add("hidden");});
  select.onchange=function(){currentBreed=this.value;showBreedEcologyPanel(this.value);};
}
function showBreedEcologyPanel(breedId){
  const panel=document.getElementById("breedEcologyPanel");
  if(!panel)return;
  if(!breedId){panel.innerHTML="";return;}
  const breed=cachedBreeds.find(b=>b.id===breedId);
  const eco=breed&&breed.ecology?breed.ecology:null;
  if(!eco){panel.innerHTML="";return;}
  const bName=currentLang==="ja"?(breed.name_ja||breed.name):breed.name;
  const rows=[];
  if(eco.lifespan)rows.push({icon:"⏱",label:currentLang==="ja"?"平均寿命":"Lifespan",val:`${eco.lifespan.min}–${eco.lifespan.max} ${eco.lifespan.unit==="years"?(currentLang==="ja"?"年":"yrs"):eco.lifespan.unit}`});
  if(eco.weight)rows.push({icon:"⚖️",label:currentLang==="ja"?"体重":"Weight",val:`${eco.weight.min}–${eco.weight.max} ${eco.weight.unit}`});
  if(eco.temperature)rows.push({icon:"🌡",label:currentLang==="ja"?"適正温度":"Temperature",val:`${eco.temperature.min}–${eco.temperature.max}${eco.temperature.unit}`});
  if(eco.humidity)rows.push({icon:"💧",label:currentLang==="ja"?"適正湿度":"Humidity",val:`${eco.humidity.min}–${eco.humidity.max}${eco.humidity.unit}`});
  const diet=currentLang==="ja"?(eco.diet_ja||eco.diet||""):(eco.diet||eco.diet_ja||"");
  const housing=currentLang==="ja"?(eco.housing_ja||eco.housing||""):(eco.housing||eco.housing_ja||"");
  const notes=currentLang==="ja"?(eco.notes_ja||eco.notes||""):(eco.notes||eco.notes_ja||"");
  panel.innerHTML=`<div class="breed-ecology-section" style="margin-top:10px">
    <div class="breed-ecology-header">🐾 ${escapeHtml(bName)} ${currentLang==="ja"?"の生態・飼育環境":"Ecology & Husbandry"}</div>
    <div class="breed-ecology-grid">${rows.map(r=>`<div class="breed-ecology-item"><span class="breed-ecology-icon">${r.icon}</span><span class="breed-ecology-label">${r.label}</span><span class="breed-ecology-val">${r.val}</span></div>`).join("")}</div>
    ${diet?`<div class="breed-ecology-field"><strong>${currentLang==="ja"?"食事":"Diet"}:</strong> ${escapeHtml(diet)}</div>`:""}
    ${housing?`<div class="breed-ecology-field"><strong>${currentLang==="ja"?"飼育環境":"Housing"}:</strong> ${escapeHtml(housing)}</div>`:""}
    ${notes?`<div class="breed-ecology-field"><strong>${currentLang==="ja"?"特記事項":"Notes"}:</strong> ${escapeHtml(notes)}</div>`:""}
  </div>`;
}

function loadSymptoms(species){
  const requestId=++symptomRequestId;
  const list=document.getElementById("symptomList");
  if(list)list.innerHTML='<div class="skeleton skeleton-line" style="margin:12px"></div><div class="skeleton skeleton-line medium" style="margin:12px"></div><div class="skeleton skeleton-line short" style="margin:12px"></div><div class="skeleton skeleton-line" style="margin:12px"></div>';
  fetchWithTimeout(`/api/species/${species}/symptoms`).then(r=>r.json()).then(data=>{
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

function toggleSymptomSort(){symptomSortMode=symptomSortMode==="category"?(currentLang==="ja"?"kana":"az"):"category";renderSymptomList(symptomData);}
function renderSymptomList(symptoms){
  const symptomSearch=document.getElementById("symptomSearch");
  const list=document.getElementById("symptomList");
  if(!list){console.warn("symptomList element not found");return;}
  const search=(symptomSearch?.value||"").toLowerCase();
  const sortLabel=symptomSortMode==="category"?(currentLang==="ja"?"あいうえお順":"A-Z"):(currentLang==="ja"?"カテゴリ順":"By Category");
  let html=`<button class="symptom-sort-toggle" aria-label="Switch sort mode">${escapeHtml(sortLabel)}</button>`;
  const mkItem=s=>{const sel=selectedSymptoms.has(s.id);const primary=currentLang==="ja"?(s.name_ja||s.name_en):(s.name_en||s.name_ja);const secondary=currentLang==="ja"?(s.name_en||""):(s.name_ja||"");return`<div class="symptom-item" role="checkbox" aria-checked="${sel}" tabindex="0" data-id="${escapeHtml(s.id)}"><span class="sym-icon" aria-hidden="true">${sel?"\u2713":"+"}</span><span>${escapeHtml(primary)} <span style="color:var(--gray-600)">${escapeHtml(secondary)}</span></span></div>`;};
  const matchSearch=s=>{if(!search)return true;return(s.name_ja||"").toLowerCase().includes(search)||(s.name_en||"").toLowerCase().includes(search)||(s.id||"").toLowerCase().includes(search);};
  if(symptomSortMode==="category"){
    const categories={};
    symptoms.forEach(s=>{const cat=s.category||"other";if(!categories[cat])categories[cat]=[];categories[cat].push(s);});
    const catLabels=t("catLabels");
    for(const[cat,items]of Object.entries(categories)){
      const filtered=items.filter(matchSearch);
      if(!filtered.length)continue;
      html+=`<div class="symptom-cat" role="heading" aria-level="4">${catLabels[cat]||cat}</div>`;
      for(const s of filtered)html+=mkItem(s);
    }
  }else{
    const sorted=symptoms.filter(matchSearch).slice().sort((a,b)=>{const an=currentLang==="ja"?(a.name_ja||a.name_en||""):(a.name_en||a.name_ja||"");const bn=currentLang==="ja"?(b.name_ja||b.name_en||""):(b.name_en||b.name_ja||"");return an.localeCompare(bn,currentLang==="ja"?"ja":"en");});
    for(const s of sorted)html+=mkItem(s);
  }
  list.innerHTML=html||`<div style="padding:20px;text-align:center;color:var(--gray-500)">${t("noMatchingSymptom")}</div>`;
  const sortToggle=list.querySelector(".symptom-sort-toggle");
  if(sortToggle)sortToggle.addEventListener("click",toggleSymptomSort);
  list.onclick=e=>{const item=e.target.closest(".symptom-item");if(item)toggleSymptom(item.dataset.id);};
  list.onkeydown=e=>{const item=e.target.closest(".symptom-item");if(item&&(e.key==="Enter"||e.key===" ")){e.preventDefault();toggleSymptom(item.dataset.id);}};
}

function toggleSymptom(id){const adding=!selectedSymptoms.has(id);if(adding)selectedSymptoms.add(id);else selectedSymptoms.delete(id);renderSelectedSymptoms();renderSymptomList(symptomData);if(adding)trackEvent("add_symptom",{species:currentSpecies,symptom:id,total:selectedSymptoms.size});}

function renderSelectedSymptoms(){
  const area=document.getElementById("selectedSymptoms"),btn=document.getElementById("analyzeBtn");
  if(selectedSymptoms.size===0){area.innerHTML=`<span style="color:var(--gray-500);font-size:.78rem">${t("noSymptomsSelected")}</span>`;btn.disabled=true;return;}
  btn.disabled=false;
  area.innerHTML=[...selectedSymptoms].map(id=>{const sym=symptomData.find(s=>s.id===id);const label=sym?(currentLang==="ja"?(sym.name_ja||sym.name_en):(sym.name_en||sym.name_ja)):id;const ariaLabel=t("removeLabel").replace("%s%",label);return`<span class="selected-tag">${escapeHtml(label)} <button class="remove" type="button" aria-label="${escapeHtml(ariaLabel)}" data-id="${escapeHtml(id)}">&times;</button></span>`;}).join("");
  area.querySelectorAll(".remove").forEach(b=>b.addEventListener("click",e=>{e.stopPropagation();toggleSymptom(b.dataset.id);}));
}

function collectPainScore(){
  const checked=document.querySelector('#painScaleOptions input[name="painScore"]:checked');
  return checked?parseInt(checked.value,10):null;
}
function updatePainScaleVisibility(){
  const section=document.getElementById("painScaleDetails");
  if(section) section.style.display=(currentSpecies==="dog")?"":"none";
}
document.addEventListener("change",e=>{
  if(e.target.matches('#painScaleOptions input[name="painScore"]')){
    const score=parseInt(e.target.value,10);
    const badge=document.getElementById("painScaleBadge");
    const labels=["\u75db\u307f\u306a\u3057","\u8efd\u5ea6","\u4e2d\u7b49\u5ea6","\u4e2d\u301c\u91cd\u5ea6","\u91cd\u5ea6"];
    const colors=["#16a34a","#65a30d","#eab308","#ea580c","#dc2626"];
    if(badge){badge.style.display="inline";badge.textContent=`\u30b9\u30b3\u30a2 ${score}: ${labels[score]}`;badge.style.background=colors[score];}
  }
});

function collectLabValues(){
  const vals={};
  document.querySelectorAll("#labValuesGrid input[data-lab]").forEach(el=>{
    if(el.value.trim()!==""){const v=parseFloat(el.value);if(!isNaN(v))vals[el.dataset.lab]=v;}
  });
  return Object.keys(vals).length>0?vals:null;
}
let _labRangesCache={};
function updateLabRangesForSpecies(species){
  if(_labRangesCache[species]){_applyLabRanges(_labRangesCache[species]);return;}
  fetch(`/api/lab-ranges/${encodeURIComponent(species)}`)
    .then(r=>r.ok?r.json():null)
    .then(data=>{
      if(!data||!data.ranges||species!==currentSpecies)return;
      _labRangesCache[species]=data.ranges;
      _applyLabRanges(data.ranges);
    }).catch(()=>{});
}
function _applyLabRanges(ranges){
  document.querySelectorAll("#labValuesGrid input[data-lab]").forEach(el=>{
    const id=el.dataset.lab;
    const r=ranges[id];
    if(!r)return;
    el.dataset.lo=r.low;
    el.dataset.hi=r.high;
    el.placeholder=`${r.low}–${r.high===99?"":r.high}`;
  });
  highlightLabAbnormals();
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
  if(currentLang==="ja")return `${name}の${label}に関する詳細情報は現在準備中です。`;
  return `Detailed ${label.toLowerCase()} information for ${name} is being prepared.`;
}


function escapeHtml(value){
  return String(value??"").replace(/[&<>"']/g,ch=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[ch]));
}

function slugify(text){
  return String(text??"")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g,"-")
    .replace(/^-+|-+$/g,"");
}

function sanitizeUrl(value){
  try{
    const url=new URL(String(value??""),window.location.origin);
    return ["http:","https:"].includes(url.protocol)?url.href:"#";
  }catch{
    return "#";
  }
}

function renderOrthopedicReferences(d){
  const sections=[
    {key:"prognosis_references",label:currentLang==="ja"?"予後エビデンス":"Prognosis Evidence"},
    {key:"rehabilitation_references",label:currentLang==="ja"?"リハビリ文献":"Rehabilitation References"},
    {key:"nutrition_references",label:currentLang==="ja"?"栄養管理文献":"Nutrition References"},
  ];
  const rendered=sections.map(sec=>{
    const refs=(d[sec.key]&&Array.isArray(d[sec.key].references))?d[sec.key].references:[];
    if(!refs.length)return "";
    const items=refs.map(r=>{
      // Authors: string "FirstAuthor, SecondAuthor, ..." → extract first + " et al."
      const authStr=r.authors||"Unknown";
      const authors=(typeof authStr==="string"&&authStr.length>0)
        ?authStr.split(",")[0].trim()+(authStr.includes(",")?"":" et al.")
        :"Unknown";
      const year=r.year||"";
      const journal=r.journal?`<em>${escapeHtml(r.journal)}</em>`:"";
      const vol=r.volume?` ${r.volume}`:""
      const pages=r.pages?`:${r.pages}`:"";
      const doi=r.doi?`<a href="https://doi.org/${encodeURIComponent(r.doi)}" target="_blank" rel="noopener" style="color:var(--green);font-size:.78rem">DOI</a>`:"";
      const pmid=r.pmid?`<a href="https://pubmed.ncbi.nlm.nih.gov/${encodeURIComponent(r.pmid)}/" target="_blank" rel="noopener" style="color:var(--blue,#2563eb);font-size:.78rem">PMID</a>`:"";
      const evid=r.evidence_level?`<span style="font-size:.75rem;color:var(--gray-500)">[${escapeHtml(r.evidence_level)}]</span>`:"";
      const links=[doi,pmid].filter(Boolean).join(" ");
      return `<li style="margin-bottom:4px"><span style="font-weight:600">${escapeHtml(authors)} (${year})</span> ${escapeHtml(r.title||"")}. ${journal}${vol}${pages}. ${links} ${evid}</li>`;
    }).join("");
    return `<div style="margin-top:8px"><div style="font-size:.8rem;font-weight:700;color:var(--gray-600);margin-bottom:4px">${sec.label}</div><ul style="list-style:none;padding:0;margin:0;font-size:.82rem;color:var(--gray-700)">${items}</ul></div>`;
  }).filter(Boolean).join("");
  if(!rendered)return "";
  return `<div class="ortho-refs" style="margin-top:12px;padding:10px;background:var(--gray-50,#f9fafb);border-radius:6px;border-left:3px solid var(--green)"><div style="font-size:.78rem;font-weight:700;text-transform:uppercase;letter-spacing:.05em;color:var(--green);margin-bottom:6px">📚 ${currentLang==="ja"?"参考文献（エビデンスベース）":"References (Evidence-based)"}</div>${rendered}</div>`;
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

function showRelatedSuggestions(){
  if(!currentSpecies||selectedSymptoms.size===0||selectedSymptoms.size>=3)return;
  const existing=document.getElementById("relatedSuggestions");
  if(existing)existing.remove();
  fetchWithTimeout(`/api/related-symptoms/${encodeURIComponent(currentSpecies)}`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({symptoms:[...selectedSymptoms]})})
  .then(r=>r.json())
  .then(data=>{
    if(!data.related||data.related.length===0)return;
    const container=document.createElement("div");
    container.id="relatedSuggestions";
    container.className="related-suggestions";
    const label=currentLang==="ja"?"関連する症状を追加すると精度が向上します:":"Adding related symptoms improves accuracy:";
    container.innerHTML=`<p class="related-label">${label}</p>`;
    const btns=document.createElement("div");
    btns.className="related-btns";
    data.related.forEach(s=>{
      const btn=document.createElement("button");
      btn.className="related-sym-btn";
      btn.textContent=`+ ${currentLang==="ja"?s.name_ja:s.name_en}`;
      btn.onclick=()=>{
        selectedSymptoms.add(s.id);
        renderSelectedSymptoms();
        renderSymptomList(symptomData);
        btn.disabled=true;
        btn.classList.add("added");
        btn.textContent=`\u2713 ${currentLang==="ja"?s.name_ja:s.name_en}`;
      };
      btns.appendChild(btn);
    });
    container.appendChild(btns);
    const resultsArea=document.getElementById("resultsArea");
    if(resultsArea)resultsArea.parentNode.insertBefore(container,resultsArea);
  })
  .catch(()=>{});
}

function doAnalyze(){
  if(!currentSpecies||selectedSymptoms.size===0)return;
  showRelatedSuggestions();
  trackEvent("analyze_symptoms",{species:currentSpecies,symptom_count:selectedSymptoms.size});
  const btn=document.getElementById("analyzeBtn");btn.disabled=true;btn.innerHTML=`<span class="spinner"></span> ${t("analyzing")}`;
  const progress=document.getElementById("analyzeProgress");
  if(progress)progress.classList.add("active");
  const payload={species:currentSpecies,symptoms:[...selectedSymptoms],lang:currentLang};
  if(currentBreed)payload.breed=currentBreed;
  const labVals=collectLabValues();
  if(labVals)payload.lab_values=labVals;
  const painVal=collectPainScore();
  if(painVal!==null)payload.pain_score=painVal;
  fetchWithTimeout("/api/analyze-symptoms",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)})
  .then(r=>{if(!r.ok)throw new Error(`HTTP ${r.status}: ${r.statusText}`);return r.json();})
  .then(data=>{renderResults(data);trackEvent("view_results",{species:currentSpecies,result_count:data.suspected_diseases?.length||0,symptom_count:selectedSymptoms.size});if(typeof showToast==="function")showToast(currentLang==="ja"?`${data.suspected_diseases?.length||0}件の疾患が見つかりました`:`${data.suspected_diseases?.length||0} diseases found`,"success");const ra=document.getElementById("resultsArea");if(ra)ra.scrollIntoView({behavior:"smooth",block:"start"});})
  .catch(err=>{trackEvent("api_error",{endpoint:"analyze-symptoms",error:String(err.message||"unknown").substring(0,100),species:currentSpecies});const ra=document.getElementById("resultsArea");ra.innerHTML=`<div class="severity-bar high" style="display:flex;flex-direction:column;gap:10px"><div>${escapeHtml(t("networkError"))}</div><button class="retry-analyze-btn" style="align-self:flex-start;padding:8px 20px;background:var(--navy);color:var(--white);border:none;border-radius:6px;cursor:pointer;font-size:.84rem">${t("retry")}</button></div>`;const retryBtn=ra.querySelector(".retry-analyze-btn");if(retryBtn)retryBtn.addEventListener("click",doAnalyze);})
  .finally(()=>{btn.disabled=false;btn.textContent=t("analyzeBtn");if(progress)progress.classList.remove("active");});
}

function createResultsDisclaimer(){
  const d=document.createElement("div");
  d.className="results-disclaimer";
  d.innerHTML='<strong>&#9888; </strong><span data-i18n="resultsDisclaimer">'+t("resultsDisclaimer")+'</span>';
  return d;
}

function createFeedbackWidget(){
  const w=document.createElement("div");
  w.className="feedback-widget";
  w.innerHTML='<span data-i18n="feedbackQuestion">'+t("feedbackQuestion")+'</span><div class="feedback-btns"><button class="feedback-btn helpful">&#128077; '+t("feedbackYes")+'</button><button class="feedback-btn not-helpful">&#128078; '+t("feedbackNo")+'</button></div>';
  w.querySelector(".feedback-btn.helpful").addEventListener("click",function(){sendFeedback(true);});
  w.querySelector(".feedback-btn.not-helpful").addEventListener("click",function(){sendFeedback(false);});
  return w;
}

function sendFeedback(helpful){
  const species=currentSpecies||"unknown";
  const symptoms=[...selectedSymptoms].join(",");
  if(typeof gtag==="function")gtag("event","diagnosis_feedback",{helpful:helpful,species:species,symptom_count:selectedSymptoms.size});
  const btns=document.querySelectorAll(".feedback-btn");
  btns.forEach(b=>b.disabled=true);
  const widget=document.querySelector(".feedback-widget");
  if(widget){widget.innerHTML='<span class="feedback-thanks">'+t("feedbackThanks")+'</span>';}
}

function createShareWidget(diseases){
  const w=document.createElement("div");
  w.className="share-widget";
  const speciesName=SPECIES_ICONS[currentSpecies]||"";
  const sp=SPECIES.find(s=>s.id===currentSpecies);
  const spLabel=sp?(currentLang==="ja"?sp.name:sp.nameEn):(currentSpecies||"");
  const topDisease=diseases.length>0?(currentLang==="ja"?(diseases[0].name_ja||diseases[0].name):(diseases[0].name||diseases[0].name_ja)):"";
  const shareText=currentLang==="ja"
    ?`VetDictで${speciesName}の鑑別診断: ${topDisease} 他${diseases.length}疾患`
    :`VetDict differential diagnosis: ${topDisease} and ${diseases.length} more`;
  /* Share URL: link to top disease page if available, else species index */
  const topDiseaseEn=diseases.length>0?(diseases[0].name||""):"";
  const topSlug=topDiseaseEn.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');
  const shareUrl=topSlug?`https://vetdict.info/diseases/${currentSpecies}/${topSlug}`:`https://vetdict.info/?species=${currentSpecies}#checker`;
  const twitterUrl=`https://twitter.com/intent/tweet?text=${encodeURIComponent(shareText)}&url=${encodeURIComponent(shareUrl)}`;
  const lineUrl=`https://social-plugins.line.me/lineit/share?url=${encodeURIComponent(shareUrl)}&text=${encodeURIComponent(shareText)}`;
  /* 詳細結果テキスト生成 */
  const sympList=[...selectedSymptoms].map(id=>{const s=symptomData.find(x=>x.id===id);return s?(currentLang==="ja"?(s.name_ja||s.name_en):s.name_en):id;}).join(", ");
  const diseaseLines=diseases.slice(0,10).map((d,i)=>{const name=currentLang==="ja"?(d.name_ja||d.name):d.name;const pct=d.match_percent||d.confidence||0;return`${i+1}. ${name} (${pct}%)`;}).join("\n");
  const fullText=currentLang==="ja"
    ?`【VetDict 鑑別診断結果】\n動物種: ${spLabel}\n症状: ${sympList}\n\n${diseaseLines}\n\n※ 参考情報です。獣医師の診察を受けてください。\n${shareUrl}`
    :`[VetDict Differential Diagnosis]\nSpecies: ${spLabel}\nSymptoms: ${sympList}\n\n${diseaseLines}\n\nNote: For reference only. Consult a veterinarian.\n${shareUrl}`;
  w.innerHTML=`<span>${t("shareResults")}</span><div class="share-btns"><a href="${twitterUrl}" target="_blank" rel="noopener" class="share-btn twitter">X</a><a href="${lineUrl}" target="_blank" rel="noopener" class="share-btn line">LINE</a><button class="share-btn copy">${t("shareCopy")}</button><button class="share-btn copy-full" style="background:var(--navy)">${currentLang==="ja"?"詳細コピー":"Copy Full"}</button></div>`;
  w.querySelector(".share-btn.twitter").addEventListener("click",function(){trackEvent("share_results",{method:"twitter",species:currentSpecies});});
  w.querySelector(".share-btn.line").addEventListener("click",function(){trackEvent("share_results",{method:"line",species:currentSpecies});});
  w.querySelector(".share-btn.copy").addEventListener("click",function(){navigator.clipboard.writeText(shareText+" "+shareUrl).then(()=>{this.textContent=t("shareCopied");trackEvent("share_results",{method:"copy",species:currentSpecies});});});
  w.querySelector(".share-btn.copy-full").addEventListener("click",function(){navigator.clipboard.writeText(fullText).then(()=>{this.textContent=t("shareCopied");trackEvent("share_results",{method:"copy_full",species:currentSpecies});setTimeout(()=>{this.textContent=currentLang==="ja"?"詳細コピー":"Copy Full";},2000);});});
  return w;
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
  /* Low-confidence warning: alert when symptom count <=2 or top confidence <50% */
  const topPct=diseases[0]?diseases[0].match_percent||diseases[0].confidence||0:0;
  const symCount=selectedSymptoms?selectedSymptoms.size:0;
  if(symCount<=2||topPct<50){
    const warnMsg=currentLang==="ja"
      ?`⚠ 入力症状が${symCount}個${symCount<=2?"（推奨: 3個以上）":""}のため、鑑別精度が制限されています（最高信頼度 ${topPct.toFixed(1)}%）。症状を追加すると精度が大幅に向上します。`
      :`⚠ With only ${symCount} symptom${symCount!==1?"s":""} entered${symCount<=2?" (3+ recommended)":""}, diagnostic accuracy is limited (top confidence ${topPct.toFixed(1)}%). Adding more symptoms will significantly improve results.`;
    html+=`<div style="padding:10px 14px;margin-bottom:12px;border-radius:var(--radius);font-size:.82rem;font-weight:500;background:#fef3c7;border-left:4px solid #f59e0b;color:#92400e">${warnMsg}</div>`;
  }
  /* Next steps banner based on severity */
  const nextSteps=currentLang==="ja"?{
    emergency:"⚠️ 緊急：直ちに獣医師の診察を受けてください。応急処置が必要な場合があります。",
    high:"🔴 早急に獣医師の診察を予約してください。24時間以内の受診を推奨します。",
    moderate:"🟡 近日中に獣医師にご相談ください。経過観察しながら1週間以内の受診を推奨します。",
    low:"🟢 通常の健康診断時にご相談ください。症状が悪化した場合は早めの受診を。",
  }:{
    emergency:"⚠️ Emergency: Seek immediate veterinary care. First aid may be required.",
    high:"🔴 Schedule a veterinary visit urgently. Within 24 hours recommended.",
    moderate:"🟡 Consult your veterinarian soon. Visit within 1 week recommended.",
    low:"🟢 Discuss at next routine checkup. Seek earlier care if symptoms worsen.",
  };
  if(nextSteps[severity])html+=`<div style="padding:10px 14px;margin-bottom:12px;border-radius:var(--radius);font-size:.84rem;font-weight:500;background:var(--gray-50);border-left:4px solid ${severity==='emergency'||severity==='high'?'#ef4444':severity==='moderate'?'#f59e0b':'#22a853'}">${nextSteps[severity]}</div>`;
  if(data.lab_boost_applied&&data.lab_values){
    const labNames={bun:"BUN",creatinine:"Cre",sdma:"SDMA",alt:"ALT",alp:"ALP",ggt:"GGT",tbil:"T-Bil",albumin:"Alb",glucose:"Glu",lipase:"Lipase",potassium:"K",sodium:"Na",calcium:"Ca",phosphorus:"P",wbc:"WBC",pcv:"PCV",platelets:"PLT",t4:"T4",crp:"CRP",usg:"USG"};
    const sp=currentSpecies||"dog";
    const cachedRanges=_labRangesCache[sp]||{};
    const defaultRanges={bun:[7,27],creatinine:[0.5,1.8],sdma:[0,14],alt:[10,125],alp:[23,212],ggt:[0,11],tbil:[0,0.5],albumin:[2.3,4],glucose:[74,143],lipase:[10,160],potassium:[3.5,5.8],sodium:[140,155],calcium:[7.9,12],phosphorus:[2.5,6.8],wbc:[5.5,16.9],pcv:[37,55],platelets:[175,500],t4:[1,4],crp:[0,10],usg:[1.03,99]};
    let bars="";let abnCount=0;
    for(const[k,v]of Object.entries(data.lab_values)){
      const cr=cachedRanges[k];
      const lo=cr?cr.low:defaultRanges[k]?defaultRanges[k][0]:0;
      const hi=cr?cr.high:defaultRanges[k]?defaultRanges[k][1]:100;
      if(hi===99||hi===0)continue;
      const name=escapeHtml(labNames[k]||k);
      const isHigh=v>hi,isLow=v<lo,isAbn=isHigh||isLow;
      if(isAbn)abnCount++;
      const range=hi-lo;const margin=range*0.5;
      const scaleMin=Math.max(0,lo-margin),scaleMax=hi+margin;
      const scaleRange=scaleMax-scaleMin;
      const normLo=((lo-scaleMin)/scaleRange*100).toFixed(1);
      const normHi=((hi-scaleMin)/scaleRange*100).toFixed(1);
      const valPos=Math.max(0,Math.min(100,((v-scaleMin)/scaleRange*100))).toFixed(1);
      const dotColor=isHigh?"#e74c3c":isLow?"#2980b9":"#16a34a";
      const flag=isHigh?"\u2191":isLow?"\u2193":"";
      bars+=`<div class="lab-bar-row"><span class="lab-bar-label" style="color:${isAbn?dotColor:"var(--gray-700)"};font-weight:${isAbn?700:500}">${name} <b>${v}</b>${flag}</span><div class="lab-bar-track"><div class="lab-bar-normal" style="left:${normLo}%;width:${normHi-normLo}%"></div><div class="lab-bar-dot" style="left:${valPos}%;background:${dotColor}"></div></div><span class="lab-bar-range">${lo}–${hi}</span></div>`;
    }
    const title=currentLang==="ja"?(abnCount>0?`\u{1F4CA} 血液検査: ${abnCount}項目に異常`:`\u{1F4CA} 血液検査: 基準値内`):(abnCount>0?`\u{1F4CA} Lab Results: ${abnCount} abnormal`:`\u{1F4CA} Lab Results: within range`);
    html+=`<div class="lab-results-viz"><div class="lab-viz-title" style="color:${abnCount>0?"#e74c3c":"#16a34a"}">${title}</div>${bars}</div>`;
  }
  // Pain score display
  if(data.pain_score!==undefined&&data.pain_score!==null&&currentSpecies==="dog"){
    const ps=data.pain_score;
    const painLabels=currentLang==="ja"?["痛みなし","軽度","中等度","中〜重度","重度"]:["No Pain","Mild","Moderate","Severe","Excruciating"];
    const painColors=["#16a34a","#65a30d","#eab308","#ea580c","#dc2626"];
    const painPct=ps*25;
    html+=`<div class="lab-results-viz" style="border-color:${painColors[ps]}33"><div class="lab-viz-title" style="color:${painColors[ps]}">&#x1F9D1;&#x200D;&#x2695;&#xFE0F; ${currentLang==="ja"?"痛み評価":"Pain Assessment"}: ${painLabels[ps]} (${ps}/4)</div><div class="pain-meter"><div class="pain-meter-fill" style="width:${painPct}%;background:${painColors[ps]}"></div></div>${ps>=3?`<div style="font-size:.74rem;color:${painColors[ps]};margin-top:4px;font-weight:600">${currentLang==="ja"?"⚠ 強い痛みが検出されました。早急な鎮痛処置を検討してください。":"⚠ Severe pain detected. Consider immediate analgesic intervention."}</div>`:""}</div>`;
  }
  const adviceText=currentLang==="ja"?adviceJa:(data.general_advice||adviceJa);
  if(adviceText)html+=`<div style="font-size:.82rem;color:var(--gray-700);margin-bottom:12px;padding:8px 12px;background:var(--gray-50);border-radius:var(--radius)">${escapeHtml(adviceText)}</div>`;

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
      html+=renderDiseaseCard(d,data);
    });
  }

  if(tests.length){html+=`<div style="margin-top:16px"><strong style="font-size:.86rem">${t("dtRecTestList")}</strong><ul class="test-list">${tests.map(x=>{const label=typeof x==="string"?x:(currentLang==="ja"?(x.name_ja||x.name):(x.name||x.name_ja));const priority=x.priority?` <span style="color:var(--gray-500);font-size:.75rem">[${escapeHtml(x.priority)}]</span>`:"";return`<li>\u{1F52C} ${escapeHtml(label)}${priority}</li>`;}).join("")}</ul></div>`;}
  html+=`<div id="commonDiseasesArea"></div><div id="breedEcologyArea"></div>`;
  area.innerHTML="";
  area.appendChild(createResultsDisclaimer());
  const contentDiv=document.createElement("div");
  contentDiv.innerHTML=html;
  /* Disease card expand/collapse — event delegation on contentDiv */
  contentDiv.addEventListener("click",function(e){
    if(e.target.closest("a"))return; /* don't intercept link clicks */
    const head=e.target.closest(".disease-head");
    if(head)toggleDetail(head);
  });
  contentDiv.addEventListener("keydown",function(e){if(e.key==="Enter"||e.key===" "){const head=e.target.closest(".disease-head");if(head){e.preventDefault();toggleDetail(head);}}});
  area.appendChild(contentDiv);
  area.appendChild(createFeedbackWidget());
  area.appendChild(createShareWidget(diseases));
  area.appendChild(createPrintButton());
  loadCommonDiseases(currentSpecies);
  loadBreedEcology(currentSpecies,currentBreed);
  /* Save diagnosis to history (localStorage) */
  saveDiagnosisHistory(data,diseases);
}

/* ===== Print / Export ===== */
function createPrintButton(){
  const btn=document.createElement("button");
  btn.className="print-results-btn";
  btn.style.cssText="display:block;margin:12px auto;padding:10px 24px;background:var(--white);border:2px solid var(--navy);color:var(--navy);border-radius:8px;font-size:.84rem;font-weight:600;cursor:pointer";
  btn.textContent=currentLang==="ja"?"🖨 診断結果を印刷":"🖨 Print Results";
  btn.addEventListener("click",function(){
    trackEvent("print_results",{species:currentSpecies});
    window.print();
  });
  return btn;
}

/* ===== Diagnosis History (localStorage) ===== */
function saveDiagnosisHistory(data,diseases){
  try{
    const entry={
      id:Date.now(),
      date:new Date().toISOString(),
      species:currentSpecies,
      symptoms:[...selectedSymptoms],
      topDiseases:diseases.slice(0,5).map(d=>({name:d.name||"",name_ja:d.name_ja||"",confidence:d.match_percent||d.confidence||0})),
      severity:data.severity||"",
    };
    const history=JSON.parse(localStorage.getItem("vetdict-history")||"[]");
    history.unshift(entry);
    if(history.length>50)history.length=50;
    localStorage.setItem("vetdict-history",JSON.stringify(history));
  }catch(e){/* quota exceeded or private mode */}
}

function loadDiagnosisHistory(){
  try{return JSON.parse(localStorage.getItem("vetdict-history")||"[]");}catch(e){return[];}
}

function renderHistoryPanel(){
  const history=loadDiagnosisHistory();
  if(!history.length)return"";
  const sp=id=>SPECIES.find(s=>s.id===id);
  const items=history.slice(0,10).map(h=>{
    const s=sp(h.species);
    const icon=s?s.icon:"🐾";
    const spName=s?(currentLang==="ja"?s.name:s.nameEn):(h.species||"");
    const date=new Date(h.date).toLocaleDateString(currentLang==="ja"?"ja-JP":"en-US",{month:"short",day:"numeric",hour:"2-digit",minute:"2-digit"});
    const top=h.topDiseases&&h.topDiseases[0]?(currentLang==="ja"?(h.topDiseases[0].name_ja||h.topDiseases[0].name):h.topDiseases[0].name):"";
    return`<div class="history-item" data-id="${h.id}" style="padding:8px 12px;border-bottom:1px solid var(--gray-100);cursor:pointer;font-size:.82rem"><span>${icon}</span> <strong>${escapeHtml(spName)}</strong> <span style="color:var(--gray-500)">${date}</span><br><span style="color:var(--navy)">${escapeHtml(top)}</span> <span style="color:var(--gray-400)">${h.symptoms?h.symptoms.length:0}症状</span></div>`;
  }).join("");
  return`<div class="history-panel" style="margin-top:12px"><div style="font-size:.82rem;font-weight:700;color:var(--navy);padding:8px 12px;border-bottom:2px solid var(--green)">${currentLang==="ja"?"📋 診断履歴":"📋 Diagnosis History"}</div>${items}</div>`;
}

function loadCommonDiseases(species){
  const area=document.getElementById("commonDiseasesArea");
  if(!area||!species)return;
  fetchWithTimeout(`/api/species/${encodeURIComponent(species)}/common-diseases`).then(r=>r.json()).then(data=>{
    if(species!==currentSpecies)return;
    const diseases=data.common_diseases||[];
    if(!diseases.length){area.innerHTML="";return;}
    const veryCommon=diseases.filter(d=>d.prevalence==="very_common");
    const common=diseases.filter(d=>d.prevalence==="common");
    const renderList=(list,cls)=>list.map(d=>{
      const name=currentLang==="ja"?(d.name_ja||d.name):d.name;
      const sub=currentLang==="ja"?d.name:(d.name_ja||"");
      return `<span class="common-disease-tag ${cls}">${escapeHtml(name)}${sub?` <span class="common-disease-sub">${escapeHtml(sub)}</span>`:""}</span>`;
    }).join("");
    area.innerHTML=`<div class="common-diseases-section">
      <div class="common-diseases-header">${currentLang==="ja"?"📋 この動物種でよくみられる疾患":"📋 Common diseases in this species"}</div>
      ${veryCommon.length?`<div class="common-diseases-group"><span class="common-diseases-tier tier-very-common">${currentLang==="ja"?"非常に多い":"Very Common"}</span>${renderList(veryCommon,"tag-very-common")}</div>`:""}
      ${common.length?`<div class="common-diseases-group"><span class="common-diseases-tier tier-common">${currentLang==="ja"?"多い":"Common"}</span>${renderList(common,"tag-common")}</div>`:""}
      <div class="common-diseases-hint">${currentLang==="ja"?"※ 鑑別診断の参考としてご活用ください":"※ Use as reference for differential diagnosis"}</div>
    </div>`;
  }).catch(()=>{if(area)area.innerHTML="";});
}

function loadBreedEcology(species,breedId){
  const area=document.getElementById("breedEcologyArea");
  if(!area||!species)return;
  fetch(`/api/breeds/${encodeURIComponent(species)}`).then(r=>r.json()).then(data=>{
    const breeds=data.breeds||[];
    const breed=breedId?breeds.find(b=>b.id===breedId):null;
    const eco=breed&&breed.ecology?breed.ecology:null;
    if(!eco){area.innerHTML="";return;}
    const bName=currentLang==="ja"?(breed.name_ja||breed.name):breed.name;
    const rows=[];
    if(eco.lifespan)rows.push({icon:"⏱",label:currentLang==="ja"?"平均寿命":"Lifespan",val:`${eco.lifespan.min}–${eco.lifespan.max} ${eco.lifespan.unit==="years"?(currentLang==="ja"?"年":"yrs"):eco.lifespan.unit}`});
    if(eco.weight)rows.push({icon:"⚖️",label:currentLang==="ja"?"体重":"Weight",val:`${eco.weight.min}–${eco.weight.max} ${eco.weight.unit}`});
    if(eco.temperature)rows.push({icon:"🌡",label:currentLang==="ja"?"適正温度":"Temperature",val:`${eco.temperature.min}–${eco.temperature.max}${eco.temperature.unit}`});
    if(eco.humidity)rows.push({icon:"💧",label:currentLang==="ja"?"適正湿度":"Humidity",val:`${eco.humidity.min}–${eco.humidity.max}${eco.humidity.unit}`});
    const diet=currentLang==="ja"?(eco.diet_ja||eco.diet||""):(eco.diet||eco.diet_ja||"");
    const housing=currentLang==="ja"?(eco.housing_ja||eco.housing||""):(eco.housing||eco.housing_ja||"");
    const notes=currentLang==="ja"?(eco.notes_ja||eco.notes||""):(eco.notes||eco.notes_ja||"");
    area.innerHTML=`<div class="breed-ecology-section">
      <div class="breed-ecology-header">🐾 ${bName} ${currentLang==="ja"?"の生態・飼育環境":"Ecology & Husbandry"}</div>
      <div class="breed-ecology-grid">${rows.map(r=>`<div class="breed-ecology-item"><span class="breed-ecology-icon">${r.icon}</span><span class="breed-ecology-label">${r.label}</span><span class="breed-ecology-val">${r.val}</span></div>`).join("")}</div>
      ${diet?`<div class="breed-ecology-field"><strong>${currentLang==="ja"?"食事":"Diet"}:</strong> ${escapeHtml(diet)}</div>`:""}
      ${housing?`<div class="breed-ecology-field"><strong>${currentLang==="ja"?"飼育環境":"Housing"}:</strong> ${escapeHtml(housing)}</div>`:""}
      ${notes?`<div class="breed-ecology-field"><strong>${currentLang==="ja"?"特記事項":"Notes"}:</strong> ${escapeHtml(notes)}</div>`:""}
    </div>`;
  }).catch(()=>{if(area)area.innerHTML="";});
}

function renderMissingKeySymptoms(d,data){
  const missingKeys=d.missing_key_symptoms||[];
  if(!missingKeys.length)return "";
  const symNames=data.symptom_names||{};
  const items=missingKeys.map(s=>{
    const n=symNames[s];
    if(!n)return `<span class="missing-sym-tag">${s}</span>`;
    const label=currentLang==="ja"?`${n.ja} <span class="missing-sym-sub">${n.en}</span>`:`${n.en} <span class="missing-sym-sub">${n.ja}</span>`;
    return `<span class="missing-sym-tag">${label}</span>`;
  }).join("");
  const title=currentLang==="ja"?"確認すべき症状（未報告）":"Key symptoms to check (not reported)";
  return `<div class="detail-missing-symptoms"><div class="detail-missing-header">\u{1F50E} ${title}</div><div class="detail-missing-list">${items}</div><div class="detail-missing-hint">${currentLang==="ja"?"これらの症状の有無を確認すると、鑑別精度が向上します。":"Checking for these symptoms will improve diagnostic accuracy."}</div></div>`;
}

function renderScoringDetail(d){
  const sd=d.scoring_detail;
  if(!sd)return "";
  const pctBar=(val,label,color)=>{
    const w=Math.min(Math.round(val*100),100);
    return `<div class="score-row"><span class="score-label">${label}</span><div class="score-bar-track"><div class="score-bar-fill" style="width:${w}%;background:${color}"></div></div><span class="score-value">${w}%</span></div>`;
  };
  const recallLabel=currentLang==="ja"?"症状一致度":"Symptom Recall";
  const coverageLabel=currentLang==="ja"?"疾患カバレッジ":"Disease Coverage";
  let html=`<div class="detail-scoring"><div class="detail-scoring-header">\u{1F9E0} ${currentLang==="ja"?"診断根拠スコア":"Diagnostic Evidence Score"}</div>`;
  html+=pctBar(sd.weighted_recall||0,recallLabel,"#22c55e");
  html+=pctBar(sd.coverage||0,coverageLabel,"#3b82f6");
  const badges=[];
  if(sd.cluster_boost&&sd.cluster_boost>1)badges.push(`<span class="score-badge boost">${currentLang==="ja"?"病徴パターン一致":"Pathognomonic Match"} +${Math.round((sd.cluster_boost-1)*100)}%</span>`);
  if(sd.negative_penalty&&sd.negative_penalty<1)badges.push(`<span class="score-badge penalty">${currentLang==="ja"?"欠如症状ペナルティ":"Missing Symptom Penalty"} -${Math.round((1-sd.negative_penalty)*100)}%</span>`);
  if(sd.specificity_bonus&&sd.specificity_bonus>0)badges.push(`<span class="score-badge boost">${currentLang==="ja"?"高特異度ボーナス":"High Specificity Bonus"} +${Math.round(sd.specificity_bonus*100)}%</span>`);
  if(sd.prevalence_prior&&sd.prevalence_prior!==1)badges.push(`<span class="score-badge ${sd.prevalence_prior>1?"boost":"penalty"}">${currentLang==="ja"?"有病率調整":"Prevalence Adj."} ${sd.prevalence_prior>1?"+":""}${Math.round((sd.prevalence_prior-1)*100)}%</span>`);
  if(badges.length)html+=`<div class="score-badges">${badges.join("")}</div>`;
  html+=`</div>`;
  return html;
}

/* Map disease name/category to anesthesia condition tags */
const DISEASE_ANESTHESIA_MAP={
  /* Keywords in disease name → condition tags */
  "cardiac":"cardiac_disease","heart":"cardiac_disease","cardiomyopathy":"cardiomyopathy",
  "hcm":"cat_hcm","dcm":"cardiac_disease","valve":"cardiac_disease","stenosis":"cardiac_disease",
  "arrhythmia":"cardiac_disease","bradycardia":"bradycardia",
  "renal":"renal_disease","kidney":"renal_disease","ckd":"ckd","nephro":"renal_disease",
  "hepatic":"hepatic_disease","liver":"hepatic_disease","lipidosis":"hepatic_lipidosis",
  "seizure":"seizure","epilep":"epilepsy","convulsion":"seizure",
  "gastric dilatation":"gdv","gdv":"gdv","bloat":"gdv",
  "diabetes":"diabetes","diabetic":"diabetes","insulinoma":"insulinoma",
  "coagulo":"coagulopathy","thrombocyto":"thrombocytopenia","dic":"dic","hemophilia":"coagulopathy",
  "brachycephalic":"brachycephalic","短頭":"brachycephalic",
  "laryngeal":"laryngeal_paralysis","tracheal collapse":"upper_airway_obstruction",
  "pregnancy":"pregnancy","dystocia":"pregnancy","pyometra":"pregnancy",
  "腎":"renal_disease","心":"cardiac_disease","肝":"hepatic_disease",
  "てんかん":"epilepsy","痙攣":"seizure","糖尿":"diabetes",
  "胃拡張":"gdv","妊娠":"pregnancy","難産":"pregnancy",
};
function renderAnesthesiaConsiderations(d){
  if(!anesthesiaContraRules||!anesthesiaContraRules.length)return"";
  const name=((d.name||"")+" "+(d.name_ja||"")).toLowerCase();
  /* Find matching condition tags from disease name */
  const tags=new Set();
  for(const[kw,tag]of Object.entries(DISEASE_ANESTHESIA_MAP)){
    if(name.includes(kw.toLowerCase()))tags.add(tag);
  }
  if(!tags.size)return"";
  /* Check all rules against these tags + species */
  const sp=(currentSpecies||"").toLowerCase();
  const allTags=new Set([...tags]);
  if(sp)allTags.add(sp);
  const warnings=[];
  const seen=new Set();
  for(const rule of anesthesiaContraRules){
    const condMatch=rule.conditions.some(c=>allTags.has(c.toLowerCase()));
    if(!condMatch)continue;
    const key=rule.drug_patterns[0]+"|"+rule.severity;
    if(seen.has(key))continue;
    seen.add(key);
    warnings.push(rule);
  }
  if(!warnings.length)return"";
  const sevColors={contraindicated:"#dc2626",caution:"#ea580c",monitor:"#ca8a04"};
  const sevIcons={contraindicated:"⛔",caution:"⚠️",monitor:"🔍"};
  const sevLabels={contraindicated:t("anesthesiaContraindicated"),caution:t("anesthesiaCaution"),monitor:t("anesthesiaMonitorExtra")};
  const title=currentLang==="ja"?"🏥 この疾患の麻酔注意事項":"🏥 Anesthesia Considerations for This Condition";
  let html=`<div class="detail-anesthesia-notes" style="margin-top:10px;padding:10px 14px;background:#fffbeb;border:1px solid #fde68a;border-radius:8px"><strong style="font-size:.84rem">${title}</strong><div style="margin-top:6px;display:flex;flex-direction:column;gap:4px">`;
  warnings.slice(0,6).forEach(w=>{
    const msg=currentLang==="ja"?(w.message_ja||w.message_en):(w.message_en||w.message_ja);
    const drugs=w.drug_patterns.slice(0,3).join(", ");
    const sev=w.severity;
    html+=`<div style="font-size:.8rem;padding:4px 0;border-bottom:1px dotted #fde68a"><span class="anesthesia-contra-badge" style="background:${sevColors[sev]||"#ea580c"}">${sevIcons[sev]||"⚠️"} ${escapeHtml(sevLabels[sev]||sev)}</span> <strong>${escapeHtml(drugs)}</strong>: ${escapeHtml(msg)}</div>`;
  });
  html+=`</div></div>`;
  return html;
}
function renderMentionedDrugs(d){
  const drugs=d.mentioned_drugs;
  if(!drugs||!drugs.length)return"";
  const title=currentLang==="ja"?"💊 関連薬品・投与量":"💊 Related Drugs & Dosage";
  let html=`<div class="detail-drugs" style="margin-top:10px"><strong style="font-size:.84rem">${title}</strong><div style="display:flex;flex-direction:column;gap:6px;margin-top:6px">`;
  drugs.forEach(dr=>{
    const name=currentLang==="ja"?(dr.name_ja||dr.name):(dr.name||dr.name_ja);
    const hasDosage=dr.dosage||dr.dosage_ja;
    const dosage=currentLang==="ja"?(dr.dosage_ja||dr.dosage):(dr.dosage||dr.dosage_ja);
    const notes=currentLang==="ja"?(dr.notes_ja||dr.notes):(dr.notes||dr.notes_ja);
    const safeClass=dr.safe===false?"drug-unsafe":"drug-safe";
    const safeIcon=dr.safe===false?"✗":"✓";
    const safeLabel=dr.safe===false?(currentLang==="ja"?"禁忌":"Contraindicated"):"";
    html+=`<div class="drug-mention-card" style="padding:8px 12px;background:${dr.safe===false?"#fef2f2":"#f0f7ff"};border:1px solid ${dr.safe===false?"#fecaca":"#bfdbfe"};border-radius:6px;font-size:.82rem">`;
    html+=`<div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap"><span style="font-weight:600;color:var(--navy)">${escapeHtml(name)}</span>`;
    if(dr.safe===false)html+=`<span style="color:#dc2626;font-weight:600;font-size:.75rem">⚠ ${safeLabel}</span>`;
    html+=`</div>`;
    if(hasDosage&&dr.safe!==false)html+=`<div style="margin-top:3px;color:var(--gray-700)"><span style="font-weight:500">${currentLang==="ja"?"投与量":"Dosage"}:</span> ${escapeHtml(dosage)}</div>`;
    if(notes&&dr.safe!==false)html+=`<div style="margin-top:2px;color:var(--gray-500);font-size:.76rem">${escapeHtml(notes)}</div>`;
    html+=`</div>`;
  });
  html+=`</div><div style="font-size:.7rem;color:var(--gray-400);margin-top:4px">${currentLang==="ja"?"※ 投与量は参考値です。必ず獣医師の指示に従ってください。":"※ Dosages are for reference only. Always follow veterinary guidance."}</div></div>`;
  return html;
}

function renderDiseaseCard(d,data){
  const nameEn=d.name||d.name_ja||"",nameJa=d.name_ja||"";
  const name=currentLang==="ja"?(nameJa||nameEn):nameEn;
  const nameSecondary=currentLang==="ja"?nameEn:nameJa;
  const pct=d.match_percent||d.confidence||0;
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
  const matchDisplay=matchSymptoms.map(s=>{const n=symNames[s];if(!n)return escapeHtml(s);return currentLang==="ja"?`${escapeHtml(n.ja)} <span style="color:var(--gray-500);font-size:.78rem">${escapeHtml(n.en)}</span>`:`${escapeHtml(n.en)} <span style="color:var(--gray-500);font-size:.78rem">${escapeHtml(n.ja)}</span>`;}).join("&ensp;|&ensp;");
  const completeness=Number(d.completeness_score||100);
  const missing=(d.missing_fields||[]);
  const qualityClass=completeness>=90?"quality-ok":"quality-warn";
  const prevalenceTier=d.prevalence_tier||"unknown";
  const prevalenceLabel={very_common:(currentLang==="ja"?"非常に一般的":"Very Common"),common:(currentLang==="ja"?"一般的":"Common"),uncommon:(currentLang==="ja"?"稀":"Uncommon"),rare:(currentLang==="ja"?"非常に稀":"Rare"),unknown:(currentLang==="ja"?"不明":"Unknown")}[prevalenceTier]||"";

  const urgencyIcon=likelihood==="high"?"\u26A0\uFE0F":likelihood==="moderate"?"\u{1F7E1}":"\u{1F7E2}";
  let html=`<div class="disease-result disease-${escapeHtml(likelihood)}">
    <div class="disease-head" role="button" tabindex="0" aria-expanded="false">
      <div class="disease-head-info">
        <div class="disease-name-row">
          <span class="disease-name">${escapeHtml(name)}</span>
          ${nameSecondary&&nameSecondary!==name?`<span class="disease-name-ja">${escapeHtml(nameSecondary)}</span>`:""}
          <span class="quality-badge ${qualityClass}">${completeness}%</span>
          ${prevalenceLabel?`<span class="prevalence-badge">${escapeHtml(prevalenceLabel)}</span>`:""}
        </div>
        <div class="disease-match-bar-row">
          <div class="disease-match-bar"><div class="disease-match-fill disease-match-${likelihood}" style="width:${Math.min(pct,100)}%"></div></div>
          <span class="disease-match-label">${urgencyIcon} ${pct}%</span>
        </div>
      </div>
      <span class="expand-icon">&#9660;</span>
    </div>
    <div class="disease-detail">
      <div class="detail-grid">
        <div class="detail-section">
          <div class="detail-section-header"><span class="detail-icon">\u{1F4CB}</span> ${t("dtDescription")}</div>
          <div class="detail-section-body">${escapeHtml(desc||buildFieldFallback(t("dtDescription"),diseaseName))}</div>
        </div>
        <div class="detail-section">
          <div class="detail-section-header"><span class="detail-icon">\u{1F9EC}</span> ${t("dtPathophysiology")}</div>
          <div class="detail-section-body">${escapeHtml(patho)}</div>
        </div>
        <div class="detail-section">
          <div class="detail-section-header"><span class="detail-icon">\u{1F50D}</span> ${t("dtCauses")}</div>
          <div class="detail-section-body">${escapeHtml(causes)}</div>
        </div>
        <div class="detail-section">
          <div class="detail-section-header"><span class="detail-icon">\u{1F48A}</span> ${t("dtTreatment")}</div>
          <div class="detail-section-body">${escapeHtml(treatment)}</div>
        </div>
        <div class="detail-section">
          <div class="detail-section-header"><span class="detail-icon">\u{1F6E1}\uFE0F</span> ${t("dtPrevention")}</div>
          <div class="detail-section-body">${escapeHtml(prevention)}</div>
        </div>
        <div class="detail-section">
          <div class="detail-section-header"><span class="detail-icon">\u{1F4CA}</span> ${t("dtPrognosis")}</div>
          <div class="detail-section-body">${escapeHtml(prognosis)}</div>
        </div>
      </div>
      ${matchSymptoms.length?`<div class="detail-matched"><strong>${t("dtMatchedSymptoms")}:</strong> ${matchDisplay}</div>`:""}
      ${renderMissingKeySymptoms(d,data)}
      ${renderScoringDetail(d)}
      ${recTests.length?`<div class="detail-tests"><strong>${t("dtRecommendedTests")}:</strong><div style="display:flex;flex-wrap:wrap;gap:4px;margin-top:4px">${recTests.map(x=>{const label=typeof x==="string"?x:(currentLang==="ja"?(x.name_ja||x.name):(x.name||x.name_ja));return`<span style="display:inline-block;padding:3px 8px;background:#f0f7ff;border:1px solid #bfdbfe;border-radius:4px;font-size:.78rem;color:var(--navy)">\u{1F52C} ${escapeHtml(label)}</span>`;}).join("")}</div></div>`:""}
      ${renderMentionedDrugs(d)}
      ${renderAnesthesiaConsiderations(d)}
      <div class="detail-page-link"><a href="/diseases/${encodeURIComponent(currentSpecies)}/${encodeURIComponent(nameEn.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,''))}" target="_blank" rel="noopener" style="font-size:.82rem;color:var(--green);font-weight:600;text-decoration:none">${currentLang==="ja"?"📖 この疾患の詳細ページを見る":"📖 View full disease page"} →</a></div>
      ${d.content_origin?`<div class="missing-note">${currentLang==="ja"?"データソース":"Content source"}: ${escapeHtml(d.content_origin)}</div>`:""}${renderCitationMap(d)}${renderReferenceLinks(d)}${missing.length?`<div class="missing-note">${currentLang==="ja"?"要確認データ":"Data needs review"}: ${escapeHtml(missing.join(", "))}</div>`:""}
    </div>
  </div>`;
  return html;
}

/* ===== Husbandry / Care Environment ===== */
let husbandryRequestId=0;
function loadHusbandry(species){
  const requestId=++husbandryRequestId;
  const container=document.getElementById("husbandryPanel");
  if(!container)return;
  container.innerHTML=`<div class="skeleton skeleton-line" style="margin:12px"></div>`;
  fetch(`/api/species/${encodeURIComponent(species)}/husbandry`).then(r=>r.json()).then(data=>{
    if(requestId!==husbandryRequestId||species!==currentSpecies)return;
    if(data.husbandry){renderHusbandry(data.husbandry,container);}
    else{container.innerHTML=`<p style="padding:12px;color:var(--gray-500)">${t("husbandryError")}</p>`;}
  }).catch(()=>{if(requestId===husbandryRequestId)container.innerHTML=`<p style="padding:12px;color:var(--gray-500)">${t("husbandryError")}</p>`;});
}
function renderHusbandry(h,container){
  const lang=currentLang;
  const icon=k=>({"temperature":"\uD83C\uDF21\uFE0F","humidity":"\uD83D\uDCA7","housing":"\uD83C\uDFE0","diet":"\uD83C\uDF7D\uFE0F","enrichment":"\uD83C\uDFAE","socialization":"\uD83E\uDD1D","notes":"\uD83D\uDCCB"}[k]||"");
  const labelKey=k=>({"temperature":"husbandryTemp","humidity":"husbandryHumidity","housing":"husbandryHousing","diet":"husbandryDiet","enrichment":"husbandryEnrichment","socialization":"husbandrySocial","notes":"husbandryNotes"}[k]||k);
  const fields=["temperature","humidity","housing","diet","enrichment","socialization","notes"];
  function renderCards(data){
    let out="";
    for(const f of fields){
      const val=data[f];if(!val)continue;
      const text=val[lang]||val.en||val.ja||"";
      out+=`<div class="husbandry-card"><div class="husbandry-card-icon">${icon(f)}</div><div class="husbandry-card-label">${t(labelKey(f))}</div><div class="husbandry-card-text">${escapeHtml(text)}</div></div>`;
    }
    return out;
  }
  let html=`<h3 class="husbandry-title">${icon("notes")} ${t("husbandryTitle")}</h3><div class="husbandry-grid">${renderCards(h)}</div>`;
  if(h.subtypes&&h.subtypes.length){
    html+=`<div class="husbandry-subtypes">`;
    for(const st of h.subtypes){
      const stName=lang==="ja"?(st.name_ja||st.name):(st.name||st.name_ja);
      html+=`<details class="husbandry-subtype"><summary class="husbandry-subtype-title">${escapeHtml(stName)}</summary><div class="husbandry-grid">${renderCards(st)}</div></details>`;
    }
    html+=`</div>`;
  }
  container.innerHTML=html;
}

function loadDiseaseDb(species){
  const requestId=++diseaseRequestId;
  const list=document.getElementById("diseaseDbList");
  if(!list){console.warn("diseaseDbList element not found");return;}
  list.innerHTML='<div style="padding:12px"><div class="skeleton skeleton-card"></div><div class="skeleton skeleton-card" style="height:80px"></div><div class="skeleton skeleton-card" style="height:100px"></div></div>';
  fetchWithTimeout(`/api/health-check/diseases?species=${encodeURIComponent(species)}`).then(r=>r.json()).then(data=>{if(requestId!==diseaseRequestId||species!==currentSpecies)return;if(data.diseases){allDiseases=data.diseases;renderAzNav();renderDiseaseDb();}})
  .catch(()=>{if(requestId===diseaseRequestId&&list){list.innerHTML=`<div style="padding:20px;text-align:center;color:var(--gray-500)">${t("loadFailed")}<br><button class="retry-db-btn" style="margin-top:10px;padding:8px 20px;background:var(--navy);color:var(--white);border:none;border-radius:6px;cursor:pointer;font-size:.84rem">${t("reload")}</button></div>`;const rb=list.querySelector(".retry-db-btn");if(rb)rb.addEventListener("click",()=>loadDiseaseDb(species));}});
}

const DISEASE_CATEGORIES={
  infectious:{en:"Infectious",ja:"感染症",keywords:/infect|viral|virus|bacter|feline\s+(herpes|calici|immuno|leuk|panleuk)|parvovir|distemper|leptospir|bordetella|chlamyd|mycoplasm|fungal|aspergill|crypto|blastomyc|histoplasm|fip\b|fiv\b|felv\b|septice|abscess|pyometra|peritonitis|pneumonia|ehrlich|anaplasm|babesi|leishman|borreli|bartonell|neorick|hemoplasm|mycobact|nocardia|actinomyc|pythio|coccidio|dermatophyt|ringworm|sporotrich/i},
  neoplastic:{en:"Neoplastic",ja:"腫瘍",keywords:/tumor|tumour|neoplas|cancer|carcinom|lymphom|sarcoma|melanom|adenocarcin|fibrosarcom|hemangio|mast\s*cell|leukemia|lymphosarcom|meningiom|osteosarcom|squamous\s*cell|thymom|insulinom|pheochromocyt|chemodectom|histiocyt|plasmacytom|seminoma|mammary.*neoplas/i},
  cardiovascular:{en:"Cardiovascular",ja:"循環器",keywords:/cardi|heart|arrhythm|murmur|endocardi|myocardi|pericard|thromboembol|aortic|hypertens|dcm\b|hcm\b|valve|congesti.*heart|patent\s*ductus|tetralogy|atrial|ventricul|tachy|brady|fibrillat/i},
  respiratory:{en:"Respiratory",ja:"呼吸器",keywords:/respir|pulmonar|lung|bronch|trache|laryn|pleural|pneumothorax|asthma|rhinit|nasal.*polyp|brachycephal.*airway|collaps.*trache|pyothorax|chylothorax|diaphragm/i},
  gastrointestinal:{en:"Gastrointestinal",ja:"消化器",keywords:/gastro|intestin|digest|bowel|colitis|enterit|pancrea|hepat|liver|cholang|esophag|megaesoph|bloat|gastric.*dilat|volvulus|obstruct|foreign\s*body|ibd\b|exocrine|lipidos|cirrhos|portosystem|intussuscept|megacolon|constipat|ileus|stomatit|gingivit/i},
  renal:{en:"Renal/Urinary",ja:"泌尿器",keywords:/renal|kidney|urinar|urolithi|cystit|bladder|ureter|urethr|nephro|glomerul|polycyst|azotemi|ckd\b|akut.*kidney|flutd|fus\b|hydronephros/i},
  endocrine:{en:"Endocrine",ja:"内分泌",keywords:/endocrin|thyroid|diabet|cushing|addison|adrenal|hyperadrenocort|hypoadrenocort|insulin|pituitar|parathyroid|hypoglyce|hyperglyce|hypothyroid|hyperthyroid|acromegal/i},
  dermatological:{en:"Dermatological",ja:"皮膚",keywords:/dermat|skin|cutane|alopecia|pyoderma|atop|allerg.*dermat|hot\s*spot|mange|demodex|scabies|flea.*allerg|pemphig|lupus.*erythematos|sebace|follicul|acne|interdig|pododermat|erythem|pruritus|urticar/i},
  neurological:{en:"Neurological",ja:"神経",keywords:/neurolog|brain|spinal|seizure|epilep|vestibul|mening|encephal|myelop|disc\s*disease|ivdd|paralys|paresis|neuropath|polyneuropath|myasthenia|degenerat.*myelop|cerebell|hydrocephal|cognit.*dysfunction|wobbler|syringomyel|narcolep|head\s*tilt|ataxia/i},
  musculoskeletal:{en:"Musculoskeletal",ja:"筋骨格",keywords:/musculoskelet|orthop|fractur|luxat|cruciat|ligament|arthrit|dysplasia|osteochondr|spondyl|myosit|polymyosit|rhabdomyol|tendon|patella|elbow|hip\s*dysplasia|legg.*calve|hypertrophic.*osteodystro/i},
  ophthalmological:{en:"Ophthalmological",ja:"眼科",keywords:/ophthalm|eye|ocular|cornea|conjunctiv|glaucom|catarct|uveitis|retinal|keratit|ulcer.*cornea|corneal.*ulcer|cherry\s*eye|entropion|ectropion|prolapse.*eye|proptosis|lens.*luxat|progressive.*retinal|pannus|dry\s*eye|kcs\b|exophthalm/i},
  hematological:{en:"Hematological",ja:"血液",keywords:/hematolog|anemia|anaemia|thrombocytopen|pancytopen|coagulopath|hemolyt|polycythem|von\s*willebrand|hemophilia|dic\b|disseminat.*intravas|immune.*mediat.*anemia|imha\b|itp\b|blood.*parasit/i},
  dental:{en:"Dental",ja:"歯科",keywords:/dental|tooth|teeth|periodon|oral.*mass|epulis|oral.*tumor|gingiv|stomatit|resorptive.*lesion|odontoclast/i},
  parasitic:{en:"Parasitic",ja:"寄生虫",keywords:/parasit|heartworm|dirofilar|hookworm|roundworm|whipworm|tapeworm|giardia|coccidia|toxoplasm|tick.*borne|flea\b|mite|demodic|sarcoptic|ear\s*mite|cheyletiell|toxocar|ancylostom|trichuris|isospora|tritrichomonas/i},
  reproductive:{en:"Reproductive",ja:"生殖器",keywords:/reproduct|uterine|ovarian|testicular|prostat|mammary(?!.*neoplas)|dystocia|eclampsia|mastitis|cryptorchid|vaginal|vulvar|penile|balanoposthit/i},
  toxicological:{en:"Toxicological",ja:"中毒",keywords:/toxic|poison|intoxicat|overdose|envenomation|xylitol|chocolate|antifreeze|lily\s*toxic|nsaid.*toxic|acetaminophen|rat.*poison|rodenticide|organophos|ethylene\s*glycol/i},
  behavioral:{en:"Behavioral",ja:"行動",keywords:/behavio|anxiety|aggress|compulsive|phobia|cognit.*dysfunct|separ.*anxiety|noise.*phobia/i},
  congenital:{en:"Congenital",ja:"先天性",keywords:/congenit|develop|heredit|portosystem.*shunt|cleft.*palate|megaesoph.*congenit|atresia/i},
  immune:{en:"Immune-mediated",ja:"免疫",keywords:/immune.*mediat|auto.*immune|sle\b|systemic.*lupus|pemphig|polyarthrit.*immune|vasculit|eosinophil.*granulom/i},
};
const DISEASE_CAT_ORDER=["infectious","neoplastic","cardiovascular","respiratory","gastrointestinal","renal","endocrine","dermatological","neurological","musculoskeletal","ophthalmological","hematological","dental","parasitic","reproductive","toxicological","behavioral","congenital","immune"];
function classifyDisease(d){
  const text=(d.name||"")+" "+(d.name_ja||"")+" "+(d.description||"");
  for(const catId of DISEASE_CAT_ORDER){
    if(DISEASE_CATEGORIES[catId].keywords.test(text))return catId;
  }
  return "other";
}

let diseaseNavMode=null;
function _buildCatCounts(){
  const counts={};
  if(!allDiseases)return counts;
  allDiseases.forEach(d=>{const c=classifyDisease(d);counts[c]=(counts[c]||0)+1;});
  return counts;
}
function renderAzNav(){
  const azNav=document.getElementById("azNav");
  const catGrid=document.getElementById("diseaseCategoryGrid");
  if(!azNav){console.warn("azNav element not found");return;}
  if(diseaseNavMode===null)diseaseNavMode="category";
  const modeLabels={az:{next:"kana",label:"A-Z",switchLabel:currentLang==="ja"?"あいうえお順へ":"Switch to Kana"},kana:{next:"category",label:currentLang==="ja"?"あいうえお順":"Kana",switchLabel:currentLang==="ja"?"カテゴリ別へ":"Switch to Category"},category:{next:"az",label:currentLang==="ja"?"カテゴリ別":"Category",switchLabel:"A-Z"}};
  const cur=modeLabels[diseaseNavMode]||modeLabels.az;
  if(diseaseNavMode==="category"){
    azNav.style.display="none";
    if(catGrid){
      catGrid.style.display="";
      const counts=_buildCatCounts();
      const cats=[...DISEASE_CAT_ORDER,"other"];
      catGrid.innerHTML=`<div class="disease-cat-grid-header"><span>${currentLang==="ja"?"カテゴリで探す":"Browse by Category"}</span><button class="az-mode-toggle" aria-label="Switch sort mode">${cur.switchLabel}</button></div><div class="disease-cat-grid-body">`+cats.map(c=>{
        const cat=DISEASE_CATEGORIES[c];
        const lbl=currentLang==="ja"?(cat?.ja||"その他"):(cat?.en||"Other");
        const cnt=counts[c]||0;
        if(cnt===0)return"";
        const isActive=diseaseFilter===c;
        return`<button class="disease-cat-card${isActive?" active":""}" data-cat="${escapeHtml(c)}" aria-label="${escapeHtml(lbl)}"><span class="disease-cat-label">${escapeHtml(lbl)}</span><span class="disease-cat-count">${cnt}</span></button>`;
      }).join("")+`</div>`;
      const nextMode=cur.next;
      catGrid.querySelector(".az-mode-toggle").addEventListener("click",function(){diseaseNavMode=nextMode;diseaseFilter='';renderAzNav();renderDiseaseDb();});
      catGrid.addEventListener("click",e=>{
        const btn=e.target.closest(".disease-cat-card[data-cat]");
        if(!btn)return;
        const cat=btn.dataset.cat;
        if(diseaseFilter===cat){diseaseFilter='';btn.classList.remove("active");}
        else{catGrid.querySelectorAll(".disease-cat-card").forEach(b=>b.classList.remove("active"));btn.classList.add("active");diseaseFilter=cat;}
        diseaseDisplayLimit=100;renderDiseaseDb();
      });
    }
  }else{
    azNav.style.display="";
    if(catGrid)catGrid.style.display="none";
    const isAz=diseaseNavMode==="az";
    const letters=isAz?"ABCDEFGHIJKLMNOPQRSTUVWXYZ".split(""):"あ か さ た な は ま や ら わ".split(" ");
    azNav.innerHTML=`<button class="az-mode-toggle" aria-label="Switch sort mode">${cur.switchLabel}</button><button class="active" data-letter="" aria-label="Show all">ALL</button>`+letters.map(l=>`<button data-letter="${l}" aria-label="Filter by ${l}">${l}</button>`).join("");
    const nextMode=cur.next;
    azNav.querySelector(".az-mode-toggle").addEventListener("click",function(){diseaseNavMode=nextMode;diseaseFilter='';renderAzNav();renderDiseaseDb();});
    azNav.addEventListener("click",e=>{const btn=e.target.closest("button[data-letter]");if(btn)filterDiseaseDb(btn.dataset.letter);});
  }
}

function filterDiseaseDb(letter){
  diseaseFilter=letter;
  diseaseDisplayLimit=100;
  document.querySelectorAll(".az-nav button:not(.az-mode-toggle)").forEach(b=>b.classList.toggle("active",b.dataset.letter===letter));
  renderDiseaseDb();
}

let diseaseDisplayLimit=100;
function renderDiseaseDb(){
  const list=document.getElementById("diseaseDbList");
  const search=(document.getElementById("diseaseSearch").value||"").toLowerCase();
  let filtered=allDiseases;
  if(diseaseFilter){
    if(diseaseNavMode==="kana"){
      /* あいうえお行フィルタ: localeCompare("ja")で漢字も読み順でグループ化 */
      const kanaRanges={"あ":["あ","か"],"か":["か","さ"],"さ":["さ","た"],"た":["た","な"],"な":["な","は"],"は":["は","ま"],"ま":["ま","や"],"や":["や","ら"],"ら":["ら","わ"],"わ":["わ","\uffff"]};
      const kanaRow={"あ":"あいうえお","か":"かきくけこがぎぐげご","さ":"さしすせそざじずぜぞ","た":"たちつてとだぢづでど","な":"なにぬねの","は":"はひふへほばびぶべぼぱぴぷぺぽ","ま":"まみむめも","や":"やゆよ","ら":"らりるれろ","わ":"わをん"};
      const range=kanaRanges[diseaseFilter];
      const row=kanaRow[diseaseFilter]||diseaseFilter;
      filtered=filtered.filter(d=>{
        /* name_ja_sort があればまずそれで判定 */
        const sort=(d.name_ja_sort||"");
        if(sort&&row.includes(sort.charAt(0)))return true;
        /* localeCompare レンジチェック（漢字を読み順で判定） */
        const ja=(d.name_ja||"");
        if(!ja)return false;
        if(range&&ja.localeCompare(range[0],"ja")>=0&&ja.localeCompare(range[1],"ja")<0)return true;
        return row.includes(ja.charAt(0));
      });
    }else if(diseaseNavMode==="category"){
      filtered=filtered.filter(d=>classifyDisease(d)===diseaseFilter);
    }else{
      filtered=filtered.filter(d=>(d.name||"").toUpperCase().startsWith(diseaseFilter));
    }
  }
  if(search)filtered=filtered.filter(d=>(d.name||"").toLowerCase().includes(search)||(d.name_ja||"").toLowerCase().includes(search)||(d.description||"").toLowerCase().includes(search)||(d.description_ja||"").toLowerCase().includes(search));
  const sortJa=(a,b)=>(a.name_ja_sort||a.name_ja||a.name||"").localeCompare(b.name_ja_sort||b.name_ja||b.name||"","ja");
  const sortEn=(a,b)=>(a.name||"").localeCompare(b.name||"","en");
  const sortFn=currentLang==="ja"?sortJa:sortEn;
  if(diseaseNavMode==="category"&&!diseaseFilter){
    /* カテゴリ別グループ表示: カテゴリごとにヘッダー + あいうえお/A-Z順 */
    filtered=filtered.slice().map(d=>({...d,_cat:classifyDisease(d)}));
    const groups={};
    filtered.forEach(d=>{const c=d._cat;if(!groups[c])groups[c]=[];groups[c].push(d);});
    for(const k of Object.keys(groups))groups[k].sort(sortFn);
    const orderedCats=[...DISEASE_CAT_ORDER,"other"].filter(c=>groups[c]&&groups[c].length);
    filtered=[];
    orderedCats.forEach(c=>{filtered.push({_catHeader:c});filtered.push(...groups[c]);});
  }else{
    filtered=filtered.slice().sort(sortFn);
  }
  const totalCount=filtered.filter(d=>!d._catHeader).length;
  document.getElementById("diseaseDbCount").textContent=t("diseaseCount").replace("%filtered%",totalCount).replace("%total%",allDiseases.length);
  if(totalCount===0){list.innerHTML=`<div style="padding:20px;text-align:center;color:var(--gray-500)">${t("noDiseaseMatch")}</div>`;return;}
  const pk=(ja,en)=>currentLang==="ja"?(ja||en||""):(en||ja||"");
  const shown=filtered.slice(0,diseaseDisplayLimit);
  list.innerHTML=shown.map(d=>{
    if(d._catHeader){const cat=DISEASE_CATEGORIES[d._catHeader];const lbl=currentLang==="ja"?(cat?.ja||"その他"):(cat?.en||"Other");return`<div class="disease-cat-header" role="heading" aria-level="3">${lbl}</div>`;}
    const diseaseName=d.name_ja||d.name||"Disease";
    const desc=pk(d.description_ja,d.description)||buildFieldFallback(t("dtDescription"),diseaseName);
    const patho=pk(d.pathophysiology_ja,d.pathophysiology)||buildFieldFallback(t("dtPathophysiology"),diseaseName);
    const causes=pk(d.causes_ja,d.causes)||buildFieldFallback(t("dtCauses"),diseaseName);
    const prevention=pk(d.prevention_ja,d.prevention)||buildFieldFallback(t("dtPrevention"),diseaseName);
    const treatment=pk(d.treatment_ja,d.treatment)||buildFieldFallback(t("dtTreatment"),diseaseName);
    const prognosis=pk(d.prognosis_detailed_ja,d.prognosis_detailed)||pk(d.prognosis_ja,d.prognosis)||buildFieldFallback(t("dtPrognosis"),diseaseName);
    const dNameEn=highlightMatch(d.name||"",search);
    const dNameJa=highlightMatch(d.name_ja||"",search);
    const dPrimary=currentLang==="ja"?dNameJa:dNameEn;
    const dSecondary=currentLang==="ja"?dNameEn:dNameJa;
    const dDesc=desc.substring(0,80)+(desc.length>80?"...":"");
    const rehab=d.rehabilitation_protocol_ja||d.rehabilitation_protocol||"";
    const nutrition=d.nutrition_management_ja||d.nutrition_management||"";
    const recoveryWeeks=d.recovery_timeline_weeks;
    const successRate=d.success_rate;
    const mortalityRate=d.mortality_rate;
    const hasEnrichment=rehab||nutrition||recoveryWeeks||successRate!==undefined;
    const _dCat=d._cat||classifyDisease(d);
    const _dCatObj=DISEASE_CATEGORIES[_dCat];
    const _dCatLbl=currentLang==="ja"?(_dCatObj?.ja||"その他"):(_dCatObj?.en||"Other");
    return`<div class="disease-db-item" role="button" tabindex="0" aria-expanded="false">
      <div class="d-name">${dPrimary} <span class="d-name-ja">${dSecondary}</span><span class="quality-badge ${(Number(d.completeness_score||100)>=90)?"quality-ok":"quality-warn"}">${Number(d.completeness_score||100)}%</span></div>
      <div class="d-meta"><span class="d-cat-badge" data-cat="${escapeHtml(_dCat)}">${escapeHtml(_dCatLbl)}</span></div>
      <div class="d-desc">${highlightMatch(dDesc,search)}</div>
      <div class="disease-detail"><dl>
        <dt>${t("dtDescription")}</dt><dd>${escapeHtml(desc)}</dd>
        <dt>${t("dtPathophysiology")}</dt><dd>${escapeHtml(patho)}</dd>
        <dt>${t("dtCauses")}</dt><dd>${escapeHtml(causes)}</dd>
        <dt>${t("dtPrevention")}</dt><dd>${escapeHtml(prevention)}</dd>
        <dt>${t("dtTreatment")}</dt><dd>${escapeHtml(treatment)}</dd>
        <dt>${t("dtPrognosis")}</dt><dd>${escapeHtml(prognosis)}</dd>
        ${d.symptoms?`<dt>${t("dtSymptoms")}</dt><dd>${escapeHtml(Array.isArray(d.symptoms)?d.symptoms.join(", "):(typeof d.symptoms==="object"?Object.keys(d.symptoms).join(", "):String(d.symptoms)))}</dd>`:""}
        ${d.recommended_tests?`<dt>${t("dtRecommendedTests")}</dt><dd>${escapeHtml(d.recommended_tests.join(", "))}</dd>`:""}
        ${rehab?`<dt>リハビリテーション/Rehabilitation</dt><dd><pre style="white-space:pre-wrap;font-family:inherit;margin:0">${escapeHtml(rehab)}</pre></dd>`:""}
        ${nutrition?`<dt>栄養管理/Nutrition Management</dt><dd><pre style="white-space:pre-wrap;font-family:inherit;margin:0">${escapeHtml(nutrition)}</pre></dd>`:""}
        ${recoveryWeeks?`<dt>回復期間/Recovery Timeline</dt><dd>${recoveryWeeks}週間 / ${recoveryWeeks} weeks</dd>`:""}
        ${successRate!==undefined?`<dt>成功率/Success Rate</dt><dd>${(successRate*100).toFixed(1)}%</dd>`:""}
        ${mortalityRate!==undefined?`<dt>死亡率/Mortality Rate</dt><dd>${(mortalityRate*100).toFixed(1)}%</dd>`:""}
      </dl>${renderOrthopedicReferences(d)}<div style="margin-top:8px"><a href="/diseases/${encodeURIComponent(currentSpecies)}/${encodeURIComponent((d.name||"").toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,''))}" target="_blank" rel="noopener" style="font-size:.82rem;color:var(--green);font-weight:600;text-decoration:none">📖 ${currentLang==="ja"?"詳細ページを見る":"View full page"} →</a></div>${d.content_origin?`<div class="missing-note">${currentLang==="ja"?"データソース":"Content source"}: ${escapeHtml(d.content_origin)}</div>`:""}${renderCitationMap(d)}${renderReferenceLinks(d)}${(d.missing_fields&&d.missing_fields.length)?`<div class="missing-note">${currentLang==="ja"?"要確認データ":"Data needs review"}: ${escapeHtml(d.missing_fields.join(", "))}</div>`:""}</div>
    </div>`}).join("");
  const shownCount=shown.filter(d=>!d._catHeader).length;
  if(totalCount>shownCount){
    const remaining=totalCount-shownCount;
    const showMoreBtn=document.createElement("button");
    showMoreBtn.className="show-more-btn";
    showMoreBtn.style.cssText="display:block;margin:16px auto;padding:8px 24px;border:1px solid var(--gray-300);border-radius:6px;background:var(--white);cursor:pointer";
    showMoreBtn.textContent=currentLang==="ja"?`さらに表示 (残り${remaining}件)`:`Show more (${remaining} remaining)`;
    showMoreBtn.addEventListener("click",function(){diseaseDisplayLimit+=100;renderDiseaseDb();});
    list.appendChild(showMoreBtn);
  }
}

function switchView(view){
  trackEvent("switch_view",{view:view});
  const views=["checker","database","chat","drugs","anesthesia"];
  const prefersReduced=window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  views.forEach(v=>{
    const tab=document.getElementById("tab-"+v);
    const panel=document.getElementById("view"+v.charAt(0).toUpperCase()+v.slice(1));
    if(tab)tab.setAttribute("aria-selected",v===view);
    if(panel){
      if(v===view){panel.classList.remove("hidden");if(!prefersReduced)panel.style.animation="fade-tab-in .3s ease-out";}
      else{panel.classList.add("hidden");panel.style.animation="";}
    }
  });
  history.replaceState(null,null,"#"+view);
  if(view==="drugs"&&!drugsLoaded)loadDrugDictionary();
  if(view==="anesthesia"&&!anesthesiaLoaded)loadAnesthesiaProtocols();
  /* フォーカスを新しいパネルの最初のインタラクティブ要素に移動 */
  const activePanel=document.getElementById("view"+view.charAt(0).toUpperCase()+view.slice(1));
  if(activePanel){const focusable=activePanel.querySelector("input,select,button:not([disabled]),textarea,[tabindex='0']");if(focusable)setTimeout(()=>focusable.focus(),50);}
  /* モバイル: ハンバーガーメニューを閉じる */
  const nav=document.getElementById("mainNav");
  if(nav&&nav.classList.contains("open")){nav.classList.remove("open");const hb=document.querySelector(".hamburger");if(hb)hb.setAttribute("aria-expanded","false");}
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
    if(["checker","database","chat","drugs","anesthesia"].includes(hash))switchView(hash);
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
  const loading=document.createElement("div");loading.className="chat-msg bot typing-indicator";loading.innerHTML='<span class="dot"></span><span class="dot"></span><span class="dot"></span>';msgs.appendChild(loading);msgs.scrollTop=msgs.scrollHeight;
  fetchWithTimeout("/api/diagnostic-chat/chat",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message:text,species:species,previous_symptoms:chatAccumulatedSymptoms,lang:currentLang})})
  .then(r=>{if(!r.ok)throw new Error(`HTTP ${r.status}`);return r.json();})
  .then(data=>{
    loading.remove();
    if(!data){addChatMsg(t("noResponse"),"bot");return;}
    if(data.accumulated_symptoms) chatAccumulatedSymptoms=data.accumulated_symptoms;
    renderChatResult(msgs,data);
  })
  .catch(err=>{
    loading.remove();
    console.error("Chat error:",err);
    const errDiv=document.createElement("div");errDiv.className="chat-msg bot";errDiv.textContent=t("commError")+" ("+err.message+")";msgs.appendChild(errDiv);
    msgs.scrollTop=msgs.scrollHeight;
  });
}

// Accumulated symptoms for chat conversation continuity
let chatAccumulatedSymptoms=[];
let chatDeniedSymptoms=[];

function _sendSymptomUpdate(symptomId,confirmed){
  const species=currentSpecies||"dog";
  if(!confirmed)chatDeniedSymptoms.push(symptomId);
  const msgs=document.getElementById("chatMessages");
  // Show brief status
  const statusMsg=confirmed?(currentLang==="ja"?"症状を追加しました。再解析中...":"Added symptom. Re-analyzing..."):(currentLang==="ja"?"了解しました。他の症状を確認します。":"Understood. Checking other symptoms.");
  addChatMsg(statusMsg,"bot-brief");
  const loading=document.createElement("div");loading.className="chat-msg bot typing-indicator";loading.innerHTML='<span class="dot"></span><span class="dot"></span><span class="dot"></span>';msgs.appendChild(loading);msgs.scrollTop=msgs.scrollHeight;
  fetchWithTimeout("/api/diagnostic-chat/chat",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message:confirmed?symptomId:"",species:species,previous_symptoms:chatAccumulatedSymptoms})})
  .then(r=>{if(!r.ok)throw new Error(`HTTP ${r.status}`);return r.json();})
  .then(data=>{
    loading.remove();
    if(!data)return;
    if(data.accumulated_symptoms)chatAccumulatedSymptoms=data.accumulated_symptoms;
    renderChatResult(msgs,data);
  })
  .catch(err=>{loading.remove();console.error("Symptom update error:",err);});
}

function sendChatMessage(){
  const input=document.getElementById("chatInput"),text=input.value.trim();if(!text)return;input.value="";
  trackEvent("chat_message",{species:currentSpecies||"dog",message_length:text.length});
  addChatMsg(text,"user");const species=currentSpecies||"dog";
  const msgs=document.getElementById("chatMessages");
  const loading=document.createElement("div");loading.className="chat-msg bot typing-indicator";loading.innerHTML='<span class="dot"></span><span class="dot"></span><span class="dot"></span>';msgs.appendChild(loading);msgs.scrollTop=msgs.scrollHeight;
  fetchWithTimeout("/api/diagnostic-chat/chat",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message:text,species:species,previous_symptoms:chatAccumulatedSymptoms,lang:currentLang})})
  .then(r=>{if(!r.ok)throw new Error(`HTTP ${r.status}`);return r.json();})
  .then(data=>{
    loading.remove();
    if(!data){addChatMsg(t("noResponse"),"bot");return;}
    // Update accumulated symptoms
    if(data.accumulated_symptoms) chatAccumulatedSymptoms=data.accumulated_symptoms;
    // Render rich response
    renderChatResult(msgs,data);
  })
  .catch(err=>{
    loading.remove();
    console.error("Chat error:",err);
    trackEvent("api_error",{endpoint:"diagnostic-chat",error:String(err.message||"unknown").substring(0,100),species:currentSpecies});
    addChatMsg(t("commError")+" ("+err.message+")","bot");
  });
}

function renderChatResult(container,data){
  const wrapper=document.createElement("div");
  wrapper.className="chat-msg bot chat-result";

  // 1. Species guidance
  if(data.species_guidance){
    const g=document.createElement("div");
    g.className="chat-species-guidance";
    g.textContent=data.species_guidance;
    wrapper.appendChild(g);
  }

  // 2. Extracted symptoms tags
  const symptoms=data.symptom_details||[];
  if(symptoms.length>0){
    const symDiv=document.createElement("div");
    symDiv.className="chat-symptoms-tags";
    const label=document.createElement("span");
    label.className="chat-symptoms-label";
    label.textContent=currentLang==="ja"?"\u691c\u51fa\u3055\u308c\u305f\u75c7\u72b6: ":"Detected symptoms: ";
    symDiv.appendChild(label);
    symptoms.forEach(s=>{
      const tag=document.createElement("span");
      tag.className="chat-symptom-tag";
      tag.textContent=currentLang==="ja"?(s.name_ja||s.name_en||s.id):(s.name_en||s.name_ja||s.id);
      symDiv.appendChild(tag);
    });
    wrapper.appendChild(symDiv);
  }

  // 3. Low-info warning (when 1-2 symptoms only)
  if(data.low_info_warning){
    const warnDiv=document.createElement("div");
    warnDiv.style.cssText="padding:8px 12px;margin:8px 0;background:#fff8e1;border-left:3px solid #f59e0b;border-radius:6px;font-size:.8rem;color:#92400e";
    warnDiv.textContent=data.low_info_warning;
    wrapper.appendChild(warnDiv);
  }

  // 4. Disease candidate cards
  const candidates=data.disease_candidates||[];
  if(candidates.length>0){
    const listDiv=document.createElement("div");
    listDiv.className="chat-disease-list";
    candidates.slice(0,5).forEach((c,i)=>{
      const card=document.createElement("div");
      card.className="chat-disease-card";
      const pct=Math.round((c.similarity_score||0)*100);
      const sevClass=c.severity==="high"||c.severity==="critical"?"sev-high":c.severity==="medium"?"sev-med":"sev-low";
      card.innerHTML=`
        <div class="chat-disease-head">
          <span class="chat-disease-rank">${i+1}</span>
          <span class="chat-disease-name">${escapeHtml(currentLang==="ja"?(c.name_ja||c.name_en||c.disease_id):(c.name_en||c.name_ja||c.disease_id))}</span>
          <span class="chat-disease-name-en">${escapeHtml(currentLang==="ja"?(c.name_en||""):(c.name_ja||""))}</span>
          <span class="chat-disease-pct ${sevClass}">${pct}%</span>
        </div>
        <div class="chat-disease-bar-bg"><div class="chat-disease-bar ${sevClass}" style="width:${pct}%"></div></div>
        ${(currentLang==="ja"?(c.description_ja||c.description):(c.description||c.description_ja))?`<div class="chat-disease-desc">${escapeHtml(currentLang==="ja"?(c.description_ja||c.description):(c.description||c.description_ja))}</div>`:""}
        ${c.matched_symptoms&&c.matched_symptoms.length?`<div class="chat-disease-matched">\u4e00\u81f4: ${c.matched_symptoms.map(s=>escapeHtml(s)).join(", ")}</div>`:""}
        ${c.mentioned_drugs&&c.mentioned_drugs.length?renderMentionedDrugs(c):""}
      `;
      listDiv.appendChild(card);
    });
    wrapper.appendChild(listDiv);
  } else if(symptoms.length>0){
    const noMatch=document.createElement("div");
    noMatch.className="chat-no-match";
    noMatch.textContent=currentLang==="ja"?"\u8a72\u5f53\u3059\u308b\u75be\u60a3\u304c\u898b\u3064\u304b\u308a\u307e\u305b\u3093\u3067\u3057\u305f\u3002\u3082\u3046\u5c11\u3057\u8a73\u3057\u304f\u75c7\u72b6\u3092\u6559\u3048\u3066\u304f\u3060\u3055\u3044\u3002":"No matching diseases found. Please describe more symptoms.";
    wrapper.appendChild(noMatch);
  } else {
    const noSym=document.createElement("div");
    noSym.className="chat-no-symptoms";
    noSym.textContent=currentLang==="ja"?"\u75c7\u72b6\u3092\u691c\u51fa\u3067\u304d\u307e\u305b\u3093\u3067\u3057\u305f\u3002\u5177\u4f53\u7684\u306a\u75c7\u72b6\u3092\u5165\u529b\u3057\u3066\u304f\u3060\u3055\u3044\u3002\n\u4f8b: \u300c\u54b3\u304c\u51fa\u308b\u300d\u300c\u8ddb\u884c\u3057\u3066\u3044\u308b\u300d\u300c\u5143\u6c17\u304c\u306a\u3044\u300d":"No symptoms detected. Please enter specific symptoms.\nExample: coughing, limping, lethargy";
    wrapper.appendChild(noSym);
  }

  // 4. Follow-up questions (interactive consultation style)
  const fqs=data.follow_up_questions||[];
  if(fqs.length>0){
    const fqDiv=document.createElement("div");
    fqDiv.className="chat-followup";
    const fqLabel=document.createElement("div");
    fqLabel.className="chat-followup-label";
    fqLabel.textContent=currentLang==="ja"?"追加の確認をさせてください：":"Let me ask a few more questions:";
    fqDiv.appendChild(fqLabel);
    fqs.forEach(fq=>{
      if(fq.type==="symptom_check"&&fq.options&&fq.options.length>=2){
        // Interactive yes/no symptom question
        const qRow=document.createElement("div");
        qRow.className="chat-symptom-question";
        const qText=document.createElement("span");
        qText.className="chat-q-text";
        qText.textContent=currentLang==="ja"?(fq.question_ja||""):(fq.question_en||"");
        qRow.appendChild(qText);
        const btnGroup=document.createElement("span");
        btnGroup.className="chat-q-btns";
        fq.options.forEach(opt=>{
          const btn=document.createElement("button");
          const isYes=opt.value.startsWith("+");
          btn.className="chat-q-btn "+(isYes?"chat-q-yes":"chat-q-no");
          btn.textContent=currentLang==="ja"?(opt.label_ja||""):(opt.label_en||"");
          btn.addEventListener("click",()=>{
            // Disable all buttons in this question row
            qRow.querySelectorAll("button").forEach(b=>{b.disabled=true;b.classList.add("answered");});
            btn.classList.add("selected");
            if(isYes){
              const sid=opt.value.substring(1);
              chatAccumulatedSymptoms.push(sid);
              // Auto-trigger re-analysis with updated symptoms
              _sendSymptomUpdate(sid,true);
            }else{
              _sendSymptomUpdate(fq.symptom_id,false);
            }
          });
          btnGroup.appendChild(btn);
        });
        qRow.appendChild(btnGroup);
        fqDiv.appendChild(qRow);
      }else{
        // Onset / age / free-text questions (existing behavior)
        if(fq.options&&fq.options.length>0){
          const qRow=document.createElement("div");
          qRow.className="chat-symptom-question";
          const qText=document.createElement("span");
          qText.className="chat-q-text";
          qText.textContent=currentLang==="ja"?(fq.question_ja||""):(fq.question_en||"");
          qRow.appendChild(qText);
          const btnGroup=document.createElement("span");
          btnGroup.className="chat-q-btns";
          fq.options.forEach(opt=>{
            const btn=document.createElement("button");
            btn.className="chat-followup-btn";
            btn.textContent=currentLang==="ja"?(opt.label_ja||""):(opt.label_en||"");
            btn.addEventListener("click",()=>{
              qRow.querySelectorAll("button").forEach(b=>{b.disabled=true;b.classList.add("answered");});
              btn.classList.add("selected");
              const chatInput=document.getElementById("chatInput");
              if(chatInput){chatInput.value=btn.textContent;sendChatMessage();}
            });
            btnGroup.appendChild(btn);
          });
          qRow.appendChild(btnGroup);
          fqDiv.appendChild(qRow);
        }else{
          const btn=document.createElement("button");
          btn.className="chat-followup-btn";
          btn.textContent=currentLang==="ja"?(fq.question_ja||""):(fq.question_en||"");
          btn.addEventListener("click",()=>{
            const chatInput=document.getElementById("chatInput");
            if(chatInput){chatInput.value=btn.textContent;sendChatMessage();}
          });
          fqDiv.appendChild(btn);
        }
      }
    });
    wrapper.appendChild(fqDiv);
  }

  // 5. Common diseases & breed ecology for chat
  if(candidates.length>0&&currentSpecies){
    const chatRef=document.createElement("div");
    chatRef.className="chat-reference-section";
    wrapper.appendChild(chatRef);
    fetchWithTimeout(`/api/species/${encodeURIComponent(currentSpecies)}/common-diseases`).then(r=>r.json()).then(data=>{
      const diseases=data.common_diseases||[];
      if(!diseases.length)return;
      const veryCommon=diseases.filter(d=>d.prevalence==="very_common");
      const common=diseases.filter(d=>d.prevalence==="common");
      const renderTags=(list,cls)=>list.map(d=>{
        const n=currentLang==="ja"?(d.name_ja||d.name):d.name;
        return `<span class="common-disease-tag ${cls}">${escapeHtml(n)}</span>`;
      }).join("");
      chatRef.innerHTML=`<div class="common-diseases-section compact">
        <div class="common-diseases-header">${currentLang==="ja"?"📋 この動物種でよくみられる疾患":"📋 Common diseases in this species"}</div>
        ${veryCommon.length?`<div class="common-diseases-group">${renderTags(veryCommon,"tag-very-common")}</div>`:""}
        ${common.length?`<div class="common-diseases-group">${renderTags(common,"tag-common")}</div>`:""}
      </div>`;
    }).catch(()=>{});
  }

  // 6. Disclaimer
  const disc=document.createElement("div");
  disc.className="chat-disclaimer";
  disc.textContent=currentLang==="ja"?"\u203b \u3053\u3061\u3089\u306f\u53c2\u8003\u60c5\u5831\u3067\u3059\u3002\u7363\u533b\u5e2b\u306e\u8a3a\u5bdf\u3092\u53d7\u3051\u3066\u304f\u3060\u3055\u3044\u3002":"\u203b This is reference information. Please consult a veterinarian.";
  wrapper.appendChild(disc);

  container.appendChild(wrapper);
  container.scrollTop=container.scrollHeight;
}

function addChatMsg(text,type){
  const msgs=document.getElementById("chatMessages"),div=document.createElement("div");
  div.className=`chat-msg ${type}`;div.textContent=text;
  msgs.appendChild(div);msgs.scrollTop=msgs.scrollHeight;
}

// =============================================================================
// GUIDED CONSULTATION (問診モード)
// =============================================================================
let guidedState={
  species:null,
  selectedSymptoms:[],
  answeredCategories:[],
  onset:null,
  ageYears:null,
  phase:"start"
};

function setupGuidedConsultation(){
  const freeBtn=document.getElementById("chatModeFree");
  const guidedBtn=document.getElementById("chatModeGuided");
  if(!freeBtn||!guidedBtn)return;
  freeBtn.addEventListener("click",()=>switchChatMode("free"));
  guidedBtn.addEventListener("click",()=>switchChatMode("guided"));
}

function switchChatMode(mode){
  const freeBtn=document.getElementById("chatModeFree");
  const guidedBtn=document.getElementById("chatModeGuided");
  const freeCont=document.getElementById("chatFreeContainer");
  const guidedCont=document.getElementById("chatGuidedContainer");
  if(!freeCont||!guidedCont)return;
  if(mode==="guided"){
    freeBtn.classList.remove("active");guidedBtn.classList.add("active");
    freeCont.classList.add("hidden");guidedCont.classList.remove("hidden");
    startGuidedConsultation();
  } else {
    guidedBtn.classList.remove("active");freeBtn.classList.add("active");
    guidedCont.classList.add("hidden");freeCont.classList.remove("hidden");
  }
}

function startGuidedConsultation(){
  guidedState={species:currentSpecies||"dog",selectedSymptoms:[],answeredCategories:[],onset:null,ageYears:null,painScore:null,phase:"start",breed:currentBreed||""};
  const msgs=document.getElementById("guidedMessages");
  const actions=document.getElementById("guidedActions");
  if(msgs)msgs.innerHTML="";
  if(actions)actions.innerHTML="";
  guidedFetch("start");
}

function guidedAddMsg(html,type){
  const msgs=document.getElementById("guidedMessages");
  if(!msgs)return;
  const div=document.createElement("div");
  div.className=`chat-msg ${type||"bot"}`;
  div.innerHTML=html;
  msgs.appendChild(div);
  msgs.scrollTop=msgs.scrollHeight;
}

function guidedSetActions(html){
  const actions=document.getElementById("guidedActions");
  if(!actions)return;
  actions.innerHTML=html;
  const msgs=document.getElementById("guidedMessages");
  if(msgs)msgs.scrollTop=msgs.scrollHeight;
}

var _guidedFetching=false;
function guidedFetch(phase,extra){
  if(_guidedFetching)return;
  _guidedFetching=true;
  // Disable all action buttons to prevent double-submission
  document.querySelectorAll("#guidedActions button").forEach(b=>{b.disabled=true;});
  const body={
    species:guidedState.species,
    phase:phase,
    selected_symptoms:guidedState.selectedSymptoms,
    answered_categories:guidedState.answeredCategories,
    onset:guidedState.onset,
    age_years:guidedState.ageYears,
    pain_score:guidedState.painScore,
    breed:guidedState.breed||"",
    lang:currentLang,
    ...(extra||{})
  };
  guidedAddMsg('<span class="dot"></span><span class="dot"></span><span class="dot"></span>',"bot typing-indicator");
  fetchWithTimeout("/api/diagnostic-chat/consultation",{
    method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)
  })
  .then(r=>{if(!r.ok)throw new Error(`HTTP ${r.status}`);return r.json();})
  .then(data=>{
    _guidedFetching=false;
    // Remove typing indicator
    const msgs=document.getElementById("guidedMessages");
    const typing=msgs?.querySelector(".typing-indicator");
    if(typing)typing.remove();
    guidedHandleResponse(data);
  })
  .catch(err=>{
    _guidedFetching=false;
    const msgs=document.getElementById("guidedMessages");
    const typing=msgs?.querySelector(".typing-indicator");
    if(typing)typing.remove();
    guidedAddMsg(escapeHtml(t("commError")+" ("+err.message+")"),"bot");
    guidedSetActions(`<div class="guided-bottom-actions"><button class="guided-action-btn secondary" id="guidedRetryBtn">${currentLang==="ja"?"やり直す":"Start Over"}</button></div>`);
    const rb=document.getElementById("guidedRetryBtn");
    if(rb)rb.addEventListener("click",()=>{guidedSetActions("");startGuidedConsultation();});
  });
}

function guidedHandleResponse(data){
  const lang=currentLang;
  const msgKey=lang==="ja"?"message_ja":"message_en";
  if(data[msgKey])guidedAddMsg(escapeHtml(data[msgKey]),"bot");

  if(data.phase==="select_category"){
    guidedRenderCategories(data.categories||[]);
  } else if(data.phase==="show_symptoms"){
    guidedRenderSymptoms(data);
  } else if(data.phase==="interim_results"){
    guidedRenderInterim(data);
  } else if(data.phase==="context_questions"){
    guidedRenderContextQuestions(data.questions||[]);
  } else if(data.phase==="final_results"){
    guidedRenderFinalResults(data);
  } else if(data.error){
    guidedAddMsg(escapeHtml(data.error),"bot");
    guidedSetActions(`<div class="guided-bottom-actions"><button class="guided-action-btn secondary" id="guidedRetryBtn">${currentLang==="ja"?"やり直す":"Start Over"}</button></div>`);
    const rb=document.getElementById("guidedRetryBtn");
    if(rb)rb.addEventListener("click",()=>{guidedSetActions("");startGuidedConsultation();});
  } else if(!data.phase&&!data[msgKey]){
    guidedAddMsg(currentLang==="ja"?"予期しないレスポンスです。やり直してください。":"Unexpected response. Please start over.","bot");
    guidedSetActions(`<div class="guided-bottom-actions"><button class="guided-action-btn secondary" id="guidedRetryBtn">${currentLang==="ja"?"やり直す":"Start Over"}</button></div>`);
    const rb2=document.getElementById("guidedRetryBtn");
    if(rb2)rb2.addEventListener("click",()=>{guidedSetActions("");startGuidedConsultation();});
  }
}

function guidedRenderCategories(categories){
  let html='<div class="guided-category-grid">';
  categories.forEach(c=>{
    const label=currentLang==="ja"?c.name_ja:c.name_en;
    html+=`<button class="guided-cat-btn" data-cat="${c.id}"><span class="guided-cat-name">${label}</span><span class="guided-cat-count">${c.symptom_count}</span></button>`;
  });
  html+='</div>';
  guidedSetActions(html);
  document.querySelectorAll(".guided-cat-btn").forEach(btn=>{
    btn.addEventListener("click",()=>{
      const cat=btn.dataset.cat;
      const label=currentLang==="ja"?btn.querySelector(".guided-cat-name").textContent:btn.querySelector(".guided-cat-name").textContent;
      guidedAddMsg(label,"user");
      guidedSetActions("");
      guidedFetch("select_symptoms",{selected_category:cat});
    });
  });
}

function guidedRenderSymptoms(data){
  const symptoms=data.symptoms||[];
  const selected=new Set(guidedState.selectedSymptoms);
  let html='<div class="guided-symptom-grid">';
  symptoms.forEach(s=>{
    const label=currentLang==="ja"?s.name_ja:s.name_en;
    const cls=selected.has(s.id)?"guided-sym-btn selected":"guided-sym-btn";
    html+=`<button class="${cls}" data-sid="${s.id}">${label}</button>`;
  });
  html+='</div>';
  html+=`<div class="guided-bottom-actions">`;
  html+=`<button class="guided-action-btn text" id="guidedBackToCategories">${currentLang==="ja"?"← カテゴリに戻る":"← Back"}</button>`;
  html+=`<button class="guided-action-btn primary" id="guidedConfirmSymptoms">${t("guidedNext")}</button>`;
  html+=`</div>`;
  guidedSetActions(html);

  // Toggle symptoms
  document.querySelectorAll(".guided-sym-btn").forEach(btn=>{
    btn.addEventListener("click",()=>{
      const sid=btn.dataset.sid;
      if(btn.classList.contains("selected")){
        btn.classList.remove("selected");
        selected.delete(sid);
      } else {
        btn.classList.add("selected");
        selected.add(sid);
      }
    });
  });

  // Back to categories
  const backBtn=document.getElementById("guidedBackToCategories");
  if(backBtn)backBtn.addEventListener("click",()=>{
    guidedSetActions("");
    guidedFetch("start");
  });

  // Confirm
  const confirmBtn=document.getElementById("guidedConfirmSymptoms");
  if(confirmBtn)confirmBtn.addEventListener("click",()=>{
    const newSymptoms=[...selected];
    if(newSymptoms.length===0){return;}
    guidedState.selectedSymptoms=newSymptoms;
    if(!guidedState.answeredCategories.includes(data.category)){
      guidedState.answeredCategories.push(data.category);
    }
    // Show selected symptoms as user message
    const labels=symptoms.filter(s=>selected.has(s.id)).map(s=>currentLang==="ja"?s.name_ja:s.name_en);
    guidedAddMsg(labels.join("、"),"user");
    guidedSetActions("");
    guidedFetch("next_category");
  });
}

function guidedRenderInterim(data){
  // Show current symptom tags (removable)
  const details=data.symptom_details||[];
  if(details.length>0){
    let tagsHtml='<div class="chat-symptoms-tags guided-removable-tags"><span class="chat-symptoms-label">'+(currentLang==="ja"?"選択中の症状 (×で解除): ":"Selected (tap × to remove): ")+'</span>';
    details.forEach(s=>{
      tagsHtml+=`<span class="chat-symptom-tag removable" data-sid="${escapeHtml(s.id)}">${currentLang==="ja"?s.name_ja:s.name_en} <button class="guided-tag-remove" type="button" aria-label="${currentLang==="ja"?"解除":"Remove"}">&times;</button></span>`;
    });
    tagsHtml+='</div>';
    guidedAddMsg(tagsHtml,"bot chat-result");
    // Wire up removal handlers
    document.querySelectorAll(".guided-removable-tags .guided-tag-remove").forEach(btn=>{
      btn.addEventListener("click",function(){
        const tag=this.closest(".chat-symptom-tag");
        if(!tag)return;
        const sid=tag.dataset.sid;
        guidedState.selectedSymptoms=guidedState.selectedSymptoms.filter(s=>s!==sid);
        tag.remove();
        if(guidedState.selectedSymptoms.length>0){
          // Re-run interim diagnosis with updated symptoms
          guidedSetActions("");
          guidedFetch("next_category");
        } else {
          // No symptoms left — go back to category selection
          guidedSetActions("");
          guidedFetch("start");
        }
      });
    });
  }

  // Show disease candidates
  const candidates=data.disease_candidates||[];
  if(candidates.length>0){
    let html=`<div class="guided-interim-label">${t("guidedInterimTitle")}</div>`;
    html+='<div class="chat-disease-list">';
    candidates.slice(0,3).forEach((c,i)=>{
      const pct=Math.round((c.similarity_score||0)*100);
      const sevClass=pct>=70?"sev-high":pct>=45?"sev-med":"sev-low";
      html+=`<div class="chat-disease-card">
        <div class="chat-disease-head">
          <span class="chat-disease-rank">${i+1}</span>
          <span class="chat-disease-name">${escapeHtml(currentLang==="ja"?(c.name_ja||c.name_en):(c.name_en||c.name_ja))}</span>
          <span class="chat-disease-pct ${sevClass}">${pct}%</span>
        </div>
        <div class="chat-disease-bar-bg"><div class="chat-disease-bar ${sevClass}" style="width:${pct}%"></div></div>
      </div>`;
    });
    html+='</div>';
    guidedAddMsg(html,"bot chat-result");
  }

  // Action buttons
  const nextCats=data.next_categories||[];
  let actHtml='<div class="guided-next-actions">';
  if(nextCats.length>0){
    actHtml+=`<div class="guided-next-label">${currentLang==="ja"?"さらに確認したいカテゴリ:":"Check more categories:"}</div>`;
    actHtml+='<div class="guided-category-grid compact">';
    nextCats.forEach(c=>{
      const label=currentLang==="ja"?c.name_ja:c.name_en;
      actHtml+=`<button class="guided-cat-btn suggested" data-cat="${c.id}"><span class="guided-cat-name">${label}</span></button>`;
    });
    actHtml+='</div>';
  }
  actHtml+=`<div class="guided-bottom-actions">`;
  actHtml+=`<button class="guided-action-btn secondary" id="guidedAskContext">${t("guidedFinish")}</button>`;
  actHtml+=`<button class="guided-action-btn text" id="guidedRestartBtn">${t("guidedRestart")}</button>`;
  actHtml+=`</div></div>`;
  guidedSetActions(actHtml);

  // Category buttons
  document.querySelectorAll(".guided-cat-btn.suggested").forEach(btn=>{
    btn.addEventListener("click",()=>{
      const cat=btn.dataset.cat;
      const label=btn.querySelector(".guided-cat-name").textContent;
      guidedAddMsg(label,"user");
      guidedSetActions("");
      guidedFetch("select_symptoms",{selected_category:cat});
    });
  });

  // Finish button -> ask context
  const finishBtn=document.getElementById("guidedAskContext");
  if(finishBtn)finishBtn.addEventListener("click",()=>{
    guidedSetActions("");
    guidedFetch("ask_context");
  });

  // Restart
  const restartBtn=document.getElementById("guidedRestartBtn");
  if(restartBtn)restartBtn.addEventListener("click",()=>{
    guidedSetActions("");
    startGuidedConsultation();
  });
}

function guidedRenderContextQuestions(questions){
  if(questions.length===0){
    // No context needed, go straight to finalize
    guidedFetch("finalize");
    return;
  }
  let html='<div class="guided-context-questions">';
  questions.forEach(q=>{
    const label=currentLang==="ja"?q.question_ja:q.question_en;
    html+=`<div class="guided-context-q"><div class="guided-context-label">${label}</div><div class="guided-context-options">`;
    (q.options||[]).forEach(o=>{
      const olabel=currentLang==="ja"?o.label_ja:o.label_en;
      html+=`<button class="guided-context-opt" data-type="${q.type}" data-value="${o.value}">${olabel}</button>`;
    });
    html+=`<button class="guided-context-opt skip" data-type="${q.type}" data-value="">${currentLang==="ja"?"スキップ":"Skip"}</button>`;
    html+='</div></div>';
  });
  html+=`<div class="guided-bottom-actions"><button class="guided-action-btn primary" id="guidedFinalizeBtn">${t("guidedFinish")}</button></div>`;
  html+='</div>';
  guidedSetActions(html);

  // Context option selection
  document.querySelectorAll(".guided-context-opt").forEach(btn=>{
    btn.addEventListener("click",()=>{
      const type=btn.dataset.type;
      const val=btn.dataset.value;
      // Deselect siblings
      btn.parentElement.querySelectorAll(".guided-context-opt").forEach(b=>b.classList.remove("selected"));
      if(val)btn.classList.add("selected");
      if(type==="onset"&&val)guidedState.onset=val;
      if(type==="age"&&val)guidedState.ageYears=parseFloat(val);
      if(type==="pain_score"&&val!=="")guidedState.painScore=parseInt(val,10);
    });
  });

  // Finalize
  const finalBtn=document.getElementById("guidedFinalizeBtn");
  if(finalBtn)finalBtn.addEventListener("click",()=>{
    guidedSetActions("");
    guidedFetch("finalize");
  });
}

function guidedRenderFinalResults(data){
  const result=data.result||{};
  const diseases=result.suspected_diseases||[];
  const details=data.symptom_details||[];

  // Symptom summary (removable — re-runs finalize on removal)
  if(details.length>0){
    let tagsHtml='<div class="chat-symptoms-tags guided-removable-tags guided-final-tags"><span class="chat-symptoms-label">'+(currentLang==="ja"?"検出症状 (×で解除して再診断): ":"Symptoms (tap × to remove & re-diagnose): ")+'</span>';
    details.forEach(s=>{
      tagsHtml+=`<span class="chat-symptom-tag removable" data-sid="${escapeHtml(s.id)}">${escapeHtml(currentLang==="ja"?s.name_ja:s.name_en)} <button class="guided-tag-remove" type="button" aria-label="${currentLang==="ja"?"解除":"Remove"}">&times;</button></span>`;
    });
    tagsHtml+='</div>';
    guidedAddMsg(tagsHtml,"bot chat-result");
    // Wire up removal handlers
    document.querySelectorAll(".guided-final-tags .guided-tag-remove").forEach(btn=>{
      btn.addEventListener("click",function(){
        const tag=this.closest(".chat-symptom-tag");
        if(!tag)return;
        const sid=tag.dataset.sid;
        guidedState.selectedSymptoms=guidedState.selectedSymptoms.filter(s=>s!==sid);
        tag.remove();
        if(guidedState.selectedSymptoms.length>0){
          // Re-run finalize with updated symptoms
          guidedSetActions("");
          guidedFetch("finalize");
        } else {
          guidedSetActions("");
          guidedFetch("start");
        }
      });
    });
  }

  // Context info
  let ctxParts=[];
  if(data.onset)ctxParts.push((currentLang==="ja"?"発症: ":"Onset: ")+data.onset);
  if(data.age_years)ctxParts.push((currentLang==="ja"?"年齢: ":"Age: ")+data.age_years+(currentLang==="ja"?"歳":"y"));
  if(data.pain_score!=null)ctxParts.push((currentLang==="ja"?"疼痛: ":"Pain: ")+data.pain_score+"/4");
  if(ctxParts.length>0)guidedAddMsg(ctxParts.join(" / "),"bot");

  // Low-confidence warning
  const topPct=diseases.length>0?(diseases[0].match_percent||0):0;
  const symCount=details.length;
  if(symCount<=2||topPct<50){
    const warnMsg=currentLang==="ja"
      ?`症状${symCount}個での診断です（最高信頼度 ${topPct}%）。症状を追加すると精度が大幅に向上します。`
      :`Diagnosis based on ${symCount} symptom(s) (top confidence ${topPct}%). Adding more symptoms will significantly improve accuracy.`;
    guidedAddMsg(`<div class="guided-low-confidence-warn">${escapeHtml(warnMsg)}</div>`,"bot chat-result");
  }

  // Disease results
  if(diseases.length>0){
    let html=`<div class="guided-final-label">${t("guidedFinalTitle")}</div>`;
    html+='<div class="chat-disease-list">';
    diseases.slice(0,5).forEach((d,i)=>{
      const pct=d.match_percent||0;
      const sevClass=pct>=70?"sev-high":pct>=45?"sev-med":"sev-low";
      const name=escapeHtml(currentLang==="ja"?(d.name_ja||d.name||""):(d.name||d.name_ja||""));
      const nameSecondary=escapeHtml(currentLang==="ja"?(d.name||""):(d.name_ja||""));
      const desc=escapeHtml(currentLang==="ja"?(d.description_ja||d.description||""):(d.description||d.description_ja||""));
      const matched=escapeHtml((d.matching_symptoms||[]).map(sid=>{
        const found=details.find(s=>s.id===sid);
        return found?(currentLang==="ja"?(found.name_ja||found.name_en):(found.name_en||found.name_ja)):sid;
      }).join(", "));
      html+=`<div class="chat-disease-card">
        <div class="chat-disease-head">
          <span class="chat-disease-rank">${i+1}</span>
          <span class="chat-disease-name">${name}</span>
          <span class="chat-disease-name-en">${nameSecondary}</span>
          <span class="chat-disease-pct ${sevClass}">${pct}%</span>
        </div>
        <div class="chat-disease-bar-bg"><div class="chat-disease-bar ${sevClass}" style="width:${pct}%"></div></div>
        ${desc?`<div class="chat-disease-desc">${desc}</div>`:""}
        ${matched?`<div class="chat-disease-matched">${currentLang==="ja"?"一致: ":"Matched: "}${matched}</div>`:""}
      </div>`;
    });
    html+='</div>';
    guidedAddMsg(html,"bot chat-result");
  } else {
    guidedAddMsg(currentLang==="ja"?"該当する疾患が見つかりませんでした。":"No matching diseases found.","bot");
  }

  // Disclaimer + recommendations
  const rec=data.recommendations||{};
  const disclaimer=currentLang==="ja"?rec.next_step_ja:rec.next_step_en;
  if(disclaimer)guidedAddMsg(`<div class="chat-disclaimer">${escapeHtml(disclaimer)}</div>`,"bot chat-result");

  // Action buttons: add more symptoms + restart
  const addMoreLabel=currentLang==="ja"?"+ 症状を追加して再診断":"+ Add symptoms & re-diagnose";
  guidedSetActions(`<div class="guided-bottom-actions"><button class="guided-action-btn primary" id="guidedAddMore">${addMoreLabel}</button><button class="guided-action-btn text" id="guidedRestartFinal">${t("guidedRestart")}</button></div>`);
  const addBtn=document.getElementById("guidedAddMore");
  if(addBtn)addBtn.addEventListener("click",()=>{guidedSetActions("");guidedFetch("next_category");});
  const rb=document.getElementById("guidedRestartFinal");
  if(rb)rb.addEventListener("click",()=>{guidedSetActions("");startGuidedConsultation();});
}

let drugsLoaded=false,allDrugs=[],drugCategories={};

function loadDrugDictionary(){
  const list=document.getElementById("drugList");
  list.innerHTML='<div style="padding:12px"><div class="skeleton skeleton-card"></div><div class="skeleton skeleton-card" style="height:70px"></div><div class="skeleton skeleton-card" style="height:90px"></div><div class="skeleton skeleton-card" style="height:60px"></div></div>';
  Promise.all([fetchWithTimeout("/api/drugs").then(r=>r.json()),fetchWithTimeout("/api/drug-categories").then(r=>r.json())])
  .then(([drugsData,catData])=>{
    allDrugs=drugsData.drugs||[];drugCategories=drugsData.categories||{};
    pendingStats.drugs=allDrugs.length;animateCount(document.getElementById("statDrugs"),allDrugs.length,800);
    const catSelect=document.getElementById("drugCategoryFilter");
    catSelect.innerHTML=`<option value="">${t("allCategories")}</option>`;
    (catData.categories||[]).forEach(c=>{if(c.count>0){const cName=currentLang==="ja"?(c.name_ja||c.name_en):(c.name_en||c.name_ja);catSelect.insertAdjacentHTML("beforeend",`<option value="${escapeHtml(c.id)}">${escapeHtml(cName)} (${c.count})</option>`);}});
    const spSelect=document.getElementById("drugSpeciesFilter");
    spSelect.innerHTML=`<option value="">${t("allSpecies")}</option>`;
    SPECIES.forEach(sp=>{const primary=currentLang==="ja"?sp.name:sp.nameEn;const secondary=currentLang==="ja"?sp.nameEn:sp.name;spSelect.insertAdjacentHTML("beforeend",`<option value="${escapeHtml(sp.id)}">${escapeHtml(primary)} ${escapeHtml(secondary)}</option>`);});
    drugsLoaded=true;
    /* Auto-select current species in drug filter */
    if(currentSpecies){spSelect.value=currentSpecies;}
    renderDrugList();
  }).catch(()=>{list.innerHTML=`<div style="padding:20px;text-align:center;color:var(--gray-500)">${t("loadFailed")}</div>`;});
  document.getElementById("drugSearch").addEventListener("input",debounce(renderDrugList,200));
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
      const safeLabel=si.safe?`<span class="drug-safe-label">\u2713 ${t("safe")}</span>`:`<span class="drug-unsafe-label">\u2717 ${t("contraindicated")}</span>`;
      const doseText=currentLang==="ja"?(si.dosage_ja||si.dosage||"N/A"):(si.dosage||si.dosage_ja||"N/A");
      const noteText=currentLang==="ja"?(si.notes_ja||si.notes||""):(si.notes||si.notes_ja||"");
      dosageHtml=`<div class="drug-dosage-box ${si.safe?"drug-safe":"drug-unsafe"}">${safeLabel} | ${t("dosageLabel")}${escapeHtml(doseText)}<br/><span class="drug-dosage-note">${escapeHtml(noteText)}</span></div>`;
    }
    const catLabel=drugCategories[d.category]?(currentLang==="ja"?(drugCategories[d.category].ja||drugCategories[d.category].en):(drugCategories[d.category].en||drugCategories[d.category].ja)):(currentLang==="ja"?(d.category_ja||d.category):(d.category||d.category_ja));
    const sponsorBadge=d.sponsor?'<span class="sponsor-badge-tag">Sponsor</span>':"";
    const sponsorLink=d.sponsor?`<div class="drug-sponsor-link"><strong class="drug-sponsor-name">${escapeHtml(d.sponsor_name||"Equine & Canine Vet Nutrition")}</strong><br/><span class="drug-sponsor-vet">${t("sponsorVetLabel")}</span><br/><a href="${sanitizeUrl(d.sponsor_url||d.sponsor_url_dog||'https://www.caninevet.jp/')}" target="_blank" class="drug-sponsor-url">${t("productDetails")}</a></div>`:"";
    const dName=highlightMatch(d.name||"",search);
    const dNameJa=highlightMatch(d.name_ja||"",search);
    return`<div class="disease-db-item drug-item${d.sponsor?" drug-sponsored":""}" role="button" tabindex="0" aria-expanded="false">
      <div class="drug-head-row">
        <div class="d-name">${dName} <span class="d-name-ja">${dNameJa}</span>${sponsorBadge}</div>
        <span class="drug-category-tag">${escapeHtml(catLabel)}</span>
      </div>${dosageHtml}
      <div class="disease-detail">${sponsorLink}
        <dl><dt>${t("dtContraindications")}</dt><dd>${escapeHtml(currentLang==="ja"?(d.contraindications_ja||d.contraindications||""):(d.contraindications||d.contraindications_ja||""))}</dd></dl>
        ${d.routes_ja||d.routes?`<dl><dt>${t("dtRoutes")}</dt><dd>${escapeHtml(currentLang==="ja"?(d.routes_ja||[]).join(", "):(d.routes||[]).join(", "))}</dd></dl>`:""}
        ${d.formulations_ja||d.formulations?`<dl><dt>${t("dtFormulations")}</dt><dd>${escapeHtml(currentLang==="ja"?(d.formulations_ja||d.formulations||[]).join(", "):(d.formulations||d.formulations_ja||[]).join(", "))}</dd></dl>`:""}
        ${d.drug_interactions&&d.drug_interactions.length?`<dl><dt>${t("dtInteractions")}</dt><dd>${d.drug_interactions.map(di=>`<span class="drug-interaction-tag">${escapeHtml(di.drug)}: ${escapeHtml(currentLang==="ja"?(di.effect_ja||di.effect):(di.effect||di.effect_ja))}</span>`).join("")}</dd></dl>`:""}
        <div class="drug-species-section"><strong class="drug-species-title">${t("dtSpeciesInfo")}</strong>
          <div class="drug-species-grid">
            ${Object.entries(d.species_info||{}).map(([sp,info])=>{const spName=SPECIES.find(s=>s.id===sp);const label=spName?(currentLang==="ja"?spName.name:spName.nameEn):sp;const dose=currentLang==="ja"?(info.dosage_ja||info.dosage||""):(info.dosage||info.dosage_ja||"");const note=currentLang==="ja"?(info.notes_ja||info.notes||""):(info.notes||info.notes_ja||"");return`<div class="drug-species-card ${info.safe?"drug-safe":"drug-unsafe"}"><strong>${escapeHtml(label)}</strong>: ${info.safe?'\u2713':'\u2717'} ${escapeHtml(dose)}${note?'<br/><span class="drug-dosage-note">'+escapeHtml(note)+'</span>':''}</div>`;}).join("")}
          </div>
        </div>
      </div>
    </div>`;
  }).join("");
}

/* ===== Anesthesia Protocols ===== */
let anesthesiaLoaded=false,anesthesiaData=null,anesthesiaCategories={},anesthesiaAsaData=null,anesthesiaContraRules=null;

function loadAnesthesiaProtocols(){
  const list=document.getElementById("anesthesiaList");
  list.innerHTML='<div style="padding:12px"><div class="skeleton skeleton-card"></div><div class="skeleton skeleton-card" style="height:70px"></div></div>';
  const sp=currentSpecies||"";
  const url=sp?"/api/anesthesia/protocols?species="+encodeURIComponent(sp):"/api/anesthesia/protocols";
  fetchWithTimeout(url).then(r=>r.json()).then(data=>{
    anesthesiaData=data;
    anesthesiaCategories=data.categories||{};
    anesthesiaLoaded=true;
    const catSel=document.getElementById("anesthesiaCategoryFilter");
    catSel.innerHTML=`<option value="">${t("allCategories")}</option>`;
    Object.entries(anesthesiaCategories).forEach(([k,v])=>{const name=currentLang==="ja"?(v.ja||v.en):(v.en||v.ja);catSel.insertAdjacentHTML("beforeend",`<option value="${escapeHtml(k)}">${escapeHtml(name)}</option>`);});
    renderAnesthesiaOverview(data);
    renderAnesthesiaList();
  }).catch(()=>{list.innerHTML=`<div style="padding:20px;text-align:center;color:var(--gray-500)">${t("loadFailed")}</div>`;});
  /* Fetch ASA classification */
  fetchWithTimeout("/api/anesthesia/categories").then(r=>r.json()).then(d=>{anesthesiaAsaData=d.asa_classification||null;}).catch(()=>{});
  /* Fetch contraindication rules */
  fetchWithTimeout("/api/anesthesia/contraindications?all=true").then(r=>r.json()).then(d=>{anesthesiaContraRules=d.rules||[];}).catch(()=>{});
  document.getElementById("anesthesiaSearch").addEventListener("input",debounce(renderAnesthesiaList,200));
  document.getElementById("anesthesiaCategoryFilter").addEventListener("change",renderAnesthesiaList);
  /* Weight-based dose calculator */
  const weightInput=document.getElementById("anesthesiaWeight");
  if(weightInput){
    weightInput.addEventListener("input",debounce(renderAnesthesiaList,300));
    document.getElementById("anesthesiaWeightClear").addEventListener("click",()=>{weightInput.value="";renderAnesthesiaList();});
  }
  /* Emergency protocol quick-access */
  const emergBtn=document.getElementById("anesthesiaEmergencyBtn");
  if(emergBtn){
    emergBtn.addEventListener("click",()=>{
      const catSel=document.getElementById("anesthesiaCategoryFilter");
      const isActive=emergBtn.classList.toggle("active");
      if(isActive){catSel.value="emergency";} else {catSel.value="";}
      renderAnesthesiaList();
    });
  }
  /* ASA filter */
  const asaFilter=document.getElementById("anesthesiaAsaFilter");
  if(asaFilter)asaFilter.addEventListener("change",renderAnesthesiaList);
  /* Print checklist */
  const printBtn=document.getElementById("anesthesiaPrintBtn");
  if(printBtn)printBtn.addEventListener("click",printAnesthesiaChecklist);
}

function reloadAnesthesiaForSpecies(){
  if(!anesthesiaLoaded)return;
  const sp=currentSpecies||"";
  const url=sp?"/api/anesthesia/protocols?species="+encodeURIComponent(sp):"/api/anesthesia/protocols";
  fetchWithTimeout(url).then(r=>r.json()).then(data=>{
    anesthesiaData=data;
    renderAnesthesiaOverview(data);
    renderAnesthesiaList();
  }).catch(()=>{});
}

function renderAnesthesiaOverview(data){
  const ov=document.getElementById("anesthesiaOverview");
  const lb=document.getElementById("anesthesiaSpeciesLabel");
  if(!data||(!data.overview&&!data.species_name)){
    ov.style.display="block";
    ov.innerHTML=`<div style="text-align:center;padding:16px"><span style="font-size:2rem" aria-hidden="true">&#128137;</span><p style="margin-top:8px;font-size:.88rem;color:var(--navy)">${t("anesthesiaSelectSpecies")}</p></div>`;
    lb.textContent="";
    return;
  }
  if(data.species_name){
    const spName=currentLang==="ja"?(data.species_name.ja||data.species_name.en):(data.species_name.en||data.species_name.ja);
    lb.innerHTML=`<strong>${escapeHtml(spName)}</strong>`;
  }
  if(data.overview||data.fasting){
    const ovText=currentLang==="ja"?(data.overview?.ja||data.overview?.en||""):(data.overview?.en||data.overview?.ja||"");
    const fastText=currentLang==="ja"?(data.fasting?.ja||data.fasting?.en||""):(data.fasting?.en||data.fasting?.ja||"");
    ov.style.display="block";
    ov.innerHTML=`<div class="anesthesia-overview-text"><strong>${t("anesthesiaOverviewLabel")}:</strong> ${escapeHtml(ovText)}</div>`
      +(fastText?`<div class="anesthesia-fasting-text"><strong>${t("anesthesiaFastingLabel")}:</strong> ${escapeHtml(fastText)}</div>`:"");
  } else { ov.style.display="none"; }
}

/* Parse dose string like "0.2-0.4 mg/kg" and calculate for given weight */
function calcDoseForWeight(doseStr,weightKg){
  if(!doseStr||!weightKg||weightKg<=0)return null;
  /* Match patterns: "0.2 mg/kg", "0.2-0.4 mg/kg", "2-4 μg/kg", "0.5 mL/kg", "5-10 mg/kg IV" */
  const m=doseStr.match(/(\d+(?:\.\d+)?)\s*[-–~～]\s*(\d+(?:\.\d+)?)\s*(mg|μg|µg|mcg|mL|ml|IU|U)\s*\/\s*kg/i);
  const s=doseStr.match(/(\d+(?:\.\d+)?)\s*(mg|μg|µg|mcg|mL|ml|IU|U)\s*\/\s*kg/i);
  if(m){
    const lo=parseFloat(m[1])*weightKg;
    const hi=parseFloat(m[2])*weightKg;
    const unit=m[3].replace(/µg|mcg/i,"μg");
    return{lo:roundDose(lo),hi:roundDose(hi),unit:unit,isRange:true};
  }
  if(s){
    const val=parseFloat(s[1])*weightKg;
    const unit=s[2].replace(/µg|mcg/i,"μg");
    return{lo:roundDose(val),hi:null,unit:unit,isRange:false};
  }
  return null;
}
function roundDose(v){return v>=10?Math.round(v*10)/10:v>=1?Math.round(v*100)/100:Math.round(v*1000)/1000;}

/* Check contraindications for a drug against current species/breed */
function checkDrugContra(drugName){
  if(!anesthesiaContraRules||!drugName)return[];
  const dn=drugName.toLowerCase();
  const sp=(currentSpecies||"").toLowerCase();
  const breed=(document.getElementById("breedSelect")||{}).value||"";
  const tags=new Set();
  if(sp)tags.add(sp);
  if(breed)tags.add(breed.toLowerCase());
  /* Add common species aliases */
  const spMap={dog:"canine",cat:"feline",horse:"equine",rabbit:"rabbit",hamster:"hamster",ferret:"ferret"};
  if(spMap[sp])tags.add(spMap[sp]);
  return anesthesiaContraRules.filter(r=>{
    const drugMatch=r.drug_patterns.some(p=>dn.includes(p.toLowerCase()));
    if(!drugMatch)return false;
    return r.conditions.some(c=>tags.has(c.toLowerCase()));
  });
}
function renderAnesthesiaList(){
  const list=document.getElementById("anesthesiaList");
  const search=(document.getElementById("anesthesiaSearch").value||"").toLowerCase();
  const cat=document.getElementById("anesthesiaCategoryFilter").value;
  if(!anesthesiaData){list.innerHTML="";return;}

  let protocols=anesthesiaData.protocols||[];
  /* If no species selected, use results array */
  if(!protocols.length&&anesthesiaData.results){
    protocols=anesthesiaData.results.map(r=>({...r.protocol,_species:r.species,_species_name:r.species_name}));
  }
  if(cat)protocols=protocols.filter(p=>p.category===cat);
  const asaVal=(document.getElementById("anesthesiaAsaFilter")||{}).value||"";
  if(asaVal){
    const asaRisk={"I":"low","II":"low","III":"moderate","IV":"high","V":"high","E":"high"};
    const targetRisk=asaRisk[asaVal]||"";
    if(targetRisk)protocols=protocols.filter(p=>p.risk_level===targetRisk);
  }
  if(search){
    protocols=protocols.filter(p=>{
      const s=[p.name?.ja||"",p.name?.en||"",p.notes_ja||"",p.notes||""].concat((p.drugs||[]).map(d=>(d.name||"")+" "+(d.name_ja||""))).join(" ").toLowerCase();
      return s.includes(search);
    });
  }
  const countEl=document.getElementById("anesthesiaCount");
  countEl.textContent=t("diseaseCount").replace("%filtered%",protocols.length).replace("%total%",anesthesiaData.protocols?.length||anesthesiaData.total||protocols.length);

  if(!protocols.length){list.innerHTML=`<div style="padding:20px;text-align:center;color:var(--gray-500)">${t("noAnesthesiaMatch")}</div>`;return;}

  const riskLabels={low:t("anesthesiaRiskLow"),moderate:t("anesthesiaRiskModerate"),high:t("anesthesiaRiskHigh")};
  const riskColors={low:"#16a34a",moderate:"#ea580c",high:"#dc2626"};
  const weightEl=document.getElementById("anesthesiaWeight");
  const patientWeight=weightEl?parseFloat(weightEl.value):0;

  list.innerHTML=protocols.map(p=>{
    const pName=currentLang==="ja"?(p.name?.ja||p.name?.en||""):(p.name?.en||p.name?.ja||"");
    const catKey=p.category||"";
    const catInfo=anesthesiaCategories[catKey]||{};
    const catLabel=currentLang==="ja"?(catInfo.ja||catInfo.en||catKey):(catInfo.en||catInfo.ja||catKey);
    const risk=p.risk_level||"";
    const riskLabel=riskLabels[risk]||"";
    const riskColor=riskColors[risk]||"#6b7280";
    const notes=currentLang==="ja"?(p.notes_ja||p.notes||""):(p.notes||p.notes_ja||"");
    const spLabel=p._species_name?(currentLang==="ja"?(p._species_name.ja||""):(p._species_name.en||"")):"";

    let drugsHtml="";
    if(p.drugs&&p.drugs.length){
      const hasCalc=patientWeight>0;
      const calcHeader=hasCalc?`<th>${t("anesthesiaCalcDose")} (${patientWeight}kg)</th>`:"";
      drugsHtml=`<div class="anesthesia-drugs-table"><table><thead><tr><th>${currentLang==="ja"?"薬品":"Drug"}</th><th>${t("anesthesiaDose")}</th>${calcHeader}<th>${t("anesthesiaRoute")}</th><th>${t("anesthesiaOnset")}</th><th>${t("anesthesiaDuration")}</th></tr></thead><tbody>`
        +p.drugs.map(d=>{
          const dNotes=currentLang==="ja"?(d.notes_ja||d.notes||""):(d.notes||d.notes_ja||"");
          let calcCell="";
          if(hasCalc){
            const calc=calcDoseForWeight(d.dose,patientWeight);
            if(calc){
              calcCell=calc.isRange
                ?`<td><span class="anesthesia-calc-dose">${calc.lo}–${calc.hi} ${escapeHtml(calc.unit)}</span></td>`
                :`<td><span class="anesthesia-calc-dose">${calc.lo} ${escapeHtml(calc.unit)}</span></td>`;
            } else { calcCell=`<td><span style="color:var(--gray-400);font-size:.76rem">—</span></td>`; }
          }
          const cols=hasCalc?6:5;
          /* Check contraindications */
          const contras=checkDrugContra(d.name||"");
          let contraHtml="";
          if(contras.length){
            const sevLabels={contraindicated:t("anesthesiaContraindicated"),caution:t("anesthesiaCaution"),monitor:t("anesthesiaMonitorExtra")};
            const sevColors={contraindicated:"#dc2626",caution:"#ea580c",monitor:"#ca8a04"};
            const sevIcons={contraindicated:"⛔",caution:"⚠️",monitor:"🔍"};
            contraHtml=contras.map(c=>{
              const msg=currentLang==="ja"?(c.message_ja||c.message_en):(c.message_en||c.message_ja);
              const sev=c.severity||"caution";
              return`<tr class="anesthesia-contra-row"><td colspan="${cols}"><span class="anesthesia-contra-badge" style="background:${sevColors[sev]||"#ea580c"}">${sevIcons[sev]||"⚠️"} ${escapeHtml(sevLabels[sev]||sev)}</span> ${escapeHtml(msg)}</td></tr>`;
            }).join("");
          }
          return`<tr><td><strong>${escapeHtml(d.name||"")}</strong><br/><span class="d-name-ja">${escapeHtml(d.name_ja||"")}</span></td><td>${escapeHtml(d.dose||"")}</td>${calcCell}<td>${escapeHtml(d.route||"")}</td><td>${escapeHtml(d.onset||"")}</td><td>${escapeHtml(d.duration||"")}</td></tr>`
          +contraHtml
          +(dNotes?`<tr class="anesthesia-drug-note"><td colspan="${cols}">${escapeHtml(dNotes)}</td></tr>`:"");
        }).join("")
        +`</tbody></table></div>`;
    }

    let monitorHtml="";
    if(p.monitoring_params&&p.monitoring_params.length){
      monitorHtml=`<div class="anesthesia-monitor-section"><strong>${t("anesthesiaMonitoring")}</strong><table><thead><tr><th>Parameter</th><th>${t("anesthesiaTarget")}</th><th>Notes</th></tr></thead><tbody>`
        +p.monitoring_params.map(m=>{
          const mNotes=currentLang==="ja"?(m.notes_ja||m.notes||""):(m.notes||m.notes_ja||"");
          return`<tr><td><strong>${escapeHtml(m.param||"")}</strong></td><td>${escapeHtml(m.target||"")}</td><td>${escapeHtml(mNotes)}</td></tr>`;
        }).join("")
        +`</tbody></table></div>`;
    }

    return`<div class="disease-db-item anesthesia-item" role="button" tabindex="0" aria-expanded="false">
      <div class="drug-head-row">
        <div class="d-name">${escapeHtml(pName)}${spLabel?` <span class="d-name-ja">(${escapeHtml(spLabel)})</span>`:""}</div>
        <span class="drug-category-tag">${escapeHtml(catLabel)}</span>
        ${riskLabel?`<span class="anesthesia-risk-tag" style="background:${riskColor}">${escapeHtml(riskLabel)}</span>`:""}
      </div>
      <div class="disease-detail">
        ${notes?`<div class="anesthesia-notes">${escapeHtml(notes)}</div>`:""}
        ${drugsHtml}${monitorHtml}${p.references&&p.references.length?`<div class="anesthesia-references"><strong>${currentLang==="ja"?"参考文献":"References"}</strong><ul>${p.references.map(r=>`<li>${escapeHtml(r)}</li>`).join("")}</ul></div>`:""}
      </div>
    </div>`;
  }).join("");

  /* Breed considerations */
  if(anesthesiaData.breed_considerations&&anesthesiaData.breed_considerations.length&&!cat&&!search){
    const breedHtml=`<div class="anesthesia-breed-section"><h4>${t("anesthesiaBreedConsider")}</h4>`
      +anesthesiaData.breed_considerations.map(b=>{
        const breed=currentLang==="ja"?(b.breed_ja||b.breed):(b.breed||b.breed_ja);
        const notes=currentLang==="ja"?(b.notes_ja||b.notes):(b.notes||b.notes_ja);
        return`<div class="anesthesia-breed-item"><strong>${escapeHtml(breed)}</strong><p>${escapeHtml(notes)}</p></div>`;
      }).join("")
      +`</div>`;
    list.insertAdjacentHTML("beforeend",breedHtml);
  }

  /* ASA Classification reference */
  if(anesthesiaAsaData&&!cat&&!search){
    const riskColors={low:"#16a34a",moderate:"#ea580c",high:"#dc2626"};
    const riskLabels={low:t("anesthesiaRiskLow"),moderate:t("anesthesiaRiskModerate"),high:t("anesthesiaRiskHigh")};
    const asaHtml=`<div class="anesthesia-breed-section"><h4>${t("anesthesiaAsaTitle")}</h4>`
      +["I","II","III","IV","V","E"].map(cls=>{
        const a=anesthesiaAsaData[cls];if(!a)return"";
        const desc=currentLang==="ja"?(a.ja||a.en):(a.en||a.ja);
        const guidance=currentLang==="ja"?(a.guidance_ja||a.guidance_en):(a.guidance_en||a.guidance_ja);
        const rc=riskColors[a.risk]||"#6b7280";
        const rl=riskLabels[a.risk]||"";
        return`<div class="anesthesia-breed-item"><strong>ASA ${cls}</strong> <span class="anesthesia-risk-tag" style="background:${rc};font-size:.72rem">${escapeHtml(rl)}</span><p>${escapeHtml(desc)}</p><p style="font-size:.8rem;color:var(--gray-600)"><strong>${t("anesthesiaAsaGuidance")}:</strong> ${escapeHtml(guidance)}</p></div>`;
      }).join("")
      +`</div>`;
    list.insertAdjacentHTML("beforeend",asaHtml);
  }

  /* Species-level references */
  if(anesthesiaData.references&&anesthesiaData.references.length&&!cat&&!search){
    const refsHtml=`<div class="anesthesia-breed-section"><h4>${currentLang==="ja"?"参考文献":"References"}</h4><ul class="anesthesia-ref-list">${anesthesiaData.references.map(r=>`<li>${escapeHtml(r)}</li>`).join("")}</ul></div>`;
    list.insertAdjacentHTML("beforeend",refsHtml);
  }
}

/* Print anesthesia checklist */
function printAnesthesiaChecklist(){
  const sp=currentSpecies||"";
  const weightEl=document.getElementById("anesthesiaWeight");
  const weight=weightEl?weightEl.value:"";
  const spLabel=document.getElementById("anesthesiaSpeciesLabel");
  const spName=spLabel?spLabel.textContent:"";
  const now=new Date().toLocaleDateString();
  const preopItems=t("anesthesiaPrintPreopItems").split(",");
  const intraopItems=t("anesthesiaPrintIntraopItems").split(",");
  const postopItems=t("anesthesiaPrintPostopItems").split(",");
  const makeChecklist=(items)=>items.map(i=>`<div class="ck-item"><span class="ck-box">☐</span> ${escapeHtml(i.trim())}</div>`).join("");

  /* Collect currently visible protocols with drugs */
  const cat=document.getElementById("anesthesiaCategoryFilter").value;
  let visibleProtocols=[];
  if(anesthesiaData){
    let prots=anesthesiaData.protocols||[];
    if(cat)prots=prots.filter(p=>p.category===cat);
    visibleProtocols=prots.slice(0,10);
  }
  let drugSummary="";
  if(visibleProtocols.length&&weight){
    const wKg=parseFloat(weight);
    drugSummary=visibleProtocols.filter(p=>p.drugs&&p.drugs.length).map(p=>{
      const pN=currentLang==="ja"?(p.name?.ja||p.name?.en||""):(p.name?.en||p.name?.ja||"");
      const rows=p.drugs.map(d=>{
        const calc=calcDoseForWeight(d.dose,wKg);
        const calcStr=calc?(calc.isRange?`${calc.lo}–${calc.hi} ${calc.unit}`:`${calc.lo} ${calc.unit}`):"—";
        return`<tr><td>${escapeHtml(d.name||"")}</td><td>${escapeHtml(d.dose||"")}</td><td><strong>${calcStr}</strong></td><td>${escapeHtml(d.route||"")}</td></tr>`;
      }).join("");
      return`<h4 style="margin:12px 0 4px">${escapeHtml(pN)}</h4><table><thead><tr><th>Drug</th><th>Dose/kg</th><th>Calculated</th><th>Route</th></tr></thead><tbody>${rows}</tbody></table>`;
    }).join("");
  }

  const html=`<!DOCTYPE html><html><head><meta charset="utf-8"><title>${t("anesthesiaPrintTitle")}</title>
<style>body{font-family:sans-serif;padding:20px;font-size:13px;color:#333}
h2{text-align:center;margin-bottom:4px}h3{margin:16px 0 6px;border-bottom:2px solid #333;padding-bottom:4px}h4{font-size:13px;color:#555}
.info-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:16px;border:1px solid #ccc;padding:12px;border-radius:4px}
.info-grid div{font-size:13px}.info-grid strong{display:inline-block;min-width:60px}
.ck-item{padding:4px 0;border-bottom:1px dotted #ddd;font-size:13px}.ck-box{font-size:16px;margin-right:6px}
table{width:100%;border-collapse:collapse;font-size:12px;margin-bottom:8px}th,td{border:1px solid #ccc;padding:4px 8px;text-align:left}
th{background:#f0f0f0;font-weight:600}.notes{margin-top:20px;border-top:2px solid #333;padding-top:8px}
.notes-area{width:100%;height:80px;border:1px solid #ccc;border-radius:4px;margin-top:4px}
@media print{body{padding:10px}}</style></head><body>
<h2>${t("anesthesiaPrintTitle")}</h2>
<div class="info-grid">
<div><strong>${t("anesthesiaPrintSpecies")}:</strong> ${escapeHtml(spName||sp)}</div>
<div><strong>${t("anesthesiaPrintWeight")}:</strong> ${escapeHtml(weight?weight+" kg":"_____ kg")}</div>
<div><strong>${t("anesthesiaPrintDate")}:</strong> ${escapeHtml(now)}</div>
<div><strong>ASA:</strong> ☐I ☐II ☐III ☐IV ☐V ☐E</div>
</div>
${drugSummary?`<h3>Drug Protocol</h3>${drugSummary}`:""}
<h3>${t("anesthesiaPrintPreop")}</h3>${makeChecklist(preopItems)}
<h3>${t("anesthesiaPrintIntraop")}</h3>${makeChecklist(intraopItems)}
<h3>${t("anesthesiaPrintPostop")}</h3>${makeChecklist(postopItems)}
<div class="notes"><h3>Notes</h3><div class="notes-area" contenteditable="true"></div></div>
</body></html>`;
  const win=window.open("","_blank");
  if(win){win.document.write(html);win.document.close();win.focus();setTimeout(()=>win.print(),300);}
}

/* Print anesthesia checklist */
function printAnesthesiaChecklist(){
  const sp=currentSpecies||"";
  const weightEl=document.getElementById("anesthesiaWeight");
  const weight=weightEl?weightEl.value:"";
  const spLabel=document.getElementById("anesthesiaSpeciesLabel");
  const spName=spLabel?spLabel.textContent:"";
  const now=new Date().toLocaleDateString();
  const preopItems=t("anesthesiaPrintPreopItems").split(",");
  const intraopItems=t("anesthesiaPrintIntraopItems").split(",");
  const postopItems=t("anesthesiaPrintPostopItems").split(",");
  const makeChecklist=(items)=>items.map(i=>`<div class="ck-item"><span class="ck-box">☐</span> ${escapeHtml(i.trim())}</div>`).join("");

  /* Collect currently visible protocols with drugs */
  const cat=document.getElementById("anesthesiaCategoryFilter").value;
  let visibleProtocols=[];
  if(anesthesiaData){
    let prots=anesthesiaData.protocols||[];
    if(cat)prots=prots.filter(p=>p.category===cat);
    visibleProtocols=prots.slice(0,10);
  }
  let drugSummary="";
  if(visibleProtocols.length&&weight){
    const wKg=parseFloat(weight);
    drugSummary=visibleProtocols.filter(p=>p.drugs&&p.drugs.length).map(p=>{
      const pN=currentLang==="ja"?(p.name?.ja||p.name?.en||""):(p.name?.en||p.name?.ja||"");
      const rows=p.drugs.map(d=>{
        const calc=calcDoseForWeight(d.dose,wKg);
        const calcStr=calc?(calc.isRange?`${calc.lo}–${calc.hi} ${calc.unit}`:`${calc.lo} ${calc.unit}`):"—";
        return`<tr><td>${escapeHtml(d.name||"")}</td><td>${escapeHtml(d.dose||"")}</td><td><strong>${calcStr}</strong></td><td>${escapeHtml(d.route||"")}</td></tr>`;
      }).join("");
      return`<h4 style="margin:12px 0 4px">${escapeHtml(pN)}</h4><table><thead><tr><th>Drug</th><th>Dose/kg</th><th>Calculated</th><th>Route</th></tr></thead><tbody>${rows}</tbody></table>`;
    }).join("");
  }

  const html=`<!DOCTYPE html><html><head><meta charset="utf-8"><title>${t("anesthesiaPrintTitle")}</title>
<style>body{font-family:sans-serif;padding:20px;font-size:13px;color:#333}
h2{text-align:center;margin-bottom:4px}h3{margin:16px 0 6px;border-bottom:2px solid #333;padding-bottom:4px}h4{font-size:13px;color:#555}
.info-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:16px;border:1px solid #ccc;padding:12px;border-radius:4px}
.info-grid div{font-size:13px}.info-grid strong{display:inline-block;min-width:60px}
.ck-item{padding:4px 0;border-bottom:1px dotted #ddd;font-size:13px}.ck-box{font-size:16px;margin-right:6px}
table{width:100%;border-collapse:collapse;font-size:12px;margin-bottom:8px}th,td{border:1px solid #ccc;padding:4px 8px;text-align:left}
th{background:#f0f0f0;font-weight:600}.notes{margin-top:20px;border-top:2px solid #333;padding-top:8px}
.notes-area{width:100%;height:80px;border:1px solid #ccc;border-radius:4px;margin-top:4px}
@media print{body{padding:10px}}</style></head><body>
<h2>${t("anesthesiaPrintTitle")}</h2>
<div class="info-grid">
<div><strong>${t("anesthesiaPrintSpecies")}:</strong> ${escapeHtml(spName||sp)}</div>
<div><strong>${t("anesthesiaPrintWeight")}:</strong> ${escapeHtml(weight?weight+" kg":"_____ kg")}</div>
<div><strong>${t("anesthesiaPrintDate")}:</strong> ${escapeHtml(now)}</div>
<div><strong>ASA:</strong> ☐I ☐II ☐III ☐IV ☐V ☐E</div>
</div>
${drugSummary?`<h3>Drug Protocol</h3>${drugSummary}`:""}
<h3>${t("anesthesiaPrintPreop")}</h3>${makeChecklist(preopItems)}
<h3>${t("anesthesiaPrintIntraop")}</h3>${makeChecklist(intraopItems)}
<h3>${t("anesthesiaPrintPostop")}</h3>${makeChecklist(postopItems)}
<div class="notes"><h3>Notes</h3><div class="notes-area" contenteditable="true"></div></div>
</body></html>`;
  const win=window.open("","_blank");
  if(win){win.document.write(html);win.document.close();win.focus();setTimeout(()=>win.print(),300);}
}

/* Print anesthesia checklist */
function printAnesthesiaChecklist(){
  const sp=currentSpecies||"";
  const weightEl=document.getElementById("anesthesiaWeight");
  const weight=weightEl?weightEl.value:"";
  const spLabel=document.getElementById("anesthesiaSpeciesLabel");
  const spName=spLabel?spLabel.textContent:"";
  const now=new Date().toLocaleDateString();
  const preopItems=t("anesthesiaPrintPreopItems").split(",");
  const intraopItems=t("anesthesiaPrintIntraopItems").split(",");
  const postopItems=t("anesthesiaPrintPostopItems").split(",");
  const makeChecklist=(items)=>items.map(i=>`<div class="ck-item"><span class="ck-box">☐</span> ${escapeHtml(i.trim())}</div>`).join("");

  /* Collect currently visible protocols with drugs */
  const cat=document.getElementById("anesthesiaCategoryFilter").value;
  let visibleProtocols=[];
  if(anesthesiaData){
    let prots=anesthesiaData.protocols||[];
    if(cat)prots=prots.filter(p=>p.category===cat);
    visibleProtocols=prots.slice(0,10);
  }
  let drugSummary="";
  if(visibleProtocols.length&&weight){
    const wKg=parseFloat(weight);
    drugSummary=visibleProtocols.filter(p=>p.drugs&&p.drugs.length).map(p=>{
      const pN=currentLang==="ja"?(p.name?.ja||p.name?.en||""):(p.name?.en||p.name?.ja||"");
      const rows=p.drugs.map(d=>{
        const calc=calcDoseForWeight(d.dose,wKg);
        const calcStr=calc?(calc.isRange?`${calc.lo}–${calc.hi} ${calc.unit}`:`${calc.lo} ${calc.unit}`):"—";
        return`<tr><td>${escapeHtml(d.name||"")}</td><td>${escapeHtml(d.dose||"")}</td><td><strong>${calcStr}</strong></td><td>${escapeHtml(d.route||"")}</td></tr>`;
      }).join("");
      return`<h4 style="margin:12px 0 4px">${escapeHtml(pN)}</h4><table><thead><tr><th>Drug</th><th>Dose/kg</th><th>Calculated</th><th>Route</th></tr></thead><tbody>${rows}</tbody></table>`;
    }).join("");
  }

  const html=`<!DOCTYPE html><html><head><meta charset="utf-8"><title>${t("anesthesiaPrintTitle")}</title>
<style>body{font-family:sans-serif;padding:20px;font-size:13px;color:#333}
h2{text-align:center;margin-bottom:4px}h3{margin:16px 0 6px;border-bottom:2px solid #333;padding-bottom:4px}h4{font-size:13px;color:#555}
.info-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:16px;border:1px solid #ccc;padding:12px;border-radius:4px}
.info-grid div{font-size:13px}.info-grid strong{display:inline-block;min-width:60px}
.ck-item{padding:4px 0;border-bottom:1px dotted #ddd;font-size:13px}.ck-box{font-size:16px;margin-right:6px}
table{width:100%;border-collapse:collapse;font-size:12px;margin-bottom:8px}th,td{border:1px solid #ccc;padding:4px 8px;text-align:left}
th{background:#f0f0f0;font-weight:600}.notes{margin-top:20px;border-top:2px solid #333;padding-top:8px}
.notes-area{width:100%;height:80px;border:1px solid #ccc;border-radius:4px;margin-top:4px}
@media print{body{padding:10px}}</style></head><body>
<h2>${t("anesthesiaPrintTitle")}</h2>
<div class="info-grid">
<div><strong>${t("anesthesiaPrintSpecies")}:</strong> ${escapeHtml(spName||sp)}</div>
<div><strong>${t("anesthesiaPrintWeight")}:</strong> ${escapeHtml(weight?weight+" kg":"_____ kg")}</div>
<div><strong>${t("anesthesiaPrintDate")}:</strong> ${escapeHtml(now)}</div>
<div><strong>ASA:</strong> ☐I ☐II ☐III ☐IV ☐V ☐E</div>
</div>
${drugSummary?`<h3>Drug Protocol</h3>${drugSummary}`:""}
<h3>${t("anesthesiaPrintPreop")}</h3>${makeChecklist(preopItems)}
<h3>${t("anesthesiaPrintIntraop")}</h3>${makeChecklist(intraopItems)}
<h3>${t("anesthesiaPrintPostop")}</h3>${makeChecklist(postopItems)}
<div class="notes"><h3>Notes</h3><div class="notes-area" contenteditable="true"></div></div>
</body></html>`;
  const win=window.open("","_blank");
  if(win){win.document.write(html);win.document.close();win.focus();setTimeout(()=>win.print(),300);}
}

/* ===== Shared helpers ===== */

/* Toggle detail panel with accessibility */
function toggleDetail(head){
  /* Find detail section: nextElementSibling or querySelector within parent */
  let detail=head.nextElementSibling;
  if(!detail||!detail.classList.contains("disease-detail")){
    const parent=head.closest(".disease-result");
    if(parent)detail=parent.querySelector(".disease-detail");
  }
  if(!detail)return;
  const icon=head.querySelector(".expand-icon");
  const isOpen=detail.classList.toggle("open");
  head.setAttribute("aria-expanded",isOpen);
  if(icon)icon.classList.toggle("rotated",isOpen);
}

/* Attach click/keyboard handlers to .disease-db-item elements via event delegation */
function _attachDbItemHandlers(container){
  container.addEventListener("click",function(e){if(e.target.closest("a"))return;if(e.target.closest(".disease-detail.open"))return;const item=e.target.closest(".disease-db-item");if(item)toggleDbItem(item);});
  container.addEventListener("keydown",function(e){if(e.key==="Enter"||e.key===" "){const item=e.target.closest(".disease-db-item");if(item&&!e.target.closest("a")&&!e.target.closest(".disease-detail.open")){e.preventDefault();toggleDbItem(item);}}});
}

/* Toggle disease DB item */
function toggleDbItem(el){
  const detail=el.querySelector(".disease-detail");
  if(detail){
    const isOpen=detail.classList.toggle("open");
    el.setAttribute("aria-expanded",isOpen);
    if(isOpen){
      const nameEl=el.querySelector(".d-name");
      trackEvent("view_disease_detail",{species:currentSpecies,disease:(nameEl?nameEl.textContent:"").substring(0,80)});
      /* Scroll the opened item into view after transition starts */
      requestAnimationFrame(()=>{el.scrollIntoView({behavior:"smooth",block:"nearest"});});
      /* Lazy-load drug info on first open */
      if(!detail.dataset.drugsLoaded){
        detail.dataset.drugsLoaded="1";
        _loadDbItemDrugs(detail);
      }
    }
  }
}

/* Load and display related drugs for a disease DB item */
function _loadDbItemDrugs(detail){
  const treatmentDd=detail.querySelectorAll("dd");
  let treatmentText="";
  /* Treatment is the 5th <dd> (index 4) in the <dl> */
  const dl=detail.querySelector("dl");
  if(dl){
    const dts=dl.querySelectorAll("dt");
    dts.forEach((dt,i)=>{
      const ddList=dl.querySelectorAll("dd");
      if(dt.textContent.includes(t("dtTreatment"))&&ddList[i])treatmentText=ddList[i].textContent;
    });
  }
  if(!treatmentText)return;
  const lowerText=treatmentText.toLowerCase();

  function doMatch(){
    if(!allDrugs.length)return;
    const matched=[];
    for(const dr of allDrugs){
      const name=dr.name||"";
      const nameJa=dr.name_ja||"";
      if((name&&lowerText.includes(name.toLowerCase()))||(nameJa&&lowerText.includes(nameJa))){
        const entry={name,name_ja:nameJa,id:dr.id||"",category:dr.category||""};
        const si=(dr.species_info||{})[currentSpecies];
        if(si){entry.dosage=si.dosage||"";entry.dosage_ja=si.dosage_ja||"";entry.safe=si.safe;entry.notes=si.notes||"";entry.notes_ja=si.notes_ja||"";}
        matched.push(entry);
        if(matched.length>=10)break;
      }
    }
    if(!matched.length)return;
    const container=document.createElement("div");
    container.style.cssText="margin-top:10px;border-top:1px solid var(--gray-200);padding-top:10px";
    container.innerHTML=renderMentionedDrugs({mentioned_drugs:matched});
    detail.appendChild(container);
  }

  if(allDrugs.length>0){doMatch();return;}
  /* Drugs not loaded yet — fetch them */
  fetchWithTimeout("/api/drugs").then(r=>r.json()).then(data=>{
    if(!allDrugs.length){allDrugs=data.drugs||[];}
    doMatch();
  }).catch(()=>{});
}

/* Debounce utility */
function debounce(fn,ms){let t;return function(...a){clearTimeout(t);t=setTimeout(()=>fn.apply(this,a),ms);};}

/* Search text highlight */
function highlightMatch(text,query){
  if(!query||!text)return escapeHtml(text);
  const safe=escapeHtml(text);
  const escaped=query.replace(/[.*+?^${}()|[\]\\]/g,"\\$&");
  return safe.replace(new RegExp(`(${escaped})`,"gi"),'<mark class="search-highlight">$1</mark>');
}

/* ===== UI/UX Enhancements ===== */

/* --- Header shadow on scroll --- */
(function(){
  let ticking=false;
  const header=document.querySelector(".header");
  if(!header)return;
  window.addEventListener("scroll",()=>{
    if(!ticking){requestAnimationFrame(()=>{header.classList.toggle("scrolled",window.scrollY>10);ticking=false;});ticking=true;}
  },{passive:true});
})();

/* --- Scroll-to-top button --- */
(function(){
  const btn=document.createElement("button");
  btn.className="scroll-top";
  btn.setAttribute("aria-label","Scroll to top");
  btn.innerHTML="\u2191";
  document.body.appendChild(btn);
  let ticking=false;
  window.addEventListener("scroll",()=>{
    if(!ticking){requestAnimationFrame(()=>{btn.classList.toggle("visible",window.scrollY>400);ticking=false;});ticking=true;}
  },{passive:true});
  btn.addEventListener("click",()=>window.scrollTo({top:0,behavior:"smooth"}));
})();

/* --- Fade-in sections on scroll --- */
(function(){
  const sections=document.querySelectorAll(".species-section,.main-content,.sponsor-section,.references,.landing-chat");
  sections.forEach(s=>s.classList.add("fade-in-section"));
  const observer=new IntersectionObserver(entries=>{
    entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add("visible");observer.unobserve(e.target);}});
  },{threshold:0.08,rootMargin:"0px 0px -40px 0px"});
  sections.forEach(s=>observer.observe(s));
})();

/* --- Stagger species card animation --- */
const _origRenderSpeciesGrid=renderSpeciesGrid;
renderSpeciesGrid=function(){
  _origRenderSpeciesGrid();
  document.querySelectorAll(".species-card").forEach((c,i)=>{c.style.animationDelay=`${i*40}ms`;});
};

/* --- Dark mode removed for better mobile readability --- */

/* --- Toast utility --- */
function showToast(msg,type,duration){
  type=type||"";duration=duration||2500;
  let toast=document.querySelector(".toast");
  if(!toast){toast=document.createElement("div");toast.className="toast";document.body.appendChild(toast);}
  toast.textContent=msg;toast.className="toast"+(type?" "+type:"");
  requestAnimationFrame(()=>{toast.classList.add("show");});
  clearTimeout(toast._timer);
  toast._timer=setTimeout(()=>toast.classList.remove("show"),duration);
}
// === multidisease-combinations.js ===
/**
 * Disease Combinations Component
 * Renders pairwise/triple disease combination hypotheses with confidence bars.
 */

/**
 * Render disease combinations section
 * @param {Array} combinations - Array of disease combination objects
 * @returns {HTMLElement}
 */
function renderCombinations(combinations) {
  const section = document.createElement('div');
  section.className = 'multidisease-combinations';

  const title = document.createElement('div');
  title.className = 'combinations-title';
  title.textContent = t('mdCombinations');
  section.appendChild(title);

  combinations.forEach((combo, index) => {
    const item = document.createElement('div');
    item.className = 'combination-item';
    if (index === 0) item.classList.add('selected');
    item.setAttribute('data-combo-id', index);
    item.setAttribute('role', 'button');
    item.setAttribute('tabindex', '0');

    // Disease names
    const diseaseDiv = document.createElement('div');
    diseaseDiv.className = 'combination-diseases';

    combo.diseases.forEach((disease, idx) => {
      if (idx > 0) {
        const connector = document.createElement('span');
        connector.className = 'combination-connector';
        connector.textContent = '+';
        diseaseDiv.appendChild(connector);
      }

      const badge = document.createElement('span');
      badge.className = 'disease-badge';
      if (idx === 0) badge.classList.add('primary');
      badge.textContent = disease;
      diseaseDiv.appendChild(badge);
    });

    item.appendChild(diseaseDiv);

    // Confidence
    if (combo.combined_confidence !== undefined) {
      const confidence = document.createElement('div');
      confidence.className = 'combination-confidence';
      const percentage = (combo.combined_confidence * 100).toFixed(1);
      confidence.textContent = `Combined Confidence: ${percentage}%`;

      const bar = document.createElement('div');
      bar.className = 'confidence-bar';

      const fill = document.createElement('div');
      fill.className = 'confidence-fill';
      fill.style.width = `${combo.combined_confidence * 100}%`;
      bar.appendChild(fill);

      item.appendChild(confidence);
      item.appendChild(bar);
    }

    // Metadata
    if (combo.intersection_size !== undefined) {
      const meta = document.createElement('div');
      meta.className = 'combination-meta';
      meta.textContent = `Shared symptoms: ${combo.intersection_size}`;
      item.appendChild(meta);
    }

    section.appendChild(item);
  });

  return section;
}

// === multidisease-ambiguity.js ===
/**
 * Ambiguity Analysis Component
 * Renders ambiguous symptom indicators and resolution recommendations.
 */

/**
 * Render ambiguity analysis section
 * @param {Object} analysis - Ambiguity analysis data from API
 * @returns {HTMLElement}
 */
function renderAmbiguityAnalysis(analysis) {
  const section = document.createElement('div');
  section.className = 'ambiguity-section';

  const title = document.createElement('div');
  title.className = 'ambiguity-title';
  title.textContent = t('mdAmbiguous');
  section.appendChild(title);

  if (
    analysis.high_ambiguity_symptoms &&
    analysis.high_ambiguity_symptoms.length > 0
  ) {
    const itemsDiv = document.createElement('div');
    itemsDiv.className = 'ambiguity-items';

    analysis.high_ambiguity_symptoms.forEach((symptom) => {
      const item = document.createElement('span');
      item.className = 'ambiguous-symptom';
      item.textContent = symptom.symptom_id;

      if (symptom.ambiguity_score !== undefined) {
        const score = document.createElement('span');
        score.className = 'ambiguity-score';
        score.textContent = (symptom.ambiguity_score * 100).toFixed(0);
        item.appendChild(score);
      }

      itemsDiv.appendChild(item);
    });

    section.appendChild(itemsDiv);
  }

  // Recommendations
  if (analysis.recommendations) {
    const recommendations = Object.entries(analysis.recommendations);
    if (recommendations.length > 0) {
      const recDiv = document.createElement('div');
      recDiv.className = 'user-guidance';
      recDiv.innerHTML = `
        <div class="guidance-title">${escapeHtml(t('mdRecommendations'))}</div>
        <ul style="margin-left: 16px; margin-top: 4px;">
          ${recommendations
            .map(([key, value]) => `<li>${value}</li>`)
            .join('')}
        </ul>
      `;
      section.appendChild(recDiv);
    }
  }

  return section;
}

// === multidisease-confidence.js ===
/**
 * Confidence Breakdown Component
 * Renders per-disease confidence bars and final combined confidence.
 */

/**
 * Render confidence breakdown section
 * @param {Object} breakdown - Confidence breakdown data from API
 * @returns {HTMLElement}
 */
function renderConfidenceBreakdown(breakdown) {
  const section = document.createElement('div');
  section.className = 'confidence-breakdown';

  const title = document.createElement('div');
  title.className = 'breakdown-title';
  title.textContent = t('mdConfidence');
  section.appendChild(title);

  // Individual confidences
  if (breakdown.individual_confidences) {
    Object.entries(breakdown.individual_confidences).forEach(
      ([disease, score]) => {
        const item = document.createElement('div');
        item.className = 'breakdown-item';

        const label = document.createElement('div');
        label.className = 'breakdown-label';
        label.innerHTML = `
          <span>${disease}</span>
          <span class="breakdown-percentage">${(score * 100).toFixed(1)}%</span>
        `;
        item.appendChild(label);

        const bar = document.createElement('div');
        bar.className = 'breakdown-bar';
        const fill = document.createElement('div');
        fill.className = 'breakdown-fill';
        fill.style.width = `${score * 100}%`;
        bar.appendChild(fill);
        item.appendChild(bar);

        section.appendChild(item);
      }
    );
  }

  // Final confidence
  if (breakdown.final_confidence !== undefined) {
    const finalDiv = document.createElement('div');
    finalDiv.style.marginTop = '10px';
    finalDiv.style.paddingTop = '10px';
    finalDiv.style.borderTop = '1px solid #d1fae5';

    const finalLabel = document.createElement('div');
    finalLabel.className = 'breakdown-label';
    finalLabel.innerHTML = `
      <span style="font-weight: 700;">Final Combined Confidence</span>
      <span class="breakdown-percentage" style="color: #16a34a;">
        ${(breakdown.final_confidence * 100).toFixed(1)}%
      </span>
    `;
    finalDiv.appendChild(finalLabel);

    section.appendChild(finalDiv);
  }

  return section;
}

// === multidisease-questions.js ===
/**
 * Clarifying Questions Component
 * Renders ranked discriminative questions with language support.
 */

/**
 * Render clarifying questions section
 * @param {Array} questions - Array of question objects from API
 * @returns {HTMLElement}
 */
function renderClarifyingQuestions(questions) {
  const section = document.createElement('div');
  section.className = 'clarifying-questions';

  const title = document.createElement('div');
  title.className = 'questions-title';
  title.textContent = t('mdClarifying');
  section.appendChild(title);

  const list = document.createElement('div');
  list.className = 'question-list';

  questions.forEach((q) => {
    const item = document.createElement('button');
    item.className = 'question-item';
    item.setAttribute('data-question-id', q.question.question_id);
    item.setAttribute('data-ranking-score', q.ranking_score);

    if (q.ranking_score > 0.8) {
      item.classList.add('recommended');
    }

    const questionText = document.createElement('span');
    questionText.className = 'question-text';
    const lang =
      typeof currentLang !== 'undefined' && currentLang === 'ja'
        ? q.question.text_ja
        : q.question.text_en;
    questionText.textContent = lang || q.question.text_en || q.question.text_ja;

    const meta = document.createElement('div');
    meta.className = 'question-meta';
    meta.innerHTML = `
      <span>${q.explanation || ''}</span>
      <span class="question-score">${(q.ranking_score * 100).toFixed(0)}%</span>
    `;

    item.appendChild(questionText);
    item.appendChild(meta);
    list.appendChild(item);
  });

  section.appendChild(list);
  return section;
}

// === multidisease-guidance.js ===
/**
 * User Guidance Component
 * Renders diagnostic guidance text with language support.
 */

/**
 * Render user guidance section
 * @param {Object} analysis - Analysis data containing explanation_en/explanation_ja
 * @returns {HTMLElement}
 */
function renderUserGuidance(analysis) {
  const guidance = document.createElement('div');
  guidance.className = 'user-guidance';

  const title = document.createElement('div');
  title.className = 'guidance-title';
  title.textContent = t('mdGuidance');
  guidance.appendChild(title);

  const text = document.createElement('div');
  text.className = 'guidance-text';

  const icon = document.createElement('span');
  icon.className = 'guidance-icon';
  icon.textContent = '\u2192'; // →

  const content = document.createElement('span');
  const lang =
    typeof currentLang !== 'undefined' && currentLang === 'ja'
      ? analysis.explanation_ja
      : analysis.explanation_en;
  content.textContent =
    lang ||
    'Review the disease combinations and answer clarifying questions to narrow down the diagnosis.';

  text.appendChild(icon);
  text.appendChild(content);
  guidance.appendChild(text);

  return guidance;
}

// === multidisease-ui.js ===
/**
 * Multi-Disease Diagnostic UI Handler (Orchestrator)
 * Phase 6 Stage 9: Frontend Integration
 *
 * Coordinates component modules:
 * - multidisease-combinations.js  (renderCombinations)
 * - multidisease-ambiguity.js     (renderAmbiguityAnalysis)
 * - multidisease-confidence.js    (renderConfidenceBreakdown)
 * - multidisease-questions.js     (renderClarifyingQuestions)
 * - multidisease-guidance.js      (renderUserGuidance)
 */

class MultiDiseaseUIHandler {
  constructor() {
    this.currentAnalysis = null;
    this.apiEndpoint = '/api/multidisease/analyze';
    this.containerSelector = '.multidisease-ui-container';
  }

  /**
   * Initialize multi-disease UI components
   */
  init() {
    this.setupEventListeners();
    this.observeSymptomChanges();
  }

  /**
   * Setup event listeners for interactive elements
   */
  setupEventListeners() {
    document.addEventListener('click', (e) => {
      if (e.target.closest('.combination-item')) {
        this.onCombinationSelected(e.target.closest('.combination-item'));
      }
      if (e.target.closest('.question-item')) {
        this.onQuestionSelected(e.target.closest('.question-item'));
      }
    });
  }

  /**
   * Observe changes to selected symptoms and trigger analysis
   */
  observeSymptomChanges() {
    const selectedSymptoms = document.querySelector('.selected-symptoms');
    if (!selectedSymptoms) return;

    const observer = new MutationObserver(() => {
      clearTimeout(this.analysisTimeout);
      this.analysisTimeout = setTimeout(() => {
        this.performMultiDiseaseAnalysis();
      }, 500);
    });

    observer.observe(selectedSymptoms, {
      childList: true,
      subtree: true,
    });
  }

  /**
   * Perform multi-disease analysis via API
   */
  async performMultiDiseaseAnalysis() {
    const symptoms = this.getSelectedSymptoms();
    const diseases = this.getSuspectedDiseases();

    if (symptoms.length < 2 || diseases.length < 2) {
      this.clearMultiDiseaseUI();
      return;
    }

    this.showLoading();

    try {
      const response = await fetch(this.apiEndpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          symptom_ids: symptoms,
          suspected_diseases: diseases,
        }),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();
      this.currentAnalysis = data;
      this.renderMultiDiseaseUI(data);
    } catch (error) {
      console.error('Multi-disease analysis error:', error);
      this.showError(`Analysis failed: ${error.message}`);
    }
  }

  /**
   * Get list of selected symptoms
   */
  getSelectedSymptoms() {
    const items = document.querySelectorAll(
      '.symptom-item[aria-checked="true"]'
    );
    return Array.from(items).map(
      (item) => item.getAttribute('data-symptom-id') || item.textContent.trim()
    );
  }

  /**
   * Get list of suspected diseases
   */
  getSuspectedDiseases() {
    return [];
  }

  /**
   * Render complete multi-disease UI using component functions
   */
  renderMultiDiseaseUI(analysis) {
    const container = this.getOrCreateContainer();
    container.innerHTML = '';

    if (!analysis.multidisease_mode_enabled) {
      return;
    }

    // Mode badge
    container.appendChild(this.createModeBadge());

    // Disease combinations (from multidisease-combinations.js)
    if (analysis.combinations && analysis.combinations.length > 0) {
      container.appendChild(renderCombinations(analysis.combinations));
    }

    // Ambiguity analysis (from multidisease-ambiguity.js)
    if (analysis.ambiguity_analysis) {
      container.appendChild(renderAmbiguityAnalysis(analysis.ambiguity_analysis));
    }

    // Confidence breakdown (from multidisease-confidence.js)
    if (analysis.confidence_breakdown) {
      container.appendChild(renderConfidenceBreakdown(analysis.confidence_breakdown));
    }

    // Clarifying questions (from multidisease-questions.js)
    if (analysis.next_questions && analysis.next_questions.length > 0) {
      container.appendChild(renderClarifyingQuestions(analysis.next_questions));
    }

    // User guidance (from multidisease-guidance.js)
    if (analysis.explanation_en || analysis.explanation_ja) {
      container.appendChild(renderUserGuidance(analysis));
    }
  }

  /**
   * Create multi-disease mode badge
   */
  createModeBadge() {
    const badge = document.createElement('div');
    badge.className = 'multidisease-badge';
    badge.textContent = t('mdActive');
    return badge;
  }

  /**
   * Get or create UI container
   */
  getOrCreateContainer() {
    let container = document.querySelector(this.containerSelector);
    if (!container) {
      const insertAfter = document.querySelector('.chat-container') ||
        document.querySelector('.diagnosis-section');
      container = document.createElement('div');
      container.className = 'multidisease-ui-container';
      if (insertAfter) {
        insertAfter.parentNode.insertBefore(container, insertAfter.nextSibling);
      } else {
        document.body.appendChild(container);
      }
    }
    return container;
  }

  /**
   * Show loading state
   */
  showLoading() {
    const container = this.getOrCreateContainer();
    container.innerHTML = `
      <div class="multidisease-loading">
        <span class="spinner"></span>
        <span>${escapeHtml(t('mdAnalyzing'))}</span>
      </div>
    `;
  }

  /**
   * Show error state
   */
  showError(message) {
    const container = this.getOrCreateContainer();
    container.innerHTML = `
      <div class="multidisease-error">
        <div class="error-title">Analysis Error</div>
        <p>${message}</p>
      </div>
    `;
  }

  /**
   * Clear multi-disease UI
   */
  clearMultiDiseaseUI() {
    const container = document.querySelector(this.containerSelector);
    if (container) {
      container.innerHTML = '';
    }
  }

  /**
   * Handle combination selection
   */
  onCombinationSelected(element) {
    document.querySelectorAll('.combination-item').forEach((item) => {
      item.classList.remove('selected');
    });
    element.classList.add('selected');
    const comboId = element.getAttribute('data-combo-id');
    // combo selection handled via data attribute
  }

  /**
   * Handle question selection
   */
  onQuestionSelected(element) {
    const questionId = element.getAttribute('data-question-id');
    const questionText = element.querySelector('.question-text').textContent;

    const chatInput = document.getElementById('chatInput');
    if (chatInput) {
      chatInput.value = questionText;
    }
    // question selection handled via input injection
  }
}

/**
 * Initialize multi-disease UI when DOM is ready
 */
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    window.multiDiseaseUI = new MultiDiseaseUIHandler();
    window.multiDiseaseUI.init();
  });
} else {
  window.multiDiseaseUI = new MultiDiseaseUIHandler();
  window.multiDiseaseUI.init();
}

/**
 * Expose API for manual triggering
 */
function triggerMultiDiseaseAnalysis() {
  if (window.multiDiseaseUI) {
    window.multiDiseaseUI.performMultiDiseaseAnalysis();
  }
}

/**
 * Global Search Box
 */
(function initGlobalSearch() {
  const searchInput=document.getElementById('globalSearch');
  const searchResults=document.getElementById('globalSearchResults');
  if(!searchInput||!searchResults)return;

  let searchTimer;
  let currentLang='ja';

  // Detect language
  const langBtns=document.querySelectorAll('.lang-toggle button');
  langBtns.forEach(btn=>{
    btn.addEventListener('click',()=>{
      currentLang=btn.getAttribute('data-lang');
    });
  });

  // Search listener
  searchInput.addEventListener('input',function(e){
    clearTimeout(searchTimer);
    const query=e.target.value.trim();

    if(query.length<2){
      searchResults.style.display='none';
      return;
    }

    searchTimer=setTimeout(()=>{
      fetchWithTimeout(`/api/diseases?q=${encodeURIComponent(query)}&limit=8`)
        .then(r=>{
          if(!r.ok)throw new Error(`HTTP ${r.status}`);
          return r.json();
        })
        .then(data=>{
          const diseases=data.diseases||[];
          const queryKeywords=data.query?.toLowerCase().split(/\s+/).filter(k=>k)||[];

          if(diseases.length===0){
            searchResults.innerHTML='<div style="padding:12px;color:var(--gray-500);text-align:center">キーワード「'+escapeHtml(data.query)+'」に一致する疾患が見つかりませんでした</div>';
          }else{
            const html=diseases.map((d,idx)=>{
              // Determine which field matched the keyword
              const name=(d.name||'').toLowerCase();
              const name_ja=(d.name_ja||'').toLowerCase();
              let matchInfo='';
              for(const kw of queryKeywords){
                if(name.includes(kw)||name_ja.includes(kw)){
                  matchInfo=kw;
                  break;
                }
              }

              // Urgency badge color
              const urgencyColor={
                'emergency':'var(--red)',
                'high':'var(--orange)',
                'moderate':'var(--gray-500)',
                'low':'var(--gray-500)'
              }[d.urgency]||'var(--gray-500)';

              return `
              <a href="/diseases/${encodeURIComponent(d.species)}/${encodeURIComponent(d.slug||slugify(d.name))}"
                 class="search-result-item"
                 role="option"
                 aria-selected="false"
                 data-disease-id="${escapeHtml(d.id)}"
                 title="${escapeHtml(d.name)}">
                <div style="flex:1">
                  <strong>${escapeHtml(d.name_ja||d.name)}</strong>
                  ${d.name_ja?'<div style="font-size:.8rem;color:var(--gray-500)">'+escapeHtml(d.name)+'</div>':''}
                </div>
                <span class="search-result-species">${escapeHtml(d.species)}</span>
                ${d.urgency?'<span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:'+urgencyColor+';margin-left:8px" title="'+escapeHtml(d.urgency)+'"></span>':''}
              </a>
            `}).join('');
            searchResults.innerHTML=html;
          }
          searchResults.style.display='block';
        })
        .catch(err=>{
          console.warn('Global search error:',err);
          searchResults.innerHTML='<div style="padding:12px;color:var(--red);text-align:center">エラーが発生しました</div>';
          searchResults.style.display='block';
        });
    },300);
  });

  // Close on ESC
  searchInput.addEventListener('keydown',function(e){
    if(e.key==='Escape'){
      searchResults.style.display='none';
      searchInput.value='';
    }
  });

  // Close when clicking outside
  document.addEventListener('click',function(e){
    if(!e.target.closest('.global-search-container')){
      searchResults.style.display='none';
    }
  });

  // Filter functionality
  let selectedSpecies=new Set();

  const filterBtn=document.getElementById('searchFilterBtn');
  const filterPanel=document.getElementById('speciesFilterPanel');
  const speciesFilterList=document.getElementById('speciesFilterList');
  const filterCloseBtn=document.getElementById('filterCloseBtn');
  const filterResetBtn=document.getElementById('filterResetBtn');

  if(filterBtn&&filterPanel){
    // Initialize species filter list
    function initFilterList(){
      const speciesOrder=['dog','cat','horse','rabbit','hamster','guinea_pig','chinchilla','ferret','hedgehog','sugar_glider','degu','bird','parakeet','parrot','reptile','tortoise','snake','lizard','amphibian','fish','exotic_other'];
      const speciesNames={dog:'犬',cat:'猫',horse:'馬',rabbit:'うさぎ',hamster:'ハムスター',guinea_pig:'モルモット',chinchilla:'チンチラ',ferret:'フェレット',hedgehog:'ハリネズミ',sugar_glider:'フクロモモンガ',degu:'デグー',bird:'鳥',parakeet:'インコ',parrot:'オウム',reptile:'爬虫類',tortoise:'リクガメ',snake:'ヘビ',lizard:'トカゲ',amphibian:'両生類',fish:'魚',exotic_other:'その他エキゾチック'};

      const html=speciesOrder.map(sp=>`
        <div class="filter-checkbox ${selectedSpecies.has(sp)?'active':''}">
          <input type="checkbox" id="filter-${sp}" value="${sp}" ${selectedSpecies.has(sp)?'checked':''}>
          <label for="filter-${sp}">${SPECIES_ICONS[sp]||'🐾'} ${speciesNames[sp]}</label>
        </div>
      `).join('');
      speciesFilterList.innerHTML=html;

      // Attach listeners
      document.querySelectorAll('#speciesFilterList input[type="checkbox"]').forEach(cb=>{
        cb.addEventListener('change',function(){
          if(this.checked){
            selectedSpecies.add(this.value);
          }else{
            selectedSpecies.delete(this.value);
          }
          this.closest('.filter-checkbox').classList.toggle('active');
          performFilteredSearch();
        });
      });
    }

    // Perform filtered search (with species and category support)
    function performFilteredSearch(){
      const query=searchInput.value.trim();
      if(query.length<2)return;

      const speciesParam=selectedSpecies.size>0?Array.from(selectedSpecies).join(','):'';
      let url=`/api/diseases?q=${encodeURIComponent(query)}&limit=8`;
      if(speciesParam)url+=`&species=${encodeURIComponent(speciesParam)}`;
      if(typeof selectedCategory!=='undefined'&&selectedCategory)url+=`&category=${encodeURIComponent(selectedCategory)}`;

      fetchWithTimeout(url)
        .then(r=>{
          if(!r.ok)throw new Error(`HTTP ${r.status}`);
          return r.json();
        })
        .then(data=>{
          const diseases=data.diseases||[];
          const queryKeywords=data.query?.toLowerCase().split(/\s+/).filter(k=>k)||[];

          if(diseases.length===0){
            searchResults.innerHTML='<div style="padding:12px;color:var(--gray-500);text-align:center">キーワード「'+escapeHtml(data.query)+'」に一致する疾患が見つかりませんでした</div>';
          }else{
            const html=diseases.map((d,idx)=>{
              const urgencyColor={emergency:'var(--red)',high:'var(--orange)',moderate:'var(--gray-500)',low:'var(--gray-500)'}[d.urgency]||'var(--gray-500)';
              return `
              <a href="/diseases/${encodeURIComponent(d.species)}/${encodeURIComponent(d.slug||slugify(d.name))}"
                 class="search-result-item"
                 role="option"
                 aria-selected="false"
                 data-disease-id="${escapeHtml(d.id)}"
                 title="${escapeHtml(d.name)}">
                <div style="flex:1">
                  <strong>${escapeHtml(d.name_ja||d.name)}</strong>
                  ${d.name_ja?'<div style="font-size:.8rem;color:var(--gray-500)">'+escapeHtml(d.name)+'</div>':''}
                </div>
                <span class="search-result-species">${escapeHtml(d.species)}</span>
                ${d.urgency?'<span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:'+urgencyColor+';margin-left:8px" title="'+escapeHtml(d.urgency)+'"></span>':''}
              </a>
            `}).join('');
            searchResults.innerHTML=html;
          }
          searchResults.style.display='block';
        })
        .catch(err=>{
          console.warn('Filtered search error:',err);
          searchResults.innerHTML='<div style="padding:12px;color:var(--red);text-align:center">エラーが発生しました</div>';
          searchResults.style.display='block';
        });
    }

    // Filter panel toggle
    filterBtn.addEventListener('click',function(e){
      e.preventDefault();
      if(filterPanel.style.display==='none'){
        initFilterList();
        filterPanel.style.display='block';
      }else{
        filterPanel.style.display='none';
      }
    });

    filterCloseBtn.addEventListener('click',function(){
      filterPanel.style.display='none';
    });

    filterResetBtn.addEventListener('click',function(){
      selectedSpecies.clear();
      document.querySelectorAll('#speciesFilterList input[type="checkbox"]').forEach(cb=>{
        cb.checked=false;
        cb.closest('.filter-checkbox').classList.remove('active');
      });
      performFilteredSearch();
    });

    // Close filter panel when clicking outside
    document.addEventListener('click',function(e){
      if(!e.target.closest('.global-search-container')){
        filterPanel.style.display='none';
      }
    });
  }

  // Category filter functionality
  let selectedCategory='';
  const categoryFilterBtn=document.getElementById('categoryFilterBtn');
  const categoryFilterPanel=document.getElementById('categoryFilterPanel');
  const categoryFilterList=document.getElementById('categoryFilterList');
  const categoryFilterCloseBtn=document.getElementById('categoryFilterCloseBtn');
  const categoryFilterResetBtn=document.getElementById('categoryFilterResetBtn');

  if(categoryFilterBtn&&categoryFilterPanel){
    const categories=[
      {id:'respiratory',name_ja:'呼吸器'},
      {id:'digestive',name_ja:'消化器'},
      {id:'neurological',name_ja:'神経'},
      {id:'musculoskeletal',name_ja:'運動器'},
      {id:'dermatological',name_ja:'皮膚'},
      {id:'urinary',name_ja:'泌尿器'},
      {id:'ophthalmological',name_ja:'眼'},
      {id:'cardiovascular',name_ja:'循環器'},
      {id:'endocrine',name_ja:'内分泌'},
      {id:'behavioral',name_ja:'行動'},
      {id:'reproductive',name_ja:'繁殖'},
      {id:'general',name_ja:'全身'},
      {id:'other',name_ja:'その他'}
    ];

    function initCategoryFilterList(){
      const html=categories.map(cat=>`
        <div class="filter-checkbox ${selectedCategory===cat.id?'active':''}">
          <input type="radio" name="category-filter" id="filter-cat-${cat.id}" value="${cat.id}" ${selectedCategory===cat.id?'checked':''}>
          <label for="filter-cat-${cat.id}">${escapeHtml(cat.name_ja)}</label>
        </div>
      `).join('');
      categoryFilterList.innerHTML=html;

      document.querySelectorAll('#categoryFilterList input[type="radio"]').forEach(rb=>{
        rb.addEventListener('change',function(){
          selectedCategory=this.value;
          document.querySelectorAll('#categoryFilterList .filter-checkbox').forEach(el=>{
            el.classList.remove('active');
          });
          this.closest('.filter-checkbox').classList.add('active');
          performFilteredSearch();
        });
      });
    }

    categoryFilterBtn.addEventListener('click',function(e){
      e.preventDefault();
      if(categoryFilterPanel.style.display==='none'){
        initCategoryFilterList();
        categoryFilterPanel.style.display='block';
      }else{
        categoryFilterPanel.style.display='none';
      }
    });

    categoryFilterCloseBtn.addEventListener('click',function(){
      categoryFilterPanel.style.display='none';
    });

    categoryFilterResetBtn.addEventListener('click',function(){
      selectedCategory='';
      document.querySelectorAll('#categoryFilterList input[type="radio"]').forEach(rb=>{
        rb.checked=false;
        rb.closest('.filter-checkbox').classList.remove('active');
      });
      performFilteredSearch();
    });
  }
})();

