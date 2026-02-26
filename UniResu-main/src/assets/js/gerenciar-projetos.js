const API_BASE_URL = 'https://uniresu-connect.onrender.com';
const token = localStorage.getItem('token');
const nome = localStorage.getItem('usuario_nome');
const vinculo = localStorage.getItem('usuario_vinculo');

if (!token || (vinculo !== 'professor' && vinculo !== 'pesquisador')) {
    alert('Acesso restrito a professores e pesquisadores.');
    window.location.href = './projetos.html';
}

document.getElementById('area-usuario').innerHTML = `
    <div class="user-menu">
        <span class="user-trigger">Olá, ${nome} <span class="arrow">▾</span></span>
        <div class="dropdown">
            <a href="./gerenciar-projetos.html">Gerenciar Projetos</a>
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

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('usuario_nome');
    localStorage.removeItem('usuario_vinculo');
    window.location.href = './projetos.html';
}

let projetoEditandoId = null;

document.getElementById('btn-novo-projeto').addEventListener('click', () => {
    projetoEditandoId = null;
    document.getElementById('form-titulo-label').textContent = 'Novo Projeto';
    document.getElementById('form-projeto').reset();
    document.getElementById('form-container').style.display = 'block';
});

document.getElementById('btn-cancelar').addEventListener('click', () => {
    document.getElementById('form-container').style.display = 'none';
    projetoEditandoId = null;
});

document.getElementById('form-projeto').addEventListener('submit', async (e) => {
    e.preventDefault();

    const payload = {
        titulo: document.getElementById('proj-titulo').value,
        descricao: document.getElementById('proj-descricao').value,
        instituicao: document.getElementById('proj-instituicao').value,
        local: document.getElementById('proj-local').value,
        area_estudo: document.getElementById('proj-area').value,
        tipo_projeto: document.getElementById('proj-tipo').value,
        nome_professor: document.getElementById('proj-nome-professor').value,
        email_professor: document.getElementById('proj-email-professor').value,
        modalidade: document.getElementById('proj-modalidade').value
    };

    const url = projetoEditandoId
        ? `${API_BASE_URL}/api/projetos/${projetoEditandoId}`
        : `${API_BASE_URL}/api/projetos/criar`;
    const method = projetoEditandoId ? 'PUT' : 'POST';

    try {
        const response = await fetch(url, {
            method,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        if (!response.ok) throw new Error(data.detail);

        alert(projetoEditandoId ? 'Projeto atualizado!' : 'Projeto criado com sucesso!');
        document.getElementById('form-container').style.display = 'none';
        carregarMeusProjetos();
    } catch (err) {
        alert(`Erro: ${err.message}`);
    }
});

async function carregarMeusProjetos() {
    const container = document.getElementById('lista-meus-projetos');
    container.innerHTML = '<p>Carregando...</p>';

    try {
        const response = await fetch(`${API_BASE_URL}/api/projetos/buscar`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const projetos = await response.json();
        const email = JSON.parse(atob(token.split('.')[1])).sub;
        const meusProjetos = projetos.filter(p => p.email_professor === email);

        if (meusProjetos.length === 0) {
            container.innerHTML = '<p>Você ainda não cadastrou nenhum projeto.</p>';
            return;
        }

        container.innerHTML = '';
        meusProjetos.forEach(projeto => {
            const card = document.createElement('div');
            card.className = 'project-card';
            card.innerHTML = `
                <div class="project-info">
                    <h3>${projeto.titulo}</h3>
                    <p>${projeto.descricao}</p>
                </div>
                <div class="project-meta">
                    <span class="institution">${projeto.instituicao || ''}</span>
                    <span class="type">${projeto.tipo || ''}</span>
                    <div style="display:flex; gap:8px; margin-top:8px;">
                        <button onclick="editarProjeto('${projeto.id}')" 
                            style="padding:6px 16px; background:#6a0dad; color:#fff; border:none; border-radius:6px; cursor:pointer;">
                            Editar
                        </button>
                        <button onclick="excluirProjeto('${projeto.id}')" 
                            style="padding:6px 16px; background:#e53935; color:#fff; border:none; border-radius:6px; cursor:pointer;">
                            Excluir
                        </button>
                    </div>
                </div>
            `;
            container.appendChild(card);
        });
    } catch (err) {
        container.innerHTML = '<p class="error">Erro ao carregar projetos.</p>';
    }
}

function editarProjeto(id) {
    fetch(`${API_BASE_URL}/api/projetos/buscar`)
        .then(r => r.json())
        .then(projetos => {
            const projeto = projetos.find(p => p.id === id);
            if (!projeto) return;

            projetoEditandoId = id;
            document.getElementById('form-titulo-label').textContent = 'Editar Projeto';
            document.getElementById('proj-titulo').value = projeto.titulo || '';
            document.getElementById('proj-descricao').value = projeto.descricao || '';
            document.getElementById('proj-instituicao').value = projeto.instituicao || '';
            document.getElementById('proj-local').value = projeto.local || '';
            document.getElementById('proj-area').value = projeto.area_estudo || '';
            document.getElementById('proj-tipo').value = projeto.tipo_projeto || '';
            document.getElementById('proj-nome-professor').value = projeto.nome_professor || '';
            document.getElementById('proj-email-professor').value = projeto.email_professor || '';
            document.getElementById('proj-modalidade').value = projeto.modalidade || 'presencial';
            document.getElementById('form-container').style.display = 'block';
            window.scrollTo(0, 0);
        });
}

async function excluirProjeto(id) {
    const confirmar = confirm('Tem certeza que deseja excluir este projeto? Esta ação não pode ser desfeita.');
    if (!confirmar) return;

    try {
        const response = await fetch(`${API_BASE_URL}/api/projetos/${id}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || 'Erro ao excluir o projeto.');
        }

        alert('Projeto excluído com sucesso!');
        carregarMeusProjetos(); 

    } catch (err) {
        console.error('Erro ao excluir:', err);
        alert(`Erro: ${err.message}`);
    }
}
