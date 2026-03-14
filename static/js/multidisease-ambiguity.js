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
