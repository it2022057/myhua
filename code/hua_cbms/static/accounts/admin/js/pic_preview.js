document.addEventListener('DOMContentLoaded', function () {
    const img_preview = document.getElementById('pic-preview-img');
    const img_input = document.getElementById('id_pic');
    // The clear checkbox is generated when the ImageField already has a file
    const clear_checkbox = document.getElementById('pic-clear_id');

    if (!img_preview || !img_input) return;

    // Keep the originally saved image src, so that the script can restore it if the user unchecks "clear"
    const previous_src = img_preview.src;

    // Used to clean up temporary browser URLs when the user selects another file
    let temporary_url = null;

    // Clear the file input on page load
    // This prevents the browser from keeping a selected file after refresh/back navigation
    img_input.value = '';

    // Listen for changes on the file input.
    img_input.addEventListener('change', function () {
        const file = img_input.files && img_input.files[0];

        // If the user opened the file picker but did not select a file, do nothing
        if (!file) return;

        // If the selected file is not an image, hide the preview
        if (!file.type.startsWith('image/')) {
            img_preview.removeAttribute('src');
            img_preview.style.display = 'none';
            return;
        }

        // Remove the previous temporary URL from memory, if there is one
        if (temporary_url) {
            URL.revokeObjectURL(temporary_url);
        }

        // Create a temporary browser URL for the selected local image
        // This is only for preview before saving
        temporary_url = URL.createObjectURL(file);

        // Show the selected image immediately
        img_preview.src = temporary_url;
        img_preview.style.display = 'inline-block';

        // If the clear checkbox was checked, uncheck it because the user selected a new image.
        if (clear_checkbox) {
            clear_checkbox.checked = false;
        }
    });

    // Listen for changes on the clear checkbox, if it exists.
    if (clear_checkbox) {
        clear_checkbox.addEventListener('change', function () {
            if (clear_checkbox.checked) {
                // If the user wants to clear the image, hide the preview and clear the input
                img_preview.removeAttribute('src');
                img_preview.style.display = 'none';
                img_input.value = '';
            } else {
                // If the user unchecks clear, restore the previously saved image
                img_preview.src = previous_src;
                img_preview.style.display = 'inline-block';
            }
        });
    }
});