const steps = [
  { title: 'What should we call you?', key: 'name', type: 'text', hint: 'A name is optional. Your answers stay in this browser.' },
  { title: 'Where are you in your studies?', key: 'education', type: 'single', hint: 'Choose your current stage.', options: ['10th completed', 'In 11th', '12th completed', 'In college', 'Other'] },
  { title: 'Which subjects do you enjoy?', key: 'subjects', type: 'multi', hint: 'Choose any that interest you.', options: ['Mathematics', 'Biology', 'Physics', 'Chemistry', 'Computers', 'Languages', 'Social Science', 'Business/Accounting', 'Art'] },
  { title: 'What activities feel interesting?', key: 'activities', type: 'multi', hint: 'Choose activities you would like to try.', options: ['coding', 'solving numerical problems', 'helping people', 'teaching', 'designing', 'writing', 'building/repairing things', 'organizing', 'working outdoors'] },
  { title: 'Which career areas would you explore?', key: 'career_areas', type: 'multi', hint: 'This is about curiosity, not a commitment.', options: ['Technology', 'Engineering', 'Healthcare', 'Business/Commerce', 'Public Service', 'Education', 'Creative/Design/Media', 'Law', 'Science/Research', 'Agriculture/Food', 'Hospitality', 'Skilled Trades'] },
  { title: 'What kind of work sounds appealing?', key: 'work_preference', type: 'single', hint: 'There is no better answer.', options: ['practical', 'theoretical', 'both'] },
  { title: 'How do you feel about competitive exams?', key: 'competitive_exams', type: 'single', hint: 'Unsure is a valid answer and will not count against you.', options: ['interested', 'unsure', 'not interested'] }
];

const blankAnswers = () => ({ name: '', education: '', subjects: [], activities: [], career_areas: [], work_preference: '', competitive_exams: 'unsure' });
let saved = store.get('answers', {});
let answers = {
  ...blankAnswers(),
  name: typeof saved.name === 'string' ? saved.name : '',
  education: typeof saved.education === 'string' ? saved.education : '',
  subjects: Array.isArray(saved.subjects) ? saved.subjects : [],
  activities: Array.isArray(saved.activities) ? saved.activities : [],
  career_areas: Array.isArray(saved.career_areas) ? saved.career_areas : [],
  work_preference: typeof saved.work_preference === 'string' ? saved.work_preference : '',
  competitive_exams: ['interested', 'unsure', 'not interested'].includes(saved.competitive_exams) ? saved.competitive_exams : 'unsure'
};
let step = 0;

function render() {
  const current = steps[step];
  $('#bar').style.width = `${((step + 1) / steps.length) * 100}%`;
  $('#bar').parentElement.setAttribute('aria-valuenow', String(step + 1));
  $('#stepLabel').textContent = `Step ${step + 1} of ${steps.length}`;
  $('#question').textContent = current.title;
  $('#hint').textContent = current.hint;
  $('#back').disabled = step === 0;
  $('#next').textContent = step === steps.length - 1 ? 'See my suggestions' : 'Next';
  $('#options').replaceChildren();

  if (current.type === 'text') {
    const label = document.createElement('label');
    label.className = 'sr-only';
    label.htmlFor = 'studentName';
    label.textContent = 'Your name';
    const input = document.createElement('input');
    input.className = 'input';
    input.id = 'studentName';
    input.autocomplete = 'given-name';
    input.placeholder = 'Your first name (optional)';
    input.value = answers.name;
    input.addEventListener('input', () => { answers.name = input.value; });
    $('#options').append(label, input);
    return;
  }

  for (const value of current.options) {
    const button = document.createElement('button');
    const selected = current.type === 'single'
      ? answers[current.key] === value
      : answers[current.key].includes(value);
    button.type = 'button';
    button.className = `choice${selected ? ' active' : ''}`;
    button.setAttribute('aria-pressed', String(selected));
    button.textContent = value;
    button.addEventListener('click', () => {
      if (current.type === 'single') answers[current.key] = value;
      else answers[current.key] = selected
        ? answers[current.key].filter(item => item !== value)
        : [...answers[current.key], value];
      render();
    });
    $('#options').append(button);
  }
}

function discoveryBack() {
  step = Math.max(0, step - 1);
  render();
}

function discoveryNext() {
  if (step < steps.length - 1) {
    step += 1;
    render();
    return;
  }
  answers.name = $('#studentName')?.value.trim() || answers.name;
  store.set('answers', answers);
  store.set('profile', { ...store.get('profile', {}), name: answers.name, education: answers.education });
  location.href = '/careers?results=1';
}

function startNewDiscovery() {
  answers = blankAnswers();
  step = 0;
  store.set('answers', answers);
  store.set('profile', { ...store.get('profile', {}), name: '', education: '' });
  render();
}

render();