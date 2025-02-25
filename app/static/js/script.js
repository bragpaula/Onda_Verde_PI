// Obtém os elementos do modal
var modal = document.getElementById("activityModal");
var openModalBtn = document.getElementById("btnCadastrarAtiv");
var closeBtn = document.getElementsByClassName("close-btn")[0];
var form = document.getElementById("activityForm");

// Quando a página carregar, verifica se o modal deve ser aberto automaticamente
document.addEventListener("DOMContentLoaded", function () {
  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.get("abrirModal") === "true" && modal) {
    modal.style.display = "block";
  }
});

// Quando o usuário clicar no botão "Cadastrar Nova Atividade", abre o modal
if (openModalBtn) {
  openModalBtn.onclick = function () {
    modal.style.display = "block";
  };
}

// Quando o usuário clicar no botão (X), fecha o modal
if (closeBtn) {
  closeBtn.onclick = function () {
    modal.style.display = "none";
  };
}

// Quando o usuário clicar fora do conteúdo do modal, fecha o modal
window.onclick = function (event) {
  if (event.target === modal) {
    modal.style.display = "none";
  }
};

// Lógica de envio do formulário
if (form) {
  form.onsubmit = function (event) {
    event.preventDefault();

    var title = document.getElementById("title").value;
    var description = document.getElementById("description").value;
    var address = document.getElementById("address").value;
    var date = document.getElementById("date").value;
    var time = document.getElementById("time").value;

    // Envio de dados para o backend (simulação)
    console.log("Nova atividade:", {
      title: title,
      description: description,
      address: address,
      date: date,
      time: time
    });

    // Fecha o modal após submeter
    modal.style.display = "none";
  };
}
