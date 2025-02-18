// Pega o modal
var modal = document.getElementById("activityModal");

// Pega o botão que abre o modal
var openModalBtn = document.getElementById("btnCadastrarAtiv");

// Pega o botão de fechar (X)
var closeBtn = document.getElementsByClassName("close-btn")[0];

// Quando o usuário clicar no botão "Cadastrar Nova Atividade", abre o modal
openModalBtn.onclick = function() {
  modal.style.display = "block";
}

// Quando o usuário clicar em (X), fecha o modal
closeBtn.onclick = function() {
  modal.style.display = "none";
}

// Quando o usuário clicar fora do conteúdo do modal, fecha o modal
window.onclick = function(event) {
  if (event.target === modal) {
    modal.style.display = "none";
  }
}

// Lógica de envio do formulário
document.getElementById("activityForm").onsubmit = function(event) {
  event.preventDefault();
  
  var title = document.getElementById("title").value;
  var description = document.getElementById("description").value;
  var address = document.getElementById("address").value;
  var date = document.getElementById("date").value;
  var time = document.getElementById("time").value;

  // Aqui você pode enviar os dados para o backend (via fetch/axios ou formulário normal)
  console.log("Nova Atividade:", {
    title: title,
    description: description,
    address: address,
    date: date,
    time: time
  });
  
  // Fecha o modal após submeter
  modal.style.display = "none";
  
  // Opcional: limpar o formulário
  document.getElementById("activityForm").reset();
};
