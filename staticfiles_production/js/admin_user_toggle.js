(function($) {
    $(document).ready(function() {
        function toggleUserFields() {
            const userType = $('#id_user_type').val();

            if (userType === 'BUSINESS') {
                $('.business-fields').show();
                $('.licensee-fields').hide();
                $('.field-user_permissions').show(); // Mostra permissões individuais
                $('.permissions-fields').find('label[for="id_user_permissions"]').parent().show();
            } else if (userType === 'LICENSEE') {
                $('.business-fields').hide();
                $('.licensee-fields').show();
                $('.field-user_permissions').hide(); // Esconde permissões individuais
                $('.permissions-fields').find('label[for="id_user_permissions"]').parent().hide();
            } else {
                $('.business-fields').hide();
                $('.licensee-fields').hide();
                $('.field-user_permissions').show();
                $('.permissions-fields').find('label[for="id_user_permissions"]').parent().show();
            }
        }

        toggleUserFields();

        $('#id_user_type').change(function() {
            toggleUserFields();
        });
    });
})(django.jQuery);
