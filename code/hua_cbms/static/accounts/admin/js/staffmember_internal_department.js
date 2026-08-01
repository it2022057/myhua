(function($) {
    $(function() {
        // Cache the related form elements
        const isInternalField = $('#id_is_internal');
        const internalDepartmentField = $('#id_internal_department');
        const internalDepartmentRow = $('.form-row.field-internal_department');

        // Return whether the user is marked as internal
        function isInternalSelected() {
            if (isInternalField.attr('type') === 'checkbox') {
                return isInternalField.is(':checked');
            }

            const value = String(isInternalField.val()).toLowerCase();

            return value === 'true' || value === '1' || value === 'yes' || value === 'on';
        }

        // Show or hide the internal department field
        function toggleInternalDepartment() {
            if (isInternalSelected()) {
                // Enable and display the field
                internalDepartmentRow.show();
                internalDepartmentField.prop('disabled', false);
            } else {
                // Clear, disable and hide the field
                internalDepartmentField.val('');
                internalDepartmentField.trigger('change');
                internalDepartmentField.prop('disabled', true);
                internalDepartmentRow.hide();
            }
        }

        // Update the field whenever the value changes
        isInternalField.on('change', toggleInternalDepartment);

        // Apply the correct state on page load
        toggleInternalDepartment();
    });
})(django.jQuery);