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
