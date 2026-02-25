const API_BASE_URL = 'http://127.0.0.1:8000';

document.getElementById('form-esqueci').addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.getElementById('input-email').value;
    const btn = document.getElementById('btn-enviar');
    const msg = document.getElementById('msg-feedback');

    btn.textContent = 'Enviando...';
    btn.disabled = true;

    try {
        const response = await fetch(`${API_BASE_URL}/api/auth/esqueci-senha`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email })
        });

        const data = await response.json();

        msg.style.display = 'block';

        if (response.ok) {
            msg.className = 'msg-feedback msg-success';
            msg.textContent = 'Link enviado! Verifique seu e-mail.';
            document.getElementById('form-esqueci').reset();
        } else {
            msg.className = 'msg-feedback msg-error';
            msg.textContent = data.detail || 'Erro ao enviar e-mail.';
        }
    } catch (err) {
        msg.style.display = 'block';
        msg.className = 'msg-feedback msg-error';
        msg.textContent = 'Erro de conexão com o servidor.';
    } finally {
        btn.textContent = 'Enviar link';
        btn.disabled = false;
    }
});