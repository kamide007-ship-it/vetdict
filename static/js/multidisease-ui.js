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

// Debug-gated logging — silent in production.
const _MD_DEBUG = (() => {
  try {
    const h = location.hostname;
    return h === 'localhost' || h === '127.0.0.1' || h === '' || location.search.indexOf('debug=1') >= 0;
  } catch (e) { return false; }
})();
const _mdLog = (...args) => { if (_MD_DEBUG && typeof console !== 'undefined') console.log(...args); };
const _mdError = (...args) => { if (_MD_DEBUG && typeof console !== 'undefined') console.error(...args); };

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
      _mdError('Multi-disease analysis error:', error);
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
    badge.textContent = 'Multi-Disease Mode Active';
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
    const comboId = element.getAttribute('data-combo-id');
    _mdLog('Selected combination:', comboId);
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
    _mdLog('Selected question:', questionId);
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
