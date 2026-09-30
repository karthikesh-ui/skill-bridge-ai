if ($('#careerList')) {
  const pageSize = 12;
  let catalogue = [];
  let visibleCount = pageSize;
  const compared = new Set();
  const resultMode = new URLSearchParams(location.search).has('results');

  function startNewDiscovery() {
    store.set('answers', { name: '', education: '', subjects: [], activities: [], career_areas: [], work_preference: '', competitive_exams: 'unsure' });
    store.set('profile', { ...store.get('profile', {}), name: '', education: '' });
    location.href = '/discovery?new=1';
  }

  function careerCard(career, personalized = false) {
    const compareControl = personalized ? '' : `<label class="compare-toggle"><input type="checkbox" data-compare="${esc(career.id)}" aria-label="Add ${esc(career.name)} to comparison"> Compare</label>`;
    return `<article class="card career-card">
      <span class="pill">${esc(career.category)}</span>
      <h3>${esc(career.name)}</h3>
      <p>${esc(career.day_to_day || career.description)}</p>
      ${career.why ? `<p><b>Why this appears:</b> ${esc(career.why)}</p>` : ''}
      ${career.route_note ? `<p class="notice">Route note: ${esc(career.route_note)}</p>` : ''}
      <div class="card-foot"><small><b>Course ideas:</b> ${esc(career.course_preview?.join(' · ') || career.preview || '')}</small>
        <div class="card-actions">${compareControl}<button class="button" type="button" data-id="${esc(career.id)}">Explore pathway</button></div>
      </div>
    </article>`;
  }

  function attachExploreButtons(root) {
    root.querySelectorAll('[data-id]').forEach(button => button.addEventListener('click', () => choose(button.dataset.id)));
  }

  function renderCatalogue() {
    const query = $('#search').value.trim().toLocaleLowerCase();
    const category = $('#categoryFilter').value;
    const matches = catalogue.filter(career => (!category || career.category === category)
      && (!query || `${career.name} ${career.category} ${career.description}`.toLocaleLowerCase().includes(query)));
    const visible = matches.slice(0, visibleCount);
    $('#careerList').innerHTML = visible.map(career => careerCard(career)).join('')
      || '<div class="card"><h3>No professions found</h3><p>Try another search or category.</p></div>';
    $('#clearSearch').hidden = !query && !category;
    $('#loadMore').hidden = visible.length >= matches.length;
    $('#catalogueStatus').textContent = `${visible.length} of ${matches.length} professions shown.`;
    attachExploreButtons($('#careerList'));
    $('#careerList').querySelectorAll('[data-compare]').forEach(input => {
      input.checked = compared.has(input.dataset.compare);
      input.addEventListener('change', onCompareChange);
    });
  }

  async function renderComparison() {
    const panel = $('#comparison');
    panel.hidden = compared.size === 0;
    if (!compared.size) return;
    const ids = [...compared];
    if (ids.length < 2) {
      $('#comparisonContent').innerHTML = '<p role="status">Select one more profession to compare.</p>';
      return;
    }
    $('#comparisonContent').innerHTML = '<p role="status">Loading comparison…</p>';
    try {
      const careers = await Promise.all(ids.map(id => api(`/api/career/${encodeURIComponent(id)}`)));
      $('#comparisonContent').innerHTML = careers.map(career => {
        const alternatives = (career.routes || []).slice(1).map(route => `${route.name}: ${route.stages?.[2]?.detail || route.stages?.[2]?.alternatives || ''}`).join('; ') || 'Compare the listed course options.';
        return `<article class="compare-column"><h3>${esc(career.name)}</h3>
          <dl><dt>Subjects</dt><dd>${esc(career.matching?.subjects?.join(', ') || 'Varies by route')}</dd>
          <dt>Courses</dt><dd>${esc(career.course_options?.map(course => course.name).join(', ') || 'See official course information')}</dd>
          <dt>Exams</dt><dd>${esc(career.exams)}</dd>
          <dt>Skills</dt><dd>${esc(career.skills?.join(', '))}</dd>
          <dt>Alternative routes</dt><dd>${esc(alternatives)}</dd></dl></article>`;
      }).join('');
    } catch (error) {
      $('#comparisonContent').innerHTML = '<p role="alert">Comparison could not load. Check that Flask is running and try again.</p>';
    }
  }

  function onCompareChange(event) {
    const id = event.currentTarget.dataset.compare;
    if (event.currentTarget.checked && compared.size >= 2) {
      event.currentTarget.checked = false;
      $('#catalogueStatus').textContent = 'Compare two professions at a time. Clear a selection to choose another.';
      return;
    }
    if (event.currentTarget.checked) compared.add(id);
    else compared.delete(id);
    renderComparison();
  }

  async function load() {
    try {
      $('#fullCatalogueLink').hidden = !resultMode;
      if (resultMode) {
        $('#personalizedSection').hidden = false;
        $('#heading').textContent = 'Your career exploration results';
        $('#personalizedList').innerHTML = '<p role="status">Loading suggestions...</p>';
        const answers = store.get('answers', {});
        const response = await api('/api/career/discover', { ...answers, profile: store.get('profile', {}) });
        const results = response.results || [];
        $('#resultsMessage').hidden = !response.message;
        $('#resultsMessage').textContent = response.message || '';
        $('#personalizedList').innerHTML = results.map(career => careerCard(career, true)).join('')
          || '<div class="card"><h3>More interests needed</h3><p>Choose a subject, activity or area to see suggestions based on your answers.</p><a class="button" href="/discovery">Add interests</a></div>';
        const related = response.related || [];
        $('#relatedSection').hidden = !related.length;
        $('#relatedList').innerHTML = related.map(career => careerCard(career, true)).join('');
        attachExploreButtons($('#personalizedList'));
        attachExploreButtons($('#relatedList'));
      }

      $('#catalogueStatus').textContent = 'Loading profession catalogue...';
      catalogue = await api('/api/careers');
      const categories = [...new Set(catalogue.map(career => career.category))].sort();
      $('#categoryFilter').insertAdjacentHTML('beforeend', categories.map(category => `<option value="${esc(category)}">${esc(category)}</option>`).join(''));
      renderCatalogue();
    } catch (error) {
      if (resultMode) $('#personalizedList').innerHTML = '<p role="alert">Suggestions could not load. Check that Flask is running, then refresh.</p>';
      $('#careerList').innerHTML = '<p role="alert">The career catalogue could not load. Check that Flask is running, then refresh.</p>';
    }
  }

  $('#search').addEventListener('input', () => { visibleCount = pageSize; renderCatalogue(); });
  $('#categoryFilter').addEventListener('change', () => { visibleCount = pageSize; renderCatalogue(); });
  $('#clearSearch').addEventListener('click', () => {
    $('#search').value = '';
    $('#categoryFilter').value = '';
    visibleCount = pageSize;
    renderCatalogue();
    $('#search').focus();
  });
  $('#loadMore').addEventListener('click', () => { visibleCount += pageSize; renderCatalogue(); });
  $('#clearComparison').addEventListener('click', () => {
    compared.clear();
    renderCatalogue();
    renderComparison();
  });
  load();
}

if ($('#detail')) {
  (async () => {
    try {
      const career = await api(`/api/career/${encodeURIComponent(selected())}`);
      document.title = `${career.name} | Skill Bridge-AI`;
      $('#detail').innerHTML = `<span class="pill">${esc(career.category)}</span><h1>${esc(career.name)}</h1>
        <p class="lead">${esc(career.day_to_day || career.overview)}</p>
        <div class="section-heading"><span class="eyebrow">Understand the route</span><h2>What comes after 10th?</h2></div>
        <div class="grid two"><article class="card"><h3>11th–12th or preparation</h3><p>${esc(career.stream)}</p><h3>Entrance and professional exams</h3><p>${esc(career.exams)}</p><p class="notice">Check the latest official admission and exam notifications before deciding.</p></article>
        <article class="card"><h3>Who might enjoy this?</h3><p>Students interested in ${esc(career.tags?.join(', '))} may like exploring this field.</p><h3>First practical step</h3><p>${esc(career.starter_actions?.[1] || career.preparation)}</p></article></div>
        <div class="section-heading"><span class="eyebrow">Compare your options</span><h2>Courses and routes</h2><p>${esc(career.decision_help || 'Compare official course requirements.')}</p></div>
        <div class="grid two">${(career.course_options || []).map((course, index) => `<article class="card course-card"><span class="course-index">${String(index + 1).padStart(2, '0')}</span><h3>${esc(course.name)}</h3><p>${esc(course.note)}</p></article>`).join('')}</div>
        <div class="section-heading"><span class="eyebrow">What to practise</span><h2>Skills and experience</h2></div>
        <div class="grid two"><article class="card"><h3>Useful skills</h3><div class="chips">${(career.skills || []).map(skill => `<span>${esc(skill)}</span>`).join('')}</div></article><article class="card"><h3>Project or preparation</h3><p>${esc(career.preparation)}</p></article></div>
        <div class="actions"><a class="button" href="/pathway">View education pathway</a><button class="button secondary" id="ask" type="button">Ask for personal guidance</button></div>
        <div class="card guidance" id="guidance" hidden><h3>Ask your career companion</h3><label for="questionInput">Your question</label><input class="input" id="questionInput" maxlength="500" placeholder="For example: what should I learn first?"><button class="button" id="sendQuestion" type="button">Get guidance</button><p id="answer" role="status" aria-live="polite"></p></div>`;
      $('#ask').addEventListener('click', () => { $('#guidance').hidden = false; $('#questionInput').focus(); });
      $('#sendQuestion').addEventListener('click', async () => {
        const answer = $('#answer');
        const button = $('#sendQuestion');
        button.disabled = true;
        answer.textContent = 'Preparing guidance…';
        try {
          const response = await api('/api/career/guidance', { career_id: career.id, question: $('#questionInput').value });
          answer.textContent = `${response.text} (${response.source === 'gemini' ? 'AI guidance' : 'built-in guidance'})`;
        } catch (error) {
          answer.textContent = 'Guidance is unavailable. Check that Flask is running and try again.';
        } finally {
          button.disabled = false;
        }
      });
    } catch (error) {
      $('#detail').innerHTML = '<div class="card"><h2>Choose a career first</h2><a class="button" href="/careers">Explore careers</a></div>';
    }
  })();
}