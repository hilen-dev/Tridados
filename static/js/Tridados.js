document.addEventListener("DOMContentLoaded", initTridados);

function initTridados() {
  console.log("Tridados iniciado com sucesso!");
  setupAttributeInputs();
  computePoints();
}

function setupAttributeInputs() {
  document.querySelectorAll("[data-atributo]").forEach(input => {
    input.addEventListener("input", computePoints);
  });
}

function sumActive(selector, dataAttr, fallback = 0) {
  return Array.from(document.querySelectorAll(`${selector} .pill.active`))
    .reduce((total, el) => total + (parseInt(el.dataset[dataAttr], 10) || fallback), 0);
}

function computePoints() {
  const initial = parseInt(document.getElementById('initialPoints')?.value, 10) || 0;

  const atributosCost = ['attrP', 'attrH', 'attrR']
    .reduce((total, id) =>
      total + (parseInt(document.getElementById(id)?.value, 10) || 0), 0);

  const perCost = document.querySelectorAll('#periciasWrap .pill.active').length;

  const vantCost = sumActive('#vantagensWrap', 'cost', 1);

  const desvGain = sumActive('#desvWrap', 'gain', 1);

  const arqCost = parseInt(document.getElementById('arquetipoCost')?.value, 10) || 0;

  const total = initial - (atributosCost + perCost + vantCost + arqCost - desvGain);

  document.getElementById('periciasCost').textContent = perCost;
  document.getElementById('vantCost').textContent = vantCost;
  document.getElementById('desvGain').textContent = desvGain;
  document.getElementById('pointsLeft').textContent = total;
}

function validateFicha() {
  const pontos = parseInt(document.getElementById('pointsLeft').textContent) || 0;

  if (pontos < 0) {
    alert("Você gastou mais pontos do que possui.");
    return false;
  }

  return true;
}

const form = document.querySelector("form");

if (form) {
  form.addEventListener("submit", e => {
    if (!validateFicha()) {
      e.preventDefault();
    }
  });
}