(function($) {
    $(document).ready(function() {
        function toggleBusinessFields() {
            if ($('#id_user_type').val() === 'BUSINESS') {
                $('.business-fields').show();
            } else {
                // Caso contrário, esconde
                $('.business-fields').hide();
            }
        }

        toggleBusinessFields();
        $('#id_user_type').change(function() {
            toggleBusinessFields();
        });
    });
})(django.jQuery);