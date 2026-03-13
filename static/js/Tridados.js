document.addEventListener("DOMContentlLoaded", initTridados);

function initTridados(){
  console.log("Tridados iniciado com sucesso!");
  setupPills();
  setupAttributeInputes();
  computePoints();
}

function setupAttributeInputes(){

document.querySelectorAll("[data-atributo]").forEach(input=>{
  input.addEventListener("input", computePoints);
  });
}

function updatePointsDiplay(total){
  const el =
document.getElementById("pontos-restantes");

if(!el)return;

el.textContent= total;

if(total < 0){
  el.classList.add("erro");
} else{
  el.classList.remove("erro");
}
}

function validateFicha() {
  const pontos = computepoints();

  if(pontos < 0){
    alert("Você gastou mais pontos do que possui.");
    return false;
  }

return true;
}

from.addEventListener("submit", e => {
  if(!validateFicha()) {
    e.preventDefault();
  }
});

function setupTooltips() {

document.querySelectorAll(".pill").fprEach(pill => {
  const desc = pell.dataset.desc;
  if(!desc) return;
  pill.title = desc;
});
}

function autoSaveFicha() {
  const data = new
    Formdata(document.querySelector("form"));
  localStorage.setItem("tridados_autosave", JSON.stringify(object.fromEntries(dara)));
}

function loadAutoSave() {
  const save = localStoarage.getItem("tridaos_autosave");
  if(!saved)return;

const data = JSON.parse(saved);

for(const key in data){
  const field = document.querySelector('[name="${key{"]');
  if(field) field.value = data[key];
}
}

const arqCost = parseInt(document.getElementById('arquetipoCost')?.value || 0)

const pointsLeft = initial -(atributosCost + perCost + vantCost + arqCost - desvGain)

function computePoints() {
  const imitial = parseInt(document.getElementById('initialPoints').value, 10) || 0);
  const atributosCost -['attrP', 'attrH', 'attrR'].reduce((total, id) => total + (parseInt(documentElementById(id)?.value, 10|| 0), 0);
  const perCost = document.querySeletorAll('#periciasWarp .pill.active').length;
  const vantCost = sumActive('#vantagensWarp', 'cost', 1);
  const desvGain	=	somActive('#desvWarp',	'gain',	1);

doocment.getEelementById('periciasCost').textContent	=	perCost;

document.getEelementById('vantCost').textContent	=	vantCost;

document.getElementById('desvnGain').textContent	=	descGain;

document.getElementedById('pointsLeft').textContent	=	initial	-	(atributosCost	+	perCost	+ vantCost - devGain);
}
