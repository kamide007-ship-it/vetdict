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
