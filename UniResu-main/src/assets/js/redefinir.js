const API_BASE_URL = 'http://127.0.0.1:8000';

        const params = new URLSearchParams(window.location.search);
        const token = params.get('token');

        if (!token) {
            document.querySelector('.auth-box').innerHTML = `
                <p class="msg-feedback msg-error">Link inválido ou expirado.</p>
                <a href="./esqueci-senha.html" class="auth-link">Solicitar novo link</a>
            `;
        }

        document.getElementById('form-redefinir').addEventListener('submit', async (e) => {
            e.preventDefault();

            const senha = document.getElementById('input-senha').value;
            const confirmar = document.getElementById('input-confirmar').value;
            const btn = document.getElementById('btn-redefinir');
            const msg = document.getElementById('msg-feedback');

            if (senha !== confirmar) {
                msg.style.display = 'block';
                msg.className = 'msg-feedback msg-error';
                msg.textContent = 'As senhas não coincidem.';
                return;
            }

            btn.textContent = 'Redefinindo...';
            btn.disabled = true;

            try {
                const response = await fetch(`${API_BASE_URL}/api/auth/redefinir-senha`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ token, nova_senha: senha })
                });

                const data = await response.json();
                msg.style.display = 'block';

                if (response.ok) {
                    msg.className = 'msg-feedback msg-success';
                    msg.textContent = 'Senha redefinida com sucesso! Redirecionando...';
                    document.getElementById('form-redefinir').style.display = 'none';
                    setTimeout(() => window.location.href = './login.html', 2500);
                } else {
                    msg.className = 'msg-feedback msg-error';
                    msg.textContent = data.detail || 'Token inválido ou expirado.';
                }
            } catch (err) {
                msg.style.display = 'block';
                msg.className = 'msg-feedback msg-error';
                msg.textContent = 'Erro de conexão com o servidor.';
            } finally {
                btn.textContent = 'Redefinir senha';
                btn.disabled = false;
            }
        });