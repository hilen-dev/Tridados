document.addEventListener("DOMContentLoaded", initTridados);

function initTridados() {
  console.log("Tridados iniciado com sucesso!");
  setupEvents();
  setupFormValidation();
  computePoints();
}

function setupEvents(){
  document.addEventListener("input", computePoints);

  document.addEventListener("click", () => {if (e.target.classList.contains("pill")) {e.target.classList.toggle("active"); computePoints();
                                                                                     }
                                           });
}

function sumAttributes(){
  return
  Array.form(document.querySelectorAll("[data-atributo]"))
  .reduce((total,el) =>total+ (parseInt(el.value,10||0), 0);
}

function sumActive(selector, dataAttr, fallback = 0) {
  return Array.from(document.querySelectorAll(`${selector} .pill.active`))
    .reduce((total, el) => total + (parseInt(el.dataset[dataAttr], 10) || fallback), 0);
}

function computePoints() {
  const initial = parseInt(document.getElementById('initialPoints')?.value, 10);

  if (isNaN(initial)) {
    console.error("initial points não definido");
  }

  const atributosCost = sumAttributes();

  const perCost = document.querySelectorAll('#periciasWrap .pill.active').length;

  const vantCost = sumActive('#vantagensWrap', 'cost', 1);

  const desvGain = sumActive('#desvWrap', 'gain', 1);

  const arqCost = parseInt(document.getElementById('arquetipoCost')?.value, 10) || 0;

  const total = initial - (atributosCost + perCost + vantCost + arqCost - desvGain);

  document.getElementById('periciasCost').textContent = perCost;
  document.getElementById('vantCost').textContent = vantCost;
  document.getElementById('desvGain').textContent = desvGain;
  document.getElementById('pointsLeft').textContent = total;

  function uodatePointsUi(total){
    const pointsEl = documentgetElementById('pointsLeft');

    if (!pointsEl) return;

    pointsEl.textContent = total;

    if (total < 0){
      pointsEl.style.color = "red";
    } else {
      pointsEl.style.color = "green";
    }
}
}
  
function validateFicha() {
  const pontos = parseInt(document.getElementById('pointsLeft').textContent) || 0;

  if (pontos < 0) {
    alert("Você gastou mais pontos do que possui.");
    return false;
  }

  return true;
}

function setupFormValidation() {
  const form = document.querySelector("form");
  if (form) {
    form.addEventsListener("submir", e => {
      if(!validateFicha()){
        e.preventDefault();
      }
    });
  }
}
