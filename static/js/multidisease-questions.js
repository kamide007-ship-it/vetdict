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
  title.textContent = 'Clarifying Questions';
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
