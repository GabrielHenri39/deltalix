document.addEventListener('DOMContentLoaded', function () {
    const cepInput = document.getElementById('id_cep');
    if (cepInput) {
        cepInput.addEventListener('blur', buscarEndereco);
    }

    function buscarEndereco() {
        const cep = cepInput.value.replace(/\D/g, '');
        if (!cep) {
            alert('CEP não informado');
            return;
        }
        if (!/^\d{8}$/.test(cep)) {
            alert('CEP inválido');
            return;
        }

        const url = `https://viacep.com.br/ws/${cep}/json/`;

        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao buscar o endereço');
                }
                return response.json();
            })
            .then(data => {
                if (data.erro) {
                    throw new Error('CEP não encontrado');
                }
                document.getElementById('id_rua').value = data.logradouro || '';
                document.getElementById('id_bairro').value = data.bairro || '';
                document.getElementById('id_cidade').value = data.localidade || '';
            })
            .catch(error => {
                console.error('Erro ao buscar o endereço:', error);
                alert('Erro ao buscar o endereço: ' + error.message);
            });
    }
});