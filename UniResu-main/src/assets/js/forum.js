document.addEventListener('DOMContentLoaded', () => {

    const CONFIG = {
        API_URL: 'https://uniresu-connect.onrender.com/api/forum',
        VINCULOS_PERMITIDOS: ["professor", "pesquisador"]
    };

    const DOM = {
        topicsList: document.getElementById("topicsList"),
        searchInput: document.getElementById("searchInput"),
        newTopicBtn: document.getElementById("newTopicBtn"),
        areaUsuario: document.getElementById("area-usuario"),

        modal: {
            overlay: document.getElementById("modalNovoTopico"),
            closeBtn: document.getElementById("closeModalBtn"),
            submitBtn: document.getElementById("btnPublicarTopico"),
            inputTitulo: document.getElementById("tituloTopico"),
            inputDescricao: document.getElementById("descricaoTopico")
        }
    };

    const State = {
        topics: [],
        user: {
            getToken: () => localStorage.getItem('token'),
            getNome: () => localStorage.getItem('usuario_nome'),
            getVinculo: () => localStorage.getItem('usuario_vinculo') || "",
            getEmail: () => localStorage.getItem('usuario_email') || "",
            isLoggedIn: () => !!localStorage.getItem('token'),
            canCreateTopic: function () {
                return CONFIG.VINCULOS_PERMITIDOS.includes(this.getVinculo().toLowerCase());
            }
        },

        votes: JSON.parse(localStorage.getItem('forum_votes') || '{}'),
        saveVotes() {
            localStorage.setItem('forum_votes', JSON.stringify(this.votes));
        },
        getUserVote(topicId) {
            return this.votes[topicId] || null;
        },
        setUserVote(topicId, type) {
            this.votes[topicId] = type;
            this.saveVotes();
        }
    };

    const ApiService = {
        getHeaders: () => ({
            "Content-Type": "application/json",
            ...(State.user.isLoggedIn() ? { "Authorization": `Bearer ${State.user.getToken()}` } : {})
        }),

        async fetchTopics() {
            try {
                const response = await fetch(CONFIG.API_URL);
                if (!response.ok) throw new Error("Erro ao buscar dados");
                State.topics = await response.json();
                Renderer.renderTopics(State.topics);
            } catch (error) {
                console.error("Erro na busca de tópicos:", error);
            }
        },

        async createTopic(payload) {
            try {
                const response = await fetch(CONFIG.API_URL, {
                    method: 'POST',
                    headers: this.getHeaders(),
                    body: JSON.stringify(payload)
                });

                if (response.status === 403) return alert("Apenas professores e pesquisadores podem criar tópicos.");
                if (!response.ok) throw await response.json();

                this.fetchTopics();
            } catch (error) {
                alert(error.detail || "Erro ao criar tópico.");
            }
        },

        async deleteTopic(id) {
            try {
                const response = await fetch(`${CONFIG.API_URL}/${id}`, {
                    method: 'DELETE',
                    headers: this.getHeaders()
                });

                if (response.status === 401) return alert("Sua sessão expirou. Faça login novamente.");
                if (response.status === 403) return alert("Você não tem permissão para deletar este tópico.");
                if (!response.ok) throw await response.json();

                this.fetchTopics();
            } catch (error) {
                alert(error.detail || "Erro ao deletar tópico.");
            }
        },

        async voteTopic(id, voteType) {
            try {
                const response = await fetch(`${CONFIG.API_URL}/${id}/votar`, {
                    method: 'PUT',
                    headers: this.getHeaders(),
                    body: JSON.stringify({ type: voteType })
                });

                if (response.status === 401) return alert("Sua sessão expirou. Faça login novamente.");
                if (!response.ok) throw await response.json();

                State.setUserVote(id, voteType);
                this.fetchTopics();
            } catch (error) {
                alert(error.detail || "Erro ao computar voto.");
            }
        }
    };

    const Renderer = {
        initNavbar() {
            if (!State.user.isLoggedIn() || !State.user.getNome()) return;

            DOM.areaUsuario.innerHTML = `
                <div class="user-menu" id="userMenu">
                    <span class="user-trigger">Olá, ${State.user.getNome()} ▾</span>
                    <div class="dropdown">
                        <a href="#" id="btnLogout">Sair</a>
                    </div>
                </div>
            `;

            document.getElementById('btnLogout').addEventListener('click', Handlers.handleLogout);

            const menu = document.getElementById('userMenu');
            menu.addEventListener('click', (e) => {
                e.stopPropagation();
                menu.classList.toggle('is-open');
            });

            document.addEventListener('click', () => menu.classList.remove('is-open'));
        },

        initTopicButton() {
            if (State.user.canCreateTopic()) {
                DOM.newTopicBtn.classList.remove('is-hidden');
            }
        },

        renderTopics(list) {
            DOM.topicsList.innerHTML = "";
            const currentEmail = State.user.getEmail();

            list.forEach(topic => {
                const isAuthor = State.user.isLoggedIn() && topic.autor_email === currentEmail;
                const userVoteLocal = State.getUserVote(topic.id);
                const userLiked   = topic.user_liked   ?? (userVoteLocal === 'like');
                const userDisliked = topic.user_disliked ?? (userVoteLocal === 'dislike');
                const likeClass    = userLiked    ? 'is-liked'    : '';
                const dislikeClass = userDisliked ? 'is-disliked' : '';
                const likeDisabled    = userDisliked ? 'disabled' : '';
                const dislikeDisabled = userLiked    ? 'disabled' : '';

                const topicCard = document.createElement("article");
                topicCard.classList.add("topic-card");

                topicCard.innerHTML = `
                    <header class="topic-header">
                        <h3 class="topic-title">${topic.titulo}</h3>
                    </header>
                    <p class="topic-description">${topic.descricao || "Sem descrição..."}</p>
                    <footer class="topic-footer">
                        <div class="topic-meta">
                            <strong>Autor:</strong> ${topic.autor_email} · ${topic.visualizacoes || 0} visualizações
                        </div>
                        <div class="topic-actions">
                            <div class="voting-group">
                                <button
                                    class="btn btn-vote ${likeClass}"
                                    data-id="${topic.id}"
                                    data-type="like"
                                    ${likeDisabled}
                                    title="${userLiked ? 'Você já curtiu este tópico' : (userDisliked ? 'Remova o dislike para curtir' : 'Curtir')}">
                                    👍 ${topic.likes || 0}
                                </button>
                                <button
                                    class="btn btn-vote ${dislikeClass}"
                                    data-id="${topic.id}"
                                    data-type="dislike"
                                    ${dislikeDisabled}
                                    title="${userDisliked ? 'Você já descurtiu este tópico' : (userLiked ? 'Remova o like para descurtir' : 'Descurtir')}">
                                    👎 ${topic.dislikes || 0}
                                </button>
                            </div>
                            ${isAuthor ? `
                                <button class="btn btn-delete" data-id="${topic.id}">
                                    🗑 Deletar
                                </button>
                            ` : ""}
                        </div>
                    </footer>
                `;
                DOM.topicsList.appendChild(topicCard);
            });
        }
    };

    const Handlers = {
        handleLogout() {
            ['token', 'usuario_nome', 'usuario_vinculo', 'usuario_email'].forEach(key => localStorage.removeItem(key));
            window.location.reload();
        },

        handleSearch(event) {
            const query = event.target.value.toLowerCase();
            const filtered = State.topics.filter(t => t.titulo.toLowerCase().includes(query));
            Renderer.renderTopics(filtered);
        },

        handleTopicClick(event) {
            const voteBtn = event.target.closest(".btn-vote");
            if (voteBtn) {
                if (!State.user.isLoggedIn()) return alert("Você precisa estar logado para votar.");

                const topicId  = voteBtn.dataset.id;
                const voteType = voteBtn.dataset.type;
                const currentVote = State.getUserVote(topicId);

                if (currentVote !== null) {
                    if (currentVote === voteType) {
                        return alert(`Você já deu ${voteType === 'like' ? 'like' : 'dislike'} neste tópico.`);
                    } else {
                        return alert("Você já votou neste tópico e não pode mudar seu voto.");
                    }
                }

                return ApiService.voteTopic(topicId, voteType);
            }

            const deleteBtn = event.target.closest(".btn-delete");
            if (deleteBtn && confirm("Tem certeza que deseja deletar este tópico?")) {
                ApiService.deleteTopic(deleteBtn.dataset.id);
            }
        },

        openModal() {
            DOM.modal.overlay.classList.add("is-active");
        },

        closeModal() {
            DOM.modal.overlay.classList.remove("is-active");
            DOM.modal.inputTitulo.value = "";
            DOM.modal.inputDescricao.value = "";
        },

        submitModal() {
            const titulo    = DOM.modal.inputTitulo.value.trim();
            const descricao = DOM.modal.inputDescricao.value.trim();

            if (!titulo)    return alert("Por favor, preencha o título do tópico!");
            if (!descricao) return alert("Por favor, adicione uma descrição ao tópico!");

            ApiService.createTopic({ titulo, descricao });
            Handlers.closeModal();
        }
    };

    function init() {
        Renderer.initNavbar();
        Renderer.initTopicButton();
        ApiService.fetchTopics();

        DOM.searchInput.addEventListener("input", Handlers.handleSearch);
        DOM.topicsList.addEventListener("click", Handlers.handleTopicClick);
        DOM.newTopicBtn.addEventListener("click", Handlers.openModal);

        if (DOM.modal.closeBtn) DOM.modal.closeBtn.addEventListener("click", Handlers.closeModal);
        DOM.modal.submitBtn.addEventListener("click", Handlers.submitModal);

        window.addEventListener("click", (e) => {
            if (e.target === DOM.modal.overlay) Handlers.closeModal();
        });
    }

    init();
});
