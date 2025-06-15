document.addEventListener('DOMContentLoaded', function() {
    const telefoneInput = document.getElementById('telefone');

    if (telefoneInput) { // Verifica se o campo de telefone existe na página
        telefoneInput.addEventListener('input', function (e) {
            let value = e.target.value.replace(/\D/g, ''); // Remove tudo que não é dígito
            let formattedValue = '';

            // Limite de 11 dígitos para DDD + 9 dígitos (celular) ou 8 dígitos (fixo)
            if (value.length > 11) {
                value = value.substring(0, 11);
            }

            if (value.length > 0) {
                formattedValue += '(' + value.substring(0, 2); // (DD
            }
            if (value.length > 2) {
                formattedValue += ') ' + value.substring(2, 7); // ) XXXXX
            }
            if (value.length > 7) {
                formattedValue += '-' + value.substring(7, 11); // -XXXX
            }

            e.target.value = formattedValue;
        });
    }
});