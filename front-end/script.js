document.getElementById('formArtigo').addEventListener('submit', async function (event) {
    event.preventDefault();

    const tema = document.getElementById('tema').value;
    const publicoAlvo = document.getElementById('publico_alvo').value;

    try {
        const response = await fetch('http://localhost:5000/criar-artigo', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                tema: tema,
                publico_alvo: publicoAlvo
            }),
        });

        const data = await response.json();

        if (response.ok) {
            const artigoTexto = document.getElementById('artigoTexto');

            // Formatar quebras de linha e negrito (**texto**)
            const textoFormatado = data.artigo
                .split('\n') // Divide o texto em linhas
                .map(paragrafo => {
                    // Aplica negrito aos trechos cercados por **
                    const paragrafoFormatado = paragrafo.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
                    return `<p>${paragrafoFormatado}</p>`; // Retorna o parágrafo formatado
                })
                .join(''); // Junta tudo de volta como HTML
            
            artigoTexto.innerHTML = textoFormatado;
            document.getElementById('resultado').classList.remove('hidden');
        } else {
            alert(data.erro || 'Erro ao criar o artigo.');
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao conectar com o servidor.');
    }
});
