/**
 * Multi-Disease Diagnostic UI Handler
 * Phase 6 Stage 9: Frontend Integration
 *
 * Manages multi-disease mode UI, including:
 * - Disease combinations display
 * - Ambiguity resolution UI
 * - Clarifying questions presentation
 * - User guidance
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

    // Use MutationObserver to detect symptom changes
    const observer = new MutationObserver((mutations) => {
      // Debounce to avoid excessive API calls
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
    // Collect current state
    const symptoms = this.getSelectedSymptoms();
    const diseases = this.getSuspectedDiseases();

    if (symptoms.length < 2 || diseases.length < 2) {
      this.clearMultiDiseaseUI();
      return;
    }

    // Show loading state
    this.showLoading();

    try {
      const response = await fetch(this.apiEndpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
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

      // Render UI components based on analysis
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
   * Get list of suspected diseases (from API response or UI state)
   */
  getSuspectedDiseases() {
    // This would typically come from previous diagnosis
    // For now, return empty array (API will provide candidates)
    return [];
  }

  /**
   * Render complete multi-disease UI
   */
  renderMultiDiseaseUI(analysis) {
    const container = this.getOrCreateContainer();
    container.innerHTML = '';

    if (!analysis.multidisease_mode_enabled) {
      container.innerHTML = '';
      return;
    }

    // Render mode badge
    if (analysis.multidisease_mode_enabled) {
      container.appendChild(this.createModeBadge());
    }

    // Render combinations
    if (analysis.combinations && analysis.combinations.length > 0) {
      container.appendChild(
        this.renderCombinations(analysis.combinations)
      );
    }

    // Render ambiguity analysis
    if (analysis.ambiguity_analysis) {
      container.appendChild(
        this.renderAmbiguityAnalysis(analysis.ambiguity_analysis)
      );
    }

    // Render confidence breakdown
    if (analysis.confidence_breakdown) {
      container.appendChild(
        this.renderConfidenceBreakdown(analysis.confidence_breakdown)
      );
    }

    // Render clarifying questions
    if (analysis.next_questions && analysis.next_questions.length > 0) {
      container.appendChild(
        this.renderClarifyingQuestions(analysis.next_questions)
      );
    }

    // Render user guidance
    if (analysis.explanation_en || analysis.explanation_ja) {
      container.appendChild(
        this.renderUserGuidance(analysis)
      );
    }
  }

  /**
   * Create multi-disease mode badge
   */
  createModeBadge() {
    const badge = document.createElement('div');
    badge.className = 'multidisease-badge';
    badge.innerHTML = '🔍 Multi-Disease Mode Active';
    return badge;
  }

  /**
   * Render disease combinations
   */
  renderCombinations(combinations) {
    const section = document.createElement('div');
    section.className = 'multidisease-combinations';

    const title = document.createElement('div');
    title.className = 'combinations-title';
    title.textContent = 'Possible Disease Combinations';
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

  /**
   * Render ambiguity analysis
   */
  renderAmbiguityAnalysis(analysis) {
    const section = document.createElement('div');
    section.className = 'ambiguity-section';

    const title = document.createElement('div');
    title.className = 'ambiguity-title';
    title.textContent = 'Ambiguous Symptoms Detected';
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
        item.innerHTML = `${symptom.symptom_id}`;

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
          <div class="guidance-title">Recommendations</div>
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

  /**
   * Render confidence breakdown
   */
  renderConfidenceBreakdown(breakdown) {
    const section = document.createElement('div');
    section.className = 'confidence-breakdown';

    const title = document.createElement('div');
    title.className = 'breakdown-title';
    title.textContent = 'Confidence Analysis';
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

  /**
   * Render clarifying questions
   */
  renderClarifyingQuestions(questions) {
    const section = document.createElement('div');
    section.className = 'clarifying-questions';

    const title = document.createElement('div');
    title.className = 'questions-title';
    title.textContent = 'Clarifying Questions';
    section.appendChild(title);

    const list = document.createElement('div');
    list.className = 'question-list';

    questions.forEach((q, index) => {
      const item = document.createElement('button');
      item.className = 'question-item';
      item.setAttribute('data-question-id', q.question.question_id);
      item.setAttribute('data-ranking-score', q.ranking_score);

      if (q.ranking_score > 0.8) {
        item.classList.add('recommended');
      }

      const questionText = document.createElement('span');
      questionText.className = 'question-text';
      const lang = currentLang === 'ja' ? q.question.text_ja : q.question.text_en;
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

  /**
   * Render user guidance
   */
  renderUserGuidance(analysis) {
    const guidance = document.createElement('div');
    guidance.className = 'user-guidance';

    const title = document.createElement('div');
    title.className = 'guidance-title';
    title.innerHTML = '💡 Diagnostic Guidance';
    guidance.appendChild(title);

    const text = document.createElement('div');
    text.className = 'guidance-text';

    const icon = document.createElement('span');
    icon.className = 'guidance-icon';
    icon.textContent = '→';

    const content = document.createElement('span');
    const explanation = currentLang === 'ja'
      ? analysis.explanation_ja
      : analysis.explanation_en;
    content.textContent = explanation || 'Review the disease combinations and answer clarifying questions to narrow down the diagnosis.';

    text.appendChild(icon);
    text.appendChild(content);
    guidance.appendChild(text);

    return guidance;
  }

  /**
   * Get or create UI container
   */
  getOrCreateContainer() {
    let container = document.querySelector(this.containerSelector);
    if (!container) {
      // Insert after chat messages or in a default location
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
        <span>Analyzing multi-disease combinations...</span>
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

    // Could trigger additional analysis or update follow-up questions
    const comboId = element.getAttribute('data-combo-id');
    console.log('Selected combination:', comboId);
  }

  /**
   * Handle question selection
   */
  onQuestionSelected(element) {
    const questionId = element.getAttribute('data-question-id');
    const questionText = element.querySelector('.question-text').textContent;

    // Add to chat or form
    const chatInput = document.getElementById('chatInput');
    if (chatInput) {
      chatInput.value = questionText;
      // Could trigger automatic submission
    }

    console.log('Selected question:', questionId);
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
