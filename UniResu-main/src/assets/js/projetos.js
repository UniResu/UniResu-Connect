document.addEventListener('DOMContentLoaded', () => {

    const API_BASE_URL = 'http://127.0.0.1:8000';
    const searchForm = document.getElementById('form-busca');
    const projectListContainer = document.getElementById('lista-projetos');
    const token = localStorage.getItem('token');
    const nomeAluno = localStorage.getItem('usuario_nome');

    loadInitialProjects();

    if (searchForm) {
        searchForm.addEventListener('submit', handleSearch);
    }

    async function handleSearch(event) {
        event.preventDefault();
        const buscar = document.getElementById('input-buscar').value;
        const local = document.getElementById('input-local').value;
        const area = document.getElementById('select-area').value;
        
        // AJUSTE AQUI: Verifica se o checkbox de remoto está marcado
        const apenasRemoto = document.getElementById('check-remoto').checked;
        
        const tipoCheckboxes = document.querySelectorAll('input[name="tipo_projeto"]:checked');
        const tipos = Array.from(tipoCheckboxes).map(cb => cb.value);

        const params = new URLSearchParams();
        if (buscar) params.append('q', buscar);
        if (local) params.append('local', local);
        if (area) params.append('area', area);
        
        // AJUSTE AQUI: Se estiver marcado, envia a string 'remoto' para bater com o novo controller
        if (apenasRemoto) params.append('modalidade', 'remoto');
        
        if (tipos.length > 0) params.append('tipos', tipos.join(','));

        fetchAndRenderProjects(`${API_BASE_URL}/api/projetos/buscar?${params.toString()}`);
    }

    async function loadInitialProjects() {
        fetchAndRenderProjects(`${API_BASE_URL}/api/projetos/buscar`);
    }

    async function fetchAndRenderProjects(apiUrl) {
        try {
            projectListContainer.innerHTML = '<p>Carregando projetos...</p>';
            const response = await fetch(apiUrl);
            if (!response.ok) throw new Error(`Erro na rede: ${response.statusText}`);
            const projetos = await response.json();
            renderProjects(projetos);
        } catch (error) {
            projectListContainer.innerHTML = '<p class="error">Erro ao carregar projetos.</p>';
        }
    }

    function renderProjects(projects) {
        projectListContainer.innerHTML = '';
        if (!projects || projects.length === 0) {
            projectListContainer.innerHTML = '<p>Nenhum projeto encontrado.</p>';
            return;
        }

        projects.forEach(project => {
            const card = document.createElement('div');
            card.className = 'project-card';
            if (token) card.style.cursor = 'pointer';

            card.innerHTML = `
                <div class="project-info">
                    <h3>${project.titulo || 'Título não disponível'}</h3>
                    <p>${project.descricao || 'Sem descrição.'}</p>
                </div>
                <div class="project-meta">
                    <span class="institution">${project.instituicao || ''}</span>
                    <span class="type">${project.tipo || ''}</span>
                    <span class="date">${project.dataPublicacao || ''}</span>
                </div>
            `;

            if (token) {
                card.addEventListener('click', () => abrirModal(project));
            }

            projectListContainer.appendChild(card);
        });
    }

    function abrirModal(project) {
        document.getElementById('modal-titulo').textContent = project.titulo || '';
        document.getElementById('modal-descricao').textContent = project.descricao || '';
        document.getElementById('modal-instituicao').textContent = project.instituicao || '';
        document.getElementById('modal-professor').textContent = project.nome_professor || 'Não informado';
        document.getElementById('modal-tipo').textContent = project.tipo || '';

        // MAPEAMENTO: Transforma o valor do banco em texto amigável
        const modalidades = { presencial: 'Presencial', hibrido: 'Híbrido', remoto: 'Remoto' };
        const modalidadeTexto = modalidades[project.modalidade] || project.modalidade || 'Não informado';

        // INJEÇÃO: Preenche o campo que estava ficando vazio
        document.getElementById('modal-modalidade').textContent = modalidadeTexto;
        document.getElementById('modal-local').textContent = project.local || 'Rio de Janeiro'; 

        const form = document.getElementById('form-candidatura');
        form.onsubmit = (e) => enviarCandidatura(e, project);

        document.getElementById('modal-projeto').style.display = 'flex';
    }

    document.getElementById('modal-fechar').addEventListener('click', () => {
        document.getElementById('modal-projeto').style.display = 'none';
    });

    window.addEventListener('click', (e) => {
        if (e.target === document.getElementById('modal-projeto')) {
            document.getElementById('modal-projeto').style.display = 'none';
        }
    });

    async function enviarCandidatura(e, project) {
        e.preventDefault();
        const emailAluno = document.getElementById('candidatura-email').value;
        const curriculo = document.getElementById('candidatura-curriculo').files[0];

        if (!curriculo) {
            alert('Por favor, anexe seu currículo.');
            return;
        }

        const formData = new FormData();
        formData.append('email_professor', project.email_professor);
        formData.append('nome_professor', project.nome_professor || 'Professor');
        formData.append('titulo_projeto', project.titulo);
        formData.append('nome_aluno', nomeAluno || 'Aluno');
        formData.append('email_aluno', emailAluno);
        formData.append('curriculo', curriculo);

        const btnEnviar = document.getElementById('btn-candidatar');
        btnEnviar.textContent = 'Enviando...';
        btnEnviar.disabled = true;

        try {
            const response = await fetch(`${API_BASE_URL}/api/projetos/candidatar`, {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.detail);

            alert('Candidatura enviada com sucesso!');
            document.getElementById('modal-projeto').style.display = 'none';
            document.getElementById('form-candidatura').reset();
        } catch (err) {
            alert(`Erro ao enviar candidatura: ${err.message}`);
        } finally {
            btnEnviar.textContent = 'Candidatar-se';
            btnEnviar.disabled = false;
        }
    }
});