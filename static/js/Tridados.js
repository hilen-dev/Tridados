document.addEventListener("DOMContentLoaded", initTridados);

function initTridados() {
  console.log("Tridados iniciado com sucesso!");
  setupEvents();
  setupFormValidation();
  computePoints();
}

function buildPills(list, containerId, hidenInputId) {
  const wrap =
    document.getElementById(containerId);

  wrap.innerHTML = "";

  list.forEach((item, index) => {
    const key = typeof item === 'string'? item: (item.k||index);
    const label = item.l||item.k||key;

    const pill = document.createElement('button');
    pill.type = 'button';
    pill.className = 'pill';

    pill.dataset.key = key;
    pill.dataset.cost = item.c||0;
    pill.dataset.gain = item.g||0;

    pill.textContent = label;

    wrap.appendChild(pill);
  });
}

function sumAttributes(){
  return Array.from(document.querySelectorAll("[data-atributo]"))
  .reduce((total, el) => total + (parseInt(el.value, 10) || 0), 0);
}

function setupEvents(){
  document.addEventListener("input", (e) => { if (e.target.matches("#initialPoints, [id^='attr']")){
    computePoints();
  }
});

document.addEventListener("click", (e) => {const pill = e.target.closest(".pill");
  if (pill) {pill.classList.toggle("active");
             computePoints();
            }
     });
}

function updatePointsUI(total){
  const pointsEl = document.getElementById('pointsLeft');

  if (!pointsEl) return;

  pointsEl.textContent = total;

  if (total < 0){
     pointsEl.style.color = "red";
  } else {
    pointsEl.style.color = "green";
    }
}

function sumActive(selector, dataAttr) {
  return Array.from(document.querySelectorAll(`${selector} .pill.active`)).reduce((total, el) => {
    const value = Number(el.dataset[dataAttr]);
    return total + (Number.isNaN(value) ? 0: value);
  }, 0);
}

function computePoints() {
  const initial = parseInt(document.getElementById('initialPoints')?.value, 10);

  if (isNaN(initial)) {
    console.error("initial points não definido");
    return;
  }

  const atributosCost = sumAttributes();

  const perCost = document.querySelectorAll('#periciasWrap .pill.active').length;

  const vantCost = sumActive('#vantagensWrap', 'cost');

  const desvGain = sumActive('#desvWrap', 'gain');

  const arqCost = parseInt(document.getElementById('arquetipoCost')?.value, 10) || 0;

  const total = initial - (atributosCost + perCost + vantCost + arqCost - desvGain);

  document.getElementById('periciasCost').textContent = perCost;
  
  document.getElementById('vantCost').textContent = vantCost;
  
  document.getElementById('desvGain').textContent = desvGain;
  
  updatePointsUI(total);
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
    form.addEventListener("submit", e => {
      if(!validateFicha()){
        e.preventDefault();
      }
    });
  }
}
