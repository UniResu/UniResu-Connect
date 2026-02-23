document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(".register-form");
    
    if(form) {
        form.addEventListener("submit", async (e) => {
            e.preventDefault(); 

            const nome = document.getElementById("nome").value;
            const email = document.getElementById("email").value;
            const senha = document.getElementById("senha").value;
            const instituicao = document.getElementById("instituicao").value;
            const vinculo = document.getElementById("vinculo").value;

            console.log("Tentando cadastrar com os dados:", { nome, email, instituicao, vinculo });

            try {
                const response = await fetch("http://127.0.0.1:8000/api/usuarios/registrar", {
                    method: "POST",
                    headers: { 
                        "Content-Type": "application/json",
                        "Accept": "application/json"
                    },
                    body: JSON.stringify({ nome, email, senha, instituicao, vinculo })
                });

                if (response.ok) {
                    alert("Cadastro realizado com sucesso!");
                    window.location.href = "login.html"; 
                } else {
                    const errorData = await response.json();
                    console.error("Erro reportado pelo backend:", errorData);
                    alert("Erro ao cadastrar: " + (errorData.detail || "Verifique os dados."));
                }
            } catch (error) {
                console.error("O Fetch falhou:", error);
                alert("Erro de conexão! Verifique se o servidor FastAPI está rodando na porta 8000.");
            }
        });
    } else {
        console.error("Formulário '.register-form' não encontrado no HTML!");
    }
});