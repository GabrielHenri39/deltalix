$(function () {
    $(".cep").mask("00000-000");
    var SPMaskBehavior = function (val) {
        return val.replace(/\D/g, '').length === 11 ? '(00) 00000-0000' : '(00) 0000-00009';
    },
    spOptions = {
        onKeyPress: function(val, e, field, options) {
            field.mask(SPMaskBehavior.apply({}, arguments), options);
        }
    };
    $('.tel').mask(SPMaskBehavior, spOptions);
    var protoMaskBehavior = function(val) {
            // Remove tudo que não seja número
            var numbers = val.replace(/\D/g, '');

            // Se tiver menos de 4 números, não coloca hífen
            if(numbers.length <= 4) {
                return 'PROTO-0000000000000000000'; // ajusta com zeros pra máscara
            }

            // Máscara dinâmica: coloca hífen antes dos últimos 4 dígitos
            return 'PROTO-00000000000000000000-0000';
        };

        var protoOptions = {
            onKeyPress: function(val, e, field, options) {
                field.mask(protoMaskBehavior.apply({}, arguments), options);
            }
        };

    $('.proto').mask(protoMaskBehavior, protoOptions);
    }
)