const search = document.getElementById('searchSymptom');
if (search) search.addEventListener('input', e => {
  const q = e.target.value.toLowerCase();
  document.querySelectorAll('.symptom').forEach(el => {
    el.style.display = el.innerText.toLowerCase().includes(q) ? '' : 'none';
  });
});
