const SPECIES_ICONS={dog:"\u{1F415}",cat:"\u{1F408}",horse:"\u{1F434}",rabbit:"\u{1F407}",hamster:"\u{1F439}",guinea_pig:"\u{1F43E}",chinchilla:"\u{1F43E}",ferret:"\u{1F43E}",hedgehog:"\u{1F994}",sugar_glider:"\u{1F43E}",degu:"\u{1F43E}",bird:"\u{1F426}",parakeet:"\u{1F424}",parrot:"\u{1F99C}",reptile:"\u{1F98E}",tortoise:"\u{1F422}",snake:"\u{1F40D}",lizard:"\u{1F98E}",amphibian:"\u{1F438}",fish:"\u{1F41F}",exotic_other:"\u{1F43E}"};

/* ===== Admin / Pro access control ===== */
// Admin verification handled server-side
// OPEN BETA: All users get Pro access for free.
// Set to false when launching paid plans.
const OPEN_BETA=true;
let isAdmin=false;
let isPro=false;

// Debug logging — only emits when running locally or with ?debug=1
const _DEBUG=(()=>{try{const h=location.hostname;return h==="localhost"||h==="127.0.0.1"||h===""||location.search.indexOf("debug=1")>=0;}catch(e){return false;}})();
function debugWarn(){if(_DEBUG&&typeof console!=="undefined")console.warn.apply(console,arguments);}
function debugError(){if(_DEBUG&&typeof console!=="undefined")console.error.apply(console,arguments);}

// Clipboard helper with execCommand fallback for older/iframe-blocked contexts.
async function copyToClipboard(text){
  try{
    if(navigator.clipboard&&window.isSecureContext){
      await navigator.clipboard.writeText(text);
      return true;
    }
  }catch(e){debugWarn("clipboard.writeText failed, falling back",e);}
  try{
    const ta=document.createElement("textarea");
    ta.value=text;
    ta.setAttribute("readonly","");
    ta.style.position="fixed";ta.style.top="-1000px";ta.style.opacity="0";
    document.body.appendChild(ta);
    ta.select();
    const ok=document.execCommand("copy");
    document.body.removeChild(ta);
    return ok;
  }catch(e){debugError("copy fallback failed",e);return false;}
}

// Coerce a possibly string/undefined field into an array. Some drug entries
// store list fields (side_effects, routes, …) as comma-separated strings;
// rendering them as arrays without this guard throws and blanks the whole list.
function toList(v){
  if(Array.isArray(v))return v;
  if(typeof v==="string")return v.split(/[、,，]/).map(s=>s.trim()).filter(Boolean);
  return v==null?[]:[v];
}

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
    badge.title=t("adminBadgeTitle")||"Admin mode";
    document.body.appendChild(badge);
  }
}

/* ===== Bilingual i18n system ===== */
let currentLang="ja";
const I18N={
  ja:{
    skipLink:"メインコンテンツへスキップ",
    logoSub:"獣医師のための臨床意思決定支援",
    navChecker:"鑑別診断",navDatabase:"疾患データベース",navChat:"臨床相談",navDrugs:"薬品辞書",navAnesthesia:"鎮静・麻酔",navEmergency:"🚨 緊急対応",
    cardEmergency:"🚨 緊急プロトコル / クイックリファレンス",emergencyImportant:"⚠ 重要:",emergencyDisclaimer:"緊急時は同時並行的に対応が必要です。本プロトコルは標準的な対応の参考ですが、実際の施行には熟練した獣医師の臨床判断が必須です。各薬品の用量・投与経路は処方前に必ず再確認してください。",
    emergencyTriggerSigns:"認識すべき徴候",emergencyKeyDrugs:"主要薬剤",emergencyMonitoring:"モニタリング指標",emergencyStepsTitle:"対応プロトコル",emergencyTimeTarget:"目標時間",
    landingChatTitle:"臨床症状から鑑別診断",
    heroTrustSpecies:"犬猫〜エキゾチック21動物種対応",heroTrustRef:"190+学術文献に基づく",heroTrustTests:"3,800+自動テスト検証済み",heroTrustOss:"オープンソース開発",
    landingChatHint:'臨床症状を入力すると鑑別疾患リストを生成します。<br/><span style="font-size:.76rem;color:var(--gray-500)">例: 「嘔吐 食欲不振 体重減少」「polyuria polydipsia lethargy」</span>',
    heroBadge:"現役獣医師が開発 — 臨床現場の鑑別診断を支援",
    heroAudience:"獣医師・獣医学生のための臨床支援ツール",
    heroLead:"臨床症状から鑑別疾患リストを即座に生成。",
    heroCta:"動物種を選択して鑑別診断を開始",heroCtaDb:"疾患データベースを見る",
    statDiseases:"疾患数",statSpecies:"対応動物種",statSymptoms:"症状項目",statDrugs:"薬品数",statProtocols:"麻酔プロトコル",
    heroStatsAria:"データベース統計",
    heroCredit:'開発: <a href="https://www.minamisoma-vet.com/" target="_blank" rel="noopener noreferrer">南相馬アニマルクリニック</a> 獣医師 上手 健太郎',
    sponsorDesc:"獣医師考案・国内製造・競走馬理化学研究所検査合格",
    sponsorCta:"詳細 →",
    sponsorAria:"スポンサー: Equine & Canine Vet Nutrition (caninevet.jp) — 別タブで開きます",
    selectSpecies:"動物種を選択",
    cardSymptoms:"&#9745; 症状を選択",cardResults:"&#128202; 検索結果",
    breedLabel:"品種を選択（任意）",breedNone:"品種を選択しない",
    symptomSearchPh:"症状を検索... (例: 咳, vomiting, 下痢)",
    analyzeBtn:"鑑別疾患を検索",checkerGuide:'💡 <strong>使い方:</strong> 上の症状リストからチェックを入れ、「鑑別疾患を検索」を押してください。<br/>症状が多いほど精度が向上します（3つ以上推奨）。',
    labSectionTitle:"&#128300; 検査値を入力（任意）",
    labCatRenal:"腎機能",labCatHepatic:"肝機能",labCatMetabolic:"代謝・膵",labCatElectrolyte:"電解質",labCatCBC:"CBC",labCatEndocrine:"内分泌・炎症・尿",
    labClear:"検査値をクリア",
    labImport:"📷 画像/テキストから取込",
    painScaleTitle:"&#x1F9D1;&#x200D;&#x2695;&#xFE0F; 痛みの評価 (CSU Pain Scale)",
    painScaleHint:"Colorado State University 犬急性痛みスケール（0〜4）を選択してください。",
    painDesc0:"快適、リラックス、尾を振る",
    painDesc1:"やや落ち着かない、リップリッキング",
    painDesc2:"体位変換、うめき声、食欲低下",
    painDesc3:"鳴き声、動かない、触ると攻撃的",
    painDesc4:"横臥、叫び声、硬直、無反応",
    resultsEmpty:'動物種を選択し、症状にチェックを入れて<br/>「鑑別疾患を検索」を押してください',
    resultsSelectSymptom:"症状を選択してください",
    selectSpeciesFirst:"まず動物種を選択すると、その種の症状リストが表示されます",
    selectSpeciesFirstBtn:"動物種を選択する",
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
    drugSearchPh:"薬品名・商品名で検索... (例: バイトリル, メロキシカム)",
    drugBrandHit:"商品名",
    drugNoMatchHint:"一般名（エンロフロキサシン）・商品名（バイトリル）・英語名（enrofloxacin）のいずれでも検索できます。",
    drugClearFilters:"フィルタを解除して %n% 件を表示",
    allCategories:"全カテゴリ",allSpecies:"全動物種",speciesAny:"動物種（任意）",
    interactionCheckerTitle:"⚠️ 薬品相互作用チェッカー",interactionCheckerDesc:"複数の薬品を併用する際の相互作用を確認します。薬品名（半角英数）をカンマ区切りで入力してください。",interactionCheckBtn:"チェック",
    drugCompareTitle:"他の獣医薬リファレンスとの比較",
    drugCompareHint:"（クリックで展開）",
    drugCompareIntro:"日常診療での使い分けの参考に、VetDict・Plumb's Veterinary Drugs・VIN（Veterinary Information Network）の特徴を比較しました。",
    drugCompareColFeature:"機能",
    drugCompareRowSource:"主な情報源",
    drugCompareVetdictSource:"Plumb's (9th ed.) / Papich (5th ed.) / BSAVA / Carpenter Formulary 等",
    drugCompareCompetitorSource1:"自社編集チームによる最新薬理データ",
    drugCompareCompetitorSource2:"複数の専門書 + 専門医の臨床知見",
    drugCompareRowFreq:"更新頻度",
    drugCompareVetdictFreq:"定期的（開発者による手動更新）",
    drugCompareCompetitorFreq1:"リアルタイム（新薬・副作用情報）",
    drugCompareCompetitorFreq2:"随時（フォーラムでの議論が先行）",
    drugCompareRowSpecies:"対応動物種",
    drugCompareVetdictSpecies:"21種（魚・エキゾチック等に強い）",
    drugCompareCompetitorSpecies1:"主要ペット・馬・産業動物",
    drugCompareCompetitorSpecies2:"全方位",
    drugCompareRowInteraction:"相互作用チェック",
    drugCompareVetdictInteraction:"疾患DB内の記述・麻酔禁忌ルールに基づく",
    drugCompareCompetitorInteraction1:"専用の相互作用シミュレーターあり",
    drugCompareCompetitorInteraction2:"検索・フォーラムでの相談",
    drugCompareRowOwner:"飼い主用資料",
    drugCompareVetdictOwner:"なし（臨床家向け特化）",
    drugCompareCompetitorOwner1:"多言語のクライアントハンドアウト付",
    drugCompareCompetitorOwner2:"飼い主向け解説サイト（Veterinary Partner）",
    drugCompareRowLang:"言語",
    drugCompareVetdictLang:"日本語・英語",
    drugCompareCompetitorLang1:"英語",
    drugCompareCompetitorLang2:"英語（一部機械翻訳）",
    drugCompareAnalysisTitle:"忖度なしの詳細分析",
    drugComparePoint1Title:"検索精度と「出典」の信頼性",
    drugComparePoint1Body:"VetDictはPlumb's・BSAVA等の世界標準の文献をベースに、現役の獣医師が日本語で整理。「日本で手に入る薬剤の一般名・商品名」で検索できる実用性が強み。一方、Plumb's最新版は米FDAの最新認可情報が即座に反映され、学術的な「最先端の正確性」では出版社直営ツールが最強。",
    drugComparePoint2Title:"「使い勝手」という名の精度",
    drugComparePoint2Body:"VetDictは「嘔吐」と日本語で入力 → 鑑別疾患 → 推奨薬剤への導線が短い。VIN等は情報量が多いぶん、特定薬剤の「今すぐ知りたい用量」に辿り着くまで時間がかかる場合あり。",
    drugComparePoint3Title:"エキゾチック・特殊動物の網羅性",
    drugComparePoint3Body:"ハリネズミ・フクロモモンガ・魚といった通常の薬剤ハンドブックでは情報が薄い動物種の投与量を日本語でまとめている点は他にない強み。Carpenter's Formulary等のエッセンスを一つの窓口で提供。",
    drugCompareConclTitle:"結論：使い分けの推奨",
    drugCompareConclDailyLabel:"日常診療（VetDict）:",
    drugCompareConclDailyBody:"「この疾患に対する一般的な用量は？」「エキゾチックの投与量は？」を日本語で即座に引きたい場面に最適。",
    drugCompareConclAdvLabel:"難症例・新薬（Plumb's / VIN）:",
    drugCompareConclAdvBody:"複数薬剤の相互作用や副作用の最新報告（エビデンス）を原文で確認したい場合は、Plumb's（有料版）やVINの専門医ネットワークを参照。",
    drugCompareDisclaimer:"※ 比較は2026年時点の各サービス公開情報に基づく一般的な傾向であり、個別の機能差は変動します。最終判断は必ず原典・添付文書をご確認ください。",
    sponsorTagline:"獣医師が考案・国内製造 — 競走馬理化学研究所の検査合格",
    sponsorSpecies:"対応動物種: 馬・犬・猫",
    sponsorEquine:"馬用サプリメント",sponsorCanine:"犬用サプリメント",
    footerDisclaimer:"※ 本サービスは獣医師の臨床意思決定を支援するための参考情報を提供するものであり、確定診断を代替するものではありません。",
    footerCredit:'開発: <a href="https://www.minamisoma-vet.com/" target="_blank" rel="noopener noreferrer">南相馬アニマルクリニック</a> 獣医師 上手 健太郎 (Kentaro Kamide, DVM)',
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
    networkErrorTimeout:"接続がタイムアウトしました。",
    networkErrorOffline:"オフラインです。ネットワーク接続を確認してください。",
    networkErrorServer:"サーバーエラーが発生しました。",
    networkErrorDetail:"詳細: ",
    noDiseaseMatch:"該当する疾患がありません",
    noDrugMatch:"該当する薬品がありません",
    errorPrefix:"エラー: ",
    overallAssessment:"総合評価: ",
    commError:"通信エラーが発生しました。ネットワーク接続を確認の上、再試行してください。",
    noResponse:"応答を取得できませんでした",
    diseaseCount:"%filtered% / %total% 件表示",
    catLabels:{respiratory:"呼吸器",digestive:"消化器",neurological:"神経",musculoskeletal:"運動器",dermatological:"皮膚",urinary:"泌尿器",ophthalmological:"眼",cardiovascular:"循環器",cardiac:"循環器",behavioral:"行動",general:"全身",skin:"体表・外観",fins:"鰭",gills:"鰓",eyes:"眼",eye:"眼",ocular:"眼",ears:"耳",eyes_ears:"眼・耳",oral:"口腔",internal:"内科・全身",developmental:"発達",limb:"四肢",hoof:"蹄",dental:"歯科",repository_exam:"検査所見",toxic:"中毒",foal:"子馬",immune:"免疫",endocrine:"内分泌",misc:"その他",body:"腹部・体型",parasites:"寄生虫",emergency:"急変",reproductive:"繁殖",behavior:"行動",other:"その他"},
    sevLabels:{low:"軽度",moderate:"中等度",high:"重度",emergency:"緊急"},
    dtDescription:"説明",dtPathophysiology:"病態生理",dtCauses:"原因",dtPrevention:"予防",dtTreatment:"治療",dtPrognosis:"予後",
    dtClinicalSigns:"臨床徴候",dtDiagnosis:"診断",
    dtMatchedSymptoms:"一致した症状",dtRecommendedTests:"推奨検査",dtRecTestList:"推奨検査一覧:",
    dtSymptoms:"症状",
    dtContraindications:"禁忌事項",dtRoutes:"投与経路",dtFormulations:"製剤",dtInteractions:"薬物相互作用",dtSpeciesInfo:"動物種別情報:",dtMechanism:"作用機序",dtSideEffects:"主な副作用",
    safe:"安全",contraindicated:"禁忌",dosageLabel:"投与量: ",
    sponsorVetLabel:"獣医師考案・国内製造・競走馬理化学研究所検査合格",
    productDetails:"製品詳細 \u2192",
    speciesCardDisease:"疾患",speciesCardDrug:"薬品",
    quickNavDiseaseDb:"疾患データベース",quickNavDrugs:"薬品辞書",quickNavChat:"臨床相談",quickNavAnesthesia:"鎮静・麻酔",quickNavChecker:"鑑別診断",quickNavEmergency:"緊急対応",
    quickNavPrompt:"機能を選択してください",
    quickNavDefault:"データベースを直接閲覧",
    emptyStateSelectSpecies:"動物種を選択してください",
    emptyStateDiseaseDb:"動物種を選択すると、その種に対応する疾患データベースが表示されます",
    emptyStateDiseaseDbHint:"または上の検索ボックスに病名を入力すると、全21動物種から横断検索できます",
    xspeciesSearching:"全動物種から検索中…",
    xspeciesResultsLabel:"全種横断の検索結果（種を選ばずに調べられます）",
    emptyStateDrugs:"薬品辞書は動物種に関わらず全薬品を表示できます",
    emptyStateAnesthesia:"動物種を選択すると、種別の鎮静・麻酔プロトコルが表示されます",
    emptyStateSelectBtn:"動物種を選択する",
    breadcrumbHome:"トップ",breadcrumbNoSpecies:"動物種未選択",
    kbdShortcutsHint:"キーボード: Ctrl+1〜5でタブ切替",
    globalSearchPh:"疾患・薬品を検索...",
    menuOpen:"メニューを開く",menuClose:"メニューを閉じる",
    removeLabel:"%s%を削除",
    painLabels:["痛みなし","軽度","中等度","中〜重度","重度"],
    painScoreLabel:"スコア",
    showMoreItems:"さらに表示 (残り%n%件)",
    metabSupport:"代謝サポート",aminoAcid:"アミノ酸",digestSupport:"消化管サポート",jointSupport:"関節・運動器",
    mdCombinations:"疾患の組み合わせ候補",mdAmbiguous:"曖昧な症状が検出されました",mdConfidence:"信頼度分析",mdClarifying:"確認質問",mdGuidance:"診断ガイダンス",mdRecommendations:"推奨事項",mdActive:"複合疾患モード",mdAnalyzing:"複合疾患の組み合わせを分析中...",
    resultsDisclaimer:"本結果は鑑別診断の参考情報です。確定診断・治療方針は臨床所見・検査結果と併せて総合的にご判断ください。",
    feedbackQuestion:"この鑑別診断リストは臨床的に参考になりましたか？",
    feedbackYes:"参考になった",
    feedbackNo:"改善の余地あり",
    feedbackThanks:"フィードバックありがとうございます。",
    shareResults:"鑑別診断結果を共有",shareCopy:"コピー",shareCopied:"コピー済み",
    husbandryTitle:"飼育環境ガイド",husbandryTemp:"適正温度",husbandryHumidity:"適正湿度",husbandryHousing:"飼育環境",husbandryDiet:"食事",husbandryEnrichment:"エンリッチメント",husbandrySocial:"社会性",husbandryNotes:"その他の注意",husbandryLoading:"飼育環境情報を読み込み中...",husbandryError:"飼育環境情報の取得に失敗しました",
    offlineBanner:"オフラインです — 一部機能が制限されます",
    mobileNavChecker:"鑑別",mobileNavDatabase:"疾患DB",mobileNavChat:"相談",mobileNavDrugs:"薬品",mobileNavAnesthesia:"麻酔",mobileNavEmergency:"緊急",
    sortByConfidence:"信頼度順",sortBySeverity:"重症度順",sortByDefault:"標準",
    speciesFilterPh:"動物種を検索...",
    stepSpecies:"動物種",stepSymptoms:"症状",stepResults:"結果",
    // Header / aria-labels (i18n via data-i18n-aria / data-i18n-title)
    ariaHomeLink:"VetDict ホーム",
    ariaSearchInput:"疾患・薬品を検索",
    ariaSpeciesFilter:"動物種でフィルター",
    titleSpeciesFilter:"動物種で絞り込み",
    ariaCategoryFilter:"カテゴリーでフィルター",
    titleCategoryFilter:"症状カテゴリーで絞り込み",
    ariaCloseFilter:"閉じる",
    ariaMainNav:"メインナビゲーション",
    ariaLangToggle:"表示言語",
    ariaClearSearch:"検索をクリア",
    ariaSpeciesFilterDialog:"動物種フィルター",
    ariaCategoryFilterDialog:"症状カテゴリーフィルター",
    speciesFilterTitle:"動物種で絞り込み",
    categoryFilterTitle:"症状カテゴリーで絞り込み",
    filterReset:"リセット",
    // Cookie consent
    cookieConsentRegion:"Cookieに関するお知らせ",
    cookieConsentText:"当サイトでは利用状況の改善のためGoogle Analyticsを使用しています。あなたの選択は localStorage に保存され、後から設定変更できます。",
    cookiePrivacyLink:"プライバシーポリシー",
    cookieAccept:"同意する",
    cookieReject:"拒否する",
    cookieDismiss:"後で決める",
    cookieDismissAria:"同意せずに閉じる",
    dashboardOpen:"統計ダッシュボード",
    dashboardOpenAria:"統計ダッシュボードを開く",
    helpButton:"使い方ガイド",
    helpGuideAria:"使い方ガイドを開く",
    helpTitle:"VetDict — 使い方ガイド",
    helpClose:"閉じる",
    // Pricing
    pricingSubtitle:"現在オープンベータ — 獣医師・獣医学生は全機能を無料でご利用いただけます",
    pricingBadge:"オープンベータ",
    pricingHeader:"全機能無料",
    pricingPeriodOriginal:"¥980/月",
    pricingFeature1:"鑑別診断リスト生成（全21動物種）",
    pricingFeature2:"疾患データベース<strong>6,400+疾患</strong>閲覧",
    pricingFeature3:"薬品辞書<strong>600+薬品</strong>・種別投与量",
    pricingFeature4:"臨床相談チャット<strong>無制限</strong>",
    pricingFeature5:"検査値入力・疼痛スケール対応",
    pricingFeature6:"エキゾチック含む全21動物種対応",
    pricingCtaText:"現在すべて無料でご利用中",
    pricingNote:"正式リリース後は一部機能が有料プラン（¥980/月）に移行予定です",
    signupHeading:"🔔 正式リリース時に<span style=\"color:var(--green)\">早期割引</span>で通知を受け取る",
    signupSubtext:"ベータ期間中にご登録の獣医師限定の特典あり",
    signupEmailPh:"メールアドレス",
    signupBtn:"無料で登録",
    signupBtnSubmitting:"登録中...",
    signupBtnDone:"登録済み",
    signupSpamNote:"※ スパムは送りません。配信停止はいつでも可能です。",
    signupInvalidEmail:"有効なメールアドレスを入力してください",
    signupSuccess:"登録完了！正式リリース時にお知らせします。",
    signupGenericError:"エラーが発生しました",
    signupNetworkError:"通信エラー。時間をおいて再度お試しください。",
    // Footer / share
    shareSection:"VetDictを広める",
    shareXLabel:"X (Twitter) でポストする",
    shareFbLabel:"Facebook でシェアする",
    shareLineLabel:"LINE で送る",
    sharePostX:"X (Twitter)",sharePostXSub:"でポストする",
    sharePostFb:"Facebook",sharePostFbSub:"でシェアする",
    sharePostLine:"LINE",sharePostLineSub:"で送る",
    footerRegulatory:"本サービスは獣医師・獣医学生を対象とした臨床意思決定支援ツールです。AI解析結果は鑑別診断の参考情報であり、確定診断・治療方針の決定には臨床所見・検査結果との総合判断が必要です。本サービスは医療機器・動物用医療機器としての承認・認証を受けておらず、FDA（米国食品医薬品局）未承認、農林水産省動物用医療機器未認証です。",
    footerAiDisclosure:"⚠️ AI生成データの開示: 本データベースの治療プロトコル・症状・推奨検査の一部はAI支援で生成され獣医師レビューを経ています。エビデンスグレード（A/B/C/D）でデータ品質を可視化していますが、用量・薬品相互作用は処方前に必ず原典（Plumb's等）で再確認してください。",
    footerDeveloperHeading:"開発者",
    footerDatabaseHeading:"データベース",
    footerDbDiseases:"疾患データベース",
    footerDbSymptoms:"症状から調べる",
    footerDbDrugs:"動物用医薬品辞典",
    footerDbAnesthesia:"鎮静・麻酔プロトコル",
    footerLinksHeading:"リンク",
    footerLegalHeading:"法務",
    footerLegalTerms:"利用規約",
    footerLegalPrivacy:"プライバシーポリシー",
    footerLegalTokushoho:"特定商取引法に基づく表記",footerLegalCookies:"Cookie設定",
    footerCopyright:"© 2026 Equine Vet Synapse. All rights reserved.",
    footerPaypal:"PayPal: equinevet.owners@gmail.com",
    // Analyze button states
    analyzeSearchingDb:"データベース検索中...",
    diseasesFoundToast:"%n%件の疾患が見つかりました",
    diseasesNoneFoundToast:"該当疾患が見つかりませんでした。症状を追加してください。",
    // Admin
    adminBadgeTitle:"管理者モード — 全機能アンロック済み",
  },
  en:{
    skipLink:"Skip to main content",
    logoSub:"Clinical Decision Support for Veterinarians",
    navChecker:"Differential Dx",navDatabase:"Disease Database",navChat:"Clinical Chat",navDrugs:"Drug Dictionary",navAnesthesia:"Anesthesia",navEmergency:"🚨 Emergency",
    cardEmergency:"🚨 Emergency Protocols / Quick Reference",emergencyImportant:"⚠ Important:",emergencyDisclaimer:"Emergencies require simultaneous parallel actions. These protocols are standard references; actual execution requires experienced clinical judgment. Always verify drug doses and routes before administration.",
    emergencyTriggerSigns:"Recognize",emergencyKeyDrugs:"Key drugs",emergencyMonitoring:"Monitoring",emergencyStepsTitle:"Protocol",emergencyTimeTarget:"Time target",
    landingChatTitle:"Differential Diagnosis from Clinical Signs",
    heroTrustSpecies:"21 species — from dogs & cats to exotics",heroTrustRef:"Based on 190+ academic references",heroTrustTests:"Verified by 3,800+ automated tests",heroTrustOss:"Open-source development",
    landingChatHint:'Enter clinical signs to generate a differential diagnosis list.<br/><span style="font-size:.76rem;color:var(--gray-500)">e.g. "vomiting anorexia weight loss" "polyuria polydipsia lethargy"</span>',
    heroBadge:"Built by a practicing veterinarian — Clinical decision support",
    heroAudience:"A clinical tool for veterinarians and veterinary students",
    heroLead:"Instantly generate differential diagnosis lists from clinical signs.",
    heroCta:"Select a species to begin differential diagnosis",heroCtaDb:"Browse Disease Database",
    statDiseases:"Diseases",statSpecies:"Species",statSymptoms:"Symptoms",statDrugs:"Drugs",statProtocols:"Anesthesia",
    heroStatsAria:"Database statistics",
    heroCredit:'Developed by: <a href="https://www.minamisoma-vet.com/" target="_blank" rel="noopener noreferrer">Minamisoma Animal Clinic</a> — Kentaro Kamide, DVM',
    sponsorDesc:"Formulated by a veterinarian — Made in Japan — Passed racing lab tests",
    sponsorCta:"Details →",
    sponsorAria:"Sponsor: Equine & Canine Vet Nutrition (caninevet.jp) — opens in a new tab",
    selectSpecies:"Select Species",
    cardSymptoms:"&#9745; Select Symptoms",cardResults:"&#128202; Results",
    breedLabel:"Select breed (optional)",breedNone:"No breed selected",
    symptomSearchPh:"Search symptoms... (e.g. cough, vomiting, diarrhea)",
    analyzeBtn:"Search Differential Diagnoses",checkerGuide:'💡 <strong>How to use:</strong> Check symptoms from the list above, then press "Search Differential Diagnoses".<br/>More symptoms = better accuracy (3+ recommended).',
    labSectionTitle:"&#128300; Enter lab values (optional)",
    labCatRenal:"Renal",labCatHepatic:"Hepatic",labCatMetabolic:"Metabolic / Pancreas",labCatElectrolyte:"Electrolytes",labCatCBC:"CBC",labCatEndocrine:"Endocrine / Inflammation / Urine",
    labClear:"Clear lab values",
    labImport:"📷 Import from image/text",
    painScaleTitle:"&#x1F9D1;&#x200D;&#x2695;&#xFE0F; Pain assessment (CSU Pain Scale)",
    painScaleHint:"Select Colorado State University Canine Acute Pain Scale (0–4).",
    painDesc0:"Comfortable, relaxed, wagging tail",
    painDesc1:"Slightly restless, lip-licking",
    painDesc2:"Repositioning, whimpering, reduced appetite",
    painDesc3:"Vocalizing, immobile, aggressive when touched",
    painDesc4:"Lateral recumbency, screaming, rigid, unresponsive",
    resultsEmpty:'Select a species, check symptoms, and<br/>press "Search Differential Diagnoses"',
    resultsSelectSymptom:"Please select symptoms",
    selectSpeciesFirst:"Pick a species first to load its symptom checklist",
    selectSpeciesFirstBtn:"Choose a species",
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
    drugSearchPh:"Search drugs by generic or brand name... (e.g. Baytril, meloxicam)",
    drugBrandHit:"Brand",
    drugNoMatchHint:"You can search by generic name (enrofloxacin), brand name (Baytril), or Japanese name.",
    drugClearFilters:"Clear filters to show %n% matches",
    allCategories:"All Categories",allSpecies:"All Species",speciesAny:"Species (optional)",
    interactionCheckerTitle:"⚠️ Drug Interaction Checker",interactionCheckerDesc:"Check interactions when combining multiple drugs. Enter comma-separated drug names (lowercase Latin).",interactionCheckBtn:"Check",
    drugCompareTitle:"How VetDict compares to other veterinary drug references",
    drugCompareHint:"(click to expand)",
    drugCompareIntro:"A side-by-side look at VetDict, Plumb's Veterinary Drugs, and VIN (Veterinary Information Network) to help you pick the right tool for the job.",
    drugCompareColFeature:"Feature",
    drugCompareRowSource:"Primary sources",
    drugCompareVetdictSource:"Plumb's (9th ed.) / Papich (5th ed.) / BSAVA / Carpenter Formulary, etc.",
    drugCompareCompetitorSource1:"In-house editorial team with current pharmacology data",
    drugCompareCompetitorSource2:"Multiple textbooks + clinical insight from board-certified specialists",
    drugCompareRowFreq:"Update cadence",
    drugCompareVetdictFreq:"Periodic (manual updates by maintainer)",
    drugCompareCompetitorFreq1:"Real-time (new drugs and adverse-event data)",
    drugCompareCompetitorFreq2:"Continuous (forum discussion often leads the update)",
    drugCompareRowSpecies:"Species coverage",
    drugCompareVetdictSpecies:"21 species — strong on fish & exotics",
    drugCompareCompetitorSpecies1:"Major pets, equine, food animals",
    drugCompareCompetitorSpecies2:"Broad coverage across all domains",
    drugCompareRowInteraction:"Interaction checking",
    drugCompareVetdictInteraction:"Based on disease-DB notes and anesthesia contraindication rules",
    drugCompareCompetitorInteraction1:"Dedicated interaction simulator",
    drugCompareCompetitorInteraction2:"Search and forum-based consultation",
    drugCompareRowOwner:"Owner-facing materials",
    drugCompareVetdictOwner:"None (clinician-focused)",
    drugCompareCompetitorOwner1:"Multilingual client handouts included",
    drugCompareCompetitorOwner2:"Owner education site (Veterinary Partner)",
    drugCompareRowLang:"Languages",
    drugCompareVetdictLang:"Japanese & English",
    drugCompareCompetitorLang1:"English",
    drugCompareCompetitorLang2:"English (some machine translation)",
    drugCompareAnalysisTitle:"Honest analysis",
    drugComparePoint1Title:"Search accuracy & source credibility",
    drugComparePoint1Body:"VetDict is curated in Japanese by a practicing veterinarian on top of world-standard sources (Plumb's, BSAVA, etc.). Its strength is searching by the generic and brand names actually available in Japan. For pure academic currency on US-FDA approvals, the publisher-run tools (Plumb's latest edition) remain the gold standard.",
    drugComparePoint2Title:"Usability as a form of accuracy",
    drugComparePoint2Body:"In VetDict you can type a Japanese symptom like 「嘔吐」 and reach the differential and recommended drugs in two clicks. Information-dense tools like VIN can take longer to surface the specific dose you need right now.",
    drugComparePoint3Title:"Exotic & special-species coverage",
    drugComparePoint3Body:"Dosing data for hedgehogs, sugar gliders, fish and similar species is thin in mainstream drug handbooks. VetDict consolidates the essence of references like Carpenter's Formulary into a single Japanese-language interface — a unique advantage.",
    drugCompareConclTitle:"Recommendation: how to use them together",
    drugCompareConclDailyLabel:"Daily practice (VetDict):",
    drugCompareConclDailyBody:"Best for quickly answering 'what's the typical dose for this disease?' or 'what's the dose in this exotic species?' in Japanese.",
    drugCompareConclAdvLabel:"Complex cases / new drugs (Plumb's / VIN):",
    drugCompareConclAdvBody:"For multi-drug interaction concerns or the latest adverse-event evidence in the original language, consult Plumb's (paid) or the VIN specialist network.",
    drugCompareDisclaimer:"Note: Comparison reflects publicly available information on each service as of 2026 and represents general tendencies. Always verify against the primary source and product labeling before clinical decisions.",
    sponsorTagline:"Formulated by a veterinarian — Made in Japan — Passed racing lab tests",
    sponsorSpecies:"Supported species: Horse, Dog, Cat",
    sponsorEquine:"Equine Supplements",sponsorCanine:"Canine Supplements",
    footerDisclaimer:"Note: This service provides clinical decision support for veterinary professionals. It does not replace definitive diagnosis.",
    footerCredit:'Developed by: <a href="https://www.minamisoma-vet.com/" target="_blank" rel="noopener noreferrer">Minamisoma Animal Clinic</a> — Kentaro Kamide, DVM',
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
    networkErrorTimeout:"The request timed out.",
    networkErrorOffline:"You appear to be offline. Please check your connection.",
    networkErrorServer:"Server error.",
    networkErrorDetail:"Details: ",
    noDiseaseMatch:"No matching diseases",
    noDrugMatch:"No matching drugs",
    errorPrefix:"Error: ",
    overallAssessment:"Overall: ",
    commError:"A communication error occurred. Please check your network and retry.",
    noResponse:"Could not retrieve response",
    diseaseCount:"%filtered% / %total% shown",
    catLabels:{respiratory:"Respiratory",digestive:"Digestive",neurological:"Neurological",musculoskeletal:"Musculoskeletal",dermatological:"Dermatological",urinary:"Urinary",ophthalmological:"Ophthalmological",cardiovascular:"Cardiovascular",cardiac:"Cardiac",behavioral:"Behavioral",general:"General",skin:"Skin & Appearance",fins:"Fins",gills:"Gills",eyes:"Eyes",eye:"Eyes",ocular:"Ocular",ears:"Ears",eyes_ears:"Eyes & Ears",oral:"Oral",internal:"Internal & Systemic",developmental:"Developmental",limb:"Limbs",hoof:"Hoof",dental:"Dental",repository_exam:"Exam Findings",toxic:"Toxic",foal:"Foal",immune:"Immune",endocrine:"Endocrine",misc:"Miscellaneous",body:"Body & Shape",parasites:"Parasites",emergency:"Emergency",reproductive:"Reproductive",behavior:"Behavior",other:"Other"},
    sevLabels:{low:"Mild",moderate:"Moderate",high:"Severe",emergency:"Emergency"},
    dtDescription:"Description",dtPathophysiology:"Pathophysiology",dtCauses:"Causes",dtPrevention:"Prevention",dtTreatment:"Treatment",dtPrognosis:"Prognosis",
    dtClinicalSigns:"Clinical Signs",dtDiagnosis:"Diagnosis",
    dtMatchedSymptoms:"Matched Symptoms",dtRecommendedTests:"Recommended Tests",dtRecTestList:"Recommended Tests:",
    dtSymptoms:"Symptoms",
    dtContraindications:"Contraindications",dtRoutes:"Routes",dtFormulations:"Formulations",dtInteractions:"Drug Interactions",dtSpeciesInfo:"Species Information:",dtMechanism:"Mechanism of Action",dtSideEffects:"Common Side Effects",
    safe:"Safe",contraindicated:"Contraindicated",dosageLabel:"Dosage: ",
    sponsorVetLabel:"Formulated by a veterinarian — Made in Japan — Passed racing lab tests",
    productDetails:"Product details \u2192",
    speciesCardDisease:"diseases",speciesCardDrug:"drugs",
    quickNavDiseaseDb:"Disease Database",quickNavDrugs:"Drug Dictionary",quickNavChat:"Clinical Chat",quickNavAnesthesia:"Anesthesia",quickNavChecker:"Differential Dx",quickNavEmergency:"Emergency",
    quickNavPrompt:"Select a feature",
    quickNavDefault:"Browse databases directly",
    emptyStateSelectSpecies:"Select a species",
    emptyStateDiseaseDb:"Select a species to view its disease database",
    emptyStateDiseaseDbHint:"Or type a disease name in the search box above to search across all 21 species",
    xspeciesSearching:"Searching all species…",
    xspeciesResultsLabel:"Cross-species results (no species selection needed)",
    emptyStateDrugs:"The drug dictionary shows all drugs regardless of species",
    emptyStateAnesthesia:"Select a species to view sedation & anesthesia protocols",
    emptyStateSelectBtn:"Select a species",
    breadcrumbHome:"Home",breadcrumbNoSpecies:"No species selected",
    kbdShortcutsHint:"Keyboard: Ctrl+1-5 to switch tabs",
    globalSearchPh:"Search diseases & drugs...",
    menuOpen:"Open menu",menuClose:"Close menu",
    removeLabel:"Remove %s%",
    painLabels:["No Pain","Mild","Moderate","Severe","Excruciating"],
    painScoreLabel:"Score",
    showMoreItems:"Show more (%n% remaining)",
    metabSupport:"Metabolic Support",aminoAcid:"Amino Acids",digestSupport:"Digestive Support",jointSupport:"Joint & Mobility",
    mdCombinations:"Possible Disease Combinations",mdAmbiguous:"Ambiguous Symptoms Detected",mdConfidence:"Confidence Analysis",mdClarifying:"Clarifying Questions",mdGuidance:"Diagnostic Guidance",mdRecommendations:"Recommendations",mdActive:"Multi-Disease Mode Active",mdAnalyzing:"Analyzing multi-disease combinations...",
    resultsDisclaimer:"These results are for clinical reference. Final diagnosis and treatment decisions should integrate clinical findings and diagnostic results.",
    feedbackQuestion:"Was this differential diagnosis list clinically useful?",
    feedbackYes:"Helpful",
    feedbackNo:"Could improve",
    feedbackThanks:"Thank you for your feedback.",
    shareResults:"Share results",shareCopy:"Copy",shareCopied:"Copied!",
    husbandryTitle:"Care Environment Guide",husbandryTemp:"Temperature",husbandryHumidity:"Humidity",husbandryHousing:"Housing",husbandryDiet:"Diet",husbandryEnrichment:"Enrichment",husbandrySocial:"Socialization",husbandryNotes:"Additional Notes",husbandryLoading:"Loading care information...",husbandryError:"Failed to load care information",
    offlineBanner:"You are offline — Some features may be limited",
    mobileNavChecker:"Dx",mobileNavDatabase:"Diseases",mobileNavChat:"Chat",mobileNavDrugs:"Drugs",mobileNavAnesthesia:"Anesth.",mobileNavEmergency:"ER",
    sortByConfidence:"By Confidence",sortBySeverity:"By Severity",sortByDefault:"Default",
    speciesFilterPh:"Filter species...",
    stepSpecies:"Species",stepSymptoms:"Symptoms",stepResults:"Results",
    // Header / aria-labels
    ariaHomeLink:"VetDict home",
    ariaSearchInput:"Search diseases & drugs",
    ariaSpeciesFilter:"Filter by species",
    titleSpeciesFilter:"Filter by species",
    ariaCategoryFilter:"Filter by category",
    titleCategoryFilter:"Filter by symptom category",
    ariaCloseFilter:"Close",
    ariaMainNav:"Main navigation",
    ariaLangToggle:"Display language",
    ariaClearSearch:"Clear search",
    ariaSpeciesFilterDialog:"Species filter",
    ariaCategoryFilterDialog:"Symptom category filter",
    speciesFilterTitle:"Filter by species",
    categoryFilterTitle:"Filter by symptom category",
    filterReset:"Reset",
    // Cookie consent
    cookieConsentRegion:"Cookie notice",
    cookieConsentText:"This site uses Google Analytics to improve usability. Your choice is saved in localStorage and can be changed later.",
    cookiePrivacyLink:"Privacy policy",
    cookieAccept:"Accept",
    cookieReject:"Reject",
    cookieDismiss:"Decide later",
    cookieDismissAria:"Close without accepting",
    dashboardOpen:"Statistics Dashboard",
    dashboardOpenAria:"Open statistics dashboard",
    helpButton:"Quick Guide",
    helpGuideAria:"Open quick guide",
    helpTitle:"VetDict — Quick Guide",
    helpClose:"Close",
    // Pricing
    pricingSubtitle:"Open beta — Veterinarians and veterinary students get full access for free",
    pricingBadge:"Open Beta",
    pricingHeader:"All features free",
    pricingPeriodOriginal:"¥980/month",
    pricingFeature1:"Differential diagnosis list (all 21 species)",
    pricingFeature2:"Disease database <strong>6,400+ diseases</strong>",
    pricingFeature3:"Drug dictionary <strong>600+ drugs</strong> with species-specific dosing",
    pricingFeature4:"Clinical chat <strong>unlimited</strong>",
    pricingFeature5:"Lab values & pain scale input",
    pricingFeature6:"All 21 species (incl. exotics)",
    pricingCtaText:"All features currently free",
    pricingNote:"After official launch, some features will move to a paid plan (¥980/month)",
    signupHeading:"🔔 Get notified at launch with an <span style=\"color:var(--green)\">early-bird discount</span>",
    signupSubtext:"Exclusive benefits for veterinarians who sign up during beta",
    signupEmailPh:"Email address",
    signupBtn:"Sign up free",
    signupBtnSubmitting:"Signing up...",
    signupBtnDone:"Signed up",
    signupSpamNote:"No spam. Unsubscribe anytime.",
    signupInvalidEmail:"Please enter a valid email address",
    signupSuccess:"Sign-up complete! We'll notify you at launch.",
    signupGenericError:"An error occurred",
    signupNetworkError:"Network error. Please try again later.",
    // Footer / share
    shareSection:"Spread the word",
    shareXLabel:"Share on X (Twitter)",
    shareFbLabel:"Share on Facebook",
    shareLineLabel:"Send via LINE",
    sharePostX:"X (Twitter)",sharePostXSub:"Post",
    sharePostFb:"Facebook",sharePostFbSub:"Share",
    sharePostLine:"LINE",sharePostLineSub:"Send",
    footerRegulatory:"This service is a clinical decision support tool for veterinarians and veterinary students. AI analysis is a reference for differential diagnosis; definitive diagnosis and treatment decisions require integration with clinical findings and diagnostic results. This service is not approved or certified as a medical device or veterinary medical device — not FDA-approved (US) and not certified by Japan's Ministry of Agriculture, Forestry and Fisheries.",
    footerAiDisclosure:"⚠️ AI-Generated Data Disclosure: Portions of treatment protocols, symptoms, and recommended diagnostics in this database are AI-assisted and reviewed by veterinarians. Evidence grades (A/B/C/D) indicate data quality, but always verify doses and drug interactions against authoritative sources (Plumb's, etc.) before prescribing.",
    footerDeveloperHeading:"Developer",
    footerDatabaseHeading:"Database",
    footerDbDiseases:"Disease Database",
    footerDbSymptoms:"Browse by Symptom",
    footerDbDrugs:"Veterinary Drug Dictionary",
    footerDbAnesthesia:"Anesthesia Protocols",
    footerLinksHeading:"Links",
    footerLegalHeading:"Legal",
    footerLegalTerms:"Terms of Use",
    footerLegalPrivacy:"Privacy Policy",
    footerLegalTokushoho:"Specified Commercial Transactions Act Disclosure",footerLegalCookies:"Cookie settings",
    footerCopyright:"© 2026 Equine Vet Synapse. All rights reserved.",
    footerPaypal:"PayPal: equinevet.owners@gmail.com",
    // Analyze button states
    analyzeSearchingDb:"Searching database...",
    diseasesFoundToast:"Found %n% diseases",
    diseasesNoneFoundToast:"No matching diseases found. Try adding more symptoms.",
    // Admin
    adminBadgeTitle:"Admin mode — all features unlocked",
  }
};

function t(key){return (I18N[currentLang]&&I18N[currentLang][key])||key;}

function haptic(ms){try{if(navigator.vibrate)navigator.vibrate(ms||10);}catch(e){}}

function fetchWithTimeout(url,opts={},timeoutMs=10000){
  const ctrl=new AbortController();
  const timer=setTimeout(()=>ctrl.abort(),timeoutMs);
  return fetch(url,{...opts,signal:ctrl.signal}).finally(()=>clearTimeout(timer));
}

/* Classify a fetch failure for user-facing messaging.
   Returns {title, detail} pulled from current i18n. */
function describeFetchError(err){
  const msg=String(err&&err.message?err.message:err||"");
  let title=t("networkError");
  let detail="";
  if(typeof navigator!=="undefined"&&navigator.onLine===false){
    title=t("networkErrorOffline");
  }else if(err&&(err.name==="AbortError"||/aborted|timeout/i.test(msg))){
    title=t("networkErrorTimeout");
  }else if(/^HTTP 5\d{2}/.test(msg)){
    title=t("networkErrorServer");
    detail=msg;
  }else if(/^HTTP 4\d{2}/.test(msg)){
    title=t("networkErrorServer");
    detail=msg;
  }else if(msg){
    detail=msg;
  }
  return {title,detail};
}

function applyLanguage(){
  document.documentElement.lang=currentLang;
  document.title=currentLang==="ja"
    ?"VetDict — 獣医師のための臨床意思決定支援ツール | 鑑別診断・疾患DB・薬品辞書"
    :"VetDict — Clinical Decision Support for Veterinarians | Differential Diagnosis, Disease DB, Drug Dictionary";
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
  // Update data-i18n-aria (aria-label)
  document.querySelectorAll("[data-i18n-aria]").forEach(el=>{
    const key=el.getAttribute("data-i18n-aria");
    const val=t(key);
    if(val&&val!==key)el.setAttribute("aria-label",val);
  });
  // Update data-i18n-title (title attribute)
  document.querySelectorAll("[data-i18n-title]").forEach(el=>{
    const key=el.getAttribute("data-i18n-title");
    const val=t(key);
    if(val&&val!==key)el.setAttribute("title",val);
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
  updateBreadcrumb();
  const mbn=document.getElementById("mobileBottomNav");
  if(mbn){
    mbn.setAttribute("aria-label",currentLang==="ja"?"メインナビゲーション":"Main navigation");
    const views=["checker","database","chat","drugs","anesthesia","emergency"];
    mbn.querySelectorAll("button[data-view]").forEach((btn,i)=>{const v=views[i];if(!v)return;const sp=btn.querySelector("span");if(sp)sp.textContent=t("mobileNav"+v.charAt(0).toUpperCase()+v.slice(1));});
  }
  const ob=document.getElementById("offlineBanner");
  if(ob)ob.textContent=t("offlineBanner");
  /* Re-attach chat quick suggestion buttons — applyLanguage rewrites #chatWelcome's
     innerHTML via data-i18n-html which wipes the dynamically added suggestion row. */
  if(typeof addChatQuickSuggestions==="function")addChatQuickSuggestions();
  // Refresh pain-scale labels (array-keyed i18n)
  const _painLabels=t("painLabels");
  if(Array.isArray(_painLabels)){
    document.querySelectorAll(".pain-label-text[data-pain-label]").forEach(el=>{
      const i=parseInt(el.getAttribute("data-pain-label"),10);
      if(_painLabels[i])el.textContent=_painLabels[i];
    });
    // Refresh the selected-score badge if visible
    const _badge=document.getElementById("painScaleBadge");
    const _checked=document.querySelector('#painScaleOptions input[name="painScore"]:checked');
    if(_badge&&_checked){
      const _i=parseInt(_checked.value,10);
      const _scoreLabel=t("painScoreLabel")||"Score";
      if(_painLabels[_i])_badge.textContent=`${_scoreLabel} ${_i}: ${_painLabels[_i]}`;
    }
  }
}

function setupLanguageToggle(){
  const toggle=document.querySelector(".lang-toggle");
  if(!toggle){debugWarn(".lang-toggle element not found");return;}
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

let currentSpecies=null,currentView="checker",selectedSymptoms=new Set(),symptomData=[],allDiseases=[],diseaseFilter="",currentBreed="";
// Species used for the free-text chat. Seeded by an explicit species selection
// and updated from each response's detected species so multi-turn follow-ups
// (which may omit the species word) stay on the same animal.
let chatSpecies="";
let symptomRequestId=0,diseaseRequestId=0,breedRequestId=0;
let symptomSortMode="category";

/* ---- Sticky-chrome scroll offset -----------------------------------------
   Every in-page navigation (tabs, hamburger, mobile bottom nav, breadcrumbs,
   deep links, keyboard shortcuts, skip-link, hash routing) ultimately scrolls a
   target to the top of the scrollport. The sticky .header + .breadcrumb-bar
   overlay that top edge, so without an offset the target's own heading and
   search box land *underneath* the header and the view looks like it jumped to
   the wrong place. CSS handles the offset via --sticky-offset (scroll-margin-top
   on targets + scroll-padding-top for native anchors); the real height differs
   per breakpoint (header 52/46px, breadcrumb 30/28px, breadcrumb sometimes
   hidden), so measure it live instead of hardcoding. */
function _syncStickyOffset(){
  try{
    let off=0;
    for(const sel of [".header",".breadcrumb-bar"]){
      const el=document.querySelector(sel);
      if(!el)continue;
      const cs=getComputedStyle(el);
      /* Only chrome that actually overlays the scrollport counts. */
      if(cs.display==="none"||cs.visibility==="hidden")continue;
      if(cs.position!=="sticky"&&cs.position!=="fixed")continue;
      off+=el.getBoundingClientRect().height;
    }
    /* +10px so the target does not sit flush against the header. */
    const px=off>0?Math.round(off)+10:112;
    document.documentElement.style.setProperty("--sticky-offset",px+"px");
  }catch(_){/* keep the CSS fallback */}
}
window.addEventListener("resize",_syncStickyOffset,{passive:true});
window.addEventListener("orientationchange",_syncStickyOffset,{passive:true});
/* Measured again on first paint AND before each navigation scroll (see
   switchView): the breadcrumb bar is display:none until a view becomes active,
   so a DOMContentLoaded-only measurement misses its height permanently. */
document.addEventListener("DOMContentLoaded",_syncStickyOffset);

/* Scroll a navigation target to just below the sticky chrome.
   Replaces bare el.scrollIntoView({block:"start"}) at every in-page navigation
   site. Two failures made the old calls land in the wrong place:
     1. No sticky-chrome offset — the target's heading/search box ended up behind
        the header (measured 47-50px buried on both mobile and desktop).
     2. Async clamping — panels fill in after the click (drug dictionary grows the
        document to ~50,000px, anaesthesia ~20,000px). While the panel is still
        empty the document is short, so the browser clamps the scroll to the old
        scrollHeight; when the content arrives the target is far off-screen
        (measured: drug panel 3,250px below the viewport on first open). So
        re-assert the position while the document is still growing.
   Uses window.scrollTo with an explicitly computed y (programmatic scrollTo is
   not affected by scroll-padding-top, so the offset is applied once, not twice). */
function scrollToAnchor(el,opts){
  if(!el)return;
  opts=opts||{};
  _syncStickyOffset();
  const reduced=window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const offset=()=>parseInt(getComputedStyle(document.documentElement).getPropertyValue("--sticky-offset"),10)||112;
  const wantY=()=>Math.max(0,Math.round(el.getBoundingClientRect().top+window.scrollY-offset()));
  const first=wantY();
  /* Distance-aware motion. The content panels sit ~3,400px below the landing
     sections, so animating a tab switch smoothly meant a ~1.5s flight past the
     hero, species grid and every other section — read as "it scrolled to a
     random place / to the bottom". Worse, a long animation can be starved by the
     panel's own render (the drug dictionary lays out ~600 rows) and stall
     part-way. Jumps beyond ~1.2 viewports are therefore instant: predictable and
     interruption-proof. Short, local moves keep smooth motion, which genuinely
     helps orientation. */
  const far=Math.abs(first-window.scrollY)>window.innerHeight*1.2;
  const behavior=(reduced||opts.instant||far)?"auto":"smooth";
  window.scrollTo({top:first,behavior:behavior});
  if(opts.settle===false)return;
  /* Re-anchor while the layout is still settling.
     Two independent shifts move the target after the click, and both were
     measured on the live page:
       - content arriving INSIDE the panel (drug dictionary grows the document
         from 7k to 50k px, and takes >1.5s to lay out ~600 rows), and
       - the layout ABOVE the panel changing height (~28px), which silently
         re-anchored every view about 18px behind the sticky header.
     Watching the target's own document offset catches both causes without
     having to know which element moved. Runs on rAF (cheap: one rect read per
     frame), bounded, and yields immediately to the user's own scrolling. */
  let cancelled=false,raf=0;
  const evs=["wheel","touchstart","keydown"];
  function release(){
    if(cancelled)return;
    cancelled=true;
    if(raf)cancelAnimationFrame(raf);
    evs.forEach(ev=>window.removeEventListener(ev,release));
  }
  evs.forEach(ev=>window.addEventListener(ev,release,{passive:true}));
  const docTopOf=()=>el.getBoundingClientRect().top+window.scrollY;
  const now=()=>(window.performance&&performance.now?performance.now():Date.now());
  const doc=document.documentElement;
  let lastDocTop=docTopOf(),lastY=null,lastH=doc.scrollHeight,stillFrames=0;
  /* Generous window: a slow panel render (drug dictionary on a phone-class
     device) can take several seconds to finish laying out, and the correction is
     worthless if it expires first. The early-exit below keeps the common case to
     a couple of frames. */
  const started=now();
  const deadline=started+12000;
  /* An empty panel is trivially "settled" the frame after the scroll, so exiting
     on convergence alone released the watcher before the panel's content had
     even been fetched — the very shift it exists to absorb. Keep watching for at
     least this long so an async render is always covered. */
  const minWatchMs=2000;
  const settle=()=>{
    if(cancelled)return;
    const y=Math.round(window.scrollY);
    const docTop=docTopOf();
    const want=Math.max(0,Math.round(docTop-offset()));
    const moved=Math.abs(docTop-lastDocTop)>1;
    const grew=doc.scrollHeight!==lastH;
    /* "Still" = neither the scroll position nor the layout changed since the
       last frame, i.e. any smooth animation has finished. Only then is an
       off-target position a real error rather than an animation in progress —
       correcting mid-animation would cancel the user's smooth scroll. */
    const still=(lastY!==null&&y===lastY&&!moved&&!grew);
    stillFrames=still?stillFrames+1:0;
    if(Math.abs(want-y)>4&&(moved||stillFrames>=2)){
      window.scrollTo({top:want,behavior:"auto"});
      lastY=null;stillFrames=0;
    }else{
      lastY=y;
    }
    lastDocTop=docTop;lastH=doc.scrollHeight;
    /* Done once we are on target, nothing has moved for a few frames, and the
       minimum watch window has elapsed (so a late render cannot slip through). */
    const elapsed=now()-started;
    if(elapsed>=minWatchMs&&stillFrames>=6&&Math.abs(want-Math.round(window.scrollY))<=4)return release();
    if(now()<deadline)raf=requestAnimationFrame(settle);
    else release();
  };
  raf=requestAnimationFrame(settle);
}

/* Keep a reference element pinned to its on-screen position across a DOM update
   that changes document height.

   The disease list re-renders on every debounced keystroke. On mobile the list is
   in normal document flow (.disease-db-list is max-height:none / overflow:visible
   below the tablet breakpoint), so the *page* scrolls, not the list. Filtering
   from ~100 rows down to a handful therefore collapses the document by thousands
   of pixels; the browser clamps scrollY, and the open soft keyboard re-scrolls to
   the caret — so the page lurched up and down while typing ("いきなり上下"). On
   desktop the list is its own scroll container (fixed max-height), so the height
   never changes and delta is ~0 — this is a harmless no-op there.

   Reading the rect after the synchronous render forces a layout, so the
   correction lands in the same frame with no visible flash, and because it is a
   single synchronous adjustment per render it cannot oscillate. */
function _renderPinningAnchor(anchorEl, render) {
  if (!anchorEl || !anchorEl.isConnected) {
    render();
    return;
  }
  const before = anchorEl.getBoundingClientRect().top;
  render();
  const after = anchorEl.getBoundingClientRect().top;
  const delta = after - before;
  if (Math.abs(delta) > 1) window.scrollBy(0, delta);
}

/* In-page anchor links (skip-link, "#speciesSection", reference jumps).
   The browser's native jump uses html{scroll-padding-top}, which is only as
   fresh as the last measurement — on a first click the breadcrumb bar has not
   been shown yet, so the skip-link landed 38px under the header. Routing these
   clicks through scrollToAnchor() re-measures at click time and re-anchors after
   the layout settles, so anchor links land in the same correct place as tab
   navigation. View hashes (#database, #chat, …) are deliberately left alone:
   those are routed to switchView() by the hash router. */
document.addEventListener("click",function(e){
  const a=e.target.closest?e.target.closest('a[href^="#"]'):null;
  if(!a)return;
  const href=a.getAttribute("href")||"";
  if(href==="#"||href.length<2)return;
  const id=decodeURIComponent(href.slice(1));
  if(["checker","database","chat","drugs","anesthesia","emergency"].includes(id))return;
  const target=document.getElementById(id);
  if(!target)return;
  e.preventDefault();
  /* Keep the URL bookmarkable, and move focus so the jump is announced to
     screen readers rather than being a silent visual-only scroll. */
  try{history.pushState(null,null,href);}catch(_){/* ignore */}
  if(!target.hasAttribute("tabindex"))target.setAttribute("tabindex","-1");
  try{target.focus({preventScroll:true});}catch(_){target.focus();}
  scrollToAnchor(target);
});

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
    if(diseaseSearch)diseaseSearch.addEventListener("input",debounce(()=>{diseaseDisplayLimit=100;_renderPinningAnchor(diseaseSearch,renderDiseaseDb);},200));
    setupGlobalSearch();
    // Restore view from URL hash (silent: don't auto-focus inputs on initial load —
    // would pop the mobile keyboard for users landing on /#chat etc.)
    const hash=location.hash.replace("#","");
    if(hash&&["checker","database","chat","drugs","anesthesia","emergency"].includes(hash))switchView(hash,{silent:true});
    // Handle ?species= query param (from sitemap/SEO links)
    const spParam=new URLSearchParams(location.search).get("species");
    if(spParam&&SPECIES_ICONS[spParam])selectSpecies(spParam);
    else renderSymptomEmptyState();
    // Search clear buttons (replaces inline onclick)
    document.querySelectorAll('[data-action="clear-search"]').forEach(btn=>{
      btn.addEventListener("click",()=>{const inp=btn.previousElementSibling;inp.value='';inp.dispatchEvent(new Event('input'));inp.focus();});
    });
    // Escape clears any focused search input (a11y / keyboard convenience)
    document.querySelectorAll('.symptom-search input[type="search"]').forEach(inp=>{
      inp.addEventListener("keydown",e=>{
        if(e.key==="Escape"&&inp.value){e.preventDefault();inp.value="";inp.dispatchEvent(new Event("input"));}
      });
    });
    // Symptom search Enter: add first visible match (productivity shortcut for clinicians)
    if(symptomSearch){
      symptomSearch.addEventListener("keydown",e=>{
        if(e.key!=="Enter"||e.isComposing)return;
        e.preventDefault();
        const list=document.getElementById("symptomList");
        const first=list&&list.querySelector('.symptom-item[aria-checked="false"]');
        if(first){
          toggleSymptom(first.dataset.id);
          symptomSearch.value="";
          symptomSearch.dispatchEvent(new Event("input"));
          symptomSearch.focus();
        }
      });
    }
    // Clear lab values button
    const clearLabBtn=document.getElementById("clearLabBtn");
    if(clearLabBtn)clearLabBtn.addEventListener("click",clearLabValues);
    // Lab import (OCR / text paste) button
    const labImportBtn=document.getElementById("labImportBtn");
    if(labImportBtn)labImportBtn.addEventListener("click",openLabImportModal);
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
    ["diseaseDbList","drugList","anesthesiaList","emergencyList"].forEach(id=>{
      const el=document.getElementById(id);
      if(el&&!el.dataset.handlersAttached){el.dataset.handlersAttached="1";_attachDbItemHandlers(el);}
    });
    /* Chat containers: candidate cards embed drug links (renderMentionedDrugs) and
       "open in disease DB" buttons, but these containers never had a delegated
       handler — the dotted-underline drug links fell through to a bare #drugs hash
       jump that landed at the top of the drugs tab instead of on the drug itself.
       Delegation attaches once per container (innerHTML resets don't detach it). */
    ["chatMessages","landingChatMessages","guidedMessages"].forEach(id=>{
      const el=document.getElementById(id);
      if(el&&!el.dataset.chatNavAttached){el.dataset.chatNavAttached="1";_attachChatNavHandlers(el);}
    });
    /* Hero CTA: in-app database tab navigation */
    const heroDbBtn=document.querySelector(".hero-btn.secondary");
    if(heroDbBtn){
      heroDbBtn.addEventListener("click",e=>{
        e.preventDefault();
        switchView("database");
        const target=_navLandingTarget("database");
        if(target)scrollToAnchor(target);
      });
    }
    /* Hero stats: clickable navigation */
    setupHeroStats();
    /* Dashboard modal trigger */
    const dashBtn=document.getElementById("dashboardBtn");
    if(dashBtn)dashBtn.addEventListener("click",openDashboard);
    /* Help/Tour modal trigger */
    const helpBtn=document.getElementById("helpGuideBtn");
    if(helpBtn)helpBtn.addEventListener("click",openHelpGuide);
    /* Breadcrumb bar below header */
    updateBreadcrumb();
    /* Keyboard shortcuts for tab switching */
    setupKeyboardShortcuts();
    /* Mobile bottom tab bar */
    setupMobileBottomNav();
    /* First-visit nudge to select a species */
    setupFirstVisitCoach();
    /* Swipe gesture for tab switching */
    setupSwipeGesture();
    /* Offline indicator */
    setupOfflineIndicator();
    /* Returning user welcome */
    showReturningUserBanner();
    /* Global keyboard shortcuts */
    document.addEventListener("keydown",e=>{
      if(e.target.matches("input,textarea,select,[contenteditable]"))return;
      if(e.key==="Escape"){
        const kb=document.getElementById("kbShortcutsPanel");
        if(kb&&kb.classList.contains("visible")){_kbPanelClose();return;}
        const spPanel=document.getElementById("speciesFilterPanel");
        if(spPanel&&spPanel.style.display!=="none"){
          spPanel.style.display="none";
          const trig=document.getElementById("searchFilterBtn");
          if(trig){trig.setAttribute("aria-expanded","false");trig.focus();}
          return;
        }
        const catPanel=document.getElementById("categoryFilterPanel");
        if(catPanel&&catPanel.style.display!=="none"){
          catPanel.style.display="none";
          const trig=document.getElementById("categoryFilterBtn");
          if(trig){trig.setAttribute("aria-expanded","false");trig.focus();}
          return;
        }
        const open=document.querySelector(".disease-detail.open");
        if(open){const item=open.closest(".disease-db-item");if(item)toggleDbItem(item);}
        return;
      }
      if(e.key==="?"){toggleKbShortcuts();return;}
      if(e.key==="/"&&!e.ctrlKey&&!e.metaKey){e.preventDefault();const gs=document.getElementById("globalSearch");if(gs){gs.focus();gs.select();}return;}
      if(e.key>="1"&&e.key<="6"&&!e.ctrlKey&&!e.metaKey&&!e.altKey){
        const views=["checker","database","chat","drugs","anesthesia","emergency"];
        switchView(views[parseInt(e.key,10)-1]);return;
      }
    });
    const kbBtn=document.getElementById("kbHintBtn");
    if(kbBtn)kbBtn.addEventListener("click",toggleKbShortcuts);
  }catch(e){
    debugError("Error in DOMContentLoaded:",e);
  }
});

function setupHeroStats(){
  const mapping={statDiseases:"database",statDrugs:"drugs",statProtocols:"anesthesia"};
  Object.entries(mapping).forEach(([id,view])=>{
    const stat=document.getElementById(id);
    if(!stat)return;
    const wrapper=stat.closest(".hero-stat");
    if(!wrapper)return;
    wrapper.classList.add("hero-stat-clickable");
    wrapper.setAttribute("role","button");
    wrapper.setAttribute("tabindex","0");
    wrapper.addEventListener("click",()=>{
      switchView(view);
      const target=_navLandingTarget(view);
      if(target)scrollToAnchor(target);
    });
    wrapper.addEventListener("keydown",e=>{
      if(e.key==="Enter"||e.key===" "){e.preventDefault();wrapper.click();}
    });
  });
}

let globalSearchSpeciesFilter=null;
let globalSearchTypeFilter=null;
let globalSearchReqId=0;

function saveRecentSearch(type,name,nameJa){
  try{
    let recent=JSON.parse(localStorage.getItem("vetdict-recent-searches")||"[]");
    recent=recent.filter(r=>r.name!==name);
    recent.unshift({type,name,name_ja:nameJa,ts:Date.now()});
    if(recent.length>8)recent.length=8;
    localStorage.setItem("vetdict-recent-searches",JSON.stringify(recent));
  }catch(e){}
}
function getRecentSearches(){
  try{return JSON.parse(localStorage.getItem("vetdict-recent-searches")||"[]");}catch(e){return[];}
}
function showRecentSearches(results){
  const recent=getRecentSearches();
  if(!recent.length){results.style.display="none";return;}
  const title=currentLang==="ja"?"最近の検索":"Recent searches";
  results.innerHTML=`<div class="search-recent-title" style="padding:8px 14px;font-size:.72rem;color:var(--gray-400);font-weight:600;border-bottom:1px solid var(--gray-100)">${title}</div>`+
    recent.map(m=>{
      const icon=m.type==="disease"?"\u{1F4D6}":"\u{1F48A}";
      const label=currentLang==="ja"?(m.name_ja||m.name):(m.name||m.name_ja);
      return`<div class="search-result-item" role="option" data-type="${m.type}" data-name="${escapeHtml(m.name||"")}">${icon} ${escapeHtml(label)}</div>`;
    }).join("");
  results.style.display="block";
}

function setupGlobalSearch(){
  const input=document.getElementById("globalSearch");
  const results=document.getElementById("globalSearchResults");
  if(!input||!results)return;
  /* Keep aria-expanded in sync with dropdown visibility (WAI-ARIA combobox pattern). */
  new MutationObserver(()=>{
    const open=results.style.display!=="none"&&!!results.innerHTML.trim();
    input.setAttribute("aria-expanded",open?"true":"false");
  }).observe(results,{attributes:true,attributeFilter:["style"],childList:true,subtree:false});
  let debounceTimer=null;
  function runSearch(){
    clearTimeout(debounceTimer);
    const q=input.value.trim().toLowerCase();
    if(q.length<2){
      if(document.activeElement===input)showRecentSearches(results);
      else{results.style.display="none";results.innerHTML="";}
      return;
    }
    const reqId=++globalSearchReqId;
    function renderMatches(matches){
      if(reqId!==globalSearchReqId)return;
      if(matches.length===0){results.innerHTML=`<div class="search-result-item" style="color:var(--gray-500)">${t("noDiseaseMatch")}</div>`;results.style.display="block";return;}
      results.innerHTML=matches.slice(0,15).map(m=>{
        const icon=m.type==="disease"?"\u{1F4D6}":"\u{1F48A}";
        const label=currentLang==="ja"?(m.name_ja||m.name):(m.name||m.name_ja);
        const sub=currentLang==="ja"?(m.name||""):(m.name_ja||"");
        const sp=m.species?SPECIES.find(s=>s.id===m.species):null;
        const spTag=sp?`<span class="search-result-species">${SPECIES_ICONS[m.species]||""} ${escapeHtml(currentLang==="ja"?sp.name:sp.nameEn)}</span>`:"";
        const typeLabel=m.type==="disease"?(currentLang==="ja"?"疾患":"Disease"):(currentLang==="ja"?"薬品":"Drug");
        return`<div class="search-result-item" role="option" data-type="${m.type}" data-name="${escapeHtml(m.name||m.name_ja||"")}" data-name-ja="${escapeHtml(m.name_ja||"")}" data-species="${escapeHtml(m.species||"")}">${icon} <strong>${escapeHtml(label)}</strong>${sub?` <span style="color:var(--gray-400);font-size:.78rem">${escapeHtml(sub)}</span>`:""}${spTag} <span class="search-result-type">${typeLabel}</span></div>`;
      }).join("")+(matches.length>15?`<div class="search-result-item" style="color:var(--gray-400);font-size:.78rem;text-align:center">${currentLang==="ja"?`他${matches.length-15}件`:`${matches.length-15} more...`}</div>`:"");
      results.style.display="block";
    }
    debounceTimer=setTimeout(()=>{
      const matches=[];
      const seen=new Set();
      if(globalSearchTypeFilter!=="drug"){
        allDiseases.forEach(d=>{
          const name=(d.name||"").toLowerCase();
          const nameJa=(d.name_ja||"").toLowerCase();
          if(name.includes(q)||nameJa.includes(q)){const key="d:"+(d.name||d.name_ja||"")+":"+(currentSpecies||"");if(!seen.has(key)){seen.add(key);matches.push({type:"disease",name:d.name,name_ja:d.name_ja,species:currentSpecies||""});}}
        });
      }
      if(globalSearchTypeFilter!=="disease"){
        allDrugs.forEach(d=>{
          if(globalSearchSpeciesFilter&&d.species_info&&!d.species_info[globalSearchSpeciesFilter])return;
          const name=(d.name||"").toLowerCase();
          const nameJa=(d.name_ja||"").toLowerCase();
          if(name.includes(q)||nameJa.includes(q)){matches.push({type:"drug",name:d.name,name_ja:d.name_ja});}
        });
      }
      renderMatches(matches);
      /* 全種横断: 動物種を選ばなくても全21種から疾患をヒットさせる（ローカルに無い種の疾患を補完） */
      if(globalSearchTypeFilter!=="drug"){
        const spFilter=globalSearchSpeciesFilter?"&species="+encodeURIComponent(globalSearchSpeciesFilter):"";
        fetchWithTimeout(`/api/diseases?q=${encodeURIComponent(q)}&limit=20${spFilter}`).then(r=>r.json()).then(data=>{
          if(reqId!==globalSearchReqId)return;
          const extra=(data&&data.diseases)||[];
          extra.forEach(d=>{
            const key="d:"+(d.name||d.name_ja||"")+":"+(d.species||"");
            if(seen.has(key))return;seen.add(key);
            matches.push({type:"disease",name:d.name,name_ja:d.name_ja,species:d.species||""});
          });
          /* 疾患を先頭に並べ替え（横断結果を見つけやすく） */
          matches.sort((a,b)=>(a.type==="disease"?0:1)-(b.type==="disease"?0:1));
          renderMatches(matches);
        }).catch(err=>{debugWarn("global cross-species search failed:",err);});
      }
    },200);
  }
  input.addEventListener("input",runSearch);
  input.addEventListener("focus",()=>{if(input.value.trim().length<2)showRecentSearches(results);});
  results.addEventListener("click",e=>{
    const item=e.target.closest(".search-result-item");
    if(!item||!item.dataset.type)return;
    saveRecentSearch(item.dataset.type,item.dataset.name,item.dataset.nameJa||"");
    if(item.dataset.type==="disease"){
      const sp=item.dataset.species||"";
      if(sp&&sp!==currentSpecies)openDiseaseAcrossSpecies(item.dataset.name,sp);
      else navigateToDiseaseDb(item.dataset.name);
    }
    else{navigateToDrug(item.dataset.name);}
    input.value="";results.style.display="none";
  });
  document.addEventListener("click",e=>{
    if(!input.contains(e.target)&&!results.contains(e.target))results.style.display="none";
    const spPanel=document.getElementById("speciesFilterPanel");
    const catPanel=document.getElementById("categoryFilterPanel");
    const spBtn=document.getElementById("searchFilterBtn");
    const catBtn=document.getElementById("categoryFilterBtn");
    if(spPanel&&!spPanel.contains(e.target)&&!e.target.closest("#searchFilterBtn")&&spPanel.style.display!=="none"){
      spPanel.style.display="none";
      if(spBtn)spBtn.setAttribute("aria-expanded","false");
    }
    if(catPanel&&!catPanel.contains(e.target)&&!e.target.closest("#categoryFilterBtn")&&catPanel.style.display!=="none"){
      catPanel.style.display="none";
      if(catBtn)catBtn.setAttribute("aria-expanded","false");
    }
  });
  /* Keyboard navigation for global search dropdown (Arrow/Enter/Escape). */
  let activeIdx=-1;
  function _items(){return Array.from(results.querySelectorAll(".search-result-item[data-type]"));}
  function _highlight(items,idx){
    items.forEach((el,i)=>{
      if(i===idx){el.classList.add("active");el.setAttribute("aria-selected","true");el.scrollIntoView({block:"nearest"});}
      else{el.classList.remove("active");el.removeAttribute("aria-selected");}
    });
  }
  input.addEventListener("keydown",e=>{
    if(e.key==="Escape"){results.style.display="none";input.blur();activeIdx=-1;return;}
    if(results.style.display==="none")return;
    const items=_items();
    if(!items.length)return;
    if(e.key==="ArrowDown"){e.preventDefault();activeIdx=(activeIdx+1)%items.length;_highlight(items,activeIdx);}
    else if(e.key==="ArrowUp"){e.preventDefault();activeIdx=(activeIdx-1+items.length)%items.length;_highlight(items,activeIdx);}
    else if(e.key==="Enter"&&activeIdx>=0){e.preventDefault();items[activeIdx].click();activeIdx=-1;}
  });
  /* Reset highlight whenever the result list re-renders. */
  const _resetIdx=new MutationObserver(()=>{activeIdx=-1;});
  _resetIdx.observe(results,{childList:true});
  setupSearchFilters(runSearch);
}

function setupSearchFilters(runSearch){
  const spBtn=document.getElementById("searchFilterBtn");
  const spPanel=document.getElementById("speciesFilterPanel");
  const spList=document.getElementById("speciesFilterList");
  const spClose=document.getElementById("filterCloseBtn");
  const spReset=document.getElementById("filterResetBtn");
  const catBtn=document.getElementById("categoryFilterBtn");
  const catPanel=document.getElementById("categoryFilterPanel");
  const catList=document.getElementById("categoryFilterList");
  const catClose=document.getElementById("categoryFilterCloseBtn");
  const catReset=document.getElementById("categoryFilterResetBtn");

  function setPanelOpen(panel,btn,open){
    if(!panel||!btn)return;
    panel.style.display=open?"block":"none";
    btn.setAttribute("aria-expanded",open?"true":"false");
    if(!open&&document.activeElement&&panel.contains(document.activeElement)){
      btn.focus();
    }
  }
  function bindPanelKeydown(panel,btn){
    if(!panel||!btn)return;
    panel.addEventListener("keydown",e=>{
      if(e.key==="Escape"){e.stopPropagation();setPanelOpen(panel,btn,false);}
    });
  }

  if(spBtn&&spPanel&&spList){
    spBtn.setAttribute("aria-expanded","false");
    spBtn.setAttribute("aria-haspopup","dialog");
    bindPanelKeydown(spPanel,spBtn);
    spBtn.addEventListener("click",()=>{
      const show=spPanel.style.display==="none";
      setPanelOpen(spPanel,spBtn,show);
      if(catPanel&&catBtn)setPanelOpen(catPanel,catBtn,false);
      if(show){
        renderSpeciesFilterList();
        const first=spPanel.querySelector(".filter-checkbox,.filter-close");
        if(first)setTimeout(()=>first.focus(),50);
      }
    });
    if(spClose)spClose.addEventListener("click",()=>setPanelOpen(spPanel,spBtn,false));
    if(spReset)spReset.addEventListener("click",()=>{
      globalSearchSpeciesFilter=null;
      spBtn.classList.remove("filter-active");
      renderSpeciesFilterList();
      runSearch();
    });
    spList.addEventListener("click",e=>{
      const item=e.target.closest(".filter-checkbox");
      if(!item)return;
      const id=item.dataset.species;
      if(globalSearchSpeciesFilter===id){globalSearchSpeciesFilter=null;spBtn.classList.remove("filter-active");}
      else{globalSearchSpeciesFilter=id;spBtn.classList.add("filter-active");selectSpecies(id);}
      renderSpeciesFilterList();
      setPanelOpen(spPanel,spBtn,false);
      runSearch();
    });
  }

  if(catBtn&&catPanel&&catList){
    catBtn.setAttribute("aria-expanded","false");
    catBtn.setAttribute("aria-haspopup","dialog");
    bindPanelKeydown(catPanel,catBtn);
    catBtn.addEventListener("click",()=>{
      const show=catPanel.style.display==="none";
      setPanelOpen(catPanel,catBtn,show);
      if(spPanel&&spBtn)setPanelOpen(spPanel,spBtn,false);
      if(show){
        renderCategoryFilterList();
        const first=catPanel.querySelector(".filter-checkbox,.filter-close");
        if(first)setTimeout(()=>first.focus(),50);
      }
    });
    if(catClose)catClose.addEventListener("click",()=>setPanelOpen(catPanel,catBtn,false));
    if(catReset)catReset.addEventListener("click",()=>{
      globalSearchTypeFilter=null;
      catBtn.classList.remove("filter-active");
      renderCategoryFilterList();
      runSearch();
    });
    catList.addEventListener("click",e=>{
      const item=e.target.closest(".filter-checkbox");
      if(!item)return;
      const type=item.dataset.type;
      if(globalSearchTypeFilter===type){globalSearchTypeFilter=null;catBtn.classList.remove("filter-active");}
      else{globalSearchTypeFilter=type;catBtn.classList.add("filter-active");}
      renderCategoryFilterList();
      setPanelOpen(catPanel,catBtn,false);
      runSearch();
    });
  }
}

function renderSpeciesFilterList(){
  const list=document.getElementById("speciesFilterList");
  if(!list)return;
  list.innerHTML=SPECIES.map(sp=>{
    const active=globalSearchSpeciesFilter===sp.id?"active":"";
    const checked=globalSearchSpeciesFilter===sp.id?"checked":"";
    const label=currentLang==="ja"?sp.name:sp.nameEn;
    return`<div class="filter-checkbox ${active}" data-species="${sp.id}"><input type="radio" name="speciesFilter" ${checked} tabindex="-1"/><label>${sp.icon} ${escapeHtml(label)}</label></div>`;
  }).join("");
}

function renderCategoryFilterList(){
  const list=document.getElementById("categoryFilterList");
  if(!list)return;
  const types=[
    {type:"disease",icon:"\u{1F4D6}",ja:"疾患のみ",en:"Diseases only"},
    {type:"drug",icon:"\u{1F48A}",ja:"薬品のみ",en:"Drugs only"}
  ];
  list.innerHTML=types.map(t=>{
    const active=globalSearchTypeFilter===t.type?"active":"";
    const checked=globalSearchTypeFilter===t.type?"checked":"";
    const label=currentLang==="ja"?t.ja:t.en;
    return`<div class="filter-checkbox ${active}" data-type="${t.type}"><input type="radio" name="typeFilter" ${checked} tabindex="-1"/><label>${t.icon} ${label}</label></div>`;
  }).join("");
}

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
  if(!btn||!nav){debugWarn("hamburgerBtn or mainNav not found");return;}
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

/* --- Load stats with Promise.allSettled (degrades gracefully) --- */
function loadSpeciesStats(){
  Promise.allSettled([
    fetchWithTimeout("/api/dashboard-stats").then(r=>r.json()),
    fetchWithTimeout("/api/species-stats").then(r=>r.json()),
    fetchWithTimeout("/api/health-check/symptoms").then(r=>r.json())
  ]).then(([dashRes,speciesRes,symRes])=>{
    const dashStats=dashRes.status==="fulfilled"?dashRes.value:{};
    const speciesData=speciesRes.status==="fulfilled"?speciesRes.value:null;
    const sd=symRes.status==="fulfilled"?symRes.value:{};
    if(dashRes.status==="rejected")debugError("dashboard-stats failed:",dashRes.reason);
    if(speciesRes.status==="rejected")debugError("species-stats failed:",speciesRes.reason);
    if(symRes.status==="rejected")debugError("health-check/symptoms failed:",symRes.reason);
    try{
      if(!speciesData||!Array.isArray(speciesData.species)){
        // Critical fallback: species list is required for the grid
        setDefaultStats();
        return;
      }
      SPECIES=speciesData.species.map(sp=>({...sp,icon:SPECIES_ICONS[sp.id]||"\u{1F43E}"}));
      pendingStats={
        diseases:dashStats.total_diseases||0,
        species:dashStats.total_species||SPECIES.length,
        drugs:dashStats.total_drugs||0,
        symptoms:sd.symptoms?sd.symptoms.length:0,
        protocols:dashStats.total_protocols||0
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
    }catch(e){
      debugError("Error processing species stats:",e);
      setDefaultStats();
    }
  });
}

function setDefaultStats(){
  SPECIES=[
    {id:"dog",name:"犬",nameEn:"Dog",icon:"\u{1F415}",diseases:619,drugs:572,description:"Comprehensive disease dictionary for dogs",description_ja:"最も一般的なペットの疾患辞典"},
    {id:"cat",name:"猫",nameEn:"Cat",icon:"\u{1F408}",diseases:551,drugs:552,description:"Feline-specific diseases and symptoms",description_ja:"猫特有の疾患と症状"},
    {id:"horse",name:"馬",nameEn:"Horse",icon:"\u{1F434}",diseases:616,drugs:359,description:"Equine diseases and musculoskeletal disorders",description_ja:"馬の疾患・運動器障害を網羅"},
    {id:"rabbit",name:"うさぎ",nameEn:"Rabbit",icon:"\u{1F407}",diseases:429,drugs:270,description:"Common rabbit digestive and dental diseases",description_ja:"うさぎに多い消化器・歯科疾患"},
    {id:"hamster",name:"ハムスター",nameEn:"Hamster",icon:"\u{1F439}",diseases:311,drugs:70,description:"Hamster tumors, skin conditions, and more",description_ja:"ハムスターの腫瘍・皮膚疾患など"},
    {id:"guinea_pig",name:"モルモット",nameEn:"Guinea Pig",icon:"\u{1F43E}",diseases:331,drugs:138,description:"Vitamin C deficiency and respiratory diseases",description_ja:"ビタミンC欠乏症や呼吸器疾患"},
    {id:"chinchilla",name:"チンチラ",nameEn:"Chinchilla",icon:"\u{1F43E}",diseases:258,drugs:92,description:"Chinchilla dental and digestive conditions",description_ja:"チンチラの歯科・消化器疾患"},
    {id:"ferret",name:"フェレット",nameEn:"Ferret",icon:"\u{1F43E}",diseases:267,drugs:204,description:"Ferret endocrine and neoplastic diseases",description_ja:"フェレットの内分泌・腫瘍疾患"},
    {id:"hedgehog",name:"ハリネズミ",nameEn:"Hedgehog",icon:"\u{1F994}",diseases:236,drugs:68,description:"Hedgehog skin and neurological conditions",description_ja:"ハリネズミの皮膚・神経疾患"},
    {id:"sugar_glider",name:"フクロモモンガ",nameEn:"Sugar Glider",icon:"\u{1F43E}",diseases:214,drugs:75,description:"Nutritional diseases and stress-related conditions",description_ja:"栄養性疾患やストレス関連症状"},
    {id:"degu",name:"デグー",nameEn:"Degu",icon:"\u{1F43E}",diseases:193,drugs:158,description:"Degu diabetes and dental diseases",description_ja:"デグーの糖尿病・歯科疾患"},
    {id:"bird",name:"鳥",nameEn:"Bird",icon:"\u{1F426}",diseases:529,drugs:237,description:"Avian infections and nutritional diseases",description_ja:"鳥類全般の感染症・栄養疾患"},
    {id:"parakeet",name:"インコ",nameEn:"Parakeet",icon:"\u{1F99C}",diseases:434,drugs:237,description:"Parakeet respiratory and feather disorders",description_ja:"インコの呼吸器・羽毛疾患"},
    {id:"parrot",name:"オウム",nameEn:"Parrot",icon:"\u{1F99C}",diseases:275,drugs:237,description:"Psittacosis, PBFD, and large parrot diseases",description_ja:"オウム病やPBFDなど大型鳥の疾患"},
    {id:"reptile",name:"爬虫類",nameEn:"Reptile",icon:"\u{1F98E}",diseases:280,drugs:103,description:"Metabolic bone disease and general reptile conditions",description_ja:"爬虫類全般の代謝性骨疾患など"},
    {id:"tortoise",name:"リクガメ",nameEn:"Tortoise",icon:"\u{1F422}",diseases:278,drugs:111,description:"Tortoise shell and respiratory disorders",description_ja:"リクガメの甲羅・呼吸器疾患"},
    {id:"snake",name:"ヘビ",nameEn:"Snake",icon:"\u{1F40D}",diseases:242,drugs:110,description:"Snake respiratory infections and dysecdysis",description_ja:"ヘビの呼吸器感染症・脱皮異常"},
    {id:"lizard",name:"トカゲ",nameEn:"Lizard",icon:"\u{1F98E}",diseases:241,drugs:105,description:"Lizard parasitic and metabolic diseases",description_ja:"トカゲの寄生虫症・代謝疾患"},
    {id:"amphibian",name:"両生類",nameEn:"Amphibian",icon:"\u{1F438}",diseases:255,drugs:18,description:"Chytrid fungus and amphibian diseases",description_ja:"カエル・イモリのツボカビ症など"},
    {id:"fish",name:"魚",nameEn:"Fish",icon:"\u{1F41F}",diseases:45,drugs:28,description:"Ich, fin rot, dropsy and aquarium fish diseases",description_ja:"白点病・尾ぐされ病・松かさ病など観賞魚の疾患"},
    {id:"exotic_other",name:"その他エキゾチック",nameEn:"Exotic Other",icon:"\u{1F43E}",diseases:289,drugs:1,description:"Diseases of other exotic animals",description_ja:"その他のエキゾチックアニマルの疾患"},
  ];
  pendingStats={
    diseases:6432,
    species:21,
    drugs:637,
    symptoms:60,
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
  if(!grid){debugWarn("speciesGrid element not found");return;}
  if(!currentSpecies)updateCheckerProgress(1);
  const section=document.getElementById("speciesSection");
  if(section&&!section.querySelector(".species-filter-input")){
    const filterInput=document.createElement("input");
    filterInput.type="search";filterInput.className="species-filter-input";
    filterInput.placeholder=t("speciesFilterPh");
    filterInput.setAttribute("aria-label",t("speciesFilterPh"));
    section.insertBefore(filterInput,grid);
    filterInput.addEventListener("input",debounce(()=>{
      const q=filterInput.value.trim().toLowerCase();
      grid.querySelectorAll(".species-card").forEach(card=>{
        const text=(card.textContent||"").toLowerCase();
        card.style.display=(!q||text.includes(q))?"":"none";
      });
      grid.querySelectorAll(".species-group-label").forEach(label=>{
        const next=label.nextElementSibling;
        let hasVisible=false;
        let el=label.nextElementSibling;
        while(el&&!el.classList.contains("species-group-label")){
          if(el.classList.contains("species-card")&&el.style.display!=="none")hasVisible=true;
          el=el.nextElementSibling;
        }
        label.style.display=(!q||hasVisible)?"":"none";
      });
    },150));
  }
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
        <div class="species-stats"><span>\u{1F4CB} ${sp.diseases} ${dLabel}</span>${sp.drugs?`<span>\u{1F48A} ${sp.drugs} ${drLabel}</span>`:""}</div>
      </div>`}).join("");
  }
  grid.innerHTML=html;
  // Event delegation for species cards
  if(grid.dataset.bound==="1")return;
  grid.dataset.bound="1";
  grid.addEventListener("click",e=>{
    const card=e.target.closest(".species-card");
    if(card)selectSpecies(card.dataset.species,{scroll:true});
  });
  grid.addEventListener("keydown",e=>{
    const card=e.target.closest(".species-card");
    if(!card)return;
    if(e.key==="Enter"||e.key===" "){e.preventDefault();selectSpecies(card.dataset.species,{scroll:true});return;}
    if(["ArrowRight","ArrowLeft","ArrowDown","ArrowUp"].includes(e.key)){
      e.preventDefault();
      const cards=[...grid.querySelectorAll('.species-card:not([style*="display: none"])')];
      const idx=cards.indexOf(card);if(idx<0)return;
      const cols=Math.round(grid.offsetWidth/(card.offsetWidth||1))||3;
      let next=-1;
      if(e.key==="ArrowRight")next=idx+1;
      else if(e.key==="ArrowLeft")next=idx-1;
      else if(e.key==="ArrowDown")next=idx+cols;
      else if(e.key==="ArrowUp")next=idx-cols;
      if(next>=0&&next<cards.length){cards[next].focus();haptic(5);}
    }
  });
}

function selectSpecies(id,opts){
  trackEvent("select_species",{species:id});
  currentSpecies=id;selectedSymptoms.clear();currentBreed="";
  document.querySelectorAll(".species-card").forEach(c=>{
    const sel=c.dataset.species===id;
    c.setAttribute("aria-pressed",sel);
  });
  renderSelectedSymptoms();loadSymptoms(id);loadDiseaseDb(id);loadBreeds(id);updateLabRangesForSpecies(id);updatePainScaleVisibility();loadHusbandry(id);reloadAnesthesiaForSpecies();updateCheckerProgress(2);if(typeof renderLabCalculators==="function")renderLabCalculators();
  resetSpeciesChat(id);
  // Reset guided consultation if active
  const guidedCont=document.getElementById("chatGuidedContainer");
  if(guidedCont&&!guidedCont.classList.contains("hidden")){startGuidedConsultation();}
  else{guidedState.species=id;}
  const sp=SPECIES.find(s=>s.id===id);
  if(sp&&typeof showToast==="function"){const label=currentLang==="ja"?sp.name:sp.nameEn;showToast(currentLang==="ja"?`${label}を選択しました`:`${label} selected`,"success");}
  const resultsArea=document.getElementById("resultsArea");
  if(resultsArea){resultsArea.innerHTML=`<div class="results-empty"><span class="big-icon" aria-hidden="true">\u{1F50D}</span><p>${t("resultsSelectSymptom")}</p></div>${renderHistoryPanel()}`;attachHistoryHandlers(resultsArea);}
  updateBreadcrumb();
  updateTabBadges(id);
  /* Dismiss the first-visit coach once a species is chosen. */
  const _coach=document.querySelector(".first-visit-coach");
  if(_coach){_coach.remove();try{localStorage.setItem("vetdict-coach-seen","1");}catch(e){}}
  /* Prefetch the drug dictionary on idle so the first drug-tab open is instant. */
  if(!drugsLoaded){
    const _pf=()=>{if(!drugsLoaded)loadDrugDictionary();};
    if("requestIdleCallback" in window)requestIdleCallback(_pf,{timeout:2500});
    else setTimeout(_pf,1200);
  }
  /* On a user tap of a species card, carry the viewport to the "select symptoms"
     step so the next action is visible — on mobile the checker sits below the
     species grid and the tap otherwise looks like nothing happened. Programmatic
     calls (deep link, history restore, cross-view flows) pass no opts and never
     move the page. Skip when the card is already comfortably in view (desktop). */
  if(opts&&opts.scroll){
    const target=document.querySelector("#viewChecker .panels");
    if(target&&target.offsetParent!==null){
      const top=target.getBoundingClientRect().top;
      const stickyOffset=parseInt(getComputedStyle(document.documentElement).getPropertyValue("--sticky-offset"),10)||112;
      const comfy=top>=stickyOffset&&top<window.innerHeight*0.6;
      if(!comfy)requestAnimationFrame(()=>scrollToAnchor(target));
    }
  }
}

function updateTabBadges(speciesId){
  const sp=speciesId?SPECIES.find(s=>s.id===speciesId):null;
  const tabs={
    "tab-database":sp?sp.diseases:null,
    "tab-drugs":sp?sp.drugs:null
  };
  Object.entries(tabs).forEach(([tabId,count])=>{
    const tab=document.getElementById(tabId);
    if(!tab)return;
    let badge=tab.querySelector(".tab-badge");
    if(count&&count>0){
      if(!badge){badge=document.createElement("span");badge.className="tab-badge";tab.appendChild(badge);}
      badge.textContent=count;
    }else if(badge){badge.remove();}
  });
}

/* First-visit coach: a single dismissible nudge to select a species. Shown once
   (localStorage), only before any species is chosen. Auto-dismisses on selection
   (handled in selectSpecies). */
function setupFirstVisitCoach(){
  try{if(localStorage.getItem("vetdict-coach-seen"))return;}catch(e){}
  if(currentSpecies)return;
  const anchor=document.getElementById("speciesSection");
  if(!anchor||anchor.querySelector(".first-visit-coach"))return;
  const tip=document.createElement("div");
  tip.className="first-visit-coach";
  tip.setAttribute("role","note");
  const msg=currentLang==="ja"?"まず動物種を選択してください":"Start by selecting a species";
  const closeLabel=currentLang==="ja"?"ヒントを閉じる":"Dismiss hint";
  tip.innerHTML=`<span class="first-visit-coach-arrow" aria-hidden="true">\u{1F447}</span><span>${msg}</span><button type="button" class="first-visit-coach-close" aria-label="${closeLabel}">×</button>`;
  anchor.insertBefore(tip,anchor.firstChild);
  tip.querySelector(".first-visit-coach-close").addEventListener("click",()=>{
    tip.remove();try{localStorage.setItem("vetdict-coach-seen","1");}catch(e){}
  });
}

const VIEW_LABELS={
  checker:{ja:"鑑別診断",en:"Differential Dx"},
  database:{ja:"疾患データベース",en:"Disease Database"},
  chat:{ja:"臨床相談",en:"Clinical Chat"},
  drugs:{ja:"薬品辞書",en:"Drug Dictionary"},
  anesthesia:{ja:"鎮静・麻酔",en:"Anesthesia"},
  emergency:{ja:"緊急対応",en:"Emergency"}
};

function updateBreadcrumb(){
  let bar=document.getElementById("breadcrumbBar");
  if(!bar){
    bar=document.createElement("div");
    bar.id="breadcrumbBar";
    bar.className="breadcrumb-bar";
    bar.setAttribute("aria-label","Breadcrumb");
    const header=document.querySelector(".header");
    if(header)header.after(bar);else return;
  }
  const sp=currentSpecies?SPECIES.find(s=>s.id===currentSpecies):null;
  const spLabel=sp?(currentLang==="ja"?sp.name:sp.nameEn):t("breadcrumbNoSpecies");
  const spIcon=currentSpecies?SPECIES_ICONS[currentSpecies]||"":"";
  const viewLabel=(VIEW_LABELS[currentView]||{})[currentLang==="ja"?"ja":"en"]||currentView;
  bar.innerHTML=`<nav class="breadcrumb-inner" aria-label="Breadcrumb">`
    +`<a href="#" class="breadcrumb-item breadcrumb-home" data-action="home">${t("breadcrumbHome")}</a>`
    +`<span class="breadcrumb-sep" aria-hidden="true">/</span>`
    +`<span class="breadcrumb-item breadcrumb-species${currentSpecies?" breadcrumb-species-active":""}" data-action="species">${spIcon?`<span aria-hidden="true">${spIcon}</span> `:""}${escapeHtml(spLabel)}</span>`
    +`<span class="breadcrumb-sep" aria-hidden="true">/</span>`
    +`<span class="breadcrumb-item breadcrumb-current" aria-current="page">${escapeHtml(viewLabel)}</span>`
    +`</nav>`;
  if(!bar._listening){
    bar._listening=true;
    bar.addEventListener("click",breadcrumbClick);
  }
}

function breadcrumbClick(e){
  const item=e.target.closest("[data-action]");
  if(!item)return;
  e.preventDefault();
  if(item.dataset.action==="home"){
    window.scrollTo({top:0,behavior:"smooth"});
  }else if(item.dataset.action==="species"){
    const sp=document.getElementById("speciesSection");
    if(sp)scrollToAnchor(sp);
  }
}

function setupKeyboardShortcuts(){
  const viewMap=["checker","database","chat","drugs","anesthesia","emergency"];
  document.addEventListener("keydown",e=>{
    if(!e.ctrlKey&&!e.metaKey)return;
    if(e.target.matches("input,textarea,select,[contenteditable]"))return;
    const num=parseInt(e.key,10);
    if(num>=1&&num<=viewMap.length){
      e.preventDefault();
      switchView(viewMap[num-1]);
      const panel=document.getElementById("view"+viewMap[num-1].charAt(0).toUpperCase()+viewMap[num-1].slice(1));
      if(panel)scrollToAnchor(panel);
    }
  });
}

function setupMobileBottomNav(){
  if(document.getElementById("mobileBottomNav"))return;
  const views=["checker","database","chat","drugs","anesthesia","emergency"];
  const icons={
    checker:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11"/></svg>',
    database:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>',
    chat:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>',
    drugs:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M10.5 1.5H8.25A2.25 2.25 0 006 3.75v16.5a2.25 2.25 0 002.25 2.25h7.5A2.25 2.25 0 0018 20.25V3.75a2.25 2.25 0 00-2.25-2.25H13.5m-3 0V3h3V1.5m-3 0h3m-6 9h6m-6 4h6"/></svg>',
    anesthesia:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    emergency:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>'
  };
  const nav=document.createElement("nav");
  nav.id="mobileBottomNav";
  nav.className="mobile-bottom-nav";
  nav.setAttribute("aria-label",currentLang==="ja"?"メインナビゲーション":"Main navigation");
  views.forEach(v=>{
    const btn=document.createElement("button");
    btn.type="button";
    btn.dataset.view=v;
    btn.className=v===currentView?"active":"";
    btn.innerHTML=icons[v]+'<span>'+t("mobileNav"+v.charAt(0).toUpperCase()+v.slice(1))+'</span>';
    btn.setAttribute("aria-label",t("mobileNav"+v.charAt(0).toUpperCase()+v.slice(1)));
    nav.appendChild(btn);
  });
  nav.addEventListener("click",e=>{
    const btn=e.target.closest("button[data-view]");
    if(!btn)return;
    haptic(10);
    switchView(btn.dataset.view,{focusSearch:true});
    const target=_navLandingTarget(btn.dataset.view);
    if(target)scrollToAnchor(target);
  });
  document.body.appendChild(nav);
}

function updateMobileBottomNav(){
  const nav=document.getElementById("mobileBottomNav");
  if(!nav)return;
  nav.querySelectorAll("button[data-view]").forEach(btn=>{
    btn.classList.toggle("active",btn.dataset.view===currentView);
  });
}

function setupSwipeGesture(){
  const views=["checker","database","chat","drugs","anesthesia","emergency"];
  let touchStartX=0,touchStartY=0,touchStartTime=0;
  document.addEventListener("touchstart",e=>{
    if(e.target.closest(".chat-container,#chatGuidedContainer,.global-search-results,input,textarea,select"))return;
    touchStartX=e.touches[0].clientX;
    touchStartY=e.touches[0].clientY;
    touchStartTime=Date.now();
  },{passive:true});
  document.addEventListener("touchend",e=>{
    if(e.target.closest(".chat-container,#chatGuidedContainer,.global-search-results,input,textarea,select"))return;
    const dx=e.changedTouches[0].clientX-touchStartX;
    const dy=e.changedTouches[0].clientY-touchStartY;
    const dt=Date.now()-touchStartTime;
    if(Math.abs(dx)<60||Math.abs(dy)>Math.abs(dx)*0.7||dt>500)return;
    const idx=views.indexOf(currentView);
    if(idx<0)return;
    let nextIdx=-1;
    if(dx<-60&&idx<views.length-1)nextIdx=idx+1;
    else if(dx>60&&idx>0)nextIdx=idx-1;
    if(nextIdx>=0){
      haptic(15);
      switchView(views[nextIdx]);
      const panel=document.getElementById("view"+views[nextIdx].charAt(0).toUpperCase()+views[nextIdx].slice(1));
      if(panel)scrollToAnchor(panel);
    }
  },{passive:true});
}

let _kbPanelOpener=null;
function toggleKbShortcuts(){
  let panel=document.getElementById("kbShortcutsPanel");
  if(!panel){
    panel=document.createElement("div");panel.id="kbShortcutsPanel";panel.className="kb-shortcuts-panel";
    panel.setAttribute("role","dialog");
    panel.setAttribute("aria-modal","true");
    panel.setAttribute("aria-labelledby","kbShortcutsTitle");
    const isJa=currentLang==="ja";
    const closeLabel=isJa?"閉じる":"Close";
    panel.innerHTML=`<div class="kb-shortcuts-inner"><div class="kb-shortcuts-header"><h3 id="kbShortcutsTitle">${isJa?"キーボードショートカット":"Keyboard Shortcuts"}</h3><button type="button" class="kb-close" aria-label="${closeLabel}">✕</button></div><div class="kb-shortcuts-body"><div class="kb-group"><div class="kb-title">${isJa?"ナビゲーション":"Navigation"}</div><div class="kb-row"><kbd>1</kbd><span>${isJa?"症状チェッカー":"Symptom Checker"}</span></div><div class="kb-row"><kbd>2</kbd><span>${isJa?"疾患データベース":"Disease Database"}</span></div><div class="kb-row"><kbd>3</kbd><span>${isJa?"AIチャット":"AI Chat"}</span></div><div class="kb-row"><kbd>4</kbd><span>${isJa?"薬品辞書":"Drug Dictionary"}</span></div><div class="kb-row"><kbd>5</kbd><span>${isJa?"鎮静・麻酔":"Anesthesia"}</span></div><div class="kb-row"><kbd>6</kbd><span>${isJa?"緊急対応":"Emergency"}</span></div></div><div class="kb-group"><div class="kb-title">${isJa?"操作":"Actions"}</div><div class="kb-row"><kbd>/</kbd><span>${isJa?"検索にフォーカス":"Focus search"}</span></div><div class="kb-row"><kbd>Esc</kbd><span>${isJa?"パネルを閉じる":"Close panel"}</span></div><div class="kb-row"><kbd>?</kbd><span>${isJa?"このヘルプ":"This help"}</span></div><div class="kb-row"><kbd>←→↑↓</kbd><span>${isJa?"動物種グリッドを移動":"Navigate species grid"}</span></div><div class="kb-row"><kbd>↑↓</kbd><span>${isJa?"疾患・薬品リストを移動 / Enterで開く":"Move through disease/drug list · Enter to open"}</span></div></div></div></div>`;
    document.body.appendChild(panel);
    panel.querySelector(".kb-close").addEventListener("click",()=>_kbPanelClose());
    panel.addEventListener("click",e=>{if(e.target===panel)_kbPanelClose();});
  }
  const willOpen=!panel.classList.contains("visible");
  panel.classList.toggle("visible",willOpen);
  if(willOpen){
    _kbPanelOpener=document.activeElement;
    const closeBtn=panel.querySelector(".kb-close");
    if(closeBtn)setTimeout(()=>closeBtn.focus(),20);
  }else{
    _kbPanelClose();
  }
}
function _kbPanelClose(){
  const panel=document.getElementById("kbShortcutsPanel");
  if(!panel)return;
  panel.classList.remove("visible");
  if(_kbPanelOpener&&typeof _kbPanelOpener.focus==="function"){
    try{_kbPanelOpener.focus();}catch(_){}
    _kbPanelOpener=null;
  }
}

function setupOfflineIndicator(){
  const banner=document.createElement("div");
  banner.className="offline-banner";
  banner.id="offlineBanner";
  banner.textContent=t("offlineBanner");
  document.body.prepend(banner);
  function update(){banner.classList.toggle("visible",!navigator.onLine);}
  window.addEventListener("online",update);
  window.addEventListener("offline",update);
  update();
  const prog=document.createElement("div");
  prog.className="reading-progress";prog.id="readingProgress";
  document.body.appendChild(prog);
}

function resetSpeciesChat(species){
  chatAccumulatedSymptoms=[];
  chatSpecies=species||"";
  const sp=SPECIES.find(s=>s.id===species);
  const spLabel=sp?(currentLang==="ja"?sp.name:sp.nameEn):(species||"dog");
  const hint=currentLang==="ja"?`${spLabel}の症状を入力してください。`:`Please describe ${spLabel} symptoms.`;
  /* Quick symptom buttons per species */
  const quickSymptoms=currentLang==="ja"?{
    dog:["嘔吐している","元気がない","下痢している","咳が出る","足を引きずる","皮膚が痒い","おしりを地面にこすりつける"],
    cat:["食べない","吐いた","くしゃみ","目やにが出る","おしっこが出ない","毛が抜ける"],
    rabbit:["糞が小さい","食べない","歯ぎしり","首が傾いている","お腹が張っている","鼻水"],
    chinchilla:["よだれが出る","毛が抜ける","食べない","糞が出ない","歯が伸びている","砂浴びしない"],
    hamster:["下痢","元気がない","毛が抜ける","目が開かない","お腹が膨れている","食べない"],
    guinea_pig:["食べない","鼻水","足を引きずる","脱毛","下痢","くしゃみ"],
    ferret:["ぐったり","脱毛","下痢","後ろ足がふらつく","嘔吐","食べない","陰部が腫れている"],
    hedgehog:["針が抜ける","フケ","ふらつく","食べない","目が出ている","体重が減った"],
    bird:["羽を膨らませている","食べない","下痢","鼻水","羽が抜ける","くしゃみ","自分で羽を抜く"],
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
      /* Reset the once-per-session disclaimer flag for the new species. */
      delete el.dataset.disclaimerShown;
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
  if(!select)return;
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
    return fetchWithTimeout("/api/health-check/symptoms").then(r=>r.ok?r.json():Promise.reject(new Error("HTTP "+r.status))).then(data=>{
      if(requestId!==symptomRequestId||species!==currentSpecies)return;
      symptomData=data.symptoms||[];
      renderSymptomList(symptomData);
    });
  }).catch(()=>{
    if(requestId!==symptomRequestId)return;
    const sl=document.getElementById("symptomList");if(sl)sl.innerHTML=`<div style="padding:20px;text-align:center;color:var(--gray-500)">${t("loadFailed")}</div>`;
  });
}

function toggleSymptomSort(){symptomSortMode=symptomSortMode==="category"?(currentLang==="ja"?"kana":"az"):"category";renderSymptomList(symptomData);}
function renderSymptomList(symptoms){
  const symptomSearch=document.getElementById("symptomSearch");
  const list=document.getElementById("symptomList");
  if(!list){debugWarn("symptomList element not found");return;}
  const search=(symptomSearch?.value||"").toLowerCase();
  const sortLabel=symptomSortMode==="category"?(currentLang==="ja"?"あいうえお順":"A-Z"):(currentLang==="ja"?"カテゴリ順":"By Category");
  let html=`<button class="symptom-sort-toggle" aria-label="Switch sort mode">${escapeHtml(sortLabel)}</button>`;
  let matchCount=0;
  const mkItem=s=>{const sel=selectedSymptoms.has(s.id);const primary=currentLang==="ja"?(s.name_ja||s.name_en):(s.name_en||s.name_ja);const secondary=currentLang==="ja"?(s.name_en||""):(s.name_ja||"");return`<div class="symptom-item" role="checkbox" aria-checked="${sel}" tabindex="0" data-id="${escapeHtml(s.id)}"><span class="sym-icon" aria-hidden="true">${sel?"\u2713":"+"}</span><span>${escapeHtml(primary)} <span style="color:var(--gray-600)">${escapeHtml(secondary)}</span></span></div>`;};
  const matchSearch=s=>{if(!search)return true;return(s.name_ja||"").toLowerCase().includes(search)||(s.name_en||"").toLowerCase().includes(search)||(s.id||"").toLowerCase().includes(search);};
  if(symptomSortMode==="category"){
    const categories={};
    symptoms.forEach(s=>{const cat=s.category||"other";if(!categories[cat])categories[cat]=[];categories[cat].push(s);});
    const catLabels=t("catLabels");
    for(const[cat,items]of Object.entries(categories)){
      const filtered=items.filter(matchSearch);
      if(!filtered.length)continue;
      matchCount+=filtered.length;
      const hasSelected=filtered.some(s=>selectedSymptoms.has(s.id));
      const selCount=filtered.filter(s=>selectedSymptoms.has(s.id)).length;
      const badge=selCount?` <span class="cat-badge">${selCount}</span>`:"";
      const open=search||hasSelected?"open":"";
      html+=`<details class="symptom-cat-group" ${open}><summary class="symptom-cat" role="heading" aria-level="4">${catLabels[cat]||cat}${badge}<span class="cat-chevron" aria-hidden="true"></span></summary><div class="symptom-cat-items">`;
      for(const s of filtered)html+=mkItem(s);
      html+=`</div></details>`;
    }
  }else{
    const sorted=symptoms.filter(matchSearch).slice().sort((a,b)=>{const an=currentLang==="ja"?(a.name_ja||a.name_en||""):(a.name_en||a.name_ja||"");const bn=currentLang==="ja"?(b.name_ja||b.name_en||""):(b.name_en||b.name_ja||"");return an.localeCompare(bn,currentLang==="ja"?"ja":"en");});
    matchCount=sorted.length;
    for(const s of sorted)html+=mkItem(s);
  }
  if(matchCount===0){
    const noMatch=escapeHtml(t("noMatchingSymptom"));
    const clearLabel=currentLang==="ja"?"検索をクリア":"Clear search";
    const tipText=currentLang==="ja"?"別の言い回し（日本語・英語）でも検索できます":"Try alternate phrasing or switch language";
    const clearAction=search?`<button type="button" class="symptom-search-clear-inline" style="margin-top:8px;padding:6px 14px;background:var(--navy);color:#fff;border:none;border-radius:6px;font-size:.78rem;cursor:pointer">${escapeHtml(clearLabel)}</button>`:"";
    html+=`<div style="padding:20px;text-align:center;color:var(--gray-500);font-size:.84rem">${noMatch}<div style="margin-top:4px;font-size:.76rem;color:var(--gray-400)">${escapeHtml(tipText)}</div>${clearAction}</div>`;
  }
  list.innerHTML=html;
  const sortToggle=list.querySelector(".symptom-sort-toggle");
  if(sortToggle)sortToggle.addEventListener("click",toggleSymptomSort);
  const inlineClear=list.querySelector(".symptom-search-clear-inline");
  if(inlineClear)inlineClear.addEventListener("click",()=>{
    if(symptomSearch){symptomSearch.value="";symptomSearch.dispatchEvent(new Event("input"));symptomSearch.focus();}
  });
  list.onclick=e=>{const item=e.target.closest(".symptom-item");if(item)toggleSymptom(item.dataset.id);};
  list.onkeydown=e=>{const item=e.target.closest(".symptom-item");if(item&&(e.key==="Enter"||e.key===" ")){e.preventDefault();toggleSymptom(item.dataset.id);}};
}

function renderSymptomEmptyState(){
  /* Shown before any species is picked: the symptom list would otherwise be a
     blank card with just a search box, which reads as broken. */
  const list=document.getElementById("symptomList");
  if(!list||currentSpecies)return;
  list.innerHTML=`<div class="symptom-empty-state"><span class="symptom-empty-icon" aria-hidden="true">\u{1F43E}</span><p>${escapeHtml(t("selectSpeciesFirst"))}</p><button type="button" class="symptom-empty-btn">${escapeHtml(t("selectSpeciesFirstBtn"))}</button></div>`;
  const btn=list.querySelector(".symptom-empty-btn");
  if(btn)btn.addEventListener("click",()=>{const s=document.getElementById("speciesSection");if(s)scrollToAnchor(s);});
}

function toggleSymptom(id){const adding=!selectedSymptoms.has(id);if(adding)selectedSymptoms.add(id);else selectedSymptoms.delete(id);haptic(adding?12:6);renderSelectedSymptoms();renderSymptomList(symptomData);if(adding)trackEvent("add_symptom",{species:currentSpecies,symptom:id,total:selectedSymptoms.size});}

function renderSelectedSymptoms(){
  const area=document.getElementById("selectedSymptoms"),btn=document.getElementById("analyzeBtn");
  const disabledHint=currentLang==="ja"?"症状を1つ以上選択してください":"Select at least one symptom";
  if(selectedSymptoms.size===0){area.innerHTML=`<span style="color:var(--gray-500);font-size:.78rem">${t("noSymptomsSelected")}</span>`;btn.disabled=true;btn.setAttribute("aria-disabled","true");btn.setAttribute("title",disabledHint);updateSymptomFloater(0);return;}
  btn.disabled=false;btn.setAttribute("aria-disabled","false");btn.removeAttribute("title");
  const clearLabel=currentLang==="ja"?"全解除":"Clear All";
  const clearAriaLabel=currentLang==="ja"?"選択した症状をすべて解除":"Clear all selected symptoms";
  area.innerHTML=[...selectedSymptoms].map(id=>{const sym=symptomData.find(s=>s.id===id);const label=sym?(currentLang==="ja"?(sym.name_ja||sym.name_en):(sym.name_en||sym.name_ja)):id;const ariaLabel=t("removeLabel").replace("%s%",label);return`<span class="selected-tag">${escapeHtml(label)} <button class="remove" type="button" aria-label="${escapeHtml(ariaLabel)}" data-id="${escapeHtml(id)}">&times;</button></span>`;}).join("")+`<button class="clear-all-btn" type="button" aria-label="${escapeHtml(clearAriaLabel)}">${clearLabel}</button>`;
  area.querySelectorAll(".remove").forEach(b=>b.addEventListener("click",e=>{e.stopPropagation();toggleSymptom(b.dataset.id);}));
  const clearBtn=area.querySelector(".clear-all-btn");
  if(clearBtn)clearBtn.addEventListener("click",()=>{
    const prev=[...selectedSymptoms];
    selectedSymptoms.clear();renderSymptomList(symptomData);renderSelectedSymptoms();
    if(typeof showToast==="function"&&prev.length){
      const msg=currentLang==="ja"?`${prev.length}件の症状を解除しました`:`Cleared ${prev.length} symptom${prev.length>1?"s":""}`;
      const undoLabel=currentLang==="ja"?"元に戻す":"Undo";
      showToast(msg,"info",5000,{label:undoLabel,onClick:()=>{
        prev.forEach(id=>selectedSymptoms.add(id));
        renderSelectedSymptoms();renderSymptomList(symptomData);
      }});
    }
  });
  updateSymptomFloater(selectedSymptoms.size);
}

function updateSymptomFloater(count){
  let floater=document.getElementById("symptomFloater");
  if(count<1){if(floater)floater.classList.remove("visible");return;}
  if(!floater){
    floater=document.createElement("div");floater.id="symptomFloater";floater.className="symptom-floater";
    document.body.appendChild(floater);
    floater.addEventListener("click",()=>{const area=document.getElementById("selectedSymptoms");if(area)area.scrollIntoView({behavior:"smooth",block:"center"});});
  }
  floater.textContent=currentLang==="ja"?`${count}個の症状を選択中`:`${count} symptom${count>1?"s":""} selected`;
  floater.classList.add("visible");
}

function updateCheckerProgress(step){
  const cp=document.getElementById("checkerProgress");if(!cp)return;
  const steps=cp.querySelectorAll(".progress-step");
  const lines=cp.querySelectorAll(".progress-line");
  steps.forEach(s=>{
    const n=parseInt(s.dataset.step,10);
    s.classList.remove("active","completed");
    if(n<step)s.classList.add("completed");
    else if(n===step)s.classList.add("active");
  });
  lines.forEach((l,i)=>{l.classList.toggle("done",i<step-1);});
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
    const labels=t("painLabels")||["No Pain","Mild","Moderate","Severe","Excruciating"];
    const scoreLabel=t("painScoreLabel")||"Score";
    const colors=["#16a34a","#65a30d","#eab308","#ea580c","#dc2626"];
    if(badge){badge.style.display="inline";badge.textContent=`${scoreLabel} ${score}: ${labels[score]||""}`;badge.style.background=colors[score];}
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
  fetchWithTimeout(`/api/lab-ranges/${encodeURIComponent(species)}`)
    .then(r=>r.ok?r.json():null)
    .then(data=>{
      if(!data||!data.ranges||species!==currentSpecies)return;
      _labRangesCache[species]=data.ranges;
      _applyLabRanges(data.ranges);
    }).catch(()=>{/* lab ranges optional; fall back to default placeholders */});
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
  const isJa=currentLang==="ja";
  const highTxt=isJa?"\u57fa\u6e96\u7bc4\u56f2\u3088\u308a\u9ad8\u5024":"above reference range";
  const lowTxt=isJa?"\u57fa\u6e96\u7bc4\u56f2\u3088\u308a\u4f4e\u5024":"below reference range";
  document.querySelectorAll("#labValuesGrid input[data-lab]").forEach(el=>{
    const v=parseFloat(el.value),lo=parseFloat(el.dataset.lo),hi=parseFloat(el.dataset.hi);
    const flag=el.nextElementSibling;
    el.classList.remove("lab-high","lab-low");
    el.removeAttribute("aria-invalid");
    if(flag){
      flag.textContent="";
      // Marker has no accessible name when empty, so it can stay hidden from AT.
      flag.setAttribute("aria-hidden","true");
      flag.removeAttribute("aria-label");
    }
    if(isNaN(v)||el.value.trim()==="")return;
    filled++;
    if(v>hi){
      el.classList.add("lab-high");el.setAttribute("aria-invalid","true");
      if(flag){
        flag.textContent="\u2191";flag.style.color="#e74c3c";
        // Make the marker accessible: name = "above reference range"
        flag.removeAttribute("aria-hidden");
        flag.setAttribute("role","img");
        flag.setAttribute("aria-label",highTxt);
      }
      abnormal++;
    } else if(v<lo){
      el.classList.add("lab-low");el.setAttribute("aria-invalid","true");
      if(flag){
        flag.textContent="\u2193";flag.style.color="#2980b9";
        flag.removeAttribute("aria-hidden");
        flag.setAttribute("role","img");
        flag.setAttribute("aria-label",lowTxt);
      }
      abnormal++;
    }
  });
  const badge=document.getElementById("labSummaryBadge");
  if(!badge)return;
  if(filled>0){
    const filledLabel=currentLang==="ja"?`${filled}\u9805\u76ee\u5165\u529b`:`${filled} entered`;
    const abnLabel=currentLang==="ja"?` / ${abnormal}\u7570\u5e38`:` / ${abnormal} abnormal`;
    badge.style.display="inline";
    badge.textContent=abnormal>0?(filledLabel+abnLabel):filledLabel;
    badge.style.background=abnormal>0?"#e74c3c":"var(--green)";
  }else{
    badge.style.display="none";
    badge.textContent="";
  }
}
function clearLabValues(){
  document.querySelectorAll("#labValuesGrid input[data-lab]").forEach(el=>{el.value="";});
  highlightLabAbnormals();
  renderLabCalculators();
}

/* --- Lab import from image/text --- */
function openLabImportModal(){
  trackEvent("open_lab_import");
  let modal=document.getElementById("labImportModal");
  if(modal){modal.classList.add("open");document.body.style.overflow="hidden";openModalA11y(modal,".dashboard-close");return;}
  const isJa=currentLang==="ja";
  modal=document.createElement("div");
  modal.id="labImportModal";
  modal.className="dashboard-modal";
  modal.setAttribute("role","dialog");
  modal.setAttribute("aria-modal","true");
  modal.setAttribute("aria-labelledby","labImportTitle");
  modal.innerHTML=`<div class="dashboard-backdrop"></div><div class="dashboard-panel" style="max-width:700px"><div class="dashboard-header"><h2 id="labImportTitle">📷 ${isJa?"検査値の取り込み":"Import Lab Values"}</h2><button class="dashboard-close" aria-label="${isJa?"閉じる":"Close"}">✕</button></div><div class="dashboard-body">
    <div class="lab-import-tabs" role="tablist" style="display:flex;gap:6px;border-bottom:2px solid var(--gray-200);margin-bottom:14px">
      <button class="lab-import-tab active" data-tab="image" role="tab" aria-selected="true" style="padding:8px 16px;background:none;border:none;border-bottom:3px solid var(--navy);color:var(--navy);font-weight:700;cursor:pointer">${isJa?"🖼️ 画像":"🖼️ Image"}</button>
      <button class="lab-import-tab" data-tab="text" role="tab" aria-selected="false" style="padding:8px 16px;background:none;border:none;border-bottom:3px solid transparent;color:var(--gray-500);font-weight:600;cursor:pointer">${isJa?"📝 テキスト":"📝 Text"}</button>
    </div>
    <div class="lab-import-content lab-tab-image">
      <div id="labDropZone" style="border:2px dashed var(--gray-300);border-radius:10px;padding:30px;text-align:center;cursor:pointer;transition:all .2s;background:var(--gray-50)">
        <div style="font-size:2rem;margin-bottom:8px">📤</div>
        <div style="font-weight:600;color:var(--navy);margin-bottom:4px">${isJa?"クリックして画像を選択":"Click to choose image"}</div>
        <div style="font-size:.78rem;color:var(--gray-500)">${isJa?"または、ドラッグ&ドロップ／クリップボードから貼り付け (Ctrl+V)":"Or drag-and-drop / paste from clipboard (Ctrl+V)"}</div>
        <div style="font-size:.72rem;color:var(--gray-400);margin-top:6px">${isJa?"PNG/JPEG ≤ 8 MB":"PNG/JPEG ≤ 8 MB"}</div>
      </div>
      <input type="file" id="labImageInput" accept="image/*" capture="environment" style="display:none">
      <div id="labImagePreview" style="display:none;margin-top:14px;text-align:center"></div>
      <div id="labOcrProgress" style="display:none;text-align:center;padding:16px;color:var(--gray-600);font-size:.84rem"><div class="loader" style="display:inline-block;width:20px;height:20px;border:3px solid var(--gray-300);border-top-color:var(--navy);border-radius:50%;animation:spin 1s linear infinite;vertical-align:middle"></div> <span>${isJa?"画像を解析中…":"Analyzing image…"}</span></div>
    </div>
    <div class="lab-import-content lab-tab-text" style="display:none">
      <textarea id="labTextInput" rows="10" placeholder="${isJa?"検査結果テキストをここに貼り付けてください\n例:\nBUN 45 mg/dL\nクレアチニン 3.2 mg/dL\nALT 220 U/L":"Paste lab report text here\nExample:\nBUN 45 mg/dL\nCreatinine 3.2 mg/dL\nALT 220 U/L"}" style="width:100%;padding:10px;border:1.5px solid var(--gray-300);border-radius:6px;font-family:monospace;font-size:.84rem;resize:vertical"></textarea>
      <div style="margin-top:8px;display:flex;justify-content:flex-end"><button id="labTextParseBtn" style="padding:8px 16px;background:var(--navy);color:var(--white);border:none;border-radius:6px;cursor:pointer;font-weight:600">${isJa?"解析する":"Parse"}</button></div>
    </div>
    <div id="labImportResults" style="display:none;margin-top:14px"></div>
  </div></div>`;
  document.body.appendChild(modal);
  // Tab switching
  modal.querySelectorAll(".lab-import-tab").forEach(tab=>{
    tab.addEventListener("click",()=>{
      modal.querySelectorAll(".lab-import-tab").forEach(t=>{t.classList.remove("active");t.style.borderBottomColor="transparent";t.style.color="var(--gray-500)";t.setAttribute("aria-selected","false");});
      tab.classList.add("active");tab.style.borderBottomColor="var(--navy)";tab.style.color="var(--navy)";tab.setAttribute("aria-selected","true");
      modal.querySelector(".lab-tab-image").style.display=tab.dataset.tab==="image"?"block":"none";
      modal.querySelector(".lab-tab-text").style.display=tab.dataset.tab==="text"?"block":"none";
    });
  });
  // Close handlers
  modal.querySelector(".dashboard-close").addEventListener("click",closeLabImportModal);
  modal.querySelector(".dashboard-backdrop").addEventListener("click",closeLabImportModal);
  document.addEventListener("keydown",e=>{if(e.key==="Escape"&&modal.classList.contains("open"))closeLabImportModal();});
  // Image upload
  const dropZone=modal.querySelector("#labDropZone");
  const fileInput=modal.querySelector("#labImageInput");
  dropZone.addEventListener("click",()=>fileInput.click());
  fileInput.addEventListener("change",e=>{if(e.target.files[0])_handleLabImageFile(e.target.files[0]);});
  dropZone.addEventListener("dragover",e=>{e.preventDefault();dropZone.style.borderColor="var(--navy)";dropZone.style.background="rgba(26,48,104,.05)";});
  dropZone.addEventListener("dragleave",()=>{dropZone.style.borderColor="var(--gray-300)";dropZone.style.background="var(--gray-50)";});
  dropZone.addEventListener("drop",e=>{
    e.preventDefault();dropZone.style.borderColor="var(--gray-300)";dropZone.style.background="var(--gray-50)";
    const f=e.dataTransfer.files[0];if(f&&f.type.startsWith("image/"))_handleLabImageFile(f);
  });
  // Paste from clipboard
  modal.addEventListener("paste",e=>{
    const items=e.clipboardData.items;
    for(const item of items){
      if(item.type.startsWith("image/")){
        const file=item.getAsFile();
        if(file)_handleLabImageFile(file);
        break;
      }
    }
  });
  // Text parse
  modal.querySelector("#labTextParseBtn").addEventListener("click",()=>{
    const txt=modal.querySelector("#labTextInput").value.trim();
    if(!txt)return;
    _parseLabText(txt);
  });
  modal.classList.add("open");
  document.body.style.overflow="hidden";
  openModalA11y(modal,".dashboard-close");
}

function closeLabImportModal(){
  const modal=document.getElementById("labImportModal");
  if(modal)modal.classList.remove("open");
  document.body.style.overflow="";
  closeModalA11y(modal);
}

function _handleLabImageFile(file){
  if(file.size>8*1024*1024){showToast(currentLang==="ja"?"画像が大きすぎます（8MB以下）":"Image too large (max 8MB)","error");return;}
  const preview=document.getElementById("labImagePreview");
  const progress=document.getElementById("labOcrProgress");
  const results=document.getElementById("labImportResults");
  results.style.display="none";
  // Show preview
  const reader=new FileReader();
  reader.onload=e=>{
    preview.style.display="block";
    preview.innerHTML=`<img src="${e.target.result}" alt="${currentLang==="ja"?"検査結果プレビュー":"Lab preview"}" style="max-width:100%;max-height:200px;border:1px solid var(--gray-300);border-radius:6px">`;
  };
  reader.readAsDataURL(file);
  // Upload + OCR
  progress.style.display="block";
  const fd=new FormData();
  fd.append("image",file);
  fetchWithTimeout("/api/lab-ocr/image",{method:"POST",body:fd},60000)
    .then(r=>r.json())
    .then(data=>{
      progress.style.display="none";
      if(data.error){
        showToast((currentLang==="ja"?"OCR失敗: ":"OCR failed: ")+(data.error||""),"error");
        if(data.fallback)showToast(currentLang==="ja"?"📝 テキストタブに切り替えて手入力もできます":"📝 Try Text tab for manual input","info");
        return;
      }
      _renderExtractedLabs(data.labs||{},data.ocr_text||"");
    })
    .catch(err=>{
      progress.style.display="none";
      showToast((currentLang==="ja"?"取り込み失敗: ":"Failed: ")+err.message,"error");
    });
}

function _parseLabText(text){
  const results=document.getElementById("labImportResults");
  results.style.display="none";
  fetchWithTimeout("/api/lab-ocr/text",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({text})},30000)
    .then(r=>r.json())
    .then(data=>{
      if(data.error){showToast((currentLang==="ja"?"解析失敗: ":"Parse failed: ")+data.error,"error");return;}
      _renderExtractedLabs(data.labs||{},text);
    })
    .catch(err=>{showToast((currentLang==="ja"?"解析失敗: ":"Failed: ")+err.message,"error");});
}

function _renderExtractedLabs(labs,sourceText){
  const container=document.getElementById("labImportResults");
  const isJa=currentLang==="ja";
  const keys=Object.keys(labs);
  if(!keys.length){
    container.style.display="block";
    container.innerHTML=`<div style="padding:14px;background:#fef3c7;border-left:3px solid #f59e0b;border-radius:6px;color:#78350f;font-size:.86rem">${isJa?"検査値を検出できませんでした。テキストの一部を直接入力してください。":"No lab values detected. Try entering values directly."}</div>`;
    return;
  }
  let html=`<div style="padding:10px;background:rgba(34,168,79,.06);border-left:3px solid var(--green);border-radius:6px;margin-bottom:10px;font-size:.84rem"><strong style="color:var(--green)">${keys.length}${isJa?"件の検査値を検出":" lab values detected"}</strong> — ${isJa?"確認して取り込みボタンをクリック":"review and click Apply"}</div>`;
  html+=`<div style="max-height:280px;overflow-y:auto;border:1px solid var(--gray-200);border-radius:6px">`;
  html+=`<table style="width:100%;border-collapse:collapse;font-size:.84rem"><thead><tr style="background:var(--gray-100)"><th style="padding:6px 8px;text-align:left;border-bottom:1px solid var(--gray-200)">${isJa?"検査":"Lab"}</th><th style="padding:6px 8px;text-align:right;border-bottom:1px solid var(--gray-200)">${isJa?"値":"Value"}</th><th style="padding:6px 8px;text-align:left;border-bottom:1px solid var(--gray-200)">${isJa?"単位":"Unit"}</th><th style="padding:6px 8px;text-align:center;border-bottom:1px solid var(--gray-200)"><input type="checkbox" id="labImportAll" checked aria-label="${isJa?"全選択":"Select all"}"></th></tr></thead><tbody>`;
  for(const[k,v]of Object.entries(labs)){
    const input=document.querySelector(`input[data-lab="${k}"]`);
    const label=input?(input.closest(".lab-group")?.querySelector("label")?.textContent||k):k;
    html+=`<tr><td style="padding:6px 8px;border-bottom:1px solid var(--gray-100);font-weight:600">${escapeHtml(label.replace(/\s+/g," ").trim())}</td><td style="padding:6px 8px;text-align:right;border-bottom:1px solid var(--gray-100);font-family:monospace"><input type="number" step="any" value="${v.value}" data-lab-import="${escapeHtml(k)}" style="width:80px;padding:3px 6px;border:1px solid var(--gray-300);border-radius:4px;text-align:right;font-family:monospace"></td><td style="padding:6px 8px;border-bottom:1px solid var(--gray-100);color:var(--gray-500);font-size:.78rem">${escapeHtml(v.unit||"")}</td><td style="padding:6px 8px;text-align:center;border-bottom:1px solid var(--gray-100)"><input type="checkbox" class="lab-import-cb" data-lab-key="${escapeHtml(k)}" checked></td></tr>`;
  }
  html+=`</tbody></table></div>`;
  html+=`<div style="margin-top:12px;display:flex;justify-content:space-between;gap:8px"><button id="labImportApplyBtn" style="padding:8px 18px;background:var(--green);color:var(--white);border:none;border-radius:6px;cursor:pointer;font-weight:700">${isJa?"✓ 選択した値を取込":"✓ Apply Selected"}</button><button id="labImportCancelBtn" style="padding:8px 18px;background:var(--white);color:var(--gray-600);border:1px solid var(--gray-300);border-radius:6px;cursor:pointer">${isJa?"キャンセル":"Cancel"}</button></div>`;
  container.style.display="block";
  container.innerHTML=html;
  // Select-all toggle
  const selAll=container.querySelector("#labImportAll");
  selAll.addEventListener("change",e=>{container.querySelectorAll(".lab-import-cb").forEach(cb=>{cb.checked=e.target.checked;});});
  // Apply button
  container.querySelector("#labImportApplyBtn").addEventListener("click",()=>{
    let applied=0;
    container.querySelectorAll(".lab-import-cb:checked").forEach(cb=>{
      const k=cb.dataset.labKey;
      const valInput=container.querySelector(`input[data-lab-import="${k}"]`);
      const target=document.querySelector(`input[data-lab="${k}"]`);
      if(target&&valInput){
        target.value=valInput.value;
        applied++;
      }
    });
    highlightLabAbnormals();
    renderLabCalculators();
    closeLabImportModal();
    if(applied>0){
      showToast((currentLang==="ja"?"✓ ":"✓ ")+applied+(currentLang==="ja"?"件の検査値を取り込みました":" lab values imported"),"success");
      // Open lab section if collapsed
      const labDetails=document.getElementById("labDetails");
      if(labDetails)labDetails.open=true;
      trackEvent("lab_import_applied",{count:applied});
    }
  });
  container.querySelector("#labImportCancelBtn").addEventListener("click",closeLabImportModal);
}
document.addEventListener("input",e=>{if(e.target.matches("#labValuesGrid input")){highlightLabAbnormals();renderLabCalculators();}});

/* --- Clinical lab calculators (derived values from entered labs) --- */
function _getLabFloat(id){
  const el=document.getElementById(id);
  if(!el||!el.value.trim())return null;
  const v=parseFloat(el.value);
  return isNaN(v)?null:v;
}

function renderLabCalculators(){
  const container=document.getElementById("labCalculators");
  if(!container)return;
  const calcs=[];
  /* 1. Anion Gap = (Na + K) - (Cl + HCO3); normal dog 12-24, cat 13-27 */
  const na=_getLabFloat("lab-sodium"),k=_getLabFloat("lab-potassium"),cl=_getLabFloat("lab-chloride"),hco3=_getLabFloat("lab-hco3");
  if(na!==null&&k!==null&&cl!==null&&hco3!==null){
    const ag=(na+k)-(cl+hco3);
    const high=ag>24;
    const interp=high?(currentLang==="ja"?"高アニオンギャップ — DKA/乳酸/中毒/尿毒症":"High AG — DKA/lactic/toxin/uremia"):(currentLang==="ja"?"正常":"Normal");
    calcs.push({name:currentLang==="ja"?"アニオンギャップ":"Anion Gap",value:ag.toFixed(1),unit:"mEq/L",interp,high});
  }
  /* 2. Corrected Calcium for albumin (dog): Cor_Ca = Ca - Alb + 3.5 */
  const ca=_getLabFloat("lab-calcium"),alb=_getLabFloat("lab-albumin");
  if(ca!==null&&alb!==null){
    const corrected=ca-alb+3.5;
    const lo=8.5,hi=11.5;
    const flag=corrected>hi?"high":(corrected<lo?"low":"");
    const interp=flag==="high"?(currentLang==="ja"?"アルブミン補正で高Ca（リンパ腫/上皮小体機能亢進/ビタミンD中毒）":"Albumin-corrected hypercalcemia (lymphoma/hyperparathyroid/Vit D)"):
                 flag==="low"?(currentLang==="ja"?"補正後も低Ca（PLE/腎不全/低Mg）":"Corrected hypocalcemia (PLE/renal/hypoMg)"):
                 (currentLang==="ja"?"正常":"Normal");
    calcs.push({name:currentLang==="ja"?"アルブミン補正Ca":"Albumin-corrected Ca",value:corrected.toFixed(2),unit:"mg/dL",interp,high:flag==="high",low:flag==="low"});
  }
  /* 3. BUN:Creatinine ratio (>20 → prerenal/GI bleed; <10 → liver/protein loss) */
  const bun=_getLabFloat("lab-bun"),cre=_getLabFloat("lab-creatinine");
  if(bun!==null&&cre!==null&&cre>0){
    const ratio=bun/cre;
    const interp=ratio>20?(currentLang==="ja"?"高比 — 脱水/前腎性/消化管出血":"High ratio — dehydration/prerenal/GI bleed"):
                 ratio<10?(currentLang==="ja"?"低比 — 肝不全/タンパク漏出":"Low ratio — liver failure/protein-losing"):
                 (currentLang==="ja"?"正常範囲":"Normal range");
    calcs.push({name:currentLang==="ja"?"BUN:Cre 比":"BUN:Cre Ratio",value:ratio.toFixed(1),unit:"",interp,high:ratio>20,low:ratio<10});
  }
  /* 4. ALT:ALP ratio (>2 hepatocellular; <1 cholestatic) */
  const alt=_getLabFloat("lab-alt"),alp=_getLabFloat("lab-alp");
  if(alt!==null&&alp!==null&&alp>0){
    const r=alt/alp;
    const interp=r>2?(currentLang==="ja"?"肝細胞障害優位":"Hepatocellular predominant"):
                 r<1?(currentLang==="ja"?"胆汁うっ滞優位":"Cholestatic predominant"):
                 (currentLang==="ja"?"混合":"Mixed");
    calcs.push({name:"ALT:ALP",value:r.toFixed(2),unit:"",interp});
  }
  /* 5. Na:K ratio (<27 → Addisonian; 27-32 → suspicious; >32 → normal) */
  if(na!==null&&k!==null&&k>0){
    const r=na/k;
    const interp=r<27?(currentLang==="ja"?"アジソン病疑い (<27)":"Addisonian suspicion (<27)"):
                 r<32?(currentLang==="ja"?"要精査 (27-32)":"Borderline (27-32)"):
                 (currentLang==="ja"?"正常":"Normal");
    calcs.push({name:currentLang==="ja"?"Na:K 比":"Na:K Ratio",value:r.toFixed(1),unit:"",interp,low:r<27});
  }
  /* 6. Calcium × Phosphorus product (>70 → soft-tissue mineralization risk) */
  const ph=_getLabFloat("lab-phosphorus");
  if(ca!==null&&ph!==null){
    const prod=ca*ph;
    const high=prod>70;
    const interp=high?(currentLang==="ja"?"Ca×P > 70 軟部組織石灰化リスク":"Ca×P > 70 mineralization risk"):
                 (currentLang==="ja"?"正常":"Normal");
    calcs.push({name:"Ca × P",value:prod.toFixed(1),unit:"",interp,high});
  }
  /* Render */
  if(!calcs.length){
    container.innerHTML=`<div style="font-size:.72rem;color:var(--gray-500);font-style:italic">${currentLang==="ja"?"💡 検査値を入力すると自動計算（アニオンギャップ・補正Ca・BUN:Cre比・Na:K比・Ca×P 等）":"💡 Enter labs above to auto-compute (Anion Gap, corrected Ca, BUN:Cre, Na:K, Ca×P, etc.)"}</div>`;
    return;
  }
  const header=`<div style="font-size:.78rem;font-weight:700;color:var(--navy);margin-bottom:6px">${currentLang==="ja"?"📐 自動計算":"📐 Auto Calculations"}</div>`;
  const items=calcs.map(c=>{
    const color=c.high?"#e74c3c":c.low?"#2980b9":"var(--gray-700)";
    const arrow=c.high?"↑":c.low?"↓":"";
    return`<div class="lab-calc-row" style="display:flex;justify-content:space-between;align-items:center;padding:4px 0;border-bottom:1px dashed var(--gray-200);font-size:.76rem"><span style="font-weight:600">${escapeHtml(c.name)}</span><span style="color:${color};font-weight:700">${escapeHtml(c.value)} ${escapeHtml(c.unit)} ${arrow}</span><span style="color:var(--gray-600);font-size:.72rem;flex:1;text-align:right;margin-left:8px">${escapeHtml(c.interp)}</span></div>`;
  }).join("");
  container.innerHTML=header+items;
}


function buildFieldFallback(label,name){
  if(currentLang==="ja")return `${name}の${label}に関する詳細情報は現在準備中です。`;
  return `Detailed ${label.toLowerCase()} information for ${name} is being prepared.`;
}


function escapeHtml(value){
  return String(value??"").replace(/[&<>"']/g,ch=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[ch]));
}

/* Turn a raw snake_case test id (e.g. "abdominal_ultrasound", "fpl_test") into
   a readable label. Leaves entries that already contain spaces or CJK text
   (already-translated names) untouched, and keeps common abbreviations upper. */
const _TEST_ABBR=new Set(["cbc","pcr","mri","ct","ecg","ekg","crp","bun","alt","alp","ggt","sdma","usg","fpl","cpl","pcv","wbc","plt","t4","fpli","cpli","snap","ofa","csf","fna","tli","ck","ldh","ast","ph"]);
function humanizeTestId(tid){
  if(typeof tid!=="string"||!tid)return tid;
  if(/\s/.test(tid)||/[　-鿿＀-￯]/.test(tid))return tid;
  if(tid.indexOf("_")<0)return _TEST_ABBR.has(tid.toLowerCase())?tid.toUpperCase():tid;
  return tid.split("_").map(p=>_TEST_ABBR.has(p.toLowerCase())?p.toUpperCase():(p.charAt(0).toUpperCase()+p.slice(1))).join(" ");
}

/* --- Modal focus management (a11y) ---
   Saves the trigger element on open so focus can be restored on close,
   moves keyboard focus into the modal, and installs a Tab-cycle trap so
   focus cannot escape into background content. */
const _modalLastFocus=new WeakMap();
const _modalTrapHandlers=new WeakMap();
const _FOCUSABLE_SEL='button:not([disabled]),[href],input:not([disabled]),select:not([disabled]),textarea:not([disabled]),[tabindex]:not([tabindex="-1"])';
function _modalFocusables(modal){
  return Array.from(modal.querySelectorAll(_FOCUSABLE_SEL))
    .filter(el=>el.offsetParent!==null||el.getClientRects().length>0);
}
function openModalA11y(modal,initialFocusSel){
  if(!modal)return;
  const prev=document.activeElement;
  if(prev&&prev!==document.body)_modalLastFocus.set(modal,prev);
  // Defer to allow display:flex / classList transition to apply.
  requestAnimationFrame(()=>{
    let target=null;
    if(initialFocusSel)target=modal.querySelector(initialFocusSel);
    if(!target)target=modal.querySelector(".dashboard-close,[autofocus]")
      ||modal.querySelector(_FOCUSABLE_SEL);
    if(target&&typeof target.focus==="function"){try{target.focus({preventScroll:true});}catch(_){target.focus();}}
  });
  // Tab/Shift+Tab cycling trap. One handler per modal — removed on close.
  if(!_modalTrapHandlers.has(modal)){
    const handler=function(e){
      if(e.key!=="Tab")return;
      if(!modal.classList.contains("open"))return;
      const items=_modalFocusables(modal);
      if(!items.length){e.preventDefault();return;}
      const first=items[0],last=items[items.length-1];
      const active=document.activeElement;
      if(e.shiftKey){
        if(active===first||!modal.contains(active)){e.preventDefault();last.focus();}
      }else{
        if(active===last||!modal.contains(active)){e.preventDefault();first.focus();}
      }
    };
    _modalTrapHandlers.set(modal,handler);
    modal.addEventListener("keydown",handler);
  }
}
function closeModalA11y(modal){
  if(!modal)return;
  const prev=_modalLastFocus.get(modal);
  _modalLastFocus.delete(modal);
  if(prev&&typeof prev.focus==="function"&&document.body.contains(prev)){
    try{prev.focus({preventScroll:true});}catch(_){prev.focus();}
  }
}

/* Product page URLs on caninevet.jp — mirrors api/data/sponsor_adjuncts.PRODUCT_URLS
   (consistency pinned by tests/test_ecvn_pr_label.py). Tapping a product name
   in the sponsor block lands directly on its own product page. */
const ECVN_PRODUCT_URLS={
  "For Joint":"https://www.caninevet.jp/canine%E3%82%B5%E3%83%97%E3%83%AA%E3%83%A1%E3%83%B3%E3%83%88/for-joint/",
  "For Antioxidant":"https://www.caninevet.jp/canine%E3%82%B5%E3%83%97%E3%83%AA%E3%83%A1%E3%83%B3%E3%83%88/for-antioxidant-asta-melon-vitamine-cysteine/",
  "MSM+アミノコンプリート":"https://www.caninevet.jp/canine%E3%82%B5%E3%83%97%E3%83%AA%E3%83%A1%E3%83%B3%E3%83%88/msm-%E3%82%A2%E3%83%9F%E3%83%8E%E3%82%B3%E3%83%B3%E3%83%97%E3%83%AA%E3%83%BC%E3%83%88/",
  "NMNミトコンドリアアシスト":"https://www.caninevet.jp/canine%E3%82%B5%E3%83%97%E3%83%AA%E3%83%A1%E3%83%B3%E3%83%88/nmn-%E3%83%9F%E3%83%88%E3%82%B3%E3%83%B3%E3%83%89%E3%83%AA%E3%82%A2%E3%82%A2%E3%82%B7%E3%82%B9%E3%83%88/",
  "CPパウダー":"https://www.caninevet.jp/canine%E3%82%B5%E3%83%97%E3%83%AA%E3%83%A1%E3%83%B3%E3%83%88/prebiotics-probiotocs-%E3%82%B5%E3%82%A4%E3%83%AA%E3%82%A6%E3%83%A0/",
  "Relax & CBD":"https://www.caninevet.jp/canine%E3%82%B5%E3%83%97%E3%83%AA%E3%83%A1%E3%83%B3%E3%83%88/canine-vet-relax-cbd/",
  "Protain":"https://www.caninevet.jp/canine%E3%82%B5%E3%83%97%E3%83%AA%E3%83%A1%E3%83%B3%E3%83%88/canine-vet-protain/",
  "Booster & Relax":"https://www.caninevet.jp/canine%E3%82%B5%E3%83%97%E3%83%AA%E3%83%A1%E3%83%B3%E3%83%88/canine-vet-booster-relax/",
  "カミデミルク":"https://www.caninevet.jp/canine%E3%82%B5%E3%83%97%E3%83%AA%E3%83%A1%E3%83%B3%E3%83%88/%E3%82%AB%E3%83%9F%E3%83%87%E3%83%9F%E3%83%AB%E3%82%AF-1kg/"
};
function renderTreatmentWithAdjunct(text){
  const raw=String(text??"");
  const marker="[ECVN:Block]";
  const idx=raw.indexOf(marker);
  if(idx===-1) return escapeHtml(raw);
  const main=raw.slice(0,idx).replace(/\s+$/,"");
  let adjunct=raw.slice(idx+marker.length).replace(/^\s+/,"");
  // Drop the data-side header line (【…】 / […]) — the UI supplies its own PR label.
  adjunct=adjunct.replace(/^\s*[【\[][^\n]*\n?/,"").replace(/^\s+/,"");
  let adjHtml=escapeHtml(adjunct).replace(
    /caninevet\.jp/g,
    '<a href="https://www.caninevet.jp/" target="_blank" rel="sponsored noopener noreferrer">caninevet.jp</a>'
  );
  /* Linkify each product name to its caninevet.jp product page (longest name
     first so e.g. "Booster & Relax" is never split by a shorter key). */
  const _pnames=Object.keys(ECVN_PRODUCT_URLS).sort((a,b)=>b.length-a.length);
  for(const pn of _pnames){
    const esc=escapeHtml(pn);
    if(adjHtml.indexOf(esc)===-1)continue;
    adjHtml=adjHtml.split(esc).join(`<a href="${ECVN_PRODUCT_URLS[pn]}" target="_blank" rel="sponsored noopener noreferrer">${esc}</a>`);
  }
  const mainHtml=main?escapeHtml(main):"";
  const en=(typeof currentLang!=="undefined"&&currentLang==="en");
  const labelTxt=en?"PR · Sponsored (adjunct options)":"PR・自社製品（補助療法オプション）";
  const disclaimer=en
    ?"The following is a manufacturer's product promotion, not standard evidence-based treatment."
    :"以下は自社製品の紹介（広告）です。標準治療・エビデンスに基づく治療ではありません。";
  const aria=en?"Sponsored product information (advertisement)":"自社製品の広告（PR）";
  const vendorLink='<a href="https://www.caninevet.jp/" target="_blank" rel="sponsored noopener noreferrer">Equine &amp; Canine Vet Nutrition</a>';
  /* Collapsed by default (<details>): the sponsor note must never compete
     with the treatment protocol or clutter search/reading flows — one tap on
     the compact PR summary expands it, and each product links to its page. */
  return `${mainHtml}<details class="ecvn-adjunct-block" role="complementary" aria-label="${aria}">`
    +`<summary class="ecvn-adjunct-label"><span class="ecvn-pr-badge">PR</span>${escapeHtml(labelTxt)}</summary>`
    +`<div class="ecvn-adjunct-disclaimer">${escapeHtml(disclaimer)} · ${vendorLink}</div>`
    +`<div class="ecvn-adjunct-body">${adjHtml}</div></details>`;
}

// Cache of fetched drug-disease results keyed by `${species}::${diseaseName}::${lang}`
const _diseaseDrugCache=new Map();
function _drugDiseaseCacheKey(species,diseaseName){return `${species||""}::${diseaseName||""}::${currentLang||""}`;}

function buildTreatmentDrugsPlaceholder(species,diseaseName){
  if(!species||!diseaseName) return "";
  const key=_drugDiseaseCacheKey(species,diseaseName);
  const cached=_diseaseDrugCache.get(key);
  const heading=currentLang==="ja"?"治療に関連する薬品":"Related Drugs";
  if(cached){
    if(!cached.length){
      return `<div class="treatment-drugs-section" data-rendered="1"><div class="treatment-drugs-heading">${heading}</div><div class="treatment-drugs-empty">${currentLang==="ja"?"該当薬品なし":"No drug links found"}</div></div>`;
    }
    return _renderTreatmentDrugsList(cached,heading);
  }
  // Async loading placeholder; will be hydrated by hydrateTreatmentDrugs()
  const encSp=escapeHtml(species);
  const encName=escapeHtml(diseaseName);
  return `<div class="treatment-drugs-section" data-treatment-drugs="1" data-species="${encSp}" data-disease="${encName}" data-rendered="0"><div class="treatment-drugs-heading">${heading}</div><div class="treatment-drugs-loading">${currentLang==="ja"?"読み込み中…":"Loading…"}</div></div>`;
}

function _renderTreatmentDrugsList(drugs,heading){
  const items=drugs.slice(0,15).map(d=>{
    const label=currentLang==="ja"?(d.name_ja||d.name||""):(d.name||d.name_ja||"");
    const cat=d.category||"";
    return `<a class="treatment-drug-chip" href="#drugs" data-drug="${escapeHtml(d.name_ja||d.name||"")}"><span class="treatment-drug-name">${escapeHtml(label)}</span>${cat?`<span class="treatment-drug-cat">${escapeHtml(cat)}</span>`:""}</a>`;
  }).join("");
  return `<div class="treatment-drugs-section" data-rendered="1"><div class="treatment-drugs-heading">${heading}</div><div class="treatment-drugs-list">${items}</div></div>`;
}

// --- Reverse direction: drug → diseases (rendered in drug detail panel) ---
const _drugDiseasesCache=new Map();
function _drugDiseasesCacheKey(drugId,species){return `${drugId}::${species||"all"}::${currentLang||""}`;}

function buildDrugDiseasesPlaceholder(drugId){
  if(!drugId) return "";
  const headingJa="この薬品を使う疾患";
  const headingEn="Diseases Treated";
  const heading=currentLang==="ja"?headingJa:headingEn;
  const key=_drugDiseasesCacheKey(drugId,"");
  const cached=_drugDiseasesCache.get(key);
  if(cached!==undefined){
    return _renderDrugDiseasesList(cached,heading,drugId);
  }
  return `<div class="drug-diseases-section" data-drug-diseases="1" data-drug-id="${escapeHtml(drugId)}" data-rendered="0"><div class="drug-diseases-heading">${heading}</div><div class="drug-diseases-loading">${currentLang==="ja"?"読み込み中…":"Loading…"}</div></div>`;
}

function _renderDrugDiseasesList(diseases,heading,drugId){
  if(!diseases||!diseases.length){
    return `<div class="drug-diseases-section" data-rendered="1"><div class="drug-diseases-heading">${heading}</div><div class="drug-diseases-empty">${currentLang==="ja"?"該当疾患なし":"No diseases found"}</div></div>`;
  }
  // Group by species for readability
  const bySpecies=new Map();
  diseases.forEach(d=>{const s=d.species||"";if(!bySpecies.has(s))bySpecies.set(s,[]);bySpecies.get(s).push(d);});
  const urgencyColor={emergency:"badge-emergency",high:"badge-high",urgent:"badge-high",moderate:"badge-moderate",normal:"badge-normal"};
  const groups=[...bySpecies.entries()].map(([sp,list])=>{
    const spObj=SPECIES.find(x=>x.id===sp);
    const spLabel=spObj?(currentLang==="ja"?spObj.name:spObj.nameEn):sp;
    const chips=list.slice(0,12).map(d=>{
      const label=currentLang==="ja"?(d.name_ja||d.name||""):(d.name||d.name_ja||"");
      const urg=d.urgency||"";
      const badge=urg?`<span class="drug-disease-urgency ${urgencyColor[urg]||""}">${escapeHtml(urg)}</span>`:"";
      return `<a class="drug-disease-chip" href="#database" data-disease="${escapeHtml(label)}" data-species="${escapeHtml(sp)}">${escapeHtml(label)}${badge}</a>`;
    }).join("");
    const more=list.length>12?`<span class="drug-disease-more">+${list.length-12}</span>`:"";
    return `<div class="drug-disease-group"><div class="drug-disease-species-label">${escapeHtml(spLabel)} <span class="drug-disease-count">(${list.length})</span></div><div class="drug-disease-chips">${chips}${more}</div></div>`;
  }).join("");
  return `<div class="drug-diseases-section" data-rendered="1"><div class="drug-diseases-heading">${heading} <span class="drug-disease-total">${diseases.length}</span></div>${groups}</div>`;
}

function hydrateDrugDiseases(container){
  const root=container||document;
  const placeholders=root.querySelectorAll('[data-drug-diseases="1"][data-rendered="0"]');
  placeholders.forEach(ph=>{
    const drugId=ph.getAttribute("data-drug-id")||"";
    if(!drugId)return;
    ph.setAttribute("data-rendered","loading");
    const heading=currentLang==="ja"?"この薬品を使う疾患":"Diseases Treated";
    fetchWithTimeout(`/api/drugs/${encodeURIComponent(drugId)}/diseases?limit=80`)
      .then(r=>r.ok?r.json():null)
      .then(data=>{
        const diseases=(data&&Array.isArray(data.diseases))?data.diseases:[];
        _drugDiseasesCache.set(_drugDiseasesCacheKey(drugId,""),diseases);
        const html=_renderDrugDiseasesList(diseases,heading,drugId);
        const wrap=document.createElement("div");
        wrap.innerHTML=html;
        const newNode=wrap.firstElementChild;
        /* Clicks are handled by the delegated .drug-disease-chip handler in
           _attachDbItemHandlers (openDiseaseAcrossSpecies), which also covers the
           cache-rendered path and waits for a cross-species list load instead of
           racing it. No per-node listeners here — they would double-fire. */
        if(newNode&&ph.parentNode)ph.parentNode.replaceChild(newNode,ph);
      })
      .catch(()=>{
        ph.setAttribute("data-rendered","error");
        ph.innerHTML=`<div class="drug-diseases-heading">${heading}</div><div class="drug-diseases-empty">${currentLang==="ja"?"取得に失敗しました":"Failed to load"}</div>`;
      });
  });
}

function hydrateTreatmentDrugs(container){
  // Find unhydrated placeholders within the container and fetch their drug lists
  const root=container||document;
  const placeholders=root.querySelectorAll('[data-treatment-drugs="1"][data-rendered="0"]');
  placeholders.forEach(ph=>{
    const species=ph.getAttribute("data-species")||"";
    const disease=ph.getAttribute("data-disease")||"";
    if(!species||!disease)return;
    const key=_drugDiseaseCacheKey(species,disease);
    // Mark in-flight to avoid duplicate fetches
    ph.setAttribute("data-rendered","loading");
    const params=new URLSearchParams({species,name:disease,lang:currentLang||""});
    fetchWithTimeout("/api/drugs/for-disease?"+params.toString())
      .then(r=>r.ok?r.json():null)
      .then(data=>{
        const drugs=(data&&Array.isArray(data.drugs))?data.drugs:[];
        _diseaseDrugCache.set(key,drugs);
        const heading=currentLang==="ja"?"治療に関連する薬品":"Related Drugs";
        const html=drugs.length
          ? _renderTreatmentDrugsList(drugs,heading)
          : `<div class="treatment-drugs-section" data-rendered="1"><div class="treatment-drugs-heading">${heading}</div><div class="treatment-drugs-empty">${currentLang==="ja"?"該当薬品なし":"No drug links found"}</div></div>`;
        // Replace placeholder element
        const wrap=document.createElement("div");
        wrap.innerHTML=html;
        const newNode=wrap.firstElementChild;
        /* Clicks are handled by the delegated .treatment-drug-chip handlers
           (disease DB list + checker results area), which also cover the
           cache-rendered path. No per-node listeners — they would double-fire. */
        if(newNode&&ph.parentNode)ph.parentNode.replaceChild(newNode,ph);
      })
      .catch(()=>{
        ph.setAttribute("data-rendered","error");
        const heading=currentLang==="ja"?"治療に関連する薬品":"Related Drugs";
        ph.innerHTML=`<div class="treatment-drugs-heading">${heading}</div><div class="treatment-drugs-empty">${currentLang==="ja"?"取得に失敗しました":"Failed to load"}</div>`;
      });
  });
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
      const doi=r.doi?`<a href="https://doi.org/${encodeURIComponent(r.doi)}" target="_blank" rel="noopener noreferrer" style="color:var(--green);font-size:.78rem">DOI</a>`:"";
      const pmid=r.pmid?`<a href="https://pubmed.ncbi.nlm.nih.gov/${encodeURIComponent(r.pmid)}/" target="_blank" rel="noopener noreferrer" style="color:var(--blue,#2563eb);font-size:.78rem">PMID</a>`:"";
      const evid=r.evidence_level?`<span style="font-size:.75rem;color:var(--gray-500)">[${escapeHtml(r.evidence_level)}]</span>`:"";
      const links=[doi,pmid].filter(Boolean).join(" ");
      return `<li style="margin-bottom:4px"><span style="font-weight:600">${escapeHtml(authors)} (${year})</span> ${escapeHtml(r.title||"")}. ${journal}${vol}${pages}. ${links} ${evid}</li>`;
    }).join("");
    return `<div style="margin-top:8px"><div style="font-size:.8rem;font-weight:700;color:var(--gray-600);margin-bottom:4px">${sec.label}</div><ul style="list-style:none;padding:0;margin:0;font-size:.82rem;color:var(--gray-700)">${items}</ul></div>`;
  }).filter(Boolean).join("");
  if(!rendered)return "";
  return `<div class="ortho-refs" style="margin-top:12px;padding:10px;background:var(--gray-50,#f9fafb);border-radius:6px;border-left:3px solid var(--green)"><div style="font-size:.78rem;font-weight:700;text-transform:uppercase;letter-spacing:.05em;color:var(--green);margin-bottom:6px">📚 ${currentLang==="ja"?"参考文献（エビデンスベース）":"References (Evidence-based)"}</div>${rendered}</div>`;
}

/* Map a content field id (e.g. "treatment", "pathophysiology_ja") to a readable
   bilingual label so quality notes never expose raw internal field names. */
const _FIELD_LABEL_KEYS={description:"dtDescription",pathophysiology:"dtPathophysiology",causes:"dtCauses",prevention:"dtPrevention",treatment:"dtTreatment",prognosis:"dtPrognosis",clinical_signs:"dtClinicalSigns",diagnosis:"dtDiagnosis",transmission:"dtTransmission"};
function fieldLabel(field){
  const base=String(field||"").replace(/_ja$/,"");
  const key=_FIELD_LABEL_KEYS[base];
  if(key){const v=t(key);if(v&&v!==key)return v;}
  return base.replace(/_/g," ").replace(/\b\w/g,c=>c.toUpperCase());
}
/* "Data needs review" note: collapse _ja variants, drop the always auto-generated
   per-query summary fields (they aren't clinical-data gaps), and show readable
   labels. Returns "" when nothing meaningful is missing. */
function renderDataReviewNote(item){
  const raw=(item&&Array.isArray(item.missing_fields))?item.missing_fields:[];
  const seen=new Set();
  const labels=[];
  raw.forEach(f=>{
    const base=String(f||"").replace(/_ja$/,"");
    if(!base||base==="symptoms_summary"||base==="literature_summary"||seen.has(base))return;
    seen.add(base);
    labels.push(fieldLabel(base));
  });
  if(!labels.length)return "";
  return `<div class="missing-note">${currentLang==="ja"?"AI補完項目（要獣医師確認）":"AI-generated (clinician review advised)"}: ${escapeHtml(labels.join(", "))}</div>`;
}
function contentOriginLabel(origin){
  const map=currentLang==="ja"
    ?{sourced:"出典あり",mixed:"一部AI補完",generated:"AI生成"}
    :{sourced:"Sourced",mixed:"Partially AI-generated",generated:"AI-generated"};
  return map[origin]||origin;
}

function renderReferenceLinks(item){
  const refs=(item&&Array.isArray(item.evidence_sources))?item.evidence_sources:[];
  if(!refs.length)return "";
  const label=currentLang==="ja"?"参考文献":"References";
  return `<div class="missing-note">${label}: ${refs.map(r=>`<a href="${r&&r.url?sanitizeUrl(r.url):"#"}" target="_blank" rel="noopener noreferrer">${escapeHtml(r&&r.name)}</a>`).join(" | ")}</div>`;
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
  const label=currentLang==="ja"?"引用対応":"Citation map";
  return `<div class="missing-note">${label}: ${entries.map(([k,ids])=>`${escapeHtml(fieldLabel(k))} → ${ids.map(id=>idToNumber[id]?`[${escapeHtml(idToNumber[id])}]`:escapeHtml(id)).join(", ")}`).join(" / ")}</div>`;
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
      btn.type="button";
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
  .catch(err=>{debugWarn("related-symptoms fetch failed:",err);});
}

function doAnalyze(){
  if(!currentSpecies||selectedSymptoms.size===0)return;
  showRelatedSuggestions();
  /* Kick off the contraindication-rules fetch in parallel with the analysis so
     the "anesthesia considerations" box can render on the results (the rules
     used to load only when the anesthesia tab was opened first). */
  ensureAnesthesiaContraRules();
  trackEvent("analyze_symptoms",{species:currentSpecies,symptom_count:selectedSymptoms.size});
  const btn=document.getElementById("analyzeBtn");if(btn){btn.disabled=true;btn.innerHTML=`<span class="spinner"></span> ${t("analyzing")}`;}
  const progress=document.getElementById("analyzeProgress");
  if(progress)progress.classList.add("active");
  const payload={species:currentSpecies,symptoms:[...selectedSymptoms],lang:currentLang};
  if(currentBreed)payload.breed=currentBreed;
  const labVals=collectLabValues();
  if(labVals)payload.lab_values=labVals;
  const painVal=collectPainScore();
  if(painVal!==null)payload.pain_score=painVal;
  const slowTimer=setTimeout(()=>{btn.innerHTML=`<span class="spinner"></span> ${t("analyzeSearchingDb")}`;},3000);
  fetchWithTimeout("/api/analyze-symptoms",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)})
  .then(r=>{if(!r.ok)throw new Error(`HTTP ${r.status}: ${r.statusText}`);return r.json();})
  .then(data=>{clearTimeout(slowTimer);renderResults(data);trackEvent("view_results",{species:currentSpecies,result_count:data.suspected_diseases?.length||0,symptom_count:selectedSymptoms.size});if(typeof showToast==="function"){const n=data.suspected_diseases?.length||0;if(n>0)showToast(t("diseasesFoundToast").replace("%n%",n),"success");else showToast(t("diseasesNoneFoundToast"),"warning");}const ra=document.getElementById("resultsArea");if(ra)scrollToAnchor(ra);})
  .catch(err=>{trackEvent("api_error",{endpoint:"analyze-symptoms",error:String(err.message||"unknown").substring(0,100),species:currentSpecies});const ra=document.getElementById("resultsArea");if(ra){const info=describeFetchError(err);const detailHtml=info.detail?`<div class="results-error-detail">${escapeHtml(t("networkErrorDetail")+info.detail)}</div>`:"";ra.innerHTML=`<div class="results-error" role="alert"><strong>${escapeHtml(info.title)}</strong>${detailHtml}<button class="retry-analyze-btn" type="button">${escapeHtml(t("retry"))}</button></div>`;const retryBtn=ra.querySelector(".retry-analyze-btn");if(retryBtn){retryBtn.addEventListener("click",doAnalyze);setTimeout(()=>retryBtn.focus(),50);}}})
  .finally(()=>{clearTimeout(slowTimer);if(btn){btn.disabled=false;btn.textContent=t("analyzeBtn");}if(progress)progress.classList.remove("active");});
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
  w.innerHTML='<span data-i18n="feedbackQuestion">'+t("feedbackQuestion")+'</span><div class="feedback-btns"><button type="button" class="feedback-btn helpful">&#128077; '+t("feedbackYes")+'</button><button type="button" class="feedback-btn not-helpful">&#128078; '+t("feedbackNo")+'</button></div>';
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
    ?`【VetDict 鑑別診断結果】\n動物種: ${spLabel}\n症状: ${sympList}\n\n${diseaseLines}\n\n※ 鑑別の参考情報です。最終診断は臨床所見・検査結果と併せてご判断ください。\n${shareUrl}`
    :`[VetDict Differential Diagnosis]\nSpecies: ${spLabel}\nSymptoms: ${sympList}\n\n${diseaseLines}\n\nNote: differential reference only. Integrate with clinical findings and diagnostic results.\n${shareUrl}`;
  w.innerHTML=`<span>${t("shareResults")}</span><div class="share-btns"><a href="${twitterUrl}" target="_blank" rel="noopener noreferrer" class="share-btn twitter">X</a><a href="${lineUrl}" target="_blank" rel="noopener noreferrer" class="share-btn line">LINE</a><button type="button" class="share-btn copy">${t("shareCopy")}</button><button type="button" class="share-btn copy-full" style="background:var(--navy)">${currentLang==="ja"?"詳細コピー":"Copy Full"}</button></div>`;
  w.querySelector(".share-btn.twitter").addEventListener("click",function(){trackEvent("share_results",{method:"twitter",species:currentSpecies});});
  w.querySelector(".share-btn.line").addEventListener("click",function(){trackEvent("share_results",{method:"line",species:currentSpecies});});
  function _bindCopy(btn,text,trackMethod){
    if(!btn)return;
    btn.dataset.origText=btn.textContent;
    btn.addEventListener("click",function(){
      if(btn.dataset.busy==="1")return;
      btn.dataset.busy="1";
      const orig=btn.dataset.origText;
      copyToClipboard(text).then(ok=>{
        btn.textContent=ok?t("shareCopied"):(currentLang==="ja"?"コピー失敗":"Copy failed");
        if(ok)trackEvent("share_results",{method:trackMethod,species:currentSpecies});
        if(btn._restoreTimer)clearTimeout(btn._restoreTimer);
        btn._restoreTimer=setTimeout(()=>{btn.textContent=orig;btn.dataset.busy="0";},2000);
      });
    });
  }
  _bindCopy(w.querySelector(".share-btn.copy"),shareText+" "+shareUrl,"copy");
  _bindCopy(w.querySelector(".share-btn.copy-full"),fullText,"copy_full");
  return w;
}

/* Initial-display caps for differential cards. The engine returns the full
   ranked list (often 100+ low-match entries), but showing every card at once
   buries the clinically relevant differentials. We render a focused set and
   tuck the long tail behind a "show more" toggle (all cards stay in the DOM,
   so search/print/expand-all keep working). */
const DX_CAP_COMMON=12,DX_CAP_RARE=6,DX_CAP_FLAT=15;
function renderDxCards(diseases,data,cap){
  let out="";
  diseases.forEach((d,i)=>{
    let card=renderDiseaseCard(d,data);
    if(i>=cap)card=card.replace('<div class="disease-result ','<div class="disease-result dx-hidden ');
    out+=card;
  });
  if(diseases.length>cap){
    const more=diseases.length-cap;
    const label=currentLang==="ja"?`さらに${more}件の鑑別を表示`:`Show ${more} more differential${more!==1?"s":""}`;
    out+=`<button type="button" class="dx-show-more" data-action="dx-show-more" aria-label="${label}">${label} ▾</button>`;
  }
  return out;
}

function renderResults(data){
  updateCheckerProgress(3);
  _cardIndex=0;
  const area=document.getElementById("resultsArea");
  const diseases=data.suspected_diseases||data.possible_conditions||[];
  const diseasesByPhase=data.suspected_diseases_by_phase||{};
  const tests=data.recommended_tests_display||data.recommended_tests||[];
  const severity=data.severity||"low";
  const adviceJa=data.general_advice_ja||"";
  if(diseases.length===0){
    const tipsJa=[
      "\u75c7\u72b6\u30921\u301c2\u500b\u306b\u7d5e\u308a\u8fbc\u307f\u3001\u6700\u3082\u9855\u8457\u306a\u3082\u306e\u304b\u3089\u691c\u7d22\u3057\u3066\u307f\u3066\u304f\u3060\u3055\u3044",
      "\u4ee3\u66ff\u8868\u73fe\uff08\u4f8b: \u300c\u4e0b\u75e2\u300d\u2194\u300c\u8edf\u4fbf\u300d\u3001\u300cPU/PD\u300d\u2194\u300c\u591a\u98f2\u591a\u5c3f\u300d\uff09\u3092\u8a66\u3057\u3066\u304f\u3060\u3055\u3044",
      "\u75c7\u72b6\u540d\u3092\u82f1\u8a9e\u307e\u305f\u306f\u65e5\u672c\u8a9e\u306b\u5207\u308a\u66ff\u3048\u3066\u691c\u7d22",
      "\u95a2\u9023\u75c7\u72b6\uff08\u98df\u6b32\u30fb\u5143\u6c17\u30fb\u4f53\u91cd\u5909\u5316\u306a\u3069\uff09\u3092\u8ffd\u52a0",
    ];
    const tipsEn=[
      "Try narrowing to 1\u20132 most prominent symptoms",
      "Try synonyms (e.g., 'diarrhea' \u2194 'loose stool', 'PU/PD' \u2194 'polyuria/polydipsia')",
      "Switch language and try the symptom name in English or Japanese",
      "Add related vital signs (appetite, energy, weight change)",
    ];
    const tips=currentLang==="ja"?tipsJa:tipsEn;
    const heading=currentLang==="ja"?"\u8a72\u5f53\u3059\u308b\u75be\u60a3\u304c\u898b\u3064\u304b\u308a\u307e\u305b\u3093\u3067\u3057\u305f":"No matching diseases found";
    const subheading=currentLang==="ja"?"\u9451\u5225\u7cbe\u5ea6\u3092\u4e0a\u3052\u308b\u305f\u3081\u306e\u30d2\u30f3\u30c8:":"Try these tips to improve matching:";
    area.innerHTML=`<div class="results-empty"><span class="big-icon">\ud83d\udd0d</span><p style="font-weight:600;color:var(--navy);margin-bottom:6px">${escapeHtml(heading)}</p><p style="font-size:.82rem;color:var(--gray-600);margin-bottom:10px">${escapeHtml(subheading)}</p><ul style="text-align:left;display:inline-block;margin:0 auto;padding-left:18px;font-size:.82rem;color:var(--gray-700);line-height:1.6">${tips.map(x=>`<li>${escapeHtml(x)}</li>`).join("")}</ul></div>`;
    return;
  }
  const sevLabels=t("sevLabels");
  let html=`<div class="severity-bar ${severity}">${t("overallAssessment")}${sevLabels[severity]||severity}</div>`;
  /* Low-confidence warning: alert when symptom count <=2 or top confidence <50% */
  const topPct=diseases[0]?diseases[0].match_percent||diseases[0].confidence||0:0;
  const symCount=selectedSymptoms?selectedSymptoms.size:0;
  if(symCount<=2||topPct<50){
    const warnMsg=currentLang==="ja"
      ?`⚠ 入力症状が${symCount}個${symCount<=2?"（推奨: 3個以上）":""}のため、鑑別精度が制限されています（最高信頼度 ${topPct.toFixed(1)}%）。症状を追加すると精度が大幅に向上します。`
      :`⚠ With only ${symCount} symptom${symCount!==1?"s":""} entered${symCount<=2?" (3+ recommended)":""}, diagnostic accuracy is limited (top confidence ${topPct.toFixed(1)}%). Adding more symptoms will significantly improve results.`;
    /* One-tap pivot into the guided consultation: the structured step-by-step
       questioning is exactly the remedy this banner recommends. Species carries
       over (guided flow reads currentSpecies). Routed by the delegated handler. */
    const consultLabel=currentLang==="ja"?"🩺 問診モードで症状を段階的に確認する":"🩺 Continue in guided consultation";
    html+=`<div role="status" aria-live="polite" style="padding:10px 14px;margin-bottom:12px;border-radius:var(--radius);font-size:.82rem;font-weight:500;background:#fef3c7;border-left:4px solid #f59e0b;color:#92400e">${warnMsg}<div style="margin-top:8px"><button type="button" class="guided-consult-link">${consultLabel} →</button></div></div>`;
  }
  /* Next steps banner based on severity */
  const nextSteps=currentLang==="ja"?{
    emergency:"⚠️ 緊急トリアージ：安定化を最優先し、緊急対応・必要に応じ二次診療施設への紹介を。",
    high:"🔴 高リスク：24時間以内の精査（血液検査・画像診断等）と治療介入を優先。",
    moderate:"🟡 中等度：数日以内の精査を。追加検査で鑑別を絞り込んでください。",
    low:"🟢 低リスク：経過観察。症状の持続・悪化があれば精査を検討。",
  }:{
    emergency:"⚠️ Emergency triage: prioritize stabilization and emergency management; refer to a 24h/specialty facility if needed.",
    high:"🔴 High risk: prioritize diagnostic workup (bloodwork, imaging) and intervention within 24 hours.",
    moderate:"🟡 Moderate: evaluate within a few days; narrow the differential with targeted diagnostics.",
    low:"🟢 Low risk: monitor; pursue workup if symptoms persist or worsen.",
  };
  if(nextSteps[severity])html+=`<div style="padding:10px 14px;margin-bottom:12px;border-radius:var(--radius);font-size:.84rem;font-weight:500;background:var(--gray-50);border-left:4px solid ${severity==='emergency'||severity==='high'?'#ef4444':severity==='moderate'?'#f59e0b':'#22a853'}">${nextSteps[severity]}</div>`;
  html+=`<div class="results-sort-bar" role="group" aria-label="${currentLang==="ja"?"結果の並び替え":"Sort results"}"><span style="font-size:.74rem;color:var(--gray-500)">${currentLang==="ja"?"並び替え:":"Sort:"}</span><button type="button" class="results-sort-btn active" data-sort="default" aria-pressed="true">${t("sortByDefault")}</button><button type="button" class="results-sort-btn" data-sort="confidence" aria-pressed="false">${t("sortByConfidence")}</button><button type="button" class="results-sort-btn" data-sort="severity" aria-pressed="false">${t("sortBySeverity")}</button></div>`;
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
    const ps=Math.max(0,Math.min(4,parseInt(data.pain_score,10)||0));
    const painLabels=t("painLabels")||["No Pain","Mild","Moderate","Severe","Excruciating"];
    const painColors=["#16a34a","#65a30d","#eab308","#ea580c","#dc2626"];
    const painPct=ps*25;
    html+=`<div class="lab-results-viz" style="border-color:${painColors[ps]}33"><div class="lab-viz-title" style="color:${painColors[ps]}">&#x1F9D1;&#x200D;&#x2695;&#xFE0F; ${currentLang==="ja"?"痛み評価":"Pain Assessment"}: ${painLabels[ps]} (${ps}/4)</div><div class="pain-meter"><div class="pain-meter-fill" style="width:${painPct}%;background:${painColors[ps]}"></div></div>${ps>=3?`<div style="font-size:.74rem;color:${painColors[ps]};margin-top:4px;font-weight:600">${currentLang==="ja"?"⚠ 強い痛みが検出されました。早急な鎮痛処置を検討してください。":"⚠ Severe pain detected. Consider immediate analgesic intervention."}</div>`:""}</div>`;
  }
  const adviceText=currentLang==="ja"?adviceJa:(data.general_advice||adviceJa);
  if(adviceText)html+=`<div style="font-size:.82rem;color:var(--gray-700);margin-bottom:12px;padding:8px 12px;background:var(--gray-50);border-radius:var(--radius)">${escapeHtml(adviceText)}</div>`;

  // Stepwise differential diagnosis: Phase 1 (common) vs Phase 2 (rare)
  const phase1=diseasesByPhase.phase_1_common||[];
  const phase2=diseasesByPhase.phase_2_rare||[];

  html+=`<div class="results-cards-area">`;
  // Render Phase 1 (Common/Very Common)
  if(phase1.length>0){
    html+=`<div class="dx-group" style="margin-bottom:16px"><div style="font-size:.86rem;font-weight:700;color:var(--green);padding:8px 12px;background:rgba(34,168,79,.08);border-left:4px solid var(--green);border-radius:var(--radius);margin-bottom:10px">🎯 ${currentLang==="ja"?"最初に検討すべき疾患（よくある疾患）":"Primary Differential (Common diseases)"}</div>`;
    html+=renderDxCards(phase1,data,DX_CAP_COMMON);
    html+=`</div>`;
  }

  // Render Phase 2 (Uncommon/Rare)
  if(phase2.length>0){
    html+=`<div class="dx-group" style="margin-bottom:16px"><div style="font-size:.86rem;font-weight:700;color:var(--orange);padding:8px 12px;background:rgba(240,133,14,.08);border-left:4px solid var(--orange);border-radius:var(--radius);margin-bottom:10px">🔍 ${currentLang==="ja"?"さらに検討すべき疾患（稀な疾患）":"Secondary Differential (Rare/Uncommon diseases)"}</div>`;
    html+=renderDxCards(phase2,data,DX_CAP_RARE);
    html+=`</div>`;
  }

  // Fallback: render all diseases if no phase info
  if(phase1.length===0&&phase2.length===0){
    html+=`<div class="dx-group">${renderDxCards(diseases,data,DX_CAP_FLAT)}</div>`;
  }
  html+=`</div>`;

  if(tests.length){html+=`<div style="margin-top:16px"><strong style="font-size:.86rem">${t("dtRecTestList")}</strong><ul class="test-list">${tests.map(x=>{let label;if(typeof x==="string"){label=humanizeTestId(x);}else{label=currentLang==="ja"?(x.name_ja||x.name_en||x.name||x.id):(x.name_en||x.name||x.name_ja||x.id);}const priority=x.priority?` <span style="color:var(--gray-500);font-size:.75rem">[${escapeHtml(x.priority)}]</span>`:"";return`<li>\u{1F52C} ${escapeHtml(label)}${priority}</li>`;}).join("")}</ul></div>`;}
  html+=`<div id="commonDiseasesArea"></div><div id="breedEcologyArea"></div>`;
  area.innerHTML="";
  area.appendChild(createResultsDisclaimer());
  const contentDiv=document.createElement("div");
  contentDiv.innerHTML=html;
  /* Disease card expand/collapse — event delegation on contentDiv */
  contentDiv.addEventListener("click",function(e){
    const moreBtn=e.target.closest(".dx-show-more");
    if(moreBtn){
      const parent=moreBtn.parentElement;
      if(parent)parent.querySelectorAll(".disease-result.dx-hidden").forEach(c=>c.classList.remove("dx-hidden"));
      moreBtn.remove();
      return;
    }
    const drugLink=e.target.closest(".drug-nav-link");
    if(drugLink){e.preventDefault();navigateToDrug(drugLink.dataset.drug);return;}
    const dbLink=e.target.closest(".disease-db-nav-link");
    if(dbLink){e.preventDefault();navigateToDiseaseDb(dbLink.dataset.name);return;}
    /* Cache-rendered related-drug chips carry no per-node listeners — delegate. */
    const tChip=e.target.closest(".treatment-drug-chip");
    if(tChip){e.preventDefault();navigateToDrug(tChip.dataset.drug);return;}
    /* Anesthesia-considerations footer: jump to the species-synced anesthesia tab. */
    const anesthLink=e.target.closest(".anesthesia-nav-link");
    if(anesthLink){e.preventDefault();_pushNavHistory(currentView,"anesthesia","");switchView("anesthesia");_showBackNav("anesthesiaBackNav","anesthesiaSearch");const p=document.getElementById("viewAnesthesia");if(p)scrollToAnchor(p);return;}
    /* Low-confidence banner: one-tap pivot into the guided consultation with
       the checker's species carried over, landing scrolled to the chat panel. */
    const consultLink=e.target.closest(".guided-consult-link");
    if(consultLink){
      e.preventDefault();
      trackEvent("guided_consult_from_checker",{species:currentSpecies||"dog"});
      switchView("chat");
      switchChatMode("guided");
      const p=document.getElementById("viewChat");
      if(p)scrollToAnchor(p);
      return;
    }
    if(e.target.closest("a"))return;
    const head=e.target.closest(".disease-head");
    if(head)toggleDetail(head);
  });
  contentDiv.addEventListener("keydown",function(e){if(e.key==="Enter"||e.key===" "){const head=e.target.closest(".disease-head");if(head){e.preventDefault();toggleDetail(head);}}});
  /* Sort buttons — "default" restores phase grouping; others render a flat sorted list */
  contentDiv.addEventListener("click",function(e){
    const sortBtn=e.target.closest(".results-sort-btn");
    if(!sortBtn)return;
    contentDiv.querySelectorAll(".results-sort-btn").forEach(b=>{b.classList.remove("active");b.setAttribute("aria-pressed","false");});
    sortBtn.classList.add("active");
    sortBtn.setAttribute("aria-pressed","true");
    const mode=sortBtn.dataset.sort;
    const cardsArea=contentDiv.querySelector(".results-cards-area");
    if(!cardsArea)return;
    _cardIndex=0;
    if(mode==="default"){
      let groupHtml="";
      if(phase1.length>0){
        groupHtml+=`<div class="dx-group" style="margin-bottom:16px"><div style="font-size:.86rem;font-weight:700;color:var(--green);padding:8px 12px;background:rgba(34,168,79,.08);border-left:4px solid var(--green);border-radius:var(--radius);margin-bottom:10px">🎯 ${currentLang==="ja"?"最初に検討すべき疾患（よくある疾患）":"Primary Differential (Common diseases)"}</div>`;
        groupHtml+=renderDxCards(phase1,data,DX_CAP_COMMON);
        groupHtml+=`</div>`;
      }
      if(phase2.length>0){
        groupHtml+=`<div class="dx-group" style="margin-bottom:16px"><div style="font-size:.86rem;font-weight:700;color:var(--orange);padding:8px 12px;background:rgba(240,133,14,.08);border-left:4px solid var(--orange);border-radius:var(--radius);margin-bottom:10px">🔍 ${currentLang==="ja"?"さらに検討すべき疾患（稀な疾患）":"Secondary Differential (Rare/Uncommon diseases)"}</div>`;
        groupHtml+=renderDxCards(phase2,data,DX_CAP_RARE);
        groupHtml+=`</div>`;
      }
      if(phase1.length===0&&phase2.length===0){
        groupHtml+=`<div class="dx-group">${renderDxCards(diseases,data,DX_CAP_FLAT)}</div>`;
      }
      cardsArea.innerHTML=groupHtml;
      return;
    }
    const sevOrder={emergency:0,high:1,moderate:2,low:3};
    let sorted=[...diseases];
    if(mode==="confidence")sorted.sort((a,b)=>(b.match_percent||b.confidence||0)-(a.match_percent||a.confidence||0));
    else if(mode==="severity")sorted.sort((a,b)=>(sevOrder[a.severity]??4)-(sevOrder[b.severity]??4));
    cardsArea.innerHTML=`<div class="dx-group">${renderDxCards(sorted,data,DX_CAP_FLAT)}</div>`;
  });
  area.appendChild(contentDiv);
  area.appendChild(createFeedbackWidget());
  area.appendChild(createShareWidget(diseases));
  area.appendChild(createPrintButton());
  loadCommonDiseases(currentSpecies);
  loadBreedEcology(currentSpecies,currentBreed);
  /* Hydrate treatment-drug placeholders within result cards (async fetch) */
  if(typeof hydrateTreatmentDrugs==="function")hydrateTreatmentDrugs(area);
  /* Save diagnosis to history (localStorage) */
  saveDiagnosisHistory(data,diseases);
}

/* ===== Print / Export ===== */
function createPrintButton(){
  const wrap=document.createElement("div");
  wrap.className="results-actions-bar";
  wrap.style.cssText="display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin:12px auto";
  const btn=document.createElement("button");
  btn.type="button";
  btn.className="print-results-btn";
  btn.style.cssText="padding:10px 24px;background:var(--white);border:2px solid var(--navy);color:var(--navy);border-radius:8px;font-size:.84rem;font-weight:600;cursor:pointer";
  btn.textContent=currentLang==="ja"?"🖨 印刷／PDF保存":"🖨 Print / Save PDF";
  btn.title=currentLang==="ja"?"ブラウザ印刷で「PDFに保存」を選択するとPDF化できます":"Use browser print dialog \"Save as PDF\" option";
  btn.addEventListener("click",function(){
    trackEvent("print_results",{species:currentSpecies});
    document.body.classList.add("print-mode-results");
    // Auto-expand all closed disease details for printing
    document.querySelectorAll(".disease-detail").forEach(d=>{if(!d.classList.contains("open"))d.classList.add("print-expanded");});
    setTimeout(()=>{
      window.print();
      // Cleanup after print dialog closes
      setTimeout(()=>{
        document.body.classList.remove("print-mode-results");
        document.querySelectorAll(".disease-detail.print-expanded").forEach(d=>d.classList.remove("print-expanded"));
      },500);
    },50);
  });
  wrap.appendChild(btn);
  /* JSON export of result data */
  const jsonBtn=document.createElement("button");
  jsonBtn.className="export-results-btn";
  jsonBtn.style.cssText="padding:10px 24px;background:var(--white);border:2px solid var(--green);color:var(--green);border-radius:8px;font-size:.84rem;font-weight:600;cursor:pointer";
  jsonBtn.textContent=currentLang==="ja"?"💾 結果をJSON保存":"💾 Export JSON";
  jsonBtn.addEventListener("click",function(){
    try{
      const history=loadDiagnosisHistory();
      const latest=history[0];
      if(!latest)return;
      const blob=new Blob([JSON.stringify(latest,null,2)],{type:"application/json"});
      const url=URL.createObjectURL(blob);
      const a=document.createElement("a");
      a.href=url;a.download=`vetdict-case-${new Date().toISOString().slice(0,10)}.json`;
      document.body.appendChild(a);a.click();
      setTimeout(()=>{document.body.removeChild(a);URL.revokeObjectURL(url);},300);
      trackEvent("export_case_json",{species:currentSpecies});
    }catch(e){if(typeof showToast==="function")showToast(currentLang==="ja"?"エクスポート失敗":"Export failed","error");}
  });
  wrap.appendChild(jsonBtn);
  return wrap;
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

/* --- Dashboard modal: detailed VetDict statistics --- */
let _dashboardLoaded=false;
let _dashboardCache=null;

function openDashboard(){
  trackEvent("open_dashboard");
  if(_dashboardLoaded&&_dashboardCache){
    _showDashboardModal(_dashboardCache);
    return;
  }
  // Show loading skeleton
  _showDashboardModal(null);
  fetchWithTimeout("/api/dashboard-stats/detailed")
    .then(r=>r.ok?r.json():null)
    .then(data=>{
      if(!data)return;
      _dashboardCache=data;
      _dashboardLoaded=true;
      _showDashboardModal(data);
    })
    .catch(err=>{
      const body=document.getElementById("dashboardModalBody");
      if(body)body.innerHTML=`<div style="padding:24px;text-align:center;color:var(--gray-500)">${currentLang==="ja"?"統計の取得に失敗しました":"Failed to load statistics"}<br><small>${escapeHtml(err.message||"")}</small></div>`;
    });
}

function _showDashboardModal(data){
  let modal=document.getElementById("dashboardModal");
  if(!modal){
    modal=document.createElement("div");
    modal.id="dashboardModal";
    modal.className="dashboard-modal";
    modal.setAttribute("role","dialog");
    modal.setAttribute("aria-modal","true");
    modal.setAttribute("aria-labelledby","dashboardTitle");
    modal.innerHTML=`<div class="dashboard-backdrop"></div><div class="dashboard-panel"><div class="dashboard-header"><h2 id="dashboardTitle">${currentLang==="ja"?"📊 統計ダッシュボード":"📊 Statistics Dashboard"}</h2><button class="dashboard-close" aria-label="${currentLang==="ja"?"閉じる":"Close"}">✕</button></div><div class="dashboard-body" id="dashboardModalBody"><div class="dashboard-loading">${currentLang==="ja"?"読み込み中…":"Loading…"}</div></div></div>`;
    document.body.appendChild(modal);
    modal.querySelector(".dashboard-close").addEventListener("click",closeDashboard);
    modal.querySelector(".dashboard-backdrop").addEventListener("click",closeDashboard);
    document.addEventListener("keydown",e=>{if(e.key==="Escape"&&modal.classList.contains("open"))closeDashboard();});
  }
  modal.classList.add("open");
  document.body.style.overflow="hidden";
  openModalA11y(modal,".dashboard-close");
  if(!data)return;
  const body=document.getElementById("dashboardModalBody");
  if(!body)return;
  body.innerHTML=_renderDashboardContent(data);
}

function closeDashboard(){
  const modal=document.getElementById("dashboardModal");
  if(modal)modal.classList.remove("open");
  document.body.style.overflow="";
  closeModalA11y(modal);
}

/* --- In-app Help / Tour modal (educational content) --- */
function openHelpGuide(){
  trackEvent("open_help_guide");
  let modal=document.getElementById("helpGuideModal");
  if(!modal){
    modal=document.createElement("div");
    modal.id="helpGuideModal";
    modal.className="dashboard-modal";
    modal.setAttribute("role","dialog");
    modal.setAttribute("aria-modal","true");
    modal.setAttribute("aria-labelledby","helpGuideTitle");
    modal.innerHTML=`<div class="dashboard-backdrop"></div><div class="dashboard-panel"><div class="dashboard-header"><h2 id="helpGuideTitle">${currentLang==="ja"?"📖 "+t("helpTitle"):"📖 "+t("helpTitle")}</h2><button class="dashboard-close" aria-label="${t("helpClose")}">✕</button></div><div class="dashboard-body">${_renderHelpGuideContent()}</div></div>`;
    document.body.appendChild(modal);
    modal.querySelector(".dashboard-close").addEventListener("click",closeHelpGuide);
    modal.querySelector(".dashboard-backdrop").addEventListener("click",closeHelpGuide);
    document.addEventListener("keydown",e=>{if(e.key==="Escape"&&modal.classList.contains("open"))closeHelpGuide();});
  } else {
    /* Refresh content for language change */
    const body=modal.querySelector(".dashboard-body");
    if(body)body.innerHTML=_renderHelpGuideContent();
  }
  modal.classList.add("open");
  document.body.style.overflow="hidden";
  openModalA11y(modal,".dashboard-close");
}

function closeHelpGuide(){
  const modal=document.getElementById("helpGuideModal");
  if(modal)modal.classList.remove("open");
  document.body.style.overflow="";
  closeModalA11y(modal);
}

function _renderHelpGuideContent(){
  const isJa=currentLang==="ja";
  const sections=isJa?[
    {
      title:"🩺 1. 鑑別診断（症状チェッカー）",
      steps:[
        "対応動物種（21種）から該当する種を選択",
        "観察された臨床症状をチェックボックスで選択（複数可）",
        "任意：血液検査値・痛みスコア・年齢・品種を入力",
        "「鑑別診断を実行」で IDF重み付け＋特異度＋有病率補正のランキング表示",
        "各候補をクリックで病態生理・治療プロトコル・関連薬品を確認",
      ],
      tips:"💡 症状3つ以上で精度が向上。検査値が入力されると lab_factor (最大1.4倍) でスコア調整",
    },
    {
      title:"💬 2. AI 臨床相談チャット",
      steps:[
        "自由入力モード：自然言語で症状を記述（「3日前から嘔吐と下痢」等）",
        "問診モード：カテゴリ→症状→年齢→犬種→診断 のステップバイステップ",
        "AI が onset/age/breed を自動抽出して鑑別ランキングに反映",
        "結果はリアルタイムで確信度バーと共に表示",
      ],
      tips:"💡 「3週間前」「2ヶ月前」等の時間表現を自動認識し急性/亜急性/慢性を判定",
    },
    {
      title:"💊 3. 薬品辞書（600+薬品）",
      steps:[
        "薬品名（日英）・カテゴリ・動物種でフィルタ検索",
        "種別の安全性 ✓/✗ と用量（mg/kg）を表示",
        "体重を入力すると計算用量を自動表示",
        "薬物相互作用は重要度別（⛔ MAJOR / ⚠️ MODERATE / ℹ️ MINOR）で表示",
        "「この薬品を使う疾患」リンクで逆方向ナビゲーション",
      ],
      tips:"💡 治療プロトコル中の薬品名をクリックすると、そのまま薬品詳細にジャンプ",
    },
    {
      title:"💉 4. 鎮静・麻酔プロトコル（188件）",
      steps:[
        "動物種・カテゴリ（鎮静/麻酔導入/維持/緊急/CRI）でフィルタ",
        "ASA分類でリスク別表示",
        "薬品名クリックで薬品詳細にジャンプ",
        "禁忌・モニタリングパラメータ・参考文献を確認",
      ],
      tips:"💡 体重入力で計算用量を表示。チェックリストは印刷可能",
    },
    {
      title:"🚨 5. 緊急対応プロトコル（25件）",
      steps:[
        "CPR・敗血症・GDV・マムシ咬傷など25シナリオ",
        "各シナリオは time-target 付きステップ（0-5分・15-30分・以降）",
        "key_drugs と monitoring パラメータを併記",
        "RECOVER/Surviving Sepsis Campaign/CURATIVE 等のガイドライン準拠",
      ],
    },
    {
      title:"📊 6. 統計ダッシュボード・症例履歴",
      steps:[
        "📊 ボタンで動物種別疾患数・薬品カテゴリ・ECVN カバレッジを可視化",
        "診断履歴は最大50件 localStorage に保存",
        "CSV/JSON エクスポートで Excel・他システム連携",
        "印刷は全疾患詳細を自動展開して PDF 化可能",
      ],
      tips:"💡 すべての結果はブラウザ内のみで処理（個人情報外部送信なし）",
    },
  ]:[
    {
      title:"🩺 1. Differential Diagnosis (Symptom Checker)",
      steps:[
        "Select the species from 21 supported animals",
        "Check observed clinical symptoms (multiple selection)",
        "Optional: enter lab values, pain score, age, breed",
        "Click \"Run Differential\" to see IDF-weighted ranking with specificity & prevalence correction",
        "Click any candidate to expand pathophysiology, treatment, related drugs",
      ],
      tips:"💡 3+ symptoms improve accuracy. Entered labs apply lab_factor (up to 1.4×) to relevant diseases",
    },
    {
      title:"💬 2. AI Clinical Consultation Chat",
      steps:[
        "Free-input mode: natural language symptom descriptions",
        "Guided mode: step-by-step category→symptoms→age→breed",
        "AI auto-extracts onset/age/breed for ranking refinement",
        "Real-time confidence bars on results",
      ],
      tips:"💡 Auto-detects time expressions like \"3 weeks ago\" → acute/subacute/chronic",
    },
    {
      title:"💊 3. Drug Dictionary (600+ drugs)",
      steps:[
        "Filter by name (JP/EN), category, or species",
        "Species-specific safety ✓/✗ and dosing (mg/kg) shown",
        "Auto-calculate dose by patient weight",
        "Interactions ranked by severity (⛔ MAJOR / ⚠️ MODERATE / ℹ️ MINOR)",
        "Reverse-link: see diseases treated with this drug",
      ],
      tips:"💡 Click any drug name in a treatment protocol to jump directly to drug detail",
    },
    {
      title:"💉 4. Sedation/Anesthesia Protocols (188 items)",
      steps:[
        "Filter by species & category (sedation/induction/maintenance/emergency/CRI)",
        "ASA classification risk filter",
        "Click drug names to jump to drug detail",
        "View contraindications, monitoring params, references",
      ],
      tips:"💡 Weight input auto-calculates doses. Checklist is printable",
    },
    {
      title:"🚨 5. Emergency Protocols (25 scenarios)",
      steps:[
        "CPR, sepsis, GDV, mamushi snakebite, etc. — 25 scenarios",
        "Each has time-targeted steps (0-5 min, 15-30 min, etc.)",
        "Key drugs and monitoring parameters listed",
        "Following RECOVER, Surviving Sepsis Campaign, CURATIVE guidelines",
      ],
    },
    {
      title:"📊 6. Statistics Dashboard & Case History",
      steps:[
        "📊 button visualizes species-disease counts, drug categories, ECVN coverage",
        "Up to 50 diagnosis cases saved in localStorage",
        "CSV/JSON export for Excel & other system integration",
        "Print auto-expands all disease details for PDF generation",
      ],
      tips:"💡 All processing happens in your browser (no personal data sent externally)",
    },
  ];
  const intro=`<div style="padding:10px 14px;background:rgba(34,168,79,.06);border-left:3px solid var(--green);border-radius:6px;margin-bottom:14px;font-size:.82rem;color:var(--gray-700)">${isJa?"VetDict の主要機能と使い方を6セクションで解説します。各機能は独立して動作するため、必要な部分だけ参照できます。":"6 sections covering all VetDict features. Each feature works independently — reference only what you need."}</div>`;
  const sectionsHtml=sections.map(s=>{
    const stepsHtml=s.steps.map((step,i)=>`<li style="margin-bottom:4px">${escapeHtml(step)}</li>`).join("");
    const tipsHtml=s.tips?`<div style="margin-top:8px;padding:6px 10px;background:rgba(26,48,104,.05);border-radius:5px;font-size:.74rem;color:var(--gray-600)">${escapeHtml(s.tips)}</div>`:"";
    return `<details class="help-section" style="margin-bottom:10px;border:1px solid var(--gray-200);border-radius:6px;padding:0" open><summary style="cursor:pointer;padding:10px 14px;font-weight:700;color:var(--navy);background:var(--gray-50);border-radius:6px;font-size:.86rem;user-select:none">${escapeHtml(s.title)}</summary><div style="padding:10px 14px"><ol style="margin:0;padding-left:20px;font-size:.78rem;color:var(--gray-700);line-height:1.6">${stepsHtml}</ol>${tipsHtml}</div></details>`;
  }).join("");
  const disclaimer=`<div style="margin-top:14px;padding:10px;background:#fef3c7;border-left:3px solid #f59e0b;border-radius:5px;font-size:.74rem;color:#78350f">${isJa?"⚠ VetDict は臨床意思決定支援ツールであり、確定診断は獣医師の判断と検査結果との総合判断が必要です。獣医師法・FDA・農水省未認証のオフラベル投与量を含む場合があります。":"⚠ VetDict is a clinical decision-support tool. Definitive diagnosis requires veterinary judgment with diagnostic results. May contain off-label dosages not approved by veterinary boards/FDA/MAFF."}</div>`;
  return intro+sectionsHtml+disclaimer;
}

function _renderDashboardContent(data){
  const isJa=currentLang==="ja";
  /* Section 1: Overall totals */
  const totalDiseases=data.species_disease_counts.reduce((sum,s)=>sum+s.count,0);
  const totalDrugs=data.drug_category_counts.reduce((sum,c)=>sum+c.count,0);
  const totalProtocols=data.total_emergency_protocols||0;
  const overview=`<div class="dashboard-section"><h3>${isJa?"概要":"Overview"}</h3><div class="dashboard-kpi-grid">
    <div class="dashboard-kpi"><div class="kpi-value">${totalDiseases.toLocaleString()}</div><div class="kpi-label">${isJa?"総疾患数":"Total Diseases"}</div></div>
    <div class="dashboard-kpi"><div class="kpi-value">${data.species_disease_counts.length}</div><div class="kpi-label">${isJa?"対応動物種":"Species"}</div></div>
    <div class="dashboard-kpi"><div class="kpi-value">${totalDrugs}</div><div class="kpi-label">${isJa?"総薬品数":"Drugs"}</div></div>
    <div class="dashboard-kpi"><div class="kpi-value">${data.drug_category_counts.length}</div><div class="kpi-label">${isJa?"薬品カテゴリ":"Drug Categories"}</div></div>
    <div class="dashboard-kpi"><div class="kpi-value">${totalProtocols}</div><div class="kpi-label">${isJa?"緊急プロトコル":"Emergency Protocols"}</div></div>
    <div class="dashboard-kpi"><div class="kpi-value">${data.lab_combination_patterns}</div><div class="kpi-label">${isJa?"検査値パターン":"Lab Patterns"}</div></div>
  </div></div>`;

  /* Section 2: Species disease counts (bar chart) */
  const sortedSp=[...data.species_disease_counts].sort((a,b)=>b.count-a.count);
  const maxSp=sortedSp[0]?sortedSp[0].count:1;
  const speciesBars=sortedSp.map(s=>{
    const spObj=SPECIES.find(x=>x.id===s.species);
    const label=spObj?(isJa?spObj.name:spObj.nameEn):s.species;
    const pct=Math.round(s.count/maxSp*100);
    return`<div class="dashboard-bar-row"><span class="bar-label">${escapeHtml(label)}</span><div class="bar-track"><div class="bar-fill" style="width:${pct}%"></div></div><span class="bar-value">${s.count}</span></div>`;
  }).join("");
  const speciesSection=`<div class="dashboard-section"><h3>${isJa?"動物種別 疾患数":"Diseases by Species"}</h3><div class="dashboard-bars">${speciesBars}</div></div>`;

  /* Section 3: Drug category breakdown */
  const drugRows=data.drug_category_counts.slice(0,15);
  const maxDrug=drugRows[0]?drugRows[0].count:1;
  const drugBars=drugRows.map(c=>{
    const label=isJa?(c.name_ja||c.category):(c.name_en||c.category);
    const pct=Math.round(c.count/maxDrug*100);
    return`<div class="dashboard-bar-row"><span class="bar-label">${escapeHtml(label)}</span><div class="bar-track"><div class="bar-fill bar-fill-drug" style="width:${pct}%"></div></div><span class="bar-value">${c.count}</span></div>`;
  }).join("");
  const drugSection=`<div class="dashboard-section"><h3>${isJa?"薬品カテゴリ別 (上位15)":"Drug Categories (Top 15)"}</h3><div class="dashboard-bars">${drugBars}</div></div>`;

  /* Section 4: ECVN coverage */
  const ecvnRows=Object.entries(data.ecvn_coverage||{}).map(([sp,info])=>{
    const spObj=SPECIES.find(x=>x.id===sp);
    const label=spObj?(isJa?spObj.name:spObj.nameEn):sp;
    return{label,pct:info.pct,covered:info.covered,total:info.total};
  }).sort((a,b)=>b.pct-a.pct);
  const ecvnBars=ecvnRows.map(r=>{
    return`<div class="dashboard-bar-row"><span class="bar-label">${escapeHtml(r.label)}</span><div class="bar-track"><div class="bar-fill bar-fill-ecvn" style="width:${r.pct}%"></div></div><span class="bar-value">${r.covered}/${r.total} (${r.pct}%)</span></div>`;
  }).join("");
  const ecvnSection=`<div class="dashboard-section"><h3>${isJa?"ECVN補助療法カバレッジ":"ECVN Adjunct Coverage"}</h3><div class="dashboard-bars">${ecvnBars}</div></div>`;

  /* Section 5: Emergency category breakdown */
  const emRows=Object.entries(data.emergency_categories||{}).map(([k,v])=>({cat:k,count:v})).sort((a,b)=>b.count-a.count);
  const emBars=emRows.map(r=>{
    return`<div class="dashboard-bar-row"><span class="bar-label">${escapeHtml(r.cat||"-")}</span><div class="bar-track"><div class="bar-fill bar-fill-emergency" style="width:${Math.round(r.count/(emRows[0]?.count||1)*100)}%"></div></div><span class="bar-value">${r.count}</span></div>`;
  }).join("");
  const emSection=`<div class="dashboard-section"><h3>${isJa?"緊急プロトコル カテゴリ":"Emergency Protocol Categories"}</h3><div class="dashboard-bars">${emBars}</div></div>`;

  /* Section 6: User's diagnosis history */
  const history=loadDiagnosisHistory();
  let historySection="";
  if(history.length){
    const sp_counts={};
    history.forEach(h=>{if(h.species)sp_counts[h.species]=(sp_counts[h.species]||0)+1;});
    const hRows=Object.entries(sp_counts).map(([k,v])=>({sp:k,count:v})).sort((a,b)=>b.count-a.count);
    const max=hRows[0]?.count||1;
    const hBars=hRows.map(r=>{
      const spObj=SPECIES.find(x=>x.id===r.sp);
      const label=spObj?(isJa?spObj.name:spObj.nameEn):r.sp;
      return`<div class="dashboard-bar-row"><span class="bar-label">${escapeHtml(label)}</span><div class="bar-track"><div class="bar-fill bar-fill-history" style="width:${Math.round(r.count/max*100)}%"></div></div><span class="bar-value">${r.count}</span></div>`;
    }).join("");
    historySection=`<div class="dashboard-section"><h3>${isJa?"あなたの診断履歴 ("+history.length+"件)":"Your Diagnosis History ("+history.length+" cases)"}</h3><div class="dashboard-bars">${hBars}</div><div style="margin-top:10px;text-align:right"><button class="dashboard-export-btn" data-action="csv" style="margin-right:8px;padding:6px 12px;background:var(--white);border:1px solid var(--green);color:var(--green);border-radius:6px;cursor:pointer;font-size:.78rem">📊 CSV</button><button class="dashboard-export-btn" data-action="json" style="padding:6px 12px;background:var(--white);border:1px solid var(--navy);color:var(--navy);border-radius:6px;cursor:pointer;font-size:.78rem">💾 JSON</button></div></div>`;
  }

  return overview+speciesSection+drugSection+ecvnSection+emSection+historySection;
}

// Wire history export buttons after modal content loaded
document.addEventListener("click",e=>{
  const exportBtn=e.target.closest(".dashboard-export-btn");
  if(!exportBtn)return;
  if(exportBtn.dataset.action==="csv")exportHistoryAsCSV();
  else if(exportBtn.dataset.action==="json")exportHistoryAsJSON();
});

/* --- Drug interaction rendering with severity classification --- */
function _classifyInteractionSeverity(di){
  // Honor explicit severity if present
  const sev=(di.severity||"").toLowerCase();
  if(sev==="major"||sev==="severe"||sev==="contraindicated")return"major";
  if(sev==="moderate")return"moderate";
  if(sev==="minor"||sev==="mild")return"minor";
  // Heuristic: infer from effect text keywords
  const txt=((di.effect||"")+" "+(di.effect_ja||"")).toLowerCase();
  if(/contraindicat|fatal|lethal|death|severe|life.?threatening|seizure|cardiac arrest|致死|禁忌|生命|重篤/.test(txt))return"major";
  if(/toxicity|nephrotox|hepatotox|ototox|coagulopath|bleeding|hemorrhage|hypotension|arrhythmi|qt|肝毒|腎毒|耳毒|出血|低血圧|不整脈/.test(txt))return"moderate";
  return"minor";
}

/* Resolve a drug_interactions[].drug reference (a drug id or name) to a loaded
   drug so the reference can be made navigable. Many references are drug classes
   (e.g. "aminoglycosides") with no single entry — those return null and stay
   plain text. */
function _resolveInteractionDrug(ref){
  if(!ref||typeof allDrugs==="undefined"||!Array.isArray(allDrugs)||!allDrugs.length)return null;
  const key=String(ref).trim().toLowerCase();
  if(!key)return null;
  const exact=allDrugs.find(d=>(d.id||"").toLowerCase()===key||(d.name||"").toLowerCase()===key||(d.name_ja||"").toLowerCase()===key);
  if(exact)return exact;
  /* Base-name match: formulary names carry parenthetical suffixes the interaction
     texts omit ("Enoxaparin (Lovenox)" vs ref "Enoxaparin", "Insulin (Veterinary -
     Vetsulin…)" vs ref "Insulin") and refs carry qualifiers the names don't
     ("N-acetylcysteine (oral)"). Compare with parentheticals stripped from both
     sides — still equality, never fuzzy, so class words stay plain text. */
  const base=s=>String(s||"").toLowerCase().replace(/\s*[（(].*$/,"").trim();
  const refBase=base(key);
  if(!refBase)return null;
  return allDrugs.find(d=>base(d.name)===refBase||base(d.name_ja)===refBase||refBase===(d.id||"").toLowerCase())||null;
}
/* Build the drug-name cell of one interaction tag. A reference that resolves as a
   whole becomes a single link. Compound references like "Ketoconazole/itraconazole"
   or "metoclopramide/cisapride/mosapride" name several real drugs in one cell and
   never resolve as a whole — split on "/" and link each component that is itself in
   the manual, so every named drug stays one tap away. Class references ("NSAIDs",
   "aminoglycosides") resolve nowhere and remain plain text. */
function _interactionDrugCell(ref){
  const title=currentLang==="ja"?"この薬品の詳細を開く":"Open this drug";
  const partLink=(m,label)=>`<a href="#drugs" class="interaction-drug-part drug-nav-link" data-drug="${escapeHtml(m.name||label)}" title="${title}">${escapeHtml(label)}</a>`;
  const match=_resolveInteractionDrug(ref);
  if(match)return `<a href="#drugs" class="interaction-drug drug-nav-link" data-drug="${escapeHtml(match.name||ref)}" title="${title}">${escapeHtml(ref)}</a>`;
  if(ref.indexOf("/")!==-1){
    const parts=ref.split("/");
    const resolved=parts.map(p=>_resolveInteractionDrug(p.trim()));
    if(resolved.some(Boolean)){
      const html=parts.map((p,i)=>resolved[i]?partLink(resolved[i],p):escapeHtml(p)).join("/");
      return `<span class="interaction-drug">${html}</span>`;
    }
  }
  return `<span class="interaction-drug">${escapeHtml(ref)}</span>`;
}
function renderDrugInteractionsList(interactions){
  if(!interactions||!interactions.length)return"";
  // Sort by severity: major > moderate > minor
  const order={major:0,moderate:1,minor:2};
  const sorted=[...interactions].sort((a,b)=>order[_classifyInteractionSeverity(a)]-order[_classifyInteractionSeverity(b)]);
  return sorted.map(di=>{
    const sev=_classifyInteractionSeverity(di);
    const label=currentLang==="ja"?(di.effect_ja||di.effect||""):(di.effect||di.effect_ja||"");
    const sevLabel={
      major:currentLang==="ja"?"重度":"MAJOR",
      moderate:currentLang==="ja"?"中等度":"MODERATE",
      minor:currentLang==="ja"?"軽度":"MINOR",
    }[sev]||sev.toUpperCase();
    const icon={major:"⛔",moderate:"⚠️",minor:"ℹ️"}[sev]||"";
    const ref=di.drug||"";
    // When the referenced drug is itself in the manual, make it a click target
    // that jumps to and expands that drug — one tap from "reverse with X" to X.
    const drugCell=_interactionDrugCell(ref);
    return `<span class="drug-interaction-tag severity-${sev}"><span class="severity-badge">${icon} ${sevLabel}</span>${drugCell}<span class="interaction-effect">${escapeHtml(label)}</span></span>`;
  }).join("");
}

function exportHistoryAsCSV(){
  const history=loadDiagnosisHistory();
  if(!history.length){if(typeof showToast==="function")showToast(currentLang==="ja"?"履歴なし":"No history","warning");return;}
  /* CSV header */
  const headers=["id","date","species","severity","symptom_count","symptoms","top1_name","top1_confidence","top2_name","top2_confidence","top3_name","top3_confidence"];
  const escapeCsv=s=>{const t=String(s??"");return /[",\n]/.test(t)?`"${t.replace(/"/g,'""')}"`:t;};
  const rows=history.map(h=>{
    const td=h.topDiseases||[];
    return [
      h.id,
      h.date||"",
      h.species||"",
      h.severity||"",
      (h.symptoms||[]).length,
      (h.symptoms||[]).join("|"),
      td[0]?(td[0].name||td[0].name_ja||""):"",
      td[0]?td[0].confidence:"",
      td[1]?(td[1].name||td[1].name_ja||""):"",
      td[1]?td[1].confidence:"",
      td[2]?(td[2].name||td[2].name_ja||""):"",
      td[2]?td[2].confidence:"",
    ].map(escapeCsv).join(",");
  });
  const csv="﻿"+headers.join(",")+"\n"+rows.join("\n");
  const blob=new Blob([csv],{type:"text/csv;charset=utf-8"});
  const url=URL.createObjectURL(blob);
  const a=document.createElement("a");
  a.href=url;a.download=`vetdict-history-${new Date().toISOString().slice(0,10)}.csv`;
  document.body.appendChild(a);a.click();
  setTimeout(()=>{document.body.removeChild(a);URL.revokeObjectURL(url);},300);
  trackEvent("export_history_csv",{count:history.length});
}

function exportHistoryAsJSON(){
  const history=loadDiagnosisHistory();
  if(!history.length){if(typeof showToast==="function")showToast(currentLang==="ja"?"履歴なし":"No history","warning");return;}
  const blob=new Blob([JSON.stringify({exported:new Date().toISOString(),count:history.length,cases:history},null,2)],{type:"application/json"});
  const url=URL.createObjectURL(blob);
  const a=document.createElement("a");
  a.href=url;a.download=`vetdict-history-${new Date().toISOString().slice(0,10)}.json`;
  document.body.appendChild(a);a.click();
  setTimeout(()=>{document.body.removeChild(a);URL.revokeObjectURL(url);},300);
  trackEvent("export_history_json",{count:history.length});
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
  return`<div class="history-panel" style="margin-top:12px"><div style="font-size:.82rem;font-weight:700;color:var(--navy);padding:8px 12px;border-bottom:2px solid var(--green)">${currentLang==="ja"?"📋 診断履歴":"📋 Diagnosis History"} <span style="font-size:.7rem;color:var(--gray-500);font-weight:400">(${history.length})</span></div>${items}<div class="history-actions" style="padding:8px 12px;display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap"><div style="display:flex;gap:6px;flex-wrap:wrap"><button type="button" class="history-export-csv" aria-label="${currentLang==="ja"?"CSV保存":"Export CSV"}" style="font-size:.72rem;color:var(--green);background:var(--white);border:1px solid var(--green);padding:4px 10px;border-radius:6px;cursor:pointer">${currentLang==="ja"?"📊 CSV":"📊 CSV"}</button><button type="button" class="history-export-json" aria-label="${currentLang==="ja"?"JSON保存":"Export JSON"}" style="font-size:.72rem;color:var(--navy);background:var(--white);border:1px solid var(--navy);padding:4px 10px;border-radius:6px;cursor:pointer">${currentLang==="ja"?"💾 JSON":"💾 JSON"}</button></div><button type="button" class="history-clear-btn" aria-label="${currentLang==="ja"?"診断履歴をすべて削除":"Clear diagnosis history"}" style="font-size:.72rem;color:var(--gray-400);background:none;border:none;cursor:pointer;text-decoration:underline">${currentLang==="ja"?"履歴をクリア":"Clear history"}</button></div></div>`;
}

function attachHistoryHandlers(container){
  container.querySelectorAll(".history-item").forEach(item=>{
    item.addEventListener("click",()=>{
      const id=Number(item.dataset.id);
      const history=loadDiagnosisHistory();
      const entry=history.find(h=>h.id===id);
      if(!entry)return;
      if(entry.species&&entry.species!==currentSpecies)selectSpecies(entry.species);
      if(entry.symptoms&&entry.symptoms.length){
        selectedSymptoms.clear();
        entry.symptoms.forEach(s=>selectedSymptoms.add(s));
        renderSelectedSymptoms();
        renderSymptomList(symptomData);
        const analyzeBtn=document.getElementById("analyzeBtn");
        if(analyzeBtn){analyzeBtn.disabled=false;analyzeBtn.click();}
      }
    });
  });
  const clearBtn=container.querySelector(".history-clear-btn");
  if(clearBtn){clearBtn.addEventListener("click",e=>{
    e.stopPropagation();
    let prev=null;
    try{prev=localStorage.getItem("vetdict-history");}catch(_){}
    try{localStorage.removeItem("vetdict-history");}catch(_){}
    const panel=container.querySelector(".history-panel");
    if(panel)panel.remove();
    if(typeof showToast==="function"){
      const msg=currentLang==="ja"?"履歴をクリアしました":"History cleared";
      const undoLabel=currentLang==="ja"?"元に戻す":"Undo";
      showToast(msg,"success",5000,prev?{label:undoLabel,onClick:()=>{
        try{localStorage.setItem("vetdict-history",prev);}catch(_){}
        const resultsArea=document.getElementById("resultsArea");
        if(resultsArea&&!resultsArea.querySelector(".history-panel")){
          const tmp=document.createElement("div");tmp.innerHTML=renderHistoryPanel();
          while(tmp.firstChild)resultsArea.appendChild(tmp.firstChild);
          attachHistoryHandlers(resultsArea);
        }
      }}:null);
    }
  });}
  const csvBtn=container.querySelector(".history-export-csv");
  if(csvBtn)csvBtn.addEventListener("click",e=>{e.stopPropagation();exportHistoryAsCSV();});
  const jsonBtn=container.querySelector(".history-export-json");
  if(jsonBtn)jsonBtn.addEventListener("click",e=>{e.stopPropagation();exportHistoryAsJSON();});
}

/* Resolve a prevalence name (e.g. "Gout (Articular)") to the actual browsable
   disease name in the loaded DB list, so navigation opens the right entry even
   when the prevalence label differs from the canonical name. Conservative — only
   confident matches (exact, identical token set, or a unique substring either
   way) are remapped; otherwise the original name is returned so we never open
   the wrong disease. Returns the resolved name to search for. */
function _resolveCommonDiseaseName(name){
  const q=(name||"").trim();
  if(!q||!Array.isArray(allDiseases)||!allDiseases.length)return q;
  const norm=s=>(s||"").toLowerCase();
  const tokset=s=>norm(s).split(/[^a-z0-9]+/).filter(Boolean).sort().join(" ");
  const ql=norm(q),qt=tokset(q);
  // 1. exact name / name_ja
  let hit=allDiseases.find(d=>norm(d.name)===ql||norm(d.name_ja)===ql);
  // 2. identical token set (handles word-order flips like "Gout (Articular)" ↔ "Articular Gout")
  if(!hit&&qt)hit=allDiseases.find(d=>tokset(d.name)===qt);
  // 3. unique substring match either direction (handles suffixes like "(CKD)"/"(BPH)")
  if(!hit){
    const cand=allDiseases.filter(d=>{const n=norm(d.name);return n&&(n.includes(ql)||ql.includes(n));});
    if(cand.length===1)hit=cand[0];
  }
  return hit?hit.name:q;
}
/* Delegate clicks on common-disease chips to the disease DB detail. Attached
   once per container (guard) so re-renders never stack listeners. */
function _attachCommonDiseaseNav(container){
  if(!container||container.dataset.cdNav)return;
  container.dataset.cdNav="1";
  container.addEventListener("click",function(e){
    const btn=e.target.closest(".common-disease-tag");
    if(btn&&btn.dataset.disease){e.preventDefault();navigateToDiseaseDb(_resolveCommonDiseaseName(btn.dataset.disease));}
  });
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
      const inner=`${escapeHtml(name)}${sub?` <span class="common-disease-sub">${escapeHtml(sub)}</span>`:""}`;
      /* Each disease opens its full entry in the disease DB (species already
         loaded there) — one tap from "common in this species" to the detail.
         data-disease carries the canonical English name; the click handler
         resolves it against the browsable list before navigating. */
      return `<button type="button" class="common-disease-tag ${cls}" data-disease="${escapeHtml(d.name||name)}" title="${currentLang==="ja"?"疾患の詳細を開く":"Open disease details"}">${inner}</button>`;
    }).join("");
    area.innerHTML=`<div class="common-diseases-section">
      <div class="common-diseases-header">${currentLang==="ja"?"📋 この動物種でよくみられる疾患":"📋 Common diseases in this species"}</div>
      ${veryCommon.length?`<div class="common-diseases-group"><span class="common-diseases-tier tier-very-common">${currentLang==="ja"?"非常に多い":"Very Common"}</span>${renderList(veryCommon,"tag-very-common")}</div>`:""}
      ${common.length?`<div class="common-diseases-group"><span class="common-diseases-tier tier-common">${currentLang==="ja"?"多い":"Common"}</span>${renderList(common,"tag-common")}</div>`:""}
      <div class="common-diseases-hint">${currentLang==="ja"?"※ 疾患をタップすると詳細を表示。鑑別診断の参考としてご活用ください":"※ Tap a disease to view details. Use as reference for differential diagnosis"}</div>
    </div>`;
    _attachCommonDiseaseNav(area);
  }).catch(()=>{if(area)area.innerHTML="";});
}

function loadBreedEcology(species,breedId){
  const area=document.getElementById("breedEcologyArea");
  if(!area||!species)return;
  fetchWithTimeout(`/api/breeds/${encodeURIComponent(species)}`).then(r=>r.ok?r.json():Promise.reject(new Error("HTTP "+r.status))).then(data=>{
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
    /* Patterns that resolve in the drug dictionary (server-annotated drug_links)
       become one-tap links to the exact formulary entry; class terms ("NSAIDs")
       and discontinued agents stay plain text. */
    const linkByPattern={};
    (w.drug_links||[]).forEach(l=>{linkByPattern[l.pattern]=l;});
    const drugTitle=currentLang==="ja"?"この薬品の用量・詳細を開く":"Open this drug's dosage";
    const drugs=w.drug_patterns.slice(0,3).map(p=>{
      const l=linkByPattern[p];
      if(!l)return escapeHtml(p);
      return `<a href="#drugs" class="drug-nav-link anesthesia-contra-drug" data-drug="${escapeHtml(l.name||p)}" title="${drugTitle}">${escapeHtml(p)}</a>`;
    }).join(", ");
    const sev=w.severity;
    html+=`<div style="font-size:.8rem;padding:4px 0;border-bottom:1px dotted #fde68a"><span class="anesthesia-contra-badge" style="background:${sevColors[sev]||"#ea580c"}">${sevIcons[sev]||"⚠️"} ${escapeHtml(sevLabels[sev]||sev)}</span> <strong>${drugs}</strong>: ${escapeHtml(msg)}</div>`;
  });
  const protoLabel=currentLang==="ja"?"💉 この動物種の麻酔プロトコルを見る":"💉 View anesthesia protocols for this species";
  html+=`</div><div style="margin-top:8px"><a href="#anesthesia" class="anesthesia-nav-link" data-species="${escapeHtml(currentSpecies||"")}" style="font-size:.8rem;color:var(--navy);font-weight:600;text-decoration:none">${protoLabel} →</a></div></div>`;
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
    const drugSearchName=dr.name||dr.name_ja||"";
    html+=`<div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap"><a href="#drugs" class="drug-nav-link" data-drug="${escapeHtml(drugSearchName)}" style="font-weight:600;color:var(--navy);text-decoration:underline;text-decoration-style:dotted;cursor:pointer">${escapeHtml(name)}</a>`;
    if(dr.safe===false)html+=`<span style="color:#dc2626;font-weight:600;font-size:.75rem">⚠ ${safeLabel}</span>`;
    html+=`</div>`;
    if(hasDosage&&dr.safe!==false)html+=`<div style="margin-top:3px;color:var(--gray-700)"><span style="font-weight:500">${currentLang==="ja"?"投与量":"Dosage"}:</span> ${escapeHtml(dosage)}</div>`;
    if(notes&&dr.safe!==false)html+=`<div style="margin-top:2px;color:var(--gray-500);font-size:.76rem">${escapeHtml(notes)}</div>`;
    html+=`</div>`;
  });
  html+=`</div><div style="font-size:.7rem;color:var(--gray-400);margin-top:4px">${currentLang==="ja"?"※ 投与量は参考値です。必ず獣医師の指示に従ってください。":"※ Dosages are for reference only. Always follow veterinary guidance."}</div></div>`;
  return html;
}

let _cardIndex=0;
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
  /* Clinical signs / diagnostic work-up: already computed by the matcher and sent
     to the client, but previously dropped in this card. Show only when present. */
  const clinicalSigns=pick(d.clinical_signs_ja,d.clinical_signs);
  const diagnosis=pick(d.diagnosis_ja,d.diagnosis);
  const matchDisplay=matchSymptoms.map(s=>{const n=symNames[s];if(!n)return escapeHtml(s);return currentLang==="ja"?`${escapeHtml(n.ja)} <span style="color:var(--gray-500);font-size:.78rem">${escapeHtml(n.en)}</span>`:`${escapeHtml(n.en)} <span style="color:var(--gray-500);font-size:.78rem">${escapeHtml(n.ja)}</span>`;}).join("&ensp;|&ensp;");
  const prevalenceTier=d.prevalence_tier||"unknown";
  const prevalenceLabel={very_common:(currentLang==="ja"?"非常に一般的":"Very Common"),common:(currentLang==="ja"?"一般的":"Common"),uncommon:(currentLang==="ja"?"稀":"Uncommon"),rare:(currentLang==="ja"?"非常に稀":"Rare"),unknown:(currentLang==="ja"?"不明":"Unknown")}[prevalenceTier]||"";

  const urgencyIcon=likelihood==="high"?"\u26A0\uFE0F":likelihood==="moderate"?"\u{1F7E1}":"\u{1F7E2}";
  const delay=Math.min(_cardIndex++*60,600);
  const inputCount=(typeof selectedSymptoms!=="undefined"&&selectedSymptoms&&selectedSymptoms.size)||0;
  const matchedCount=matchSymptoms.length;
  const matchRatioLabel=inputCount>0&&matchedCount>0
    ?(currentLang==="ja"?`${matchedCount}/${inputCount}症状一致`:`${matchedCount}/${inputCount} symptoms matched`)
    :"";
  let html=`<div class="disease-result disease-${escapeHtml(likelihood)}" style="animation-delay:${delay}ms">
    <div class="disease-head" role="button" tabindex="0" aria-expanded="false">
      <div class="disease-head-info">
        <div class="disease-name-row">
          <span class="disease-name">${escapeHtml(name)}</span>
          ${nameSecondary&&nameSecondary!==name?`<span class="disease-name-ja">${escapeHtml(nameSecondary)}</span>`:""}
          ${prevalenceLabel?`<span class="prevalence-badge">${escapeHtml(prevalenceLabel)}</span>`:""}
        </div>
        <div class="disease-match-bar-row">
          <div class="disease-match-bar"><div class="disease-match-fill disease-match-${likelihood}" style="width:${Math.min(pct,100)}%"></div></div>
          <span class="disease-match-label">${urgencyIcon} ${pct}%</span>
          ${matchRatioLabel?`<span class="disease-match-ratio" aria-label="${escapeHtml(matchRatioLabel)}">${escapeHtml(matchRatioLabel)}</span>`:""}
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
        ${clinicalSigns?`<div class="detail-section">
          <div class="detail-section-header"><span class="detail-icon">\u{1FA7A}</span> ${t("dtClinicalSigns")}</div>
          <div class="detail-section-body">${escapeHtml(clinicalSigns)}</div>
        </div>`:""}
        <div class="detail-section">
          <div class="detail-section-header"><span class="detail-icon">\u{1F9EC}</span> ${t("dtPathophysiology")}</div>
          <div class="detail-section-body">${escapeHtml(patho)}</div>
        </div>
        <div class="detail-section">
          <div class="detail-section-header"><span class="detail-icon">\u{1F50D}</span> ${t("dtCauses")}</div>
          <div class="detail-section-body">${escapeHtml(causes)}</div>
        </div>
        ${diagnosis?`<div class="detail-section">
          <div class="detail-section-header"><span class="detail-icon">\u{1F52C}</span> ${t("dtDiagnosis")}</div>
          <div class="detail-section-body">${escapeHtml(diagnosis)}</div>
        </div>`:""}
        <div class="detail-section">
          <div class="detail-section-header"><span class="detail-icon">\u{1F48A}</span> ${t("dtTreatment")} ${evidenceBadge(quickAssessGrade(treatment))}</div>
          <div class="detail-section-body">${renderTreatmentWithAdjunct(treatment)}${buildTreatmentDrugsPlaceholder(currentSpecies||"dog",d.name_ja||d.name||"")}</div>
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
      ${(()=>{const display=d.recommended_tests_display;const list=(display&&display.length)?display:recTests;if(!list||!list.length)return"";const chips=list.map(x=>{let label;if(display&&display.length){label=currentLang==="ja"?(x.name_ja||x.name_en||x.id):(x.name_en||x.name_ja||x.id);}else{label=humanizeTestId(typeof x==="string"?x:(currentLang==="ja"?(x.name_ja||x.name):(x.name||x.name_ja)));}return`<span style="display:inline-block;padding:3px 8px;background:#f0f7ff;border:1px solid #bfdbfe;border-radius:4px;font-size:.78rem;color:var(--navy)">\u{1F52C} ${escapeHtml(label)}</span>`;}).join("");return`<div class="detail-tests"><strong>${t("dtRecommendedTests")}:</strong><div style="display:flex;flex-wrap:wrap;gap:4px;margin-top:4px">${chips}</div></div>`;})()}
      ${renderMentionedDrugs(d)}
      ${renderAnesthesiaConsiderations(d)}
      <div class="detail-page-link"><button type="button" class="disease-db-nav-link" data-name="${escapeHtml(nameEn)}" style="font-size:.82rem;color:var(--navy);font-weight:600;background:none;border:none;padding:0;cursor:pointer;text-decoration:none">${currentLang==="ja"?"🔍 疾患データベースで開く":"🔍 Open in disease database"} →</button> <a href="/diseases/${encodeURIComponent(currentSpecies)}/${encodeURIComponent(nameEn.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,''))}" target="_blank" rel="noopener noreferrer" style="font-size:.82rem;color:var(--green);font-weight:600;text-decoration:none;margin-left:12px">${currentLang==="ja"?"📖 詳細ページを見る":"📖 View full disease page"} →</a></div>
      ${d.content_origin?`<div class="missing-note">${currentLang==="ja"?"データソース":"Content source"}: ${escapeHtml(contentOriginLabel(d.content_origin))}</div>`:""}${renderCitationMap(d)}${renderReferenceLinks(d)}${renderDataReviewNote(d)}
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
  const card=document.getElementById("husbandryCard");
  fetchWithTimeout(`/api/species/${encodeURIComponent(species)}/husbandry`).then(r=>r.ok?r.json():Promise.reject(new Error("HTTP "+r.status))).then(data=>{
    if(requestId!==husbandryRequestId||species!==currentSpecies)return;
    if(data.husbandry){renderHusbandry(data.husbandry,container);if(card)card.style.display="";}
    else if(card){card.style.display="none";}
  }).catch(err=>{
    if(requestId!==husbandryRequestId||species!==currentSpecies)return;
    debugWarn("husbandry load failed:",err);
    if(card)card.style.display="none";
  });
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
  if(!list){debugWarn("diseaseDbList element not found");return;}
  list.innerHTML='<div style="padding:12px"><div class="skeleton skeleton-card"></div><div class="skeleton skeleton-card" style="height:80px"></div><div class="skeleton skeleton-card" style="height:100px"></div></div>';
  fetchWithTimeout(`/api/health-check/diseases?species=${encodeURIComponent(species)}`).then(r=>r.json()).then(data=>{if(requestId!==diseaseRequestId||species!==currentSpecies)return;if(data.diseases){allDiseases=data.diseases;renderAzNav();renderDiseaseDb();const dbTab=document.getElementById("tab-database");if(dbTab){let b=dbTab.querySelector(".tab-badge");if(!b){b=document.createElement("span");b.className="tab-badge";dbTab.appendChild(b);}b.textContent=allDiseases.length;}}})
  .catch(err=>{if(requestId===diseaseRequestId&&list){debugError("diseaseDb load failed:",err);list.innerHTML=`<div role="alert" style="padding:20px;text-align:center;color:var(--gray-500)">${t("loadFailed")}<br><button type="button" class="retry-db-btn" style="margin-top:10px;padding:8px 20px;background:var(--navy);color:var(--white);border:none;border-radius:6px;cursor:pointer;font-size:.84rem">${t("reload")}</button></div>`;const rb=list.querySelector(".retry-db-btn");if(rb)rb.addEventListener("click",()=>loadDiseaseDb(species));}});
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
  if(!azNav){debugWarn("azNav element not found");return;}
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
      const toggleBtn=catGrid.querySelector(".az-mode-toggle");
      if(toggleBtn)toggleBtn.addEventListener("click",function(){diseaseNavMode=cur.next;diseaseFilter='';renderAzNav();renderDiseaseDb();});
      if(!catGrid.dataset.handlersAttached){
        catGrid.dataset.handlersAttached="1";
        catGrid.addEventListener("click",e=>{
          const btn=e.target.closest(".disease-cat-card[data-cat]");
          if(!btn)return;
          const cat=btn.dataset.cat;
          if(diseaseFilter===cat){diseaseFilter='';btn.classList.remove("active");}
          else{catGrid.querySelectorAll(".disease-cat-card").forEach(b=>b.classList.remove("active"));btn.classList.add("active");diseaseFilter=cat;}
          diseaseDisplayLimit=100;renderDiseaseDb();
          _revealFilteredList("diseaseDbList");
        });
      }
    }
  }else{
    azNav.style.display="";
    if(catGrid)catGrid.style.display="none";
    const isAz=diseaseNavMode==="az";
    const letters=isAz?"ABCDEFGHIJKLMNOPQRSTUVWXYZ".split(""):"あ か さ た な は ま や ら わ".split(" ");
    azNav.innerHTML=`<button class="az-mode-toggle" aria-label="Switch sort mode">${cur.switchLabel}</button><button class="active" data-letter="" aria-label="Show all">ALL</button>`+letters.map(l=>`<button data-letter="${l}" aria-label="Filter by ${l}">${l}</button>`).join("");
    const toggleBtn=azNav.querySelector(".az-mode-toggle");
    if(toggleBtn)toggleBtn.addEventListener("click",function(){diseaseNavMode=cur.next;diseaseFilter='';renderAzNav();renderDiseaseDb();});
    if(!azNav.dataset.handlersAttached){
      azNav.dataset.handlersAttached="1";
      azNav.addEventListener("click",e=>{const btn=e.target.closest("button[data-letter]");if(btn)filterDiseaseDb(btn.dataset.letter);});
    }
  }
}

function filterDiseaseDb(letter){
  diseaseFilter=letter;
  diseaseDisplayLimit=100;
  document.querySelectorAll(".az-nav button:not(.az-mode-toggle)").forEach(b=>b.classList.toggle("active",b.dataset.letter===letter));
  renderDiseaseDb();
  _revealFilteredList("diseaseDbList");
}

/* Bring a freshly-filtered list to a usable reading position after an explicit
   filter tap (category card / A-Z letter). Two layouts, both handled:
     - Desktop: the list is its own scroll container (fixed max-height), so it
       keeps its previous scrollTop after a re-render — the filtered results would
       start part-way down. Reset it so they start at the top.
     - Mobile: the list is in page flow below the filter chrome; if the user had
       scrolled the results, the new top can sit above the sticky header. Re-anchor
       it just below the sticky chrome. Skipped when already comfortably in view so
       a tap on a filter that's already at the top never yanks the page.
   Deliberately NOT called from the search-typing path, which uses
   _renderPinningAnchor to hold position while the soft keyboard is open. */
function _revealFilteredList(listId){
  const list=document.getElementById(listId);
  if(!list)return;
  if(list.scrollTop>0)list.scrollTop=0;
  if(list.offsetParent===null)return;
  const top=list.getBoundingClientRect().top;
  const stickyOffset=parseInt(getComputedStyle(document.documentElement).getPropertyValue("--sticky-offset"),10)||112;
  const comfy=top>=stickyOffset-4&&top<window.innerHeight*0.6;
  if(!comfy)requestAnimationFrame(()=>scrollToAnchor(list,{settle:false}));
}

/* Emergency flag for disease-DB rows. Only the "emergency" severity is badged —
   it is a clean, high-precision signal (verified: pyothorax, saddle thrombus,
   blocked cat, DKA…), so a clinician scanning the list spots true emergencies at
   a glance without the badge becoming noise. */
function severityBadge(sev){
  if((sev||"").toLowerCase()!=="emergency")return "";
  return `<span class="d-urgency-badge badge-emergency" title="${currentLang==="ja"?"緊急疾患":"Emergency"}">🚨 ${currentLang==="ja"?"緊急":"Emergency"}</span>`;
}
let diseaseDisplayLimit=100;
function renderDiseaseDb(){
  const list=document.getElementById("diseaseDbList");
  const rawSearch=(document.getElementById("diseaseSearch").value||"").trim();
  const search=rawSearch.toLowerCase();
  /* 種未選択でも調べられるように: 動物種が未選択のまま検索した場合は全種横断APIで検索 */
  if(!currentSpecies&&rawSearch.length>=2){renderCrossSpeciesDiseaseSearch(rawSearch);return;}
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
  const dbCountEl=document.getElementById("diseaseDbCount");if(dbCountEl)dbCountEl.textContent=t("diseaseCount").replace("%filtered%",totalCount).replace("%total%",allDiseases.length);
  if(totalCount===0){
    if(!currentSpecies&&!search){list.innerHTML=renderEmptyState("database");}
    else{
      const hasFilter=!!diseaseFilter;
      const heading=t("noDiseaseMatch");
      const tipsJa=[];const tipsEn=[];
      if(search){tipsJa.push("検索キーワードを短くする（例:「腎」「kidney」）","スペルや表記ゆれ（カタカナ↔英語）を確認");tipsEn.push("Try a shorter keyword (e.g., 'kidn' instead of 'kidney')","Check spelling or try the other language");}
      if(hasFilter){tipsJa.push("カテゴリ／頭文字フィルタを解除して再検索");tipsEn.push("Clear the category / A-Z filter and search again");}
      if(!search&&!hasFilter){tipsJa.push("他の動物種を選択してみる");tipsEn.push("Try selecting a different species");}
      const tips=currentLang==="ja"?tipsJa:tipsEn;
      const subheading=currentLang==="ja"?"次の方法をお試しください:":"Try one of the following:";
      const clearBtnLbl=currentLang==="ja"?"フィルタをクリア":"Clear filters";
      const showClearBtn=search||hasFilter;
      list.innerHTML=`<div style="padding:32px 20px;text-align:center;color:var(--gray-600);background:linear-gradient(180deg,var(--gray-50),transparent);border-radius:var(--radius-lg)"><div style="font-size:2rem;margin-bottom:8px;opacity:.5">🔍</div><p style="font-weight:600;color:var(--navy);margin-bottom:4px">${escapeHtml(heading)}</p><p style="font-size:.82rem;color:var(--gray-500);margin-bottom:10px">${escapeHtml(subheading)}</p><ul style="text-align:left;display:inline-block;margin:0 auto 14px;padding-left:18px;font-size:.82rem;color:var(--gray-700);line-height:1.6">${tips.map(x=>`<li>${escapeHtml(x)}</li>`).join("")}</ul>${showClearBtn?`<div><button type="button" id="diseaseDbClearAll" class="clear-all-btn">${clearBtnLbl}</button></div>`:""}</div>`;
      const clearAllBtn=document.getElementById("diseaseDbClearAll");
      if(clearAllBtn)clearAllBtn.addEventListener("click",()=>{
        const ds=document.getElementById("diseaseSearch");if(ds){ds.value="";ds.dispatchEvent(new Event("input"));}
        diseaseFilter="";renderAzNav();renderDiseaseDb();
      });
    }
    return;
  }
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
    /* Clinical signs (臨床徴候) and diagnostic work-up (診断) are evidence-grounded
       fields present in the record but historically not surfaced. Show them only
       when real content exists (no auto-fallback) so records without them stay clean. */
    const clinicalSigns=pk(d.clinical_signs_ja,d.clinical_signs);
    const diagnosis=pk(d.diagnosis_ja,d.diagnosis);
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
    return`<div class="disease-db-item" role="button" tabindex="0" aria-expanded="false" data-name="${escapeHtml(d.name||"")}" data-name-ja="${escapeHtml(d.name_ja||"")}">
      <div class="d-name">${dPrimary} <span class="d-name-ja">${dSecondary}</span></div>
      <div class="d-meta"><span class="d-cat-badge" data-cat="${escapeHtml(_dCat)}">${escapeHtml(_dCatLbl)}</span>${severityBadge(d.severity)}</div>
      <div class="d-desc">${highlightMatch(dDesc,search)}</div>
      <div class="disease-detail"><dl>
        <dt>${t("dtDescription")}</dt><dd>${escapeHtml(desc)}</dd>
        ${clinicalSigns?`<dt>${t("dtClinicalSigns")}</dt><dd>${escapeHtml(clinicalSigns)}</dd>`:""}
        <dt>${t("dtPathophysiology")}</dt><dd>${escapeHtml(patho)}</dd>
        <dt>${t("dtCauses")}</dt><dd>${escapeHtml(causes)}</dd>
        ${diagnosis?`<dt>${t("dtDiagnosis")}</dt><dd>${escapeHtml(diagnosis)}</dd>`:""}
        <dt>${t("dtPrevention")}</dt><dd>${escapeHtml(prevention)}</dd>
        <dt>${t("dtTreatment")} ${evidenceBadge(quickAssessGrade(treatment))}</dt><dd>${renderTreatmentWithAdjunct(treatment)}${buildTreatmentDrugsPlaceholder(currentSpecies||"dog",d.name_ja||d.name||"")}</dd>
        <dt>${t("dtPrognosis")}</dt><dd>${escapeHtml(prognosis)}</dd>
        ${(d.symptoms_display&&d.symptoms_display.length)?`<dt>${t("dtSymptoms")}</dt><dd>${escapeHtml(d.symptoms_display.map(s=>currentLang==="ja"?(s.name_ja||s.id):(s.name_en||s.id)).join("、"))}${_differentialCheckButton(d)}</dd>`:(d.symptoms?`<dt>${t("dtSymptoms")}</dt><dd>${escapeHtml(Array.isArray(d.symptoms)?d.symptoms.join(", "):(typeof d.symptoms==="object"?Object.keys(d.symptoms).join(", "):String(d.symptoms)))}${_differentialCheckButton(d)}</dd>`:"")}
        ${(d.recommended_tests_display&&d.recommended_tests_display.length)?`<dt>${t("dtRecommendedTests")}</dt><dd>${escapeHtml(d.recommended_tests_display.map(x=>currentLang==="ja"?(x.name_ja||x.id):(x.name_en||x.id)).join("、"))}</dd>`:(d.recommended_tests?`<dt>${t("dtRecommendedTests")}</dt><dd>${escapeHtml(d.recommended_tests.join(", "))}</dd>`:"")}
        ${rehab?`<dt>${currentLang==="ja"?"リハビリテーション":"Rehabilitation"}</dt><dd><pre style="white-space:pre-wrap;font-family:inherit;margin:0">${escapeHtml(rehab)}</pre></dd>`:""}
        ${nutrition?`<dt>${currentLang==="ja"?"栄養管理":"Nutrition Management"}</dt><dd><pre style="white-space:pre-wrap;font-family:inherit;margin:0">${escapeHtml(nutrition)}</pre></dd>`:""}
        ${recoveryWeeks?`<dt>${currentLang==="ja"?"回復期間":"Recovery Timeline"}</dt><dd>${currentLang==="ja"?`${recoveryWeeks}週間`:`${recoveryWeeks} weeks`}</dd>`:""}
        ${successRate!==undefined?`<dt>${currentLang==="ja"?"成功率":"Success Rate"}</dt><dd>${(successRate*100).toFixed(1)}%</dd>`:""}
        ${mortalityRate!==undefined?`<dt>${currentLang==="ja"?"死亡率":"Mortality Rate"}</dt><dd>${(mortalityRate*100).toFixed(1)}%</dd>`:""}
      </dl>${renderOrthopedicReferences(d)}<div class="related-diseases-section" data-related="1" data-disease="${escapeHtml(d.name||"")}"></div><div class="cross-nav-links"><a href="#drugs" class="cross-nav-btn drug-nav-link" data-drug="${escapeHtml(d.name||"")}">\u{1F48A} ${currentLang==="ja"?"薬品辞書で検索":"Search Drug Dictionary"}</a><a href="#anesthesia" class="cross-nav-btn anesthesia-nav-link" data-species="${escapeHtml(currentSpecies||"")}">\u{1F489} ${currentLang==="ja"?"麻酔プロトコル":"Anesthesia Protocols"}</a></div><div style="margin-top:8px"><a href="/diseases/${encodeURIComponent(currentSpecies)}/${encodeURIComponent((d.name||"").toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,''))}" target="_blank" rel="noopener noreferrer" style="font-size:.82rem;color:var(--green);font-weight:600;text-decoration:none">📖 ${currentLang==="ja"?"詳細ページを見る":"View full page"} →</a></div>${d.content_origin?`<div class="missing-note">${currentLang==="ja"?"データソース":"Content source"}: ${escapeHtml(contentOriginLabel(d.content_origin))}</div>`:""}${renderCitationMap(d)}${renderReferenceLinks(d)}${renderDataReviewNote(d)}</div>
    </div>`}).join("");
  const shownCount=shown.filter(d=>!d._catHeader).length;
  if(totalCount>shownCount){
    const remaining=totalCount-shownCount;
    const showMoreBtn=document.createElement("button");
    showMoreBtn.type="button";
    showMoreBtn.className="show-more-btn";
    showMoreBtn.style.cssText="display:block;margin:16px auto;padding:8px 24px;border:1px solid var(--gray-300);border-radius:6px;background:var(--white);cursor:pointer";
    showMoreBtn.textContent=t("showMoreItems").replace("%n%",remaining);
    showMoreBtn.addEventListener("click",function(){diseaseDisplayLimit+=100;renderDiseaseDb();});
    list.appendChild(showMoreBtn);
  }
}

function renderEmptyState(tab){
  const icons={database:"\u{1F4D6}",drugs:"\u{1F48A}",anesthesia:"\u{1F489}"};
  const msgs={database:t("emptyStateDiseaseDb"),drugs:t("emptyStateDrugs"),anesthesia:t("emptyStateAnesthesia")};
  const hint=tab==="database"?`<p class="empty-state-desc empty-state-hint">${t("emptyStateDiseaseDbHint")}</p>`:"";
  return`<div class="empty-state-prompt"><span class="empty-state-icon" aria-hidden="true">${icons[tab]||"\u{1F50D}"}</span><p class="empty-state-title">${t("emptyStateSelectSpecies")}</p><p class="empty-state-desc">${msgs[tab]||""}</p>${hint}<button type="button" class="empty-state-btn" data-action="scroll-to-species">${t("emptyStateSelectBtn")}</button></div>`;
}

/* 全種横断の疾患検索（動物種未選択時にDBタブから直接調べられるようにする） */
let _xspeciesDiseaseReqId=0;
function renderCrossSpeciesDiseaseSearch(query){
  const list=document.getElementById("diseaseDbList");
  if(!list)return;
  const reqId=++_xspeciesDiseaseReqId;
  const dbCountEl=document.getElementById("diseaseDbCount");if(dbCountEl)dbCountEl.textContent="";
  list.innerHTML=`<div class="xspecies-searching" style="padding:16px;text-align:center;color:var(--gray-500)">${escapeHtml(t("xspeciesSearching"))}</div>`;
  fetchWithTimeout(`/api/diseases?q=${encodeURIComponent(query)}&limit=60`).then(r=>r.json()).then(data=>{
    if(reqId!==_xspeciesDiseaseReqId)return;
    const diseases=(data&&data.diseases)||[];
    const _searchBox=document.getElementById("diseaseSearch");
    if(!diseases.length){_renderPinningAnchor(_searchBox,()=>{list.innerHTML=`<div role="status" style="padding:20px;text-align:center;color:var(--gray-500)">${escapeHtml(t("noDiseaseMatch"))}</div>`;});return;}
    const items=diseases.map(d=>{
      const spId=d.species||"";
      const sp=SPECIES.find(s=>s.id===spId);
      const spIcon=SPECIES_ICONS[spId]||"\u{1F43E}";
      const spLabel=sp?(currentLang==="ja"?sp.name:sp.nameEn):spId;
      const label=currentLang==="ja"?(d.name_ja||d.name||""):(d.name||d.name_ja||"");
      const sub=currentLang==="ja"?(d.name||""):(d.name_ja||"");
      return`<button type="button" class="xspecies-result" data-name="${escapeHtml(d.name||d.name_ja||"")}" data-species="${escapeHtml(spId)}"><span class="xspecies-result-sp"><span aria-hidden="true">${spIcon}</span> ${escapeHtml(spLabel)}</span><span class="xspecies-result-name">${escapeHtml(label)}${sub?`<span class="xspecies-result-sub">${escapeHtml(sub)}</span>`:""}</span></button>`;
    }).join("");
    _renderPinningAnchor(_searchBox,()=>{list.innerHTML=`<div class="xspecies-results-label">${escapeHtml(t("xspeciesResultsLabel"))}</div>${items}`;});
    if(dbCountEl)dbCountEl.textContent=t("diseaseCount").replace("%filtered%",diseases.length).replace("%total%",diseases.length);
  }).catch(err=>{
    if(reqId!==_xspeciesDiseaseReqId)return;
    debugError("cross-species disease search failed:",err);
    list.innerHTML=`<div role="alert" style="padding:20px;text-align:center;color:var(--gray-500)">${escapeHtml(t("loadFailed"))}</div>`;
  });
}

/* 横断検索結果クリック時: その種を選択して疾患DBで該当疾患を開く */
function openDiseaseAcrossSpecies(name,species){
  const needSwitch=species&&species!==currentSpecies;
  if(needSwitch&&typeof selectSpecies==="function")selectSpecies(species);
  switchView("database");
  const panel=document.getElementById("viewDatabase");
  if(panel)scrollToAnchor(panel);
  let tries=0;
  const apply=()=>{
    /* 種切替後は loadDiseaseDb が非同期で allDiseases を更新する。対象疾患がロード済みになるまで待つ
       （前の種のデータが残っていても誤って処理しないよう、疾患名の存在で判定） */
    if(needSwitch){
      const ready=currentSpecies===species&&allDiseases.some(d=>d.name===name||d.name_ja===name);
      if(!ready&&tries++<25){setTimeout(apply,150);return;}
    }
    diseaseFilter="";diseaseDisplayLimit=100;
    const input=document.getElementById("diseaseSearch");
    if(input)input.value=name;
    renderDiseaseDb();
    const list=document.getElementById("diseaseDbList");
    if(list){const pick=_pickListItemByName(list,name);if(pick&&!pick.querySelector(".disease-detail.open"))toggleDbItem(pick);}
  };
  setTimeout(apply,needSwitch?200:0);
}
document.addEventListener("click",function(e){
  const btn=e.target.closest('[data-action="scroll-to-species"]');
  if(!btn)return;
  const target=document.getElementById("speciesSection");
  if(target)scrollToAnchor(target);
});

/* --- Cross-view navigation history (shared by all views) --- */
let _navHistory=[];
function _pushNavHistory(fromView,toView,query){
  _navHistory.push({from:fromView,to:toView,query:query||"",ts:Date.now()});
  if(_navHistory.length>10)_navHistory.shift();
}
function _showBackNav(containerId,searchInputId){
  const c=document.getElementById(containerId);
  if(!c||!_navHistory.length)return;
  const last=_navHistory[_navHistory.length-1];
  const vn={checker:{ja:"鑑別診断",en:"Checker"},database:{ja:"疾患DB",en:"Disease DB"},chat:{ja:"臨床相談",en:"Chat"},drugs:{ja:"薬品辞書",en:"Drugs"},anesthesia:{ja:"麻酔",en:"Anesthesia"},emergency:{ja:"緊急",en:"Emergency"}};
  const fn=vn[last.from]?(currentLang==="ja"?vn[last.from].ja:vn[last.from].en):last.from;
  c.innerHTML=`<button type="button" class="nav-back-btn" data-cid="${containerId}" data-sid="${searchInputId}">← ${fn}${currentLang==="ja"?"に戻る":""}</button><button type="button" class="nav-clear-btn" data-cid="${containerId}" data-sid="${searchInputId}">✕ ${currentLang==="ja"?"検索クリア":"Clear"}</button>`;
  c.style.display="flex";
}
document.addEventListener("click",function(e){
  const bb=e.target.closest(".nav-back-btn");
  if(bb){const si=bb.dataset.sid;if(si){const inp=document.getElementById(si);if(inp){inp.value="";inp.dispatchEvent(new Event("input"));}}const ci=document.getElementById(bb.dataset.cid);if(ci){ci.style.display="none";ci.innerHTML="";}if(_navHistory.length){const last=_navHistory.pop();switchView(last.from);
    /* switchView only auto-scrolls when the mobile menu was open, so a back tap on
       desktop switched the tab but left the page at its previous scroll position —
       the returned panel (which sits far below the landing sections) could be
       off-screen. Carry the viewport to the returned view's useful entry point,
       mirroring the tab-click and cross-link navigation. */
    const rv=last.from;const target=rv==="checker"?document.getElementById("speciesSection"):document.getElementById("view"+rv.charAt(0).toUpperCase()+rv.slice(1));if(target)scrollToAnchor(target);}return;}
  const cb=e.target.closest(".nav-clear-btn");
  if(cb){const si=cb.dataset.sid;if(si){const inp=document.getElementById(si);if(inp){inp.value="";inp.dispatchEvent(new Event("input"));}}const ci=document.getElementById(cb.dataset.cid);if(ci){ci.style.display="none";ci.innerHTML="";}return;}
});

let _drugNavReturnView=null;
function navigateToDrug(drugName){
  _pushNavHistory(currentView,"drugs",drugName);
  _drugNavReturnView=currentView;
  switchView("drugs");
  const input=document.getElementById("drugSearch");
  if(input){input.value=drugName;input.dispatchEvent(new Event("input"));}
  _showBackNav("drugBackNav","drugSearch");
  const panel=document.getElementById("viewDrugs");
  if(panel)scrollToAnchor(panel);
  setTimeout(()=>{
    const list=document.getElementById("drugList");
    if(!list)return;
    /* Prefer the item whose base name exactly matches the search term. The drug
       filter is a substring match, so "デトミジン" also lists Medetomidine and
       "メデトミジン" also lists Dexmedetomidine; matching the base name (before any
       brand suffix in parentheses) lands on the intended drug, not the first row. */
    const pick=_pickListItemByName(list,drugName);
    if(pick&&!pick.querySelector(".disease-detail.open"))toggleDbItem(pick);
  },350);
}
/* Differential pivot: one tap from a disease-detail symptom list to the symptom
   checker pre-filled with that disease's own signs, auto-analyzed. Lets a vet
   reading a disease immediately see what else presents the same way ("reverse
   lookup"), landing directly on the ranked results. Symptom IDs are filtered
   against the checker vocabulary for the loaded species, so an unmappable set
   degrades to a toast instead of a broken checker state. */
function _differentialCheckButton(d){
  let ids=[];
  if(Array.isArray(d.symptoms_display)&&d.symptoms_display.length)ids=d.symptoms_display.map(s=>s&&s.id).filter(Boolean);
  else if(Array.isArray(d.symptoms))ids=d.symptoms.filter(s=>typeof s==="string");
  else if(d.symptoms&&typeof d.symptoms==="object")ids=Object.keys(d.symptoms);
  if(!ids.length)return "";
  return `<div class="diff-check-nav"><button type="button" class="differential-check-btn" data-ids="${escapeHtml(ids.join(","))}">\u{1F50D} ${currentLang==="ja"?"この症状セットで鑑別チェック（似た疾患を探す）":"Run differential with these signs"} →</button></div>`;
}
function runDifferentialFromDisease(idsCsv){
  const ids=String(idsCsv||"").split(",").filter(Boolean);
  const valid=new Set((symptomData||[]).map(s=>s.id));
  const usable=ids.filter(id=>valid.has(id));
  if(!usable.length){
    if(typeof showToast==="function")showToast(currentLang==="ja"?"この疾患の症状はチェッカー項目に対応していません":"These signs are not in the checker's symptom list","warning");
    return;
  }
  selectedSymptoms=new Set(usable);
  renderSelectedSymptoms();
  renderSymptomList(symptomData);
  _pushNavHistory(currentView,"checker","");
  switchView("checker");
  trackEvent("differential_from_disease",{species:currentSpecies,symptom_count:usable.length});
  doAnalyze();
}
/* Guided-consultation → checker pivot: carry the interview's confirmed symptom
   set into the checkbox checker pre-selected and auto-analyzed, so the vet can
   fine-tune signs one checkbox at a time instead of restarting the interview.
   Completes the two-way flow with the checker's low-confidence banner, which
   already pivots checker → guided mode. Waits for the species' checker
   vocabulary to load when the guided species differs from the loaded one. */
function runCheckerFromGuided(){
  const sp=guidedState.species||currentSpecies||"dog";
  const ids=(guidedState.selectedSymptoms||[]).slice();
  if(!ids.length)return;
  const needSwitch=sp!==currentSpecies;
  if(needSwitch&&typeof selectSpecies==="function")selectSpecies(sp);
  let tries=0;
  const apply=()=>{
    const valid=new Set((symptomData||[]).map(s=>s.id));
    const usable=ids.filter(id=>valid.has(id));
    if(needSwitch&&(currentSpecies!==sp||!usable.length)&&tries++<25){setTimeout(apply,150);return;}
    if(!usable.length){
      if(typeof showToast==="function")showToast(currentLang==="ja"?"症状セットをチェッカーに引き継げませんでした":"Could not carry the symptom set into the checker","warning");
      return;
    }
    selectedSymptoms=new Set(usable);
    renderSelectedSymptoms();
    renderSymptomList(symptomData);
    _pushNavHistory(currentView,"checker","");
    switchView("checker");
    trackEvent("checker_from_guided",{species:sp,symptom_count:usable.length});
    doAnalyze();
  };
  setTimeout(apply,needSwitch?200:0);
}
/* Related diseases: compute the closest differentials for a disease by counting
   shared symptoms across the currently-loaded species list (allDiseases), mirroring
   the server-rendered SEO page. Rendered lazily on expand so browsing stays fast.
   Clicking a chip jumps to that disease and expands it (navigateToDiseaseDb). */
function _diseaseSymptomSet(d){
  const s=d&&d.symptoms;
  if(Array.isArray(s))return new Set(s);
  if(s&&typeof s==="object")return new Set(Object.keys(s));
  return new Set();
}
function computeRelatedDiseases(diseaseName,maxItems){
  if(!Array.isArray(allDiseases)||!allDiseases.length)return [];
  const self=allDiseases.find(x=>(x.name||"")===diseaseName||(x.name_ja||"")===diseaseName);
  if(!self)return [];
  const mine=_diseaseSymptomSet(self);
  if(mine.size<2)return [];
  const out=[];
  for(const other of allDiseases){
    if(other===self||other._catHeader)continue;
    if((other.name||"")===(self.name||""))continue;
    let shared=0;
    const os=_diseaseSymptomSet(other);
    for(const sym of os){if(mine.has(sym)){shared++;}}
    if(shared>=2)out.push({name:other.name||"",name_ja:other.name_ja||"",shared:shared});
  }
  out.sort((a,b)=>b.shared-a.shared);
  return out.slice(0,maxItems||6);
}
function hydrateRelatedDiseases(root){
  const holders=(root||document).querySelectorAll(".related-diseases-section[data-related='1']");
  holders.forEach(holder=>{
    holder.dataset.related="0";
    const name=holder.dataset.disease||"";
    const related=computeRelatedDiseases(name,6);
    if(!related.length){holder.remove();return;}
    const heading=currentLang==="ja"?"関連する疾患（共通症状）":"Related Diseases (shared signs)";
    const chips=related.map(r=>{
      const label=currentLang==="ja"?(r.name_ja||r.name):(r.name||r.name_ja);
      return `<button type="button" class="related-disease-chip" data-name="${escapeHtml(r.name||r.name_ja)}">${escapeHtml(label)}<span class="related-disease-shared">${r.shared}</span></button>`;
    }).join("");
    holder.innerHTML=`<div class="related-diseases-heading">${heading}</div><div class="related-diseases-list">${chips}</div>`;
  });
}
/* Pick the list row whose name exactly matches the navigation query. The list
   filter is a substring match, so navigating to "Gastritis" also lists
   "Chronic Gastritis" (which sorts first) — expanding the first row then opens
   the WRONG disease. Prefer an exact base-name match (before any parenthetical
   suffix, case-insensitive) in either language, mirroring the same fix already
   applied to drug navigation; fall back to the first row only when nothing
   matches exactly. */
function _pickListItemByName(list,query){
  const items=[...list.querySelectorAll(".disease-db-item")];
  if(!items.length)return null;
  const base=s=>String(s||"").toLowerCase().split(/[(（]/)[0].trim();
  const target=base(query);
  return items.find(it=>base(it.dataset.name)===target||base(it.dataset.nameJa)===target)||items[0];
}
function navigateToDiseaseDb(query){
  _pushNavHistory(currentView,"database",query);
  switchView("database");
  const input=document.getElementById("diseaseSearch");
  if(input){input.value=query;input.dispatchEvent(new Event("input"));}
  _showBackNav("diseaseBackNav","diseaseSearch");
  const panel=document.getElementById("viewDatabase");
  if(panel)scrollToAnchor(panel);
  setTimeout(()=>{
    const list=document.getElementById("diseaseDbList");
    if(!list)return;
    const pick=_pickListItemByName(list,query);
    if(pick&&!pick.querySelector(".disease-detail.open"))toggleDbItem(pick);
  },350);
}

/* タブ/メニューのタップ後に着地させる要素。検索主体のビュー（薬品/疾患DB/麻酔/救急）は
   パネル先頭ではなく検索入力欄に直接着地させ、タップ→即入力できるようにする。
   薬品タブはパネル先頭に比較表・相互作用チェッカーのアコーディオンがあり、
   パネル先頭着地では検索欄が画面外に残っていた（利用者報告）。 */
function _navLandingTarget(view){
  if(view==="checker")return document.getElementById("speciesSection")||document.getElementById("viewChecker");
  /* 相談タブ: モード切替（自由入力/問診）＋チャット欄が見える位置に着地 */
  if(view==="chat")return document.querySelector("#viewChat .chat-mode-toggle")||document.getElementById("viewChat");
  const searchInputs={database:"diseaseSearch",drugs:"drugSearch",anesthesia:"anesthesiaSearch",emergency:"emergencySearch"};
  const input=searchInputs[view]?document.getElementById(searchInputs[view]):null;
  if(input)return input.closest(".symptom-search")||input;
  return document.getElementById("view"+view.charAt(0).toUpperCase()+view.slice(1));
}
function switchView(view,opts){
  /* opts.silent — skip event tracking + auto-focus (used for initial hash routing
     on page load so the soft keyboard does not pop up unexpectedly on mobile).
     opts.focusSearch — focus the view's primary search input within the tap gesture
     so the mobile soft keyboard opens (used for explicit tab/menu taps). */
  opts=opts||{};
  if(!opts.silent)trackEvent("switch_view",{view:view});
  currentView=view;
  const views=["checker","database","chat","drugs","anesthesia","emergency"];
  const prefersReduced=window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  views.forEach(v=>{
    const tab=document.getElementById("tab-"+v);
    const panel=document.getElementById("view"+v.charAt(0).toUpperCase()+v.slice(1));
    if(tab)tab.setAttribute("aria-selected",v===view);
    if(panel){
      if(v===view){panel.classList.remove("hidden");if(!prefersReduced&&!opts.silent)panel.style.animation="fade-tab-in .3s ease-out";}
      else{panel.classList.add("hidden");panel.style.animation="";}
    }
  });
  history.replaceState(null,null,"#"+view);
  updateBreadcrumb();
  updateMobileBottomNav();
  /* Re-measure the sticky chrome AFTER the breadcrumb is shown/updated: the
     breadcrumb bar is display:none until a view becomes active, so it only
     becomes measurable once this switch has happened. Measuring any earlier
     (page load, or before the switch) undercounts it and the first navigation
     lands with the panel heading tucked under the header. Callers scroll after
     switchView returns, so the offset is correct by then. */
  _syncStickyOffset();
  if(view==="drugs"&&!drugsLoaded)loadDrugDictionary();
  if(view==="anesthesia"&&!anesthesiaLoaded)loadAnesthesiaProtocols();
  if(view==="emergency"&&!emergencyLoaded)loadEmergencyProtocols();
  /* 動物種未選択で疾患DBを開いた場合、空白ではなく案内（種選択 + 横断検索ヒント）を表示 */
  if(view==="database"&&!currentSpecies){
    const dbList=document.getElementById("diseaseDbList");
    if(dbList&&!dbList.children.length)dbList.innerHTML=renderEmptyState("database");
  }
  /* フォーカス制御:
     - opts.silent（初期ハッシュルーティング）: フォーカスしない（モバイルでキーボードが勝手に出ない）
     - opts.focusSearch（タブ/メニューのタップ）: 検索ボックスへ同期フォーカス → モバイルでキーボードが開く
     - それ以外（既定）: パネル自体へプログラムフォーカス（キーボードは出さない） */
  const activePanel=document.getElementById("view"+view.charAt(0).toUpperCase()+view.slice(1));
  const searchIds={database:"diseaseSearch",chat:"chatInput",drugs:"drugSearch",anesthesia:"anesthesiaSearch",emergency:"emergencySearch"};
  const searchEl=searchIds[view]?document.getElementById(searchIds[view]):null;
  if(opts.silent){
    /* 初期ルーティング: フォーカスもキーボードも出さない */
  }else if(opts.focusSearch&&searchEl){
    /* ユーザー操作と同じ同期コンテキストで focus → iOS/Android でソフトキーボードが起動する */
    try{searchEl.focus({preventScroll:true});}catch(_){searchEl.focus();}
  }else if(activePanel){
    if(!activePanel.hasAttribute("tabindex"))activePanel.setAttribute("tabindex","-1");
    try{activePanel.focus({preventScroll:true});}catch(_){activePanel.focus();}
  }
  /* モバイル: ハンバーガーメニューを閉じる + コンテンツへスクロール */
  const nav=document.getElementById("mainNav");
  if(nav&&nav.classList.contains("open")){
    nav.classList.remove("open");
    const hb=document.querySelector(".hamburger");
    if(hb)hb.setAttribute("aria-expanded","false");
    if(activePanel)setTimeout(()=>scrollToAnchor(_navLandingTarget(view)||activePanel),100);
  }
}

function setupNavigation(){
  const nav=document.getElementById("mainNav");
  if(!nav){debugWarn("mainNav element not found");return;}
  nav.addEventListener("click",e=>{
    const tab=e.target.closest("[role=tab]");
    if(!tab)return;
    const view=tab.dataset.view;
    const menuWasOpen=nav.classList.contains("open");
    switchView(view,{focusSearch:true});
    /* On desktop the content panels sit far below the landing sections, so a
       bare view switch happens off-screen and looks like a no-op. Scroll the
       chosen panel (or the species picker, which is the checker's entry point)
       into view. switchView already scrolls when the mobile menu was open. */
    if(!menuWasOpen){
      const target=_navLandingTarget(view);
      if(target)scrollToAnchor(target);
    }
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
    if(["checker","database","chat","drugs","anesthesia","emergency"].includes(hash))switchView(hash);
  });
}

function setupChat(){
  const chatSend=document.getElementById("chatSend");
  const chatInput=document.getElementById("chatInput");
  const landingChatSend=document.getElementById("landingChatSend");
  const landingChatInput=document.getElementById("landingChatInput");
  if(chatSend)chatSend.addEventListener("click",()=>sendChatMessage());
  if(chatInput)chatInput.addEventListener("keydown",e=>{if(e.key==="Enter"&&!e.isComposing)sendChatMessage();});
  if(landingChatSend)landingChatSend.addEventListener("click",()=>sendLandingChat());
  if(landingChatInput)landingChatInput.addEventListener("keydown",e=>{if(e.key==="Enter"&&!e.isComposing)sendLandingChat();});
  attachChatCharCounter(chatInput);
  addChatQuickSuggestions();
}

function attachChatCharCounter(input){
  if(!input||!input.maxLength||input.maxLength<=0)return;
  const row=input.closest(".chat-input-row");
  if(!row||row.querySelector(".chat-char-counter"))return;
  const max=input.maxLength;
  const counter=document.createElement("div");
  counter.className="chat-char-counter";
  counter.setAttribute("aria-live","off");
  const update=()=>{
    const n=input.value.length;
    counter.textContent=`${n}/${max}`;
    counter.classList.toggle("near-limit",n>=Math.floor(max*0.8));
    counter.classList.toggle("at-limit",n>=max);
  };
  input.addEventListener("input",update);
  row.insertAdjacentElement("afterend",counter);
  update();
}

function addChatQuickSuggestions(){
  const welcome=document.getElementById("chatWelcome");
  if(!welcome||welcome.querySelector(".chat-quick-suggestions"))return;
  const suggestions=currentLang==="ja"
    ?["犬 嘔吐 食欲不振","猫 くしゃみ 鼻水 目やに","犬 多飲多尿 体重減少","猫 血尿 頻尿","ウサギ 食べない お腹が張っている"]
    :["dog vomiting lethargy","cat sneezing nasal discharge","dog PU/PD weight loss","cat hematuria stranguria","rabbit anorexia bloating"];
  const div=document.createElement("div");
  div.className="chat-quick-suggestions";
  div.innerHTML=`<span class="chat-quick-label">${currentLang==="ja"?"💬 タップで入力:":"💬 Quick input:"}</span>`
    +suggestions.map(s=>`<button class="chat-quick-btn">${s}</button>`).join("");
  div.querySelectorAll(".chat-quick-btn").forEach(btn=>{
    btn.addEventListener("click",()=>{
      const input=document.getElementById("chatInput");
      const send=document.getElementById("chatSend");
      if(input)input.value=btn.textContent;
      if(send)send.click();
    });
  });
  welcome.appendChild(div);
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

const _CHAT_MAX_RETRIES=3;
let _landingChatRetries=0;
let _chatRetries=0;

function sendLandingChat(isRetry){
  const input=document.getElementById("landingChatInput"),text=input.value.trim();if(!text)return;
  const sendBtn=input.closest(".chat-input-row")?.querySelector("button");
  // Reset retry counter for a fresh user-initiated send so a previous failure
  // doesn't prevent retries on a new question.
  if(!isRetry)_landingChatRetries=0;
  input.value="";input.disabled=true;if(sendBtn)sendBtn.disabled=true;
  const msgs=document.getElementById("landingChatMessages");
  const userDiv=document.createElement("div");userDiv.className="chat-msg user";userDiv.textContent=text;msgs.appendChild(userDiv);msgs.scrollTop=msgs.scrollHeight;
  const species=chatSpecies||currentSpecies||"dog";
  const loading=document.createElement("div");loading.className="chat-msg bot typing-indicator";loading.innerHTML='<span class="dot"></span><span class="dot"></span><span class="dot"></span>';msgs.appendChild(loading);msgs.scrollTop=msgs.scrollHeight;
  fetchWithTimeout("/api/diagnostic-chat/chat",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message:text,species:species,previous_symptoms:chatAccumulatedSymptoms,lang:currentLang})},20000)
  .then(r=>{if(!r.ok)throw new Error(`HTTP ${r.status}`);return r.json();})
  .then(data=>{
    loading.remove();input.disabled=false;if(sendBtn)sendBtn.disabled=false;input.focus();
    if(!data){addChatMsg(t("noResponse"),"bot");return;}
    if(data.species)chatSpecies=data.species;
    if(data.accumulated_symptoms) chatAccumulatedSymptoms=data.accumulated_symptoms;
    renderChatResult(msgs,data);
    /* Keep a single "Continue in Clinical Chat" affordance — remove any from a
       previous response so they don't stack up across multiple messages. */
    msgs.querySelectorAll(".landing-chat-continue").forEach(el=>el.remove());
    const continueBtn=document.createElement("div");
    continueBtn.className="landing-chat-continue";
    continueBtn.innerHTML=`<button class="landing-continue-btn">${currentLang==="ja"?"臨床相談で詳しく相談する →":"Continue in Clinical Chat →"}</button>`;
    continueBtn.querySelector("button").addEventListener("click",()=>{
      switchView("chat");
      const mainMsgs=document.getElementById("chatMessages");
      if(mainMsgs){
        const clones=msgs.querySelectorAll(".chat-msg");
        clones.forEach(c=>{if(!c.classList.contains("typing-indicator")){const cl=c.cloneNode(true);mainMsgs.appendChild(cl);}});
        mainMsgs.scrollTop=mainMsgs.scrollHeight;
      }
      const chatPanel=document.getElementById("viewChat");
      if(chatPanel)scrollToAnchor(chatPanel);
    });
    msgs.appendChild(continueBtn);
    msgs.scrollTop=msgs.scrollHeight;
    _landingChatRetries=0;
  })
  .catch(err=>{
    loading.remove();input.disabled=false;if(sendBtn)sendBtn.disabled=false;
    debugError("Chat error:",err);
    // Restore user input so they don't lose it
    if(!input.value)input.value=text;
    const errDiv=document.createElement("div");errDiv.className="chat-msg bot";errDiv.setAttribute("role","alert");
    const canRetry=_landingChatRetries<_CHAT_MAX_RETRIES;
    const retryBtnHtml=`<button type="button" class="landing-retry-btn" style="margin-top:6px;margin-right:6px;padding:6px 14px;background:var(--navy);color:var(--white);border:none;border-radius:6px;font-size:.78rem;cursor:pointer">${t("retry")}</button>`;
    if(canRetry){
      errDiv.innerHTML=escapeHtml(t("commError"))+" "+retryBtnHtml;
      errDiv.querySelector(".landing-retry-btn").addEventListener("click",()=>{_landingChatRetries++;input.value=text;errDiv.remove();sendLandingChat(true);});
    }else{
      const giveUpMsg=currentLang==="ja"?"接続に失敗しました。ネットワークをご確認のうえ、しばらくしてから再度お試しください。":"Connection failed. Please check your network and try again later.";
      const reloadLabel=currentLang==="ja"?"ページを再読み込み":"Reload page";
      const reloadBtn=`<button type="button" class="landing-reload-btn" style="margin-top:6px;padding:6px 14px;background:var(--gray-200);color:var(--gray-800);border:none;border-radius:6px;font-size:.78rem;cursor:pointer">${reloadLabel}</button>`;
      errDiv.innerHTML=escapeHtml(giveUpMsg)+"<div style=\"margin-top:6px\">"+retryBtnHtml+reloadBtn+"</div>";
      errDiv.querySelector(".landing-retry-btn").addEventListener("click",()=>{_landingChatRetries=0;input.value=text;errDiv.remove();sendLandingChat(true);});
      errDiv.querySelector(".landing-reload-btn").addEventListener("click",()=>location.reload());
    }
    msgs.appendChild(errDiv);
    msgs.scrollTop=msgs.scrollHeight;
  });
}

// Accumulated symptoms for chat conversation continuity
let chatAccumulatedSymptoms=[];
let chatDeniedSymptoms=[];

function _sendSymptomUpdate(symptomId,confirmed){
  const species=chatSpecies||currentSpecies||"dog";
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
    if(data.species)chatSpecies=data.species;
    if(data.accumulated_symptoms)chatAccumulatedSymptoms=data.accumulated_symptoms;
    renderChatResult(msgs,data);
  })
  .catch(err=>{loading.remove();debugError("Symptom update error:",err);});
}

function sendChatMessage(isRetry){
  const input=document.getElementById("chatInput"),text=input.value.trim();if(!text)return;
  const sendBtn=document.getElementById("chatSend");
  // Reset retry counter on a fresh user-initiated send so a previous failure
  // doesn't prevent retries on a new question.
  if(!isRetry)_chatRetries=0;
  input.value="";input.disabled=true;if(sendBtn){sendBtn.disabled=true;sendBtn.setAttribute("aria-busy","true");}
  trackEvent("chat_message",{species:chatSpecies||currentSpecies||"dog",message_length:text.length});
  addChatMsg(text,"user");const species=chatSpecies||currentSpecies||"dog";
  const msgs=document.getElementById("chatMessages");
  const loading=document.createElement("div");loading.className="chat-msg bot typing-indicator";loading.setAttribute("aria-label",currentLang==="ja"?"解析中":"Analyzing");loading.innerHTML='<span class="dot"></span><span class="dot"></span><span class="dot"></span>';msgs.appendChild(loading);msgs.scrollTop=msgs.scrollHeight;
  const slowTimer=setTimeout(()=>{loading.innerHTML='<span class="dot"></span><span class="dot"></span><span class="dot"></span><div style="font-size:.72rem;color:var(--gray-400);margin-top:4px">'+(currentLang==="ja"?"解析中... 通常より時間がかかっています":"Analyzing... taking longer than usual")+'</div>';},3000);
  fetchWithTimeout("/api/diagnostic-chat/chat",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message:text,species:species,previous_symptoms:chatAccumulatedSymptoms,lang:currentLang})},20000)
  .then(r=>{if(!r.ok)throw new Error(`HTTP ${r.status}`);return r.json();})
  .then(data=>{
    clearTimeout(slowTimer);loading.remove();input.disabled=false;if(sendBtn){sendBtn.disabled=false;sendBtn.removeAttribute("aria-busy");}input.focus();
    if(!data){addChatMsg(t("noResponse"),"bot");return;}
    if(data.species)chatSpecies=data.species;
    if(data.accumulated_symptoms) chatAccumulatedSymptoms=data.accumulated_symptoms;
    renderChatResult(msgs,data);
    _chatRetries=0;
  })
  .catch(err=>{
    clearTimeout(slowTimer);loading.remove();input.disabled=false;if(sendBtn){sendBtn.disabled=false;sendBtn.removeAttribute("aria-busy");}
    debugError("Chat error:",err);
    trackEvent("api_error",{endpoint:"diagnostic-chat",error:String(err.message||"unknown").substring(0,100),species:currentSpecies});
    // Restore user input so it isn't lost
    if(!input.value)input.value=text;
    const errDiv=document.createElement("div");errDiv.className="chat-msg bot";errDiv.setAttribute("role","alert");
    const canRetry=_chatRetries<_CHAT_MAX_RETRIES;
    const retryHtml=`<button type="button" class="chat-retry-btn" style="margin-top:6px;margin-right:6px;padding:6px 14px;background:var(--navy);color:var(--white);border:none;border-radius:6px;font-size:.78rem;cursor:pointer">${t("retry")}</button>`;
    if(canRetry){
      errDiv.innerHTML=escapeHtml(t("commError"))+" "+retryHtml;
      errDiv.querySelector(".chat-retry-btn").addEventListener("click",()=>{_chatRetries++;input.value=text;errDiv.remove();sendChatMessage(true);});
    }else{
      const giveUpMsg=currentLang==="ja"?"接続に失敗しました。ネットワークをご確認のうえ、しばらくしてから再度お試しください。":"Connection failed. Please check your network and try again later.";
      const reloadLabel=currentLang==="ja"?"ページを再読み込み":"Reload page";
      const reloadBtn=`<button type="button" class="chat-reload-btn" style="margin-top:6px;padding:6px 14px;background:var(--gray-200);color:var(--gray-800);border:none;border-radius:6px;font-size:.78rem;cursor:pointer">${reloadLabel}</button>`;
      errDiv.innerHTML=escapeHtml(giveUpMsg)+"<div style=\"margin-top:6px\">"+retryHtml+reloadBtn+"</div>";
      errDiv.querySelector(".chat-retry-btn").addEventListener("click",()=>{_chatRetries=0;input.value=text;errDiv.remove();sendChatMessage(true);});
      errDiv.querySelector(".chat-reload-btn").addEventListener("click",()=>location.reload());
    }
    msgs.appendChild(errDiv);msgs.scrollTop=msgs.scrollHeight;
  });
}

function renderChatResult(container,data){
  const wrapper=document.createElement("div");
  wrapper.className="chat-msg bot chat-result";

  // 0. AI/clinical disclaimer banner — show only on the first result in this
  //    container to avoid repetitive noise after multiple exchanges. The
  //    persistent disclaimer in the chat welcome message + the per-result
  //    short footer (step 6) still keep the warning visible.
  if(!container.dataset.disclaimerShown){
    const disclaim=document.createElement("div");
    disclaim.className="chat-disclaimer-banner";
    disclaim.setAttribute("role","note");
    const disclaimText=currentLang==="ja"
      ?"⚠ AI鑑別診断結果は参考情報です。確定診断には病歴・身体検査・追加検査との総合判断が必要です。"
      :"⚠ AI differential diagnosis results are reference information. Definitive diagnosis requires integration with history, physical exam, and additional diagnostics.";
    disclaim.style.cssText="font-size:.74rem;color:#92400e;background:#fef3c7;border-left:3px solid #d97706;padding:8px 10px;border-radius:4px;margin-bottom:10px;line-height:1.5";
    disclaim.textContent=disclaimText;
    wrapper.appendChild(disclaim);
    container.dataset.disclaimerShown="1";
  }

  // 0.5. Clinical reasoning (Vetlexicon-style structured support)
  if(data.clinical_reasoning){
    const cr=renderClinicalReasoning(data.clinical_reasoning);
    if(cr)wrapper.appendChild(cr);
  }

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
      // Prefer the backend-calibrated confidence_percent (IDF + prevalence + cluster boost)
      // over the raw Jaccard similarity_score so vets see the same value the model ranks by.
      const pct=Math.round(c.confidence_percent!=null?c.confidence_percent:(c.similarity_score||0)*100);
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
        ${c.matched_symptoms&&c.matched_symptoms.length?`<div class="chat-disease-matched">${currentLang==="ja"?"\u4e00\u81f4: ":"Matched: "}${escapeHtml(c.matched_symptoms.map(sid=>{const f=(symptoms||[]).find(s=>s&&s.id===sid);return f?(currentLang==="ja"?(f.name_ja||f.name_en||sid):(f.name_en||f.name_ja||sid)):sid;}).join(", "))}</div>`:""}
        ${c.mentioned_drugs&&c.mentioned_drugs.length?renderMentionedDrugs(c):""}
        <div class="chat-disease-nav"><button type="button" class="chat-disease-open" data-name="${escapeHtml(c.name_en||c.name_ja||c.disease_id||"")}" data-species="${escapeHtml(chatSpecies||currentSpecies||"dog")}">\u{1F50D} ${currentLang==="ja"?"\u75be\u60a3DB\u3067\u8a73\u7d30\u3092\u958b\u304f":"Open in disease DB"} \u2192</button></div>
      `;
      listDiv.appendChild(card);
    });
    wrapper.appendChild(listDiv);
  } else if(symptoms.length>0){
    const noMatch=document.createElement("div");
    noMatch.className="chat-no-match";
    const headJa="\u8a72\u5f53\u3059\u308b\u75be\u60a3\u304c\u898b\u3064\u304b\u308a\u307e\u305b\u3093\u3067\u3057\u305f";
    const headEn="No matching diseases found";
    const tipsJa=["\u4ed6\u306e\u75c7\u72b6\uff08\u98df\u6b32\u30fb\u5143\u6c17\u30fb\u4f53\u91cd\u5909\u5316\u306a\u3069\uff09\u3092\u8ffd\u52a0\u3057\u3066\u307f\u308b","\u4ee3\u66ff\u8868\u73fe\uff08\u4f8b: \u300c\u4e0b\u75e2\u300d\u2194\u300c\u8edf\u4fbf\u300d\u3001\u300cPU/PD\u300d\u2194\u300c\u591a\u98f2\u591a\u5c3f\u300d\uff09\u3092\u8a66\u3059","\u52d5\u7269\u7a2e\u304c\u6b63\u3057\u304f\u9078\u629e\u3055\u308c\u3066\u3044\u308b\u304b\u78ba\u8a8d"];
    const tipsEn=["Add related signs (appetite, energy, weight change)","Try synonyms (e.g., 'diarrhea' \u2194 'loose stool')","Verify the correct species is selected"];
    const tips=currentLang==="ja"?tipsJa:tipsEn;
    const head=currentLang==="ja"?headJa:headEn;
    noMatch.innerHTML=`<div style="font-weight:600;color:var(--navy);margin-bottom:4px">${escapeHtml(head)}</div><ul style="text-align:left;display:inline-block;margin:0;padding-left:18px;font-size:.78rem;color:var(--gray-700);line-height:1.6">${tips.map(x=>`<li>${escapeHtml(x)}</li>`).join("")}</ul>`;
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
          btn.type="button";
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
            btn.type="button";
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
          btn.type="button";
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
        return `<button type="button" class="common-disease-tag ${cls}" data-disease="${escapeHtml(d.name||n)}" title="${currentLang==="ja"?"疾患の詳細を開く":"Open disease details"}">${escapeHtml(n)}</button>`;
      }).join("");
      chatRef.innerHTML=`<div class="common-diseases-section compact">
        <div class="common-diseases-header">${currentLang==="ja"?"📋 この動物種でよくみられる疾患":"📋 Common diseases in this species"}</div>
        ${veryCommon.length?`<div class="common-diseases-group">${renderTags(veryCommon,"tag-very-common")}</div>`:""}
        ${common.length?`<div class="common-diseases-group">${renderTags(common,"tag-common")}</div>`:""}
      </div>`;
      _attachCommonDiseaseNav(chatRef);
    }).catch(err=>{debugWarn("common-diseases fetch failed:",err);});
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
    freeBtn.setAttribute("aria-selected","false");guidedBtn.setAttribute("aria-selected","true");
    freeCont.classList.add("hidden");guidedCont.classList.remove("hidden");
    startGuidedConsultation();
  } else {
    guidedBtn.classList.remove("active");freeBtn.classList.add("active");
    guidedBtn.setAttribute("aria-selected","false");freeBtn.setAttribute("aria-selected","true");
    guidedCont.classList.add("hidden");freeCont.classList.remove("hidden");
  }
}

function startGuidedConsultation(){
  guidedState={species:currentSpecies||"dog",selectedSymptoms:[],answeredCategories:[],onset:null,ageYears:null,ageCategory:null,painScore:null,phase:"start",breed:currentBreed||""};
  const msgs=document.getElementById("guidedMessages");
  const actions=document.getElementById("guidedActions");
  if(msgs)msgs.innerHTML="";
  if(actions)actions.innerHTML="";
  // Pre-fetch breeds for autocomplete if not already cached for current species
  if((!cachedBreeds||cachedBreeds.length===0)&&guidedState.species){
    fetchWithTimeout("/api/breeds/"+guidedState.species).then(r=>r.json()).then(data=>{
      if(data&&data.breeds)cachedBreeds=data.breeds;
    }).catch(()=>{});
  }
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
    age_category:guidedState.ageCategory,
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
      // Use backend-calibrated confidence_percent (same field used in free-input chat results).
      const pct=Math.round(c.confidence_percent!=null?c.confidence_percent:(c.similarity_score||0)*100);
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
  // Breed autocomplete datalist (reuses cachedBreeds populated for current species)
  const breedDatalistId="guidedBreedDatalist";
  const breedOptionsHtml=(cachedBreeds&&cachedBreeds.length>0)
    ? cachedBreeds.map(b=>{
        const label=currentLang==="ja"?(b.name_ja||b.name||""):(b.name||b.name_ja||"");
        return `<option value="${escapeHtml(label)}"></option>`;
      }).join("")
    : "";
  let html='<div class="guided-context-questions">';
  if(breedOptionsHtml)html+=`<datalist id="${breedDatalistId}">${breedOptionsHtml}</datalist>`;
  questions.forEach(q=>{
    const label=currentLang==="ja"?q.question_ja:q.question_en;
    html+=`<div class="guided-context-q"><div class="guided-context-label">${label}</div>`;
    if(q.input_type==="text"){
      // Free-text input (e.g. breed) — wire datalist autocomplete for breed
      const ph=currentLang==="ja"?(q.placeholder_ja||""):(q.placeholder_en||"");
      const initialVal=q.type==="breed"?(guidedState.breed||""):"";
      const listAttr=(q.type==="breed"&&breedOptionsHtml)?` list="${breedDatalistId}"`:"";
      html+=`<div class="guided-context-text-wrap"><input type="text" class="guided-context-text-input" data-type="${q.type}" placeholder="${escapeHtml(ph)}" value="${escapeHtml(initialVal)}" autocomplete="off"${listAttr}></div>`;
    }else if(q.type==="age"){
      // Age: dual-mode — categorical buttons (preferred) + optional numeric override
      // Buttons map directly to age_category for transparency
      const ageCats=[
        {value:"young",      label_ja:"幼若 (1歳未満)",    label_en:"Young (under 1y)"},
        {value:"young_adult",label_ja:"若齢 (1〜3歳)",     label_en:"Young adult (1–3y)"},
        {value:"adult",      label_ja:"成熟 (3〜7歳)",     label_en:"Adult (3–7y)"},
        {value:"senior",     label_ja:"高齢 (7歳以上)",    label_en:"Senior (7y+)"},
      ];
      html+='<div class="guided-context-options">';
      ageCats.forEach(o=>{
        const olabel=currentLang==="ja"?o.label_ja:o.label_en;
        html+=`<button class="guided-context-opt" data-type="age_category" data-value="${o.value}">${olabel}</button>`;
      });
      html+=`<button class="guided-context-opt skip" data-type="age_category" data-value="">${currentLang==="ja"?"スキップ":"Skip"}</button>`;
      html+='</div>';
    }else{
      html+='<div class="guided-context-options">';
      (q.options||[]).forEach(o=>{
        const olabel=currentLang==="ja"?o.label_ja:o.label_en;
        html+=`<button class="guided-context-opt" data-type="${q.type}" data-value="${o.value}">${olabel}</button>`;
      });
      html+=`<button class="guided-context-opt skip" data-type="${q.type}" data-value="">${currentLang==="ja"?"スキップ":"Skip"}</button>`;
      html+='</div>';
    }
    html+='</div>';
  });
  html+=`<div class="guided-bottom-actions"><button class="guided-action-btn primary" id="guidedFinalizeBtn">${t("guidedFinish")}</button></div>`;
  html+='</div>';
  guidedSetActions(html);

  // Map age_category back to representative ageYears for backend compatibility
  const _ageCategoryToYears={young:0.5,young_adult:2.0,adult:5.0,senior:10.0};

  // Context option selection (buttons)
  document.querySelectorAll(".guided-context-opt").forEach(btn=>{
    btn.addEventListener("click",()=>{
      const type=btn.dataset.type;
      const val=btn.dataset.value;
      // Deselect siblings
      btn.parentElement.querySelectorAll(".guided-context-opt").forEach(b=>b.classList.remove("selected"));
      if(val)btn.classList.add("selected");
      if(type==="onset"&&val)guidedState.onset=val;
      if(type==="age"&&val)guidedState.ageYears=parseFloat(val);
      if(type==="age_category"){
        if(val){
          guidedState.ageCategory=val;
          // Also set ageYears so backend's analyze_species_symptoms (which uses age_years)
          // can apply its own age multiplier consistently
          if(_ageCategoryToYears[val]!==undefined)guidedState.ageYears=_ageCategoryToYears[val];
        }else{
          guidedState.ageCategory=null;
          guidedState.ageYears=null;
        }
      }
      if(type==="pain_score"&&val!=="")guidedState.painScore=parseInt(val,10);
    });
  });
  // Text input handlers (e.g. breed)
  document.querySelectorAll(".guided-context-text-input").forEach(inp=>{
    const sync=()=>{
      const type=inp.dataset.type;
      const val=inp.value.trim();
      if(type==="breed")guidedState.breed=val;
    };
    inp.addEventListener("input",sync);
    inp.addEventListener("change",sync);
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
        <div class="chat-disease-nav"><button type="button" class="chat-disease-open" data-name="${escapeHtml(d.name||d.name_ja||"")}" data-species="${escapeHtml(guidedState.species||currentSpecies||"dog")}">\u{1F50D} ${currentLang==="ja"?"疾患DBで詳細を開く":"Open in disease DB"} →</button></div>
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

  // Action buttons: add more symptoms + checker pivot + restart
  const addMoreLabel=currentLang==="ja"?"+ 症状を追加して再診断":"+ Add symptoms & re-diagnose";
  const checkerLabel=currentLang==="ja"?"\u{1F9EA} チェッカーで症状を微調整して再解析":"\u{1F9EA} Refine signs in the checker";
  const checkerBtn=(guidedState.selectedSymptoms||[]).length>0
    ?`<button class="guided-action-btn secondary" id="guidedToChecker">${checkerLabel}</button>`
    :"";
  guidedSetActions(`<div class="guided-bottom-actions"><button class="guided-action-btn primary" id="guidedAddMore">${addMoreLabel}</button>${checkerBtn}<button class="guided-action-btn text" id="guidedRestartFinal">${t("guidedRestart")}</button></div>`);
  const addBtn=document.getElementById("guidedAddMore");
  if(addBtn)addBtn.addEventListener("click",()=>{guidedSetActions("");guidedFetch("next_category");});
  const chkBtn=document.getElementById("guidedToChecker");
  if(chkBtn)chkBtn.addEventListener("click",()=>{runCheckerFromGuided();});
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
  }).catch((err)=>{
    debugError("loadDrugDictionary failed:",err);
    list.innerHTML=`<div role="alert" style="padding:20px;text-align:center;color:var(--gray-500)">${t("loadFailed")}<br><button type="button" class="retry-drug-btn" style="margin-top:10px;padding:8px 20px;background:var(--navy);color:var(--white);border:none;border-radius:6px;cursor:pointer;font-size:.84rem">${t("reload")}</button></div>`;
    const rb=list.querySelector(".retry-drug-btn");
    if(rb)rb.addEventListener("click",()=>{drugsLoaded=false;loadDrugDictionary();});
  });
  if(!list.dataset.drugListenersAttached){
    list.dataset.drugListenersAttached="1";
    document.getElementById("drugSearch").addEventListener("input",debounce(renderDrugList,200));
    document.getElementById("drugCategoryFilter").addEventListener("change",()=>{renderDrugList();_revealFilteredList("drugList");});
    document.getElementById("drugSpeciesFilter").addEventListener("change",()=>{renderDrugList();_revealFilteredList("drugList");});
    const dwInput=document.getElementById("drugWeight");
    if(dwInput){
      const saved=localStorage.getItem("vetdict-drug-weight");
      if(saved&&!isNaN(parseFloat(saved)))dwInput.value=saved;
      dwInput.addEventListener("input",debounce(()=>{
        const v=dwInput.value.trim();
        if(v===""){localStorage.removeItem("vetdict-drug-weight");}
        else if(!isNaN(parseFloat(v))){localStorage.setItem("vetdict-drug-weight",v);}
        renderDrugList();
      },300));
    }
    // Interaction checker
    setupInteractionChecker();
  }
}

// Vetlexicon-style structured clinical reasoning renderer
function renderClinicalReasoning(reasoning){
  if(!reasoning)return null;
  const root=document.createElement("div");
  root.className="clinical-reasoning";
  root.style.cssText="margin:12px 0;padding:14px;background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px";
  // Emergency banner
  if(reasoning.emergency_alert){
    const eb=document.createElement("div");
    eb.style.cssText="background:#dc2626;color:#fff;padding:8px 12px;border-radius:6px;font-weight:700;font-size:.84rem;margin-bottom:10px";
    eb.textContent=currentLang==="ja"?"🚨 緊急対応が必要な可能性があります":"🚨 Possible emergency presentation";
    root.appendChild(eb);
  }
  // Bottom Line
  if(reasoning.bottom_line){
    const bl=document.createElement("div");
    bl.style.cssText="background:#1e40af;color:#fff;padding:10px 14px;border-radius:6px;margin-bottom:10px;font-size:.86rem;line-height:1.5";
    const blText=currentLang==="ja"?reasoning.bottom_line.ja:reasoning.bottom_line.en;
    const evGrade=reasoning.bottom_line_evidence||"C";
    bl.innerHTML=`<div style="font-weight:700;font-size:.78rem;margin-bottom:4px;letter-spacing:.05em">${currentLang==="ja"?"📋 BOTTOM LINE":"📋 BOTTOM LINE"} ${evidenceBadge(evGrade)}</div><div>${escapeHtml(blText)}</div>`;
    root.appendChild(bl);
  }
  // Confidence warning
  if(reasoning.confidence_warning){
    const cw=document.createElement("div");
    cw.style.cssText="font-size:.76rem;color:#92400e;background:#fef9c3;padding:6px 10px;border-radius:4px;margin-bottom:10px;border-left:3px solid #d97706";
    cw.textContent="ℹ "+reasoning.confidence_warning;
    root.appendChild(cw);
  }
  // Per-disease structured reasoning (top 3)
  const diffs=reasoning.differentials||[];
  if(diffs.length>0){
    const diffHeader=document.createElement("div");
    diffHeader.style.cssText="font-weight:700;font-size:.84rem;color:#334155;margin-bottom:8px;padding-bottom:6px;border-bottom:2px solid #e2e8f0";
    diffHeader.textContent=currentLang==="ja"?"🔬 鑑別疾患の臨床推論":"🔬 Differential clinical reasoning";
    root.appendChild(diffHeader);
    diffs.slice(0,3).forEach(d=>{
      root.appendChild(renderDiseaseReasoning(d));
    });
  }
  // Overall next steps
  if(reasoning.next_steps&&reasoning.next_steps.length>0){
    const ns=document.createElement("div");
    ns.style.cssText="margin-top:12px;padding:10px 12px;background:#ecfdf5;border-left:4px solid #16a34a;border-radius:4px";
    const nsTitle=currentLang==="ja"?"💡 次の診断ステップ":"💡 Next diagnostic steps";
    const nsItems=reasoning.next_steps.map(s=>{const nm=currentLang==="ja"?(s.name_ja||s.name_en||s.id):(s.name_en||s.name_ja||s.id);return `<li style="margin:2px 0">${escapeHtml(nm)}</li>`;}).join("");
    ns.innerHTML=`<div style="font-weight:700;font-size:.82rem;color:#166534;margin-bottom:4px">${nsTitle}</div><ul style="margin:4px 0 0 20px;padding:0;font-size:.82rem;color:#166534">${nsItems}</ul>`;
    root.appendChild(ns);
  }
  return root;
}

function renderDiseaseReasoning(d){
  const card=document.createElement("div");
  card.className="disease-reasoning-card";
  const urgencyColors={emergency:"#dc2626",high:"#ea580c",moderate:"#0891b2",low:"#64748b"};
  const uColor=urgencyColors[d.urgency]||"#64748b";
  card.style.cssText=`margin-bottom:10px;padding:10px 12px;background:#fff;border:1px solid #e2e8f0;border-left:4px solid ${uColor};border-radius:6px`;
  const name=currentLang==="ja"?(d.disease_name_ja||d.disease_name):d.disease_name;
  const conf=Math.round((d.confidence||0)*100);
  let html=`<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px"><strong style="font-size:.88rem;color:#1e293b">${escapeHtml(name)}</strong><span style="font-size:.74rem;font-weight:700;color:${uColor};padding:2px 8px;background:${uColor}1a;border-radius:10px">${conf}%</span></div>`;
  // Matching symptoms
  if(d.matching_symptoms&&d.matching_symptoms.length>0){
    const items=d.matching_symptoms.map(s=>{const nm=currentLang==="ja"?(s.name_ja||s.name_en||s.id):(s.name_en||s.name_ja||s.id);return `<span style="display:inline-block;padding:2px 8px;background:#dcfce7;color:#166534;border-radius:10px;font-size:.72rem;margin:2px 4px 2px 0">✓ ${escapeHtml(nm)}</span>`;}).join("");
    html+=`<div style="font-size:.74rem;color:#475569;margin:4px 0"><strong>${currentLang==="ja"?"支持症状":"Supporting"}:</strong> ${items}</div>`;
  }
  // Missing typical symptoms
  if(d.missing_typical_symptoms&&d.missing_typical_symptoms.length>0){
    const items=d.missing_typical_symptoms.map(s=>{const nm=currentLang==="ja"?(s.name_ja||s.name_en||s.id):(s.name_en||s.name_ja||s.id);return `<span style="display:inline-block;padding:2px 8px;background:#fef3c7;color:#92400e;border-radius:10px;font-size:.72rem;margin:2px 4px 2px 0">? ${escapeHtml(nm)}</span>`;}).join("");
    html+=`<div style="font-size:.74rem;color:#475569;margin:4px 0"><strong>${currentLang==="ja"?"確認推奨":"Check for"}:</strong> ${items}</div>`;
  }
  // Rule-out questions
  if(d.rule_out_questions&&d.rule_out_questions.length>0){
    const qs=d.rule_out_questions.map(q=>`<li style="margin:2px 0">${escapeHtml(q)}</li>`).join("");
    html+=`<div style="font-size:.74rem;color:#475569;margin:6px 0 2px"><strong>${currentLang==="ja"?"鑑別質問":"Rule-out Q"}:</strong><ul style="margin:2px 0 0 18px;padding:0">${qs}</ul></div>`;
  }
  // Red flags — translate IDs using already-humanized symptom maps in the same response
  if(d.red_flags&&d.red_flags.length>0){
    const lookup={};
    [...(d.matching_symptoms||[]),...(d.missing_typical_symptoms||[]),...(d.next_diagnostic_steps||[])].forEach(s=>{if(s&&s.id)lookup[s.id]=s;});
    const labels=d.red_flags.map(rid=>{
      const e=lookup[rid];
      if(!e)return rid.replace(/_/g," ").replace(/\b\w/g,c=>c.toUpperCase());
      return currentLang==="ja"?(e.name_ja||e.name_en||rid):(e.name_en||e.name_ja||rid);
    });
    html+=`<div style="font-size:.74rem;color:#dc2626;margin:6px 0;padding:4px 8px;background:#fee2e2;border-radius:4px"><strong>🚨 ${currentLang==="ja"?"レッドフラグ":"Red flags"}:</strong> ${labels.map(escapeHtml).join(", ")}</div>`;
  }
  card.innerHTML=html;
  return card;
}

// Evidence grading helper - assesses treatment text severity
function evidenceBadge(grade){
  if(!grade)return"";
  const labels={A:{ja:"高エビデンス",en:"Strong"},B:{ja:"中等度",en:"Moderate"},C:{ja:"限定的",en:"Limited"},D:{ja:"不明",en:"Unclear"}};
  const colors={A:"#16a34a",B:"#0891b2",C:"#d97706",D:"#6b7280"};
  const label=(labels[grade]||labels.D)[currentLang]||(labels[grade]||labels.D).en;
  const color=colors[grade]||colors.D;
  return `<span class="evidence-badge" title="${currentLang==="ja"?"エビデンスグレード":"Evidence grade"}: ${grade}" style="display:inline-block;padding:2px 8px;background:${color};color:#fff;border-radius:10px;font-size:.66rem;font-weight:700;letter-spacing:.05em;margin-left:6px;vertical-align:middle">${grade} · ${label}</span>`;
}

// Quick client-side grading without API call (for performance)
function quickAssessGrade(text){
  if(!text||text.length<10)return"D";
  const tl=text.toLowerCase();
  const hasHighRef=/\b(acvim|aaha|aafp|isfm|wsava|recover|iscaid|ecvn|bsava)\b/i.test(text);
  const hasTextbookRef=/\b(plumb|lumb|jones|ettinger|stashak|mader|quesenberry|carpenter|dixon)\b/i.test(text);
  const hasJournalRef=/\b(javma|jvim|jfms|jsap|jaaha)\b/i.test(text);
  const hasYearRef=/\(\d{4}\)|\bRef:|\b(19|20)\d{2}\b/i.test(text);
  const hasDose=/\d+(?:\.\d+)?\s*(?:[-~–]\s*\d+(?:\.\d+)?)?\s*(?:mg|μg|ug|mcg|g|iu|u)\s*\/\s*kg/i.test(text);
  const hasRoute=/\b(IV|IM|SC|PO|IO|IP|topical|inhaled|nebulized)\b/.test(text);
  const hasInterval=/\bq\d+(?:[-~–]\d+)?\s*(?:h|d|wk)\b/i.test(text);
  const hasMonitoring=/(monitor|monitoring|モニタリング|監視|trough|level|BUN|creatinine|PCV|血糖)/i.test(tl);
  let score=0;
  if(hasHighRef)score+=40;else if(hasTextbookRef)score+=30;else if(hasJournalRef)score+=25;else if(hasYearRef)score+=10;
  if(hasDose)score+=20;
  if(hasRoute)score+=15;
  if(hasInterval)score+=10;
  if(hasMonitoring)score+=15;
  if(score>=70&&(hasHighRef||hasTextbookRef))return"A";
  if(score>=50)return"B";
  if(score>=25)return"C";
  return"D";
}

function setupInteractionChecker(){
  const btn=document.getElementById("interactionCheckBtn");
  const speciesSel=document.getElementById("interactionSpecies");
  if(!btn||!speciesSel)return;
  // Populate species options
  if(speciesSel.options.length<=1){
    SPECIES.forEach(sp=>{
      const opt=document.createElement("option");
      opt.value=sp.id;
      opt.textContent=currentLang==="ja"?sp.name:sp.nameEn;
      speciesSel.appendChild(opt);
    });
  }
  btn.addEventListener("click",runInteractionCheck);
  const input=document.getElementById("interactionDrugIds");
  if(input)input.addEventListener("keydown",e=>{if(e.key==="Enter"&&!e.isComposing){e.preventDefault();runInteractionCheck();}});
}

function runInteractionCheck(){
  const input=document.getElementById("interactionDrugIds");
  const speciesSel=document.getElementById("interactionSpecies");
  const results=document.getElementById("interactionResults");
  if(!input||!results)return;
  const raw=(input.value||"").trim();
  if(!raw){results.innerHTML="";return;}
  const drugIds=raw.split(/[,，、]+/).map(s=>s.trim().toLowerCase().replace(/\s+/g,"_").replace(/-/g,"_")).filter(Boolean);
  if(drugIds.length<2){
    const msg=currentLang==="ja"?"⚠ 2つ以上の薬品名をカンマ区切りで入力してください。":"⚠ Please enter at least two drug names separated by commas.";
    results.innerHTML=`<div role="alert" style="padding:10px 12px;background:#fef3c7;border-left:4px solid #d97706;border-radius:6px;color:#92400e;font-size:.84rem">${msg}</div>`;
    return;
  }
  results.innerHTML=`<div role="status" aria-live="polite" style="padding:10px;color:var(--gray-500)">${currentLang==="ja"?"確認中...":"Checking..."}</div>`;
  fetchWithTimeout("/api/drugs/check-interactions",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({drug_ids:drugIds,species:speciesSel.value||""})
  }).then(r=>r.json()).then(data=>{
    renderInteractionResults(data,drugIds);
  }).catch(err=>{
    debugError("interaction check failed:",err);
    results.innerHTML=`<div role="alert" style="padding:10px;color:var(--red-700,#b91c1c)">${currentLang==="ja"?"通信エラー — 時間をおいて再度お試しください。":"Network error — please retry shortly."}</div>`;
  });
}

function renderInteractionResults(data,drugIds){
  const results=document.getElementById("interactionResults");
  if(!results)return;
  const ix=data.interactions||[];
  const sw=data.species_specific_warnings||[];
  const unknown=data.unknown_drug_ids||[];
  const recognized=data.recognized_drug_ids||(drugIds||[]).filter(d=>!unknown.includes(d));
  let html="";
  // Surface unknown drug IDs so users know they typed a wrong name.
  if(unknown.length){
    const msg=currentLang==="ja"
      ?`薬品名が認識できませんでした: <strong>${unknown.map(escapeHtml).join(", ")}</strong><br/><span style="font-size:.78rem;opacity:.85">下の検索バーから正しい薬品IDをご確認ください（半角英数小文字 / 例: meloxicam, prednisolone）</span>`
      :`Unrecognized drug names: <strong>${unknown.map(escapeHtml).join(", ")}</strong><br/><span style="font-size:.78rem;opacity:.85">Check the correct drug ID using the search bar below (lowercase Latin, e.g. meloxicam, prednisolone).</span>`;
    html+=`<div role="alert" style="padding:10px 12px;background:#fef3c7;border-left:4px solid #d97706;border-radius:6px;color:#92400e;font-size:.84rem;margin-bottom:8px">⚠ ${msg}</div>`;
  }
  if(ix.length===0&&sw.length===0){
    if(recognized.length===0&&unknown.length>0){
      // All inputs unknown — don't show the green "no interactions" message.
      results.innerHTML=html;
      return;
    }
    const okMsg=currentLang==="ja"?"既知の相互作用は検出されませんでした":"No known interactions detected";
    const drugLabel=currentLang==="ja"?"薬品":"drugs";
    html+=`<div role="status" style="padding:12px;background:var(--green-50,#f0fdf4);border-left:4px solid var(--green-600,#16a34a);border-radius:6px;color:var(--green-800,#166534);font-size:.86rem">✅ ${okMsg} (${recognized.length} ${drugLabel})</div>`;
    results.innerHTML=html;
    return;
  }
  const sevColor={contraindicated:{bg:"#fee2e2",border:"#dc2626",text:"#991b1b",label:currentLang==="ja"?"禁忌":"CONTRAINDICATED"},major:{bg:"#fef3c7",border:"#d97706",text:"#92400e",label:currentLang==="ja"?"重大":"MAJOR"},moderate:{bg:"#dbeafe",border:"#2563eb",text:"#1e40af",label:currentLang==="ja"?"中等度":"MODERATE"}};
  if(ix.length>0){
    html+=`<div style="font-weight:600;margin:8px 0;font-size:.84rem">${currentLang==="ja"?"薬品-薬品相互作用":"Drug-drug interactions"}: ${ix.length}</div>`;
    ix.forEach(i=>{
      const c=sevColor[i.severity]||sevColor.moderate;
      const effect=currentLang==="ja"?(i.effect_ja||i.effect_en||""):(i.effect_en||i.effect_ja||"");
      const mgmt=currentLang==="ja"?(i.management_ja||i.management_en||""):(i.management_en||i.management_ja||"");
      const mech=i.mechanism||"";
      html+=`<div style="padding:10px 12px;background:${c.bg};border-left:4px solid ${c.border};border-radius:6px;margin-bottom:8px;font-size:.84rem">
        <div style="display:flex;gap:8px;align-items:center;margin-bottom:6px"><span style="font-weight:700;color:${c.text};font-size:.74rem;padding:2px 8px;background:${c.border};color:#fff;border-radius:4px">${c.label}</span><strong style="color:${c.text}">${escapeHtml(i.drug_a)} + ${escapeHtml(i.drug_b)}</strong></div>
        ${mech?`<div style="color:${c.text};font-size:.78rem;margin-bottom:4px">${currentLang==="ja"?"機序":"Mechanism"}: ${escapeHtml(mech)}</div>`:""}
        <div style="color:${c.text};margin-bottom:4px">${escapeHtml(effect)}</div>
        ${mgmt?`<div style="color:${c.text};font-size:.82rem"><strong>${currentLang==="ja"?"対応":"Management"}:</strong> ${escapeHtml(mgmt)}</div>`:""}
        ${i.ref?`<div style="color:${c.text};font-size:.74rem;margin-top:4px;opacity:.7">Ref: ${escapeHtml(i.ref)}</div>`:""}
      </div>`;
    });
  }
  if(sw.length>0){
    html+=`<div style="font-weight:600;margin:12px 0 8px;font-size:.84rem">${currentLang==="ja"?"動物種特異的警告":"Species-specific warnings"}: ${sw.length}</div>`;
    sw.forEach(i=>{
      const c=sevColor[i.severity]||sevColor.moderate;
      const effect=currentLang==="ja"?(i.effect_ja||i.effect_en||""):(i.effect_en||i.effect_ja||"");
      const mgmt=currentLang==="ja"?(i.management_ja||i.management_en||""):(i.management_en||i.management_ja||"");
      html+=`<div style="padding:10px 12px;background:${c.bg};border-left:4px solid ${c.border};border-radius:6px;margin-bottom:8px;font-size:.84rem">
        <div style="display:flex;gap:8px;align-items:center;margin-bottom:6px"><span style="font-weight:700;color:#fff;font-size:.74rem;padding:2px 8px;background:${c.border};border-radius:4px">${c.label}</span></div>
        <div style="color:${c.text};margin-bottom:4px">${escapeHtml(effect)}</div>
        ${mgmt?`<div style="color:${c.text};font-size:.82rem"><strong>${currentLang==="ja"?"対応":"Management"}:</strong> ${escapeHtml(mgmt)}</div>`:""}
      </div>`;
    });
  }
  results.innerHTML=html;
}

function parseDoseRange(doseText){
  const m=doseText.match(/([\d.]+)\s*[-–~～]\s*([\d.]+)\s*mg\/kg/i);
  if(m)return{min:parseFloat(m[1]),max:parseFloat(m[2]),unit:"mg"};
  const m2=doseText.match(/([\d.]+)\s*mg\/kg/i);
  if(m2)return{min:parseFloat(m2[1]),max:parseFloat(m2[1]),unit:"mg"};
  const m3=doseText.match(/([\d.]+)\s*[-–~～]\s*([\d.]+)\s*[μµu]g\/kg/i);
  if(m3)return{min:parseFloat(m3[1]),max:parseFloat(m3[2]),unit:"µg"};
  const m4=doseText.match(/([\d.]+)\s*[μµu]g\/kg/i);
  if(m4)return{min:parseFloat(m4[1]),max:parseFloat(m4[1]),unit:"µg"};
  return null;
}

function normalizeDrugSearchText(s){
  // NFKC（全角英数・半角カナの正規化）+ 小文字化 + ひらがな→カタカナ。
  // 「ばいとりる」「ﾊﾞｲﾄﾘﾙ」「ＢＡＹＴＲＩＬ」でも「バイトリル」に一致させる。
  return (s||"").normalize("NFKC").toLowerCase().replace(/[ぁ-ゖ]/g,ch=>String.fromCharCode(ch.charCodeAt(0)+0x60));
}
function _drugMatchesSearch(d,q){
  // 一致した場合、どのフィールドで一致したかを返す（brand一致は結果カードに表示する）
  if(normalizeDrugSearchText(d.name).includes(q)||normalizeDrugSearchText(d.name_ja).includes(q)||normalizeDrugSearchText(d.category_ja).includes(q))return{hit:"name"};
  const aliases=(d.search_aliases||[]).concat(d.aliases||[]);
  for(const a of aliases){if(normalizeDrugSearchText(a).includes(q))return{hit:"alias",alias:a};}
  return null;
}
function renderDrugList(){
  const list=document.getElementById("drugList");
  if(!list)return;
  const searchEl=document.getElementById("drugSearch");
  const catEl=document.getElementById("drugCategoryFilter");
  const spEl=document.getElementById("drugSpeciesFilter");
  const search=normalizeDrugSearchText(searchEl&&searchEl.value||"");
  const cat=catEl?catEl.value:"";
  const species=spEl?spEl.value:"";
  const wCalc=document.getElementById("drugWeightCalc");
  if(wCalc)wCalc.style.display=species?"flex":"none";
  let filtered=allDrugs;
  if(cat)filtered=filtered.filter(d=>d.category===cat);
  if(species)filtered=filtered.filter(d=>d.species_info&&d.species_info[species]);
  const aliasHits={};
  if(search)filtered=filtered.filter(d=>{
    const m=_drugMatchesSearch(d,search);
    if(m&&m.hit==="alias")aliasHits[d.id]=m.alias;
    return!!m;
  });
  const countEl=document.getElementById("drugCount");
  if(countEl)countEl.textContent=t("diseaseCount").replace("%filtered%",filtered.length).replace("%total%",allDrugs.length);
  if(filtered.length===0){
    // 0件時: フィルタが原因なら「フィルタ解除で N 件」ボタンを提示し、
    // 本当に0件なら 一般名/商品名/英語名 の検索ヒントを表示する
    let extra=`<div style="margin-top:8px;font-size:.85rem;color:var(--gray-500)">${t("drugNoMatchHint")}</div>`;
    if(search&&(cat||species)){
      const unfiltered=allDrugs.filter(d=>_drugMatchesSearch(d,search)).length;
      if(unfiltered>0)extra=`<div style="margin-top:10px"><button type="button" id="drugClearFiltersBtn" class="guided-action-btn">${t("drugClearFilters").replace("%n%",unfiltered)}</button></div>`;
    }
    list.innerHTML=`<div style="padding:20px;text-align:center;color:var(--gray-500)">${t("noDrugMatch")}${extra}</div>`;
    const clearBtn=document.getElementById("drugClearFiltersBtn");
    if(clearBtn)clearBtn.addEventListener("click",()=>{
      if(catEl)catEl.value="";
      if(spEl)spEl.value="";
      renderDrugList();
    });
    return;
  }
  filtered=[...filtered].sort((a,b)=>(b.sponsor?1:0)-(a.sponsor?1:0));
  list.innerHTML=filtered.map(d=>{
    const speciesFilter=document.getElementById("drugSpeciesFilter").value;
    let dosageHtml="";
    if(speciesFilter&&d.species_info&&d.species_info[speciesFilter]){
      const si=d.species_info[speciesFilter];
      const safeLabel=si.safe?`<span class="drug-safe-label">\u2713 ${t("safe")}</span>`:`<span class="drug-unsafe-label">\u2717 ${t("contraindicated")}</span>`;
      const doseText=currentLang==="ja"?(si.dosage_ja||si.dosage||"N/A"):(si.dosage||si.dosage_ja||"N/A");
      const noteText=currentLang==="ja"?(si.notes_ja||si.notes||""):(si.notes||si.notes_ja||"");
      const wt=parseFloat((document.getElementById("drugWeight")||{}).value)||0;
      const parsed=parseDoseRange(si.dosage||si.dosage_ja||"");
      let calcHtml="";
      if(wt>0&&parsed){
        const lo=(parsed.min*wt).toFixed(parsed.unit==="µg"?0:1);
        const hi=(parsed.max*wt).toFixed(parsed.unit==="µg"?0:1);
        calcHtml=lo===hi
          ?`<div class="drug-calc-dose">${currentLang==="ja"?"計算投与量":"Calculated"}: ${lo} ${parsed.unit} (${wt}kg)</div>`
          :`<div class="drug-calc-dose">${currentLang==="ja"?"計算投与量":"Calculated"}: ${lo}–${hi} ${parsed.unit} (${wt}kg)</div>`;
      }
      dosageHtml=`<div class="drug-dosage-box ${si.safe?"drug-safe":"drug-unsafe"}">${safeLabel} | ${t("dosageLabel")}${escapeHtml(doseText)}${calcHtml}<br/><span class="drug-dosage-note">${escapeHtml(noteText)}</span></div>`;
    }
    const catLabel=drugCategories[d.category]?(currentLang==="ja"?(drugCategories[d.category].ja||drugCategories[d.category].en):(drugCategories[d.category].en||drugCategories[d.category].ja)):(currentLang==="ja"?(d.category_ja||d.category):(d.category||d.category_ja));
    const sponsorBadge=d.sponsor?'<span class="sponsor-badge-tag">Sponsor</span>':"";
    const sponsorLink=d.sponsor?`<div class="drug-sponsor-link"><strong class="drug-sponsor-name">${escapeHtml(d.sponsor_name||"Equine & Canine Vet Nutrition")}</strong><br/><span class="drug-sponsor-vet">${t("sponsorVetLabel")}</span><br/><a href="${sanitizeUrl(d.sponsor_url||d.sponsor_url_dog||'https://www.caninevet.jp/')}" target="_blank" class="drug-sponsor-url">${t("productDetails")}</a></div>`:"";
    const dName=highlightMatch(d.name||"",search);
    const dNameJa=highlightMatch(d.name_ja||"",search);
    const brandHit=aliasHits[d.id]?`<span class="drug-brand-hit">${t("drugBrandHit")}: ${escapeHtml(aliasHits[d.id])}</span>`:"";
    return`<div class="disease-db-item drug-item${d.sponsor?" drug-sponsored":""}" role="button" tabindex="0" aria-expanded="false" data-name="${escapeHtml(d.name||"")}" data-name-ja="${escapeHtml(d.name_ja||"")}">
      <div class="drug-head-row">
        <div class="d-name">${dName} <span class="d-name-ja">${dNameJa}</span>${brandHit}${sponsorBadge}</div>
        <span class="drug-category-tag">${escapeHtml(catLabel)}</span>
      </div>${dosageHtml}
      <div class="disease-detail">${sponsorLink}
        ${d.mechanism_ja||d.mechanism?`<dl><dt>${t("dtMechanism")}</dt><dd>${escapeHtml(currentLang==="ja"?(d.mechanism_ja||d.mechanism||""):(d.mechanism||d.mechanism_ja||""))}</dd></dl>`:""}
        ${(()=>{let se=currentLang==="ja"?(d.side_effects_ja||d.side_effects):(d.side_effects||d.side_effects_ja);se=toList(se);return se.length?`<dl><dt>${t("dtSideEffects")}</dt><dd>${se.map(s=>`<span class="drug-se-tag">${escapeHtml(s)}</span>`).join("")}</dd></dl>`:"";})()}
        <dl><dt>${t("dtContraindications")}</dt><dd>${escapeHtml(currentLang==="ja"?(d.contraindications_ja||d.contraindications||""):(d.contraindications||d.contraindications_ja||""))}</dd></dl>
        ${d.routes_ja||d.routes?`<dl><dt>${t("dtRoutes")}</dt><dd>${escapeHtml(toList(currentLang==="ja"?(d.routes_ja||d.routes):(d.routes||d.routes_ja)).join(", "))}</dd></dl>`:""}
        ${d.formulations_ja||d.formulations?`<dl><dt>${t("dtFormulations")}</dt><dd>${escapeHtml(toList(currentLang==="ja"?(d.formulations_ja||d.formulations):(d.formulations||d.formulations_ja)).join(", "))}</dd></dl>`:""}
        ${d.drug_interactions&&d.drug_interactions.length?`<dl><dt>${t("dtInteractions")} <span style="font-size:.7rem;color:var(--gray-500);font-weight:400">(${d.drug_interactions.length})</span></dt><dd>${renderDrugInteractionsList(d.drug_interactions)}</dd></dl>`:""}
        <div class="drug-species-section"><strong class="drug-species-title">${t("dtSpeciesInfo")}</strong>
          <div class="drug-species-grid">
            ${Object.entries(d.species_info||{}).map(([sp,info])=>{const spName=SPECIES.find(s=>s.id===sp);const label=spName?(currentLang==="ja"?spName.name:spName.nameEn):sp;const dose=currentLang==="ja"?(info.dosage_ja||info.dosage||""):(info.dosage||info.dosage_ja||"");const note=currentLang==="ja"?(info.notes_ja||info.notes||""):(info.notes||info.notes_ja||"");const highlight=currentSpecies===sp?"drug-species-highlight":"";return`<div class="drug-species-card ${info.safe?"drug-safe":"drug-unsafe"} ${highlight}"><strong>${escapeHtml(label)}</strong>: ${info.safe?'\u2713':'\u2717'} ${escapeHtml(dose)}${note?'<br/><span class="drug-dosage-note">'+escapeHtml(note)+'</span>':''}</div>`;}).join("")}
          </div>
        </div>
        ${buildDrugDiseasesPlaceholder(d.id||"")}
        ${(()=>{const q=_anesQueryForDrug(d.name||"",d.name_ja||"");return q?`<button type="button" class="drug-anes-protocols-link" data-anes-query="${escapeHtml(q)}">\u{1F489} ${currentLang==="ja"?"この薬品を使う麻酔プロトコルを見る":"View anesthesia protocols using this drug"}</button>`:"";})()}
      </div>
    </div>`;
  }).join("");
}

/* Reverse lookup: does this formulary drug appear in the anesthesia protocol
   tables? Anesthesia→drug navigation has existed since the ANES_AGENTS
   linkifier; this closes the loop drug→anesthesia so a clinician reading e.g.
   midazolam can jump straight to every protocol that uses it (the anesthesia
   search filter matches protocol drug tables). Abbreviation aliases are
   skipped — too short to trust as containment matches. */
function _anesQueryForDrug(name,nameJa){
  if(typeof ANES_AGENTS==="undefined")return "";
  const nl=(name||"").toLowerCase();
  for(const a of ANES_AGENTS){
    for(const en of (a.en||[])){if(en.length>=4&&nl.includes(en.toLowerCase()))return a.q;}
    for(const ja of (a.ja||[])){if(ja.length>=3&&(nameJa||"").includes(ja))return a.q;}
  }
  return "";
}

/* ===== Emergency Protocols (Vetlexicon-style quick reference) ===== */
let emergencyLoaded=false,emergencyData=null,emergencyCategories={};

function loadEmergencyProtocols(){
  const list=document.getElementById("emergencyList");
  if(!list)return;
  list.innerHTML='<div style="padding:12px"><div class="skeleton skeleton-card"></div><div class="skeleton skeleton-card" style="height:70px"></div></div>';
  fetchWithTimeout("/api/emergency/protocols",{},30000).then(r=>r.json()).then(data=>{
    emergencyData=data.protocols||[];
    emergencyCategories=data.categories||{};
    emergencyLoaded=true;
    const catSel=document.getElementById("emergencyCategoryFilter");
    if(catSel){
      catSel.innerHTML=`<option value="">${t("allCategories")}</option>`;
      Object.entries(emergencyCategories).forEach(([k,v])=>{
        const name=currentLang==="ja"?(v.ja||v.en):(v.en||v.ja);
        catSel.insertAdjacentHTML("beforeend",`<option value="${escapeHtml(k)}">${escapeHtml(name)}</option>`);
      });
    }
    const spSel=document.getElementById("emergencySpeciesFilter");
    if(spSel&&spSel.options.length<=1){
      SPECIES.forEach(sp=>{
        const opt=document.createElement("option");
        opt.value=sp.id;
        opt.textContent=currentLang==="ja"?sp.name:sp.nameEn;
        spSel.appendChild(opt);
      });
    }
    renderEmergencyList();
    setupEmergencyListeners();
  }).catch(()=>{
    list.innerHTML=`<div style="padding:20px;text-align:center;color:var(--gray-500)">${t("loadFailed")}<br><button class="retry-emergency-btn" type="button" style="margin-top:10px;padding:8px 20px;background:var(--navy);color:var(--white);border:none;border-radius:6px;cursor:pointer;font-size:.84rem">${t("reload")}</button></div>`;
    const rb=list.querySelector(".retry-emergency-btn");
    if(rb)rb.addEventListener("click",()=>{emergencyLoaded=false;loadEmergencyProtocols();});
  });
}

function setupEmergencyListeners(){
  const list=document.getElementById("emergencyList");
  if(!list||list.dataset.emergencyListenersAttached)return;
  list.dataset.emergencyListenersAttached="1";
  ["emergencySearch","emergencyCategoryFilter","emergencySpeciesFilter"].forEach(id=>{
    const el=document.getElementById(id);
    if(!el)return;
    if(el.tagName==="INPUT"){
      /* 検索入力: 位置は動かさない（キーボード表示中のページ移動を避ける） */
      el.addEventListener("input",debounce(renderEmergencyList,200));
    }else{
      /* フィルタ選択: 他タブ（薬品/麻酔/疾患DB）と同様、絞り込み結果の先頭へ再アンカー */
      el.addEventListener("change",()=>{renderEmergencyList();_revealFilteredList("emergencyList");});
    }
  });
}

function renderEmergencyList(){
  const list=document.getElementById("emergencyList");
  if(!list||!emergencyData)return;
  const search=(document.getElementById("emergencySearch")?.value||"").toLowerCase();
  const cat=document.getElementById("emergencyCategoryFilter")?.value||"";
  const species=document.getElementById("emergencySpeciesFilter")?.value||"";
  let filtered=emergencyData;
  if(cat)filtered=filtered.filter(p=>p.category===cat);
  if(species)filtered=filtered.filter(p=>(p.species||[]).includes(species));
  if(search){
    filtered=filtered.filter(p=>{
      const hay=[p.title_ja,p.title_en,...(p.trigger_signs_ja||[]),...(p.trigger_signs_en||[])].join(" ").toLowerCase();
      return hay.includes(search);
    });
  }
  document.getElementById("emergencyCount").textContent=`${filtered.length} / ${emergencyData.length}`;
  if(filtered.length===0){list.innerHTML=`<div style="padding:20px;text-align:center;color:var(--gray-500)">${currentLang==="ja"?"該当するプロトコルがありません":"No matching protocols"}</div>`;return;}
  list.innerHTML=filtered.map(p=>renderEmergencyProtocol(p)).join("");
  /* Toggle/expand handlers are attached once at init via _attachDbItemHandlers
     (see the ["diseaseDbList","drugList","anesthesiaList","emergencyList"] loop),
     so an expanded protocol scrolls to a usable position, accordion-collapses
     siblings and gets a close button — identical to the other DB lists. */
}

function renderEmergencyProtocol(p){
  const title=currentLang==="ja"?p.title_ja:p.title_en;
  const triggers=currentLang==="ja"?p.trigger_signs_ja:p.trigger_signs_en;
  const catName=emergencyCategories[p.category]?(currentLang==="ja"?emergencyCategories[p.category].ja:emergencyCategories[p.category].en):p.category;
  const speciesText=(p.species||[]).map(sp=>{const s=SPECIES.find(x=>x.id===sp);return s?(currentLang==="ja"?s.name:s.nameEn):sp;}).join(", ");
  const triggerHtml=`<div style="margin:6px 0"><strong style="font-size:.78rem;color:#7f1d1d">${t("emergencyTriggerSigns")}:</strong> ${(triggers||[]).map(s=>`<span style="display:inline-block;padding:2px 8px;background:#fee2e2;color:#7f1d1d;border-radius:10px;font-size:.74rem;margin:2px 4px 2px 0">${escapeHtml(s)}</span>`).join("")}</div>`;
  const stepsHtml=(p.steps||[]).map(s=>{
    const text=currentLang==="ja"?s.ja:s.en;
    const phase=s.phase||"";
    return `<li style="margin:8px 0;padding:8px 12px;background:#fafafa;border-left:3px solid #0891b2;border-radius:4px"><div style="display:flex;justify-content:space-between;gap:8px;align-items:start;margin-bottom:4px"><strong style="font-size:.78rem;color:#0c4a6e">${s.order}. ${escapeHtml(phase)}</strong>${s.time_target?`<span style="font-size:.7rem;color:#64748b;white-space:nowrap">⏱ ${escapeHtml(s.time_target)}</span>`:""}</div><div style="font-size:.84rem;color:#1e293b;line-height:1.5">${escapeHtml(text)}</div></li>`;
  }).join("");
  const drugsHtml=(p.key_drugs||[]).map(d=>{const nm=currentLang==="ja"?(d.name_ja||d.name):d.name;return `<li style="margin:3px 0;font-size:.82rem"><strong>${escapeHtml(nm)}</strong> — ${escapeHtml(d.dose)}</li>`;}).join("");
  const monitorHtml=(p.monitoring||[]).map(m=>`<span style="display:inline-block;padding:2px 8px;background:#dbeafe;color:#1e40af;border-radius:10px;font-size:.72rem;margin:2px 4px 2px 0">${escapeHtml(m)}</span>`).join("");
  return `<div class="disease-db-item" role="button" tabindex="0" aria-expanded="false" style="border-left:5px solid #dc2626">
    <div style="display:flex;justify-content:space-between;gap:8px;align-items:start;flex-wrap:wrap">
      <div class="d-name" style="font-weight:700;color:#1e293b">${escapeHtml(title)}</div>
      <span style="background:#dc2626;color:#fff;padding:2px 10px;border-radius:12px;font-size:.7rem;font-weight:700;letter-spacing:.05em">${escapeHtml(catName)}</span>
    </div>
    <div style="font-size:.74rem;color:#64748b;margin-top:4px">🐾 ${escapeHtml(speciesText)}</div>
    ${triggerHtml}
    <div class="disease-detail">
      <div style="margin:10px 0"><strong style="font-size:.82rem;color:#0c4a6e">${t("emergencyStepsTitle")}</strong><ol style="margin:6px 0 0 0;padding:0;list-style:none">${stepsHtml}</ol></div>
      ${drugsHtml?`<div style="margin:10px 0"><strong style="font-size:.82rem;color:#0c4a6e">💊 ${t("emergencyKeyDrugs")}</strong><ul style="margin:4px 0 0 20px;padding:0">${drugsHtml}</ul></div>`:""}
      ${monitorHtml?`<div style="margin:10px 0"><strong style="font-size:.82rem;color:#0c4a6e">📊 ${t("emergencyMonitoring")}:</strong><div style="margin-top:4px">${monitorHtml}</div></div>`:""}
      ${p.ref?`<div style="margin-top:10px;padding-top:8px;border-top:1px solid #e2e8f0;font-size:.72rem;color:#64748b"><em>Ref: ${escapeHtml(p.ref)}</em></div>`:""}
    </div>
  </div>`;
}

/* ===== Anesthesia Protocols ===== */
let anesthesiaLoaded=false,anesthesiaData=null,anesthesiaCategories={},anesthesiaAsaData=null,anesthesiaContraRules=null;
/* Contraindication rules power BOTH the anesthesia tab badges and the
   "anesthesia considerations" box in checker results. Historically they were
   fetched only when the anesthesia tab first opened, so checker-first users
   never saw the considerations box. Fetch-once helper usable from both paths. */
let _contraRulesFetchStarted=false;
function ensureAnesthesiaContraRules(){
  if(_contraRulesFetchStarted||(anesthesiaContraRules&&anesthesiaContraRules.length))return;
  _contraRulesFetchStarted=true;
  fetchWithTimeout("/api/anesthesia/contraindications?all=true").then(r=>r.json()).then(d=>{anesthesiaContraRules=d.rules||[];}).catch(err=>{_contraRulesFetchStarted=false;debugWarn("anesthesia/contraindications fetch failed:",err);});
}

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
  }).catch(err=>{
    debugError("anesthesia/protocols load failed:",err);
    list.innerHTML=`<div role="alert" style="padding:20px;text-align:center;color:var(--gray-500)">${t("loadFailed")}<br><button type="button" class="retry-anesthesia-btn" style="margin-top:10px;padding:8px 20px;background:var(--navy);color:var(--white);border:none;border-radius:6px;cursor:pointer;font-size:.84rem">${t("reload")}</button></div>`;
    const rb=list.querySelector(".retry-anesthesia-btn");
    if(rb)rb.addEventListener("click",()=>{anesthesiaLoaded=false;loadAnesthesiaProtocols();});
  });
  if(!list.dataset.anesthesiaListenersAttached){
    list.dataset.anesthesiaListenersAttached="1";
    /* Fetch ASA classification */
    fetchWithTimeout("/api/anesthesia/categories").then(r=>r.json()).then(d=>{anesthesiaAsaData=d.asa_classification||null;}).catch(err=>{debugWarn("anesthesia/categories fetch failed:",err);});
    /* Fetch contraindication rules */
    ensureAnesthesiaContraRules();
    document.getElementById("anesthesiaSearch").addEventListener("input",debounce(renderAnesthesiaList,200));
    document.getElementById("anesthesiaCategoryFilter").addEventListener("change",()=>{renderAnesthesiaList();_revealFilteredList("anesthesiaList");});
    /* Weight-based dose calculator */
    const weightInput=document.getElementById("anesthesiaWeight");
    if(weightInput){
      weightInput.addEventListener("input",debounce(renderAnesthesiaList,300));
      document.getElementById("anesthesiaWeightClear").addEventListener("click",()=>{weightInput.value="";renderAnesthesiaList();});
    }
    /* Emergency protocol quick-access — toggles the emergency category filter */
    const emergBtn=document.getElementById("anesthesiaEmergencyBtn");
    if(emergBtn){
      emergBtn.setAttribute("aria-pressed","false");
      emergBtn.addEventListener("click",()=>{
        const catSel=document.getElementById("anesthesiaCategoryFilter");
        const isActive=emergBtn.classList.toggle("active");
        emergBtn.setAttribute("aria-pressed",isActive?"true":"false");
        if(isActive){catSel.value="emergency";} else {catSel.value="";}
        renderAnesthesiaList();
      });
    }
    /* ASA filter */
    const asaFilter=document.getElementById("anesthesiaAsaFilter");
    if(asaFilter)asaFilter.addEventListener("change",()=>{renderAnesthesiaList();_revealFilteredList("anesthesiaList");});
    /* Print checklist */
    const printBtn=document.getElementById("anesthesiaPrintBtn");
    if(printBtn)printBtn.addEventListener("click",printAnesthesiaChecklist);
  }
}

function reloadAnesthesiaForSpecies(){
  if(!anesthesiaLoaded)return;
  const sp=currentSpecies||"";
  const url=sp?"/api/anesthesia/protocols?species="+encodeURIComponent(sp):"/api/anesthesia/protocols";
  fetchWithTimeout(url).then(r=>r.json()).then(data=>{
    anesthesiaData=data;
    renderAnesthesiaOverview(data);
    renderAnesthesiaList();
  }).catch(err=>{debugWarn("anesthesia/protocols reload failed:",err);});
}

function renderAnesthesiaOverview(data){
  const ov=document.getElementById("anesthesiaOverview");
  const lb=document.getElementById("anesthesiaSpeciesLabel");
  if(!data||(!data.overview&&!data.species_name)){
    ov.style.display="block";
    ov.innerHTML=renderEmptyState("anesthesia");
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

/* Anaesthesia drug → drug-dictionary link resolver.
   A protocol row's drug name is often a combination ("Acepromazine + Butorphanol"),
   carries a brand/formulation suffix ("Medetomidine (Domitor)", "Ketamine CRI") or
   is a protocol acronym ("MKM-OS", "Triple Drip"). Passing the whole descriptive
   string to the drug search finds nothing. Instead we wrap each *recognised base
   agent* in its own link whose search term is guaranteed to match a real formulary
   entry, and leave acronyms / fluids / routes as plain text. The base-agent set is
   static (self-contained, no dependency on the drug list being loaded yet) and is
   covered by a test that asserts every canonical term resolves to a real drug. */
const ANES_AGENTS=[
  // dexmedetomidine MUST precede medetomidine (longer alias wins, but keep order clear)
  {q:"デクスメデトミジン",en:["dexmedetomidine"],ja:["デクスメデトミジン","デクスドミトール"],abbr:["dex"]},
  {q:"メデトミジン",en:["medetomidine"],ja:["メデトミジン","ドミトール"],abbr:["med"]},
  {q:"デトミジン",en:["detomidine"],ja:["デトミジン","ドルモセダン"]},
  {q:"ロミフィジン",en:["romifidine"],ja:["ロミフィジン"]},
  {q:"キシラジン",en:["xylazine"],ja:["キシラジン"]},
  {q:"アセプロマジン",en:["acepromazine"],ja:["アセプロマジン"],abbr:["acp"]},
  {q:"ケタミン",en:["ketamine"],ja:["ケタミン"]},
  {q:"アルファキサロン",en:["alfaxalone"],ja:["アルファキサロン","アルファキサン"],abbr:["alf"]},
  {q:"プロポフォール",en:["propofol"],ja:["プロポフォール"]},
  {q:"チオペンタール",en:["thiopental"],ja:["チオペンタール"]},
  {q:"イソフルラン",en:["isoflurane"],ja:["イソフルラン"]},
  {q:"セボフルラン",en:["sevoflurane"],ja:["セボフルラン"]},
  {q:"ブトルファノール",en:["butorphanol"],ja:["ブトルファノール"],abbr:["btr"]},
  {q:"ブプレノルフィン",en:["buprenorphine"],ja:["ブプレノルフィン"]},
  {q:"メサドン",en:["methadone"],ja:["メサドン"]},
  {q:"ヒドロモルフォン",en:["hydromorphone"],ja:["ヒドロモルフォン"]},
  {q:"モルヒネ",en:["morphine"],ja:["モルヒネ"]},
  {q:"レミフェンタニル",en:["remifentanil"],ja:["レミフェンタニル"]},
  {q:"フェンタニル",en:["fentanyl"],ja:["フェンタニル"]},
  {q:"リドカイン",en:["lidocaine"],ja:["リドカイン"]},
  {q:"ブピバカイン",en:["bupivacaine"],ja:["ブピバカイン"]},
  {q:"メピバカイン",en:["mepivacaine"],ja:["メピバカイン"]},
  {q:"ミダゾラム",en:["midazolam"],ja:["ミダゾラム"],abbr:["mdz"]},
  {q:"ジアゼパム",en:["diazepam"],ja:["ジアゼパム"]},
  {q:"アチパメゾール",en:["atipamezole"],ja:["アティパメゾール","アチパメゾール","アンチセダン"]},
  {q:"フルマゼニル",en:["flumazenil"],ja:["フルマゼニル"]},
  {q:"ナロキソン",en:["naloxone"],ja:["ナロキソン"]},
  {q:"ヨヒンビン",en:["yohimbine"],ja:["ヨヒンビン"]},
  {q:"ネオスチグミン",en:["neostigmine"],ja:["ネオスチグミン"]},
  {q:"グリコピロレート",en:["glycopyrrolate"],ja:["グリコピロレート"]},
  {q:"アトロピン",en:["atropine"],ja:["アトロピン"]},
  {q:"グアイフェネシン",en:["guaifenesin","glyceryl guaiacolate"],ja:["グアイフェネシン","グリセリルグアヤコレート"],abbr:["gge"]},
  {q:"ガバペンチン",en:["gabapentin"],ja:["ガバペンチン"]},
  // Emergency/CPR agents (RECOVER protocols): previously rendered as dead text
  // in the emergency category, the highest-stakes place to need a dose fast.
  // NOTE: bare "アドレナリン" is NOT an alias — katakana matching has no word
  // boundary, so it would also linkify the tail of "ノルアドレナリン".
  {q:"エピネフリン",en:["epinephrine","adrenaline"],ja:["エピネフリン"]},
  {q:"ドキサプラム",en:["doxapram"],ja:["ドキサプラム"]},
  {q:"ドブタミン",en:["dobutamine"],ja:["ドブタミン"]},
  {q:"デキストロース",en:["dextrose"],ja:["デキストロース"]},
  {q:"メロキシカム",en:["meloxicam"],ja:["メロキシカム"]},
  {q:"オイゲノール",en:["eugenol"],ja:["オイゲノール"]},
  {q:"EMLAクリーム",en:["emla"],ja:["EMLAクリーム"]},
  {q:"MS-222",en:["ms-222","tricaine"],ja:["ms-222","トリカイン"]},
  {q:"フェノキシエタノール",en:["phenoxyethanol"],ja:["フェノキシエタノール"]},
];
/* Flatten to {alias, q, kind} candidates. kind: 'latin' (letter-boundary match on a
   lowercased copy), 'ja' (katakana substring), 'abbr' (uppercase whole token). */
const _ANES_ALIASES=(()=>{
  const out=[];
  for(const a of ANES_AGENTS){
    (a.en||[]).forEach(x=>out.push({alias:x.toLowerCase(),q:a.q,kind:"latin"}));
    (a.ja||[]).forEach(x=>out.push({alias:x,q:a.q,kind:"ja"}));
    (a.abbr||[]).forEach(x=>out.push({alias:x.toLowerCase(),q:a.q,kind:"abbr"}));
  }
  return out;
})();
function linkifyAnesDrugName(str){
  if(!str)return "";
  const lower=str.toLowerCase();
  const isLetter=ch=>ch&&/[a-z]/i.test(ch);
  const isAlnum=ch=>ch&&/[a-z0-9]/i.test(ch);
  const matches=[];
  for(const a of _ANES_ALIASES){
    const hay=a.kind==="ja"?str:lower;
    let idx=0;
    while((idx=hay.indexOf(a.alias,idx))!==-1){
      const end=idx+a.alias.length;
      let ok=true;
      if(a.kind==="latin"){if(isLetter(str[idx-1])||isLetter(str[end]))ok=false;}
      else if(a.kind==="abbr"){if(isAlnum(str[idx-1])||isAlnum(str[end]))ok=false;}
      if(ok)matches.push({start:idx,end:end,q:a.q,len:a.alias.length});
      idx=end;
    }
  }
  if(!matches.length)return escapeHtml(str);
  // Greedy: prefer the longest match; drop any that overlap an already-chosen span.
  matches.sort((x,y)=>y.len-x.len);
  const chosen=[];
  for(const m of matches){
    if(chosen.some(c=>m.start<c.end&&m.end>c.start))continue;
    chosen.push(m);
  }
  chosen.sort((x,y)=>x.start-y.start);
  let html="",pos=0;
  const title=currentLang==="ja"?"薬品詳細を見る":"View drug details";
  for(const m of chosen){
    if(m.start>pos)html+=escapeHtml(str.slice(pos,m.start));
    html+=`<a class="anesthesia-drug-link drug-nav-link" href="#drugs" data-drug="${escapeHtml(m.q)}" title="${title}">${escapeHtml(str.slice(m.start,m.end))}</a>`;
    pos=m.end;
  }
  if(pos<str.length)html+=escapeHtml(str.slice(pos));
  return html;
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
          /* Each recognised base agent in the name (English and Japanese lines)
             becomes its own link to the drug dictionary — combinations link every
             component, suffixed single drugs link the base, acronyms stay plain. */
          const drugAnchorEn=linkifyAnesDrugName(d.name||"");
          const drugAnchorJa=d.name_ja?`<br/><span class="d-name-ja">${linkifyAnesDrugName(d.name_ja)}</span>`:"";
          return`<tr><td><strong>${drugAnchorEn}</strong>${drugAnchorJa}</td><td>${escapeHtml(d.dose||"")}</td>${calcCell}<td>${escapeHtml(d.route||"")}</td><td>${escapeHtml(d.onset||"")}</td><td>${escapeHtml(d.duration||"")}</td></tr>`
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
  /* On open, bring the card to a useful reading position — just below the sticky
     chrome — so the expanded content is not left below the fold. Mirrors
     toggleDbItem(); the disease-DB list already does this and the differential
     result cards should feel the same. Only on open, so collapsing never yanks
     the page. rAF lets the panel expand first so the target rect is final. */
  if(isOpen&&typeof scrollToAnchor==="function"){
    const card=head.closest(".disease-result")||head;
    requestAnimationFrame(()=>scrollToAnchor(card));
  }
}

/* Attach click/keyboard handlers to .disease-db-item elements via event delegation */
/* Chat containers (free chat, landing chat, guided consultation): route clicks on
   drug links and "open in disease DB" buttons to the same exact-match landing used
   everywhere else, instead of the previous dead-end #drugs hash jump. Species comes
   from the card itself (data-species) because the chat species can differ from the
   disease DB's currently loaded species — openDiseaseAcrossSpecies handles the
   switch-and-wait, then expands the exact disease at a readable scroll position. */
function _attachChatNavHandlers(container){
  container.addEventListener("click",function(e){
    const drugLink=e.target.closest(".drug-nav-link");
    if(drugLink){e.preventDefault();navigateToDrug(drugLink.dataset.drug);return;}
    const openBtn=e.target.closest(".chat-disease-open");
    if(openBtn){
      e.preventDefault();
      const name=openBtn.dataset.name||"";
      if(!name)return;
      trackEvent("chat_open_disease_db",{disease:name.substring(0,80),species:openBtn.dataset.species||""});
      openDiseaseAcrossSpecies(name,openBtn.dataset.species||currentSpecies||"");
    }
  });
}

function _attachDbItemHandlers(container){
  container.addEventListener("click",function(e){
    const xsp=e.target.closest(".xspecies-result");
    if(xsp){e.preventDefault();openDiseaseAcrossSpecies(xsp.dataset.name,xsp.dataset.species);return;}
    const drugLink=e.target.closest(".drug-nav-link");
    if(drugLink){e.preventDefault();navigateToDrug(drugLink.dataset.drug);return;}
    const relDisease=e.target.closest(".related-disease-chip");
    if(relDisease){e.preventDefault();navigateToDiseaseDb(relDisease.dataset.name);return;}
    /* Related-drug / disease chips are also rendered synchronously from cache
       (buildTreatmentDrugsPlaceholder / buildDrugDiseasesPlaceholder on a second
       open), a path that attaches no per-node listeners — delegation here makes
       every render land on the exact item instead of dead-ending on the href. */
    const tChip=e.target.closest(".treatment-drug-chip");
    if(tChip){e.preventDefault();navigateToDrug(tChip.dataset.drug);return;}
    const dChip=e.target.closest(".drug-disease-chip");
    if(dChip){e.preventDefault();openDiseaseAcrossSpecies(dChip.dataset.disease,dChip.dataset.species||currentSpecies||"");return;}
    const anesthLink=e.target.closest(".anesthesia-nav-link");
    if(anesthLink){e.preventDefault();_pushNavHistory(currentView,"anesthesia","");switchView("anesthesia");_showBackNav("anesthesiaBackNav","anesthesiaSearch");const p=document.getElementById("viewAnesthesia");if(p)scrollToAnchor(p);return;}
    /* Drug detail → anesthesia protocols using this drug: pre-fill the
       anesthesia search with the agent query and land on the filtered list.
       Setting the input before the (possibly still in-flight) protocol fetch
       is safe — loadAnesthesiaProtocols re-reads it when it renders. */
    const anesProto=e.target.closest(".drug-anes-protocols-link");
    if(anesProto){
      e.preventDefault();
      _pushNavHistory(currentView,"anesthesia","");
      switchView("anesthesia");
      _showBackNav("anesthesiaBackNav","anesthesiaSearch");
      const inp=document.getElementById("anesthesiaSearch");
      if(inp)inp.value=anesProto.dataset.anesQuery||"";
      if(anesthesiaLoaded)renderAnesthesiaList();
      trackEvent("anesthesia_from_drug",{query:anesProto.dataset.anesQuery||""});
      const p=document.getElementById("anesthesiaList");
      if(p)scrollToAnchor(p);
      return;
    }
    const diffBtn=e.target.closest(".differential-check-btn");
    if(diffBtn){e.preventDefault();runDifferentialFromDisease(diffBtn.dataset.ids);return;}
    if(e.target.closest("a"))return;if(e.target.closest(".disease-detail.open"))return;const item=e.target.closest(".disease-db-item");if(item)toggleDbItem(item);
  });
  container.addEventListener("keydown",function(e){
    if(e.key==="Enter"||e.key===" "){const item=e.target.closest(".disease-db-item");if(item&&!e.target.closest("a")&&!e.target.closest(".disease-detail.open")){e.preventDefault();toggleDbItem(item);}return;}
    /* Roving arrow navigation between disease rows so a whole list can be scanned
       from the keyboard. Only act when a collapsed row itself is focused — never
       hijack arrows inside an open detail panel or a form field. */
    if(e.key==="ArrowDown"||e.key==="ArrowUp"||e.key==="Home"||e.key==="End"){
      const item=e.target.closest(".disease-db-item");
      if(!item||e.target!==item)return;
      const items=Array.prototype.slice.call(container.querySelectorAll(".disease-db-item"));
      const idx=items.indexOf(item);
      let next;
      if(e.key==="ArrowDown")next=items[idx+1];
      else if(e.key==="ArrowUp")next=items[idx-1];
      else if(e.key==="Home")next=items[0];
      else next=items[items.length-1];
      if(next){e.preventDefault();next.focus();next.scrollIntoView({block:"nearest"});}
    }
  });
}

/* Toggle disease DB item */
function toggleDbItem(el){
  const detail=el.querySelector(".disease-detail");
  if(detail){
    const isOpen=detail.classList.toggle("open");
    el.setAttribute("aria-expanded",isOpen);
    const nameEl=el.querySelector(".d-name")||el.querySelector(".disease-name");
    const diseaseName=nameEl?(nameEl.textContent||"").trim().substring(0,80):"";
    el.setAttribute("aria-label",isOpen?(currentLang==="ja"?`${diseaseName}を閉じる`:`Close ${diseaseName}`):(currentLang==="ja"?`${diseaseName}の詳細を見る`:`View ${diseaseName} details`));
    if(isOpen){
      /* Accordion: collapse any other open item in the same list so browsing
         stays compact and oriented — one disease at a time. */
      const listEl=el.closest(".disease-db-list");
      if(listEl){
        listEl.querySelectorAll(".disease-db-item[aria-expanded='true']").forEach(other=>{
          if(other===el)return;
          const od=other.querySelector(".disease-detail.open");
          if(od)od.classList.remove("open");
          other.setAttribute("aria-expanded","false");
          const on=other.querySelector(".d-name")||other.querySelector(".disease-name");
          const onm=on?(on.textContent||"").trim().substring(0,80):"";
          other.setAttribute("aria-label",currentLang==="ja"?`${onm}の詳細を見る`:`View ${onm} details`);
        });
      }
      trackEvent("view_disease_detail",{species:currentSpecies,disease:diseaseName});
      if(!detail.querySelector(".detail-close-btn")){
        const closeBtn=document.createElement("button");
        closeBtn.type="button";
        closeBtn.className="detail-close-btn";
        closeBtn.setAttribute("aria-label",currentLang==="ja"?"閉じる":"Close");
        closeBtn.textContent="\u2715";
        closeBtn.addEventListener("click",e=>{e.stopPropagation();toggleDbItem(el);});
        detail.prepend(closeBtn);
      }
      requestAnimationFrame(()=>{
        /* One clean scroll to a reading position — NOT the 12s re-anchoring
           watcher. The detail's own markup renders synchronously (so the initial
           target is reachable immediately); the only later growth is the async
           drug tables, which append *below* the header and so never move it. On
           mobile the page itself scrolls, and letting the settle watcher keep
           re-anchoring as those tables streamed in made the page drift up and
           down while the user was trying to read it. */
        scrollToAnchor(el,{settle:false});
        /* Move focus into the panel for screen readers, but never let focus()
           scroll-into-view — that re-introduced the same vertical lurch. */
        const firstFocusable=detail.querySelector("a,button,[tabindex='0']");
        if(firstFocusable)setTimeout(()=>{try{firstFocusable.focus({preventScroll:true});}catch(_){firstFocusable.focus();}},300);
      });
      if(!detail.dataset.drugsLoaded){
        detail.dataset.drugsLoaded="1";
        _loadDbItemDrugs(detail);
      }
      /* Hydrate any server-API treatment-drug placeholders inside this panel */
      if(typeof hydrateTreatmentDrugs==="function")hydrateTreatmentDrugs(detail);
      /* Hydrate drug→diseases placeholders (drug detail panels) */
      if(typeof hydrateDrugDiseases==="function")hydrateDrugDiseases(detail);
      /* Hydrate related-disease navigation chips (computed from shared symptoms) */
      if(typeof hydrateRelatedDiseases==="function")hydrateRelatedDiseases(detail);
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
  const skeleton=document.createElement("div");
  skeleton.className="drug-loading-skeleton";
  skeleton.innerHTML='<div class="skeleton skeleton-card" style="height:40px;margin-top:10px"></div>';
  detail.appendChild(skeleton);
  fetchWithTimeout("/api/drugs").then(r=>r.json()).then(data=>{
    skeleton.remove();
    if(!allDrugs.length){allDrugs=data.drugs||[];}
    doMatch();
  }).catch(()=>{skeleton.remove();});
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

/* --- Scroll-to-top button with progress ring --- */
(function(){
  const btn=document.createElement("button");
  btn.type="button";
  btn.className="scroll-top";
  btn.setAttribute("aria-label",currentLang==="ja"?"ページの先頭へ":"Scroll to top");
  btn.innerHTML='<svg class="scroll-progress-ring" viewBox="0 0 36 36"><circle cx="18" cy="18" r="16" fill="none" stroke="rgba(255,255,255,.2)" stroke-width="2"/><circle class="scroll-progress-arc" cx="18" cy="18" r="16" fill="none" stroke="var(--green)" stroke-width="2" stroke-linecap="round" stroke-dasharray="100.53" stroke-dashoffset="100.53" transform="rotate(-90 18 18)"/></svg><span class="scroll-arrow">\u2191</span>';
  document.body.appendChild(btn);
  const arc=btn.querySelector(".scroll-progress-arc");
  const circ=2*Math.PI*16;
  let ticking=false;
  window.addEventListener("scroll",()=>{
    if(!ticking){requestAnimationFrame(()=>{
      const scrollH=document.documentElement.scrollHeight-window.innerHeight;
      const pct=scrollH>0?Math.min(window.scrollY/scrollH,1):0;
      btn.classList.toggle("visible",window.scrollY>400);
      if(arc)arc.style.strokeDashoffset=circ*(1-pct);
      const rp=document.getElementById("readingProgress");
      if(rp)rp.style.width=(pct*100)+"%";
      ticking=false;
    });ticking=true;}
  },{passive:true});
  btn.addEventListener("click",()=>{haptic(10);window.scrollTo({top:0,behavior:"smooth"});});
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
/* --- PWA Install prompt (A2HS) --- */
(function(){
  let deferredPrompt=null;
  window.addEventListener("beforeinstallprompt",e=>{
    e.preventDefault();deferredPrompt=e;
    if(localStorage.getItem("vetdict-pwa-dismissed"))return;
    setTimeout(()=>{if(!deferredPrompt)return;
      let banner=document.getElementById("pwaInstallBanner");
      if(banner)return;
      banner=document.createElement("div");banner.id="pwaInstallBanner";banner.className="pwa-install-banner";
      const isJa=typeof currentLang!=="undefined"&&currentLang==="ja";
      banner.innerHTML=`<span class="pwa-icon">📲</span><span class="pwa-text">${isJa?"VetDictをアプリとしてインストール":"Install VetDict as an app"}</span><button class="pwa-install-btn">${isJa?"インストール":"Install"}</button><button class="pwa-dismiss-btn" aria-label="Dismiss">✕</button>`;
      document.body.appendChild(banner);
      requestAnimationFrame(()=>banner.classList.add("visible"));
      const removeBanner=()=>{banner.classList.remove("visible");setTimeout(()=>banner.remove(),300);};
      banner.querySelector(".pwa-install-btn").addEventListener("click",()=>{
        removeBanner();deferredPrompt.prompt();
        deferredPrompt.userChoice.then(c=>{if(c.outcome==="accepted"){localStorage.setItem("vetdict-pwa-dismissed","1");}deferredPrompt=null;});
      });
      banner.querySelector(".pwa-dismiss-btn").addEventListener("click",()=>{
        removeBanner();localStorage.setItem("vetdict-pwa-dismissed","1");
      });
    },5000);
  });
  window.addEventListener("appinstalled",()=>{const b=document.getElementById("pwaInstallBanner");if(b)b.remove();});
})();

const _toastQueue=[];let _toastBusy=false;const _TOAST_MAX_QUEUE=5;
/* showToast(msg, type, duration, action?)
   action: optional {label, onClick} — renders an action button (e.g., "Undo") */
function showToast(msg,type,duration,action){
  type=type||"";duration=duration||(action?5000:2500);
  if(_toastQueue.length>=_TOAST_MAX_QUEUE)_toastQueue.shift();
  _toastQueue.push({msg,type,duration,action});
  if(!_toastBusy)_drainToastQueue();
}
function _drainToastQueue(){
  if(!_toastQueue.length){_toastBusy=false;return;}
  _toastBusy=true;
  const{msg,type,duration,action}=_toastQueue.shift();
  const icons={success:"✓",error:"✕",warning:"⚠",info:"ℹ"};
  let toast=document.getElementById("vetdictToast");
  if(!toast){
    toast=document.createElement("div");
    toast.id="vetdictToast";
    toast.className="toast";
    toast.setAttribute("role","status");
    toast.setAttribute("aria-live","polite");
    toast.setAttribute("aria-atomic","true");
    document.body.appendChild(toast);
  }
  if(type==="error"){toast.setAttribute("role","alert");toast.setAttribute("aria-live","assertive");}
  else{toast.setAttribute("role","status");toast.setAttribute("aria-live","polite");}
  const icon=icons[type]?"<span class=\"toast-icon\" aria-hidden=\"true\">"+icons[type]+"</span>":"";
  const actionHtml=action&&action.label?`<button type="button" class="toast-action">${escapeHtml(action.label)}</button>`:"";
  toast.innerHTML=icon+"<span class=\"toast-msg\">"+escapeHtml(msg)+"</span>"+actionHtml;
  toast.className="toast"+(type?" "+type:"")+(action?" toast-with-action":"");
  if(action&&action.onClick){
    const btn=toast.querySelector(".toast-action");
    if(btn)btn.addEventListener("click",()=>{
      try{action.onClick();}catch(e){debugError("toast action onClick failed",e);}
      clearTimeout(toast._timer);
      toast.classList.remove("show");
      setTimeout(_drainToastQueue,200);
    },{once:true});
  }
  requestAnimationFrame(()=>toast.classList.add("show"));
  clearTimeout(toast._timer);
  toast._timer=setTimeout(()=>{toast.classList.remove("show");setTimeout(_drainToastQueue,300);},duration);
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
            .map(([key, value]) => `<li>${escapeHtml(String(value))}</li>`)
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
          <span>${escapeHtml(String(disease))}</span>
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
    item.type = 'button';
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
      debugError("Multi-disease analysis error:",error);
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

