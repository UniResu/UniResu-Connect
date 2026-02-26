const DOMINIOS_INSTITUCIONAIS = [
    "usp.br", "unicamp.br", "unesp.br", "ufmg.br", "ufrj.br",
    "ufsc.br", "unb.br", "ufpr.br", "ufba.br", "ufrgs.br",
    "ufpe.br", "ufc.br", "ufpb.br", "ufv.br", "ufam.br",
    "uerj.br", "ufrn.br", "ufes.br", "ufg.br",
    "ifsp.edu.br", "ifrj.edu.br", "ifmg.edu.br",
    "capes.gov.br", "cnpq.br", "embrapa.br", "puc.br"
];

function emailInstitucionalValido(email) {
    const dominio = email.split("@")[1]?.toLowerCase();
    if (!dominio) return false;
    return DOMINIOS_INSTITUCIONAIS.some(d => dominio === d || dominio.endsWith("." + d));
}

function atualizarBotaoOrcid() {
    const vinculo = document.getElementById("vinculo").value;
    const container = document.getElementById("orcid-container");
    if (!container) return;

    if (vinculo === "professor" || vinculo === "pesquisador") {
        container.style.display = "block";
    } else {
        container.style.display = "none";
        sessionStorage.removeItem("orcid_id");
        sessionStorage.removeItem("orcid_nome");
        atualizarStatusOrcid();
    }
}

function atualizarStatusOrcid() {
    const orcidId   = sessionStorage.getItem("orcid_id");
    const orcidNome = sessionStorage.getItem("orcid_nome");
    const statusEl  = document.getElementById("orcid-status");
    const btnOrcid  = document.getElementById("btn-orcid");
    if (!statusEl) return;

    if (orcidId) {
        statusEl.innerHTML = `Conectado: <strong>${orcidNome || orcidId}</strong>`;
        statusEl.className = "orcid-status orcid-ok";
        if (btnOrcid) btnOrcid.textContent = "Reconectar ORCID";
    } else {
        statusEl.textContent = "Opcional - vincula suas publicacoes e afiliacoes ao perfil.";
        statusEl.className = "orcid-status orcid-hint";
        if (btnOrcid) btnOrcid.textContent = "Conectar com ORCID";
    }
}

function conectarOrcid() {
    sessionStorage.setItem("form_nome",        document.getElementById("nome").value.trim());
    sessionStorage.setItem("form_email",       document.getElementById("email").value.trim());
    sessionStorage.setItem("form_instituicao", document.getElementById("instituicao").value.trim());
    sessionStorage.setItem("form_vinculo",     document.getElementById("vinculo").value);
    window.location.href = "https://uniresu-connect.onrender.com/api/orcid/connect";
}

function restaurarFormulario() {
    const campos = {
        nome:        sessionStorage.getItem("form_nome"),
        email:       sessionStorage.getItem("form_email"),
        instituicao: sessionStorage.getItem("form_instituicao"),
        vinculo:     sessionStorage.getItem("form_vinculo")
    };
    for (const [id, valor] of Object.entries(campos)) {
        const el = document.getElementById(id);
        if (el && valor) el.value = valor;
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const params = new URLSearchParams(window.location.search);
    if (params.get("orcid") === "ok") {
        const orcidId   = params.get("orcid_id")  || "";
        const orcidNome = params.get("orcid_nome") || "";
        if (orcidId) {
            sessionStorage.setItem("orcid_id",   orcidId);
            sessionStorage.setItem("orcid_nome", orcidNome);
        }
        window.history.replaceState({}, "", window.location.pathname);
        restaurarFormulario();
    }

    atualizarBotaoOrcid();
    atualizarStatusOrcid();
    document.getElementById("vinculo").addEventListener("change", atualizarBotaoOrcid);

    const form = document.querySelector(".register-form");

    if(form) {
        form.addEventListener("submit", async (e) => {
            e.preventDefault(); 

            const nome        = document.getElementById("nome").value.trim();
            const email       = document.getElementById("email").value.trim().toLowerCase();
            const senha       = document.getElementById("senha").value;
            const instituicao = document.getElementById("instituicao").value.trim();
            const vinculo     = document.getElementById("vinculo").value;
            const orcidId     = sessionStorage.getItem("orcid_id") || null;

            if (!nome || nome.length < 3) {
                alert("Por favor, digite um nome valido (minimo de 3 caracteres).");
                document.getElementById("nome").focus(); 
                return; 
            }

            if (!email || !senha || senha.length < 6) {
                alert("E-mail e senha sao obrigatorios! A senha deve ter no minimo 6 caracteres.");
                return;
            }

            if ((vinculo === "professor" || vinculo === "pesquisador") && !emailInstitucionalValido(email)) {
                alert(
                    `Como ${vinculo}, e necessario usar um e-mail institucional.\n\n` +
                    `Exemplos aceitos: nome@usp.br, nome@uerj.br, nome@capes.gov.br\n\n` +
                    `O e-mail "${email}" nao pertence a uma instituicao reconhecida.`
                );
                document.getElementById("email").focus();
                return;
            }

            console.log("Tentando cadastrar com os dados:", { nome, email, instituicao, vinculo, orcidId });

            try {
                const response = await fetch("https://uniresu-connect.onrender.com/api/usuarios/registrar", {
                    method: "POST",
                    headers: { 
                        "Content-Type": "application/json",
                        "Accept": "application/json"
                    },
                    body: JSON.stringify({ nome, email, senha, instituicao, vinculo, orcid_id: orcidId })
                });

                if (response.ok) {
                    sessionStorage.removeItem("orcid_id");
                    sessionStorage.removeItem("orcid_nome");
                    sessionStorage.removeItem("form_nome");
                    sessionStorage.removeItem("form_email");
                    sessionStorage.removeItem("form_instituicao");
                    sessionStorage.removeItem("form_vinculo");

                    alert("Cadastro realizado com sucesso! Bem-vindo(a) ao UniResu.");
                    window.location.href = "login.html"; 
                } else {
                    const errorData = await response.json();
                    console.error("Erro reportado pelo backend:", errorData);

                    let mensagemErro = errorData.detail;
                    if (Array.isArray(mensagemErro)) {
                        mensagemErro = "Verifique os campos preenchidos. Alguns dados estao invalidos ou muito curtos.";
                    }
                    
                    alert("Erro ao cadastrar: " + mensagemErro);
                }
            } catch (error) {
                console.error("O Fetch falhou:", error);
                alert("Erro de conexao! Verifique se o servidor FastAPI esta rodando na porta 8000.");
            }
        });
    } else {
        console.error("Formulario '.register-form' nao encontrado no HTML!");
    }
});
