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
  title.textContent = 'Diagnostic Guidance';
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
