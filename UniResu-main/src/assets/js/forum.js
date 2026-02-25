document.addEventListener('DOMContentLoaded', () => {

    const API_URL = 'http://localhost:8000/api/forum';
    const VINCULOS_PERMITIDOS = ["professor", "pesquisador"];

    const topicsList = document.getElementById("topicsList");
    const searchInput = document.getElementById("searchInput");
    const newTopicBtn = document.getElementById("newTopicBtn");

    let topics = [];

    const getToken       = () => localStorage.getItem('token');
    const getNome        = () => localStorage.getItem('usuario_nome');
    const getVinculo     = () => localStorage.getItem('usuario_vinculo') || "";
    const getEmail       = () => localStorage.getItem('usuario_email') || "";
    const isLoggedIn     = () => !!getToken();
    const podecriarTopico = () => VINCULOS_PERMITIDOS.includes(getVinculo().toLowerCase());

    function getAuthHeaders() {
        return {
            "Content-Type": "application/json",
            ...(getToken() ? { "Authorization": `Bearer ${getToken()}` } : {})
        };
    }

    function inicializarNavbar() {
        if (!isLoggedIn() || !getNome()) return;

        document.getElementById('area-usuario').innerHTML = `
            <div class="user-menu">
                <span class="user-trigger">Olá, ${getNome()} <span class="arrow">▾</span></span>
                <div class="dropdown">
                    <a href="#" id="btn-logout">Sair</a>
                </div>
            </div>
        `;

        document.getElementById('btn-logout').addEventListener('click', logout);

        const menu = document.querySelector('.user-menu');
        menu.addEventListener('click', (e) => {
            e.stopPropagation();
            menu.classList.toggle('open');
        });

        document.addEventListener('click', () => menu.classList.remove('open'));
    }

    function logout() {
        ['token', 'usuario_nome', 'usuario_vinculo', 'usuario_email'].forEach(
            key => localStorage.removeItem(key)
        );
        window.location.reload();
    }

    function configurarBotaoNovoTopico() {
        newTopicBtn.style.display = podecriarTopico() ? "inline-block" : "none";
    }

    async function fetchTopics() {
        try {
            const response = await fetch(API_URL);
            topics = await response.json();
            renderTopics(topics);
        } catch (error) {
            console.error("Erro ao buscar tópicos:", error);
        }
    }

    async function saveTopicToDatabase(newTopic) {
        if (!isLoggedIn()) {
            alert("Você precisa estar logado para criar um tópico.");
            return;
        }

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: getAuthHeaders(),
                body: JSON.stringify(newTopic)
            });

            if (response.status === 403) {
                alert("Apenas professores e pesquisadores podem criar tópicos.");
                return;
            }

            if (!response.ok) {
                const erro = await response.json();
                alert(erro.detail || "Erro ao criar tópico.");
                return;
            }

            fetchTopics();
        } catch (error) {
            console.error("Erro ao criar tópico:", error);
        }
    }

    async function deleteTopicFromDatabase(id) {
        if (!confirm("Tem certeza que deseja deletar este tópico?")) return;

        try {
            const response = await fetch(`${API_URL}/${id}`, {
                method: 'DELETE',
                headers: getAuthHeaders()
            });

            if (response.status === 401) {
                alert("Sua sessão expirou. Faça login novamente.");
                return;
            }

            if (response.status === 403) {
                alert("Você não tem permissão para deletar este tópico.");
                return;
            }

            if (!response.ok) {
                const erro = await response.json();
                alert(erro.detail || "Erro ao deletar tópico.");
                return;
            }

            fetchTopics();
        } catch (error) {
            console.error("Erro ao deletar tópico:", error);
        }
    }

    async function sendVoteToDatabase(id, voteType) {
        if (!isLoggedIn()) {
            alert("Você precisa estar logado para votar.");
            return;
        }

        try {
            const response = await fetch(`${API_URL}/${id}/votar`, {
                method: 'PUT',
                headers: getAuthHeaders(),
                body: JSON.stringify({ type: voteType })
            });

            if (response.status === 401) {
                alert("Sua sessão expirou. Faça login novamente.");
                return;
            }

            if (!response.ok) {
                const erro = await response.json();
                alert(erro.detail || "Erro ao computar voto.");
                return;
            }

            fetchTopics();
        } catch (error) {
            console.error("Erro ao computar voto:", error);
        }
    }

    function renderTopics(list) {
        topicsList.innerHTML = "";
        const emailAtual = getEmail();

        list.forEach(t => {
            const isAutor = isLoggedIn() && t.autor_email === emailAtual;

            const topicDiv = document.createElement("div");
            topicDiv.classList.add("topic");
            topicDiv.innerHTML = `
                <div class="topic-header">
                    <h3>${t.titulo}</h3>
                    ${isAutor ? `<button class="btn-delete" data-id="${t.id}" title="Deletar tópico">🗑️</button>` : ""}
                </div>
                <div class="topic-footer">
                    <span class="topic-info">
                        <strong>Autor:</strong> ${t.autor_email} · ${t.visualizacoes} visualizações
                    </span>
                    <div class="voting">
                        <button class="btn-vote like" data-id="${t.id}" data-type="like">👍 ${t.likes}</button>
                        <button class="btn-vote dislike" data-id="${t.id}" data-type="dislike">👎 ${t.dislikes}</button>
                    </div>
                </div>
            `;
            topicsList.appendChild(topicDiv);
        });
    }

    function createNewTopic() {
        const titulo = prompt("Digite o título do novo tópico:");
        if (!titulo || titulo.trim() === "") return;

        saveTopicToDatabase({ titulo: titulo.trim() });
        searchInput.value = "";
    }

    function searchTopics(event) {
        const value = event.target.value.toLowerCase();
        const filtered = topics.filter(t => t.titulo.toLowerCase().includes(value));
        renderTopics(filtered);
    }

    function handleClick(event) {
        const voteBtn = event.target.closest(".btn-vote");
        if (voteBtn) {
            sendVoteToDatabase(voteBtn.getAttribute("data-id"), voteBtn.getAttribute("data-type"));
            return;
        }

        const deleteBtn = event.target.closest(".btn-delete");
        if (deleteBtn) {
            deleteTopicFromDatabase(deleteBtn.getAttribute("data-id"));
        }
    }

    inicializarNavbar();
    configurarBotaoNovoTopico();
    fetchTopics();

    newTopicBtn.addEventListener("click", createNewTopic);
    searchInput.addEventListener("input", searchTopics);
    topicsList.addEventListener("click", handleClick);

});