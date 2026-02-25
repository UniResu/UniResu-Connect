document.querySelector('.login-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.getElementById('email').value.trim().toLowerCase();
    const senha = document.getElementById('senha').value;

    try {
        const response = await fetch('http://127.0.0.1:8000/api/usuarios/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, senha })
        });

        const data = await response.json();

        if (!response.ok) {
            if (response.status === 422) {
                console.error('Erro de validação:', data.detail);
                alert('Dados inválidos. Verifique o preenchimento.');
            } else {
                alert(data.detail || 'Erro ao fazer login.');
            }
            return;
        }

        localStorage.setItem('token', data.access_token);
        localStorage.setItem('usuario_nome', data.nome);
        localStorage.setItem('usuario_email', data.email);
        localStorage.setItem('usuario_vinculo', data.vinculo);
        window.location.href = './projetos.html';

    } catch (err) {
        console.error('Erro no fetch:', err);
        alert('Erro de conexão! Verifique se o servidor está rodando.');
    }
});