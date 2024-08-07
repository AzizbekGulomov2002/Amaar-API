document.addEventListener('DOMContentLoaded', function () {
    console.log("Document is ready");

    const sellerTypeField = document.querySelector('#id_seller_type');
    const personalFields = document.querySelectorAll('.personal-fields');
    const yattFields = document.querySelectorAll('.ytt-fields');
    const mchjFields = document.querySelectorAll('.mchj-fields');

    function toggleFields() {
        const selectedType = sellerTypeField ? sellerTypeField.value : '';
        console.log("Seller type selected:", selectedType);

        if (selectedType === 'personal') {
            console.log("Showing personal seller fields");
            personalFields.forEach(field => field.style.display = 'block');
            yattFields.forEach(field => field.style.display = 'none');
            mchjFields.forEach(field => field.style.display = 'none');
        } else if (selectedType === 'yatt') {
            console.log("Showing YATT seller fields");
            personalFields.forEach(field => field.style.display = 'none');
            yattFields.forEach(field => field.style.display = 'block');
            mchjFields.forEach(field => field.style.display = 'none');
        } else if (selectedType === 'mchj') {
            console.log("Showing MCHJ seller fields");
            personalFields.forEach(field => field.style.display = 'none');
            yattFields.forEach(field => field.style.display = 'none');
            mchjFields.forEach(field => field.style.display = 'block');
        } else {
            console.log("Hiding all specific seller fields");
            personalFields.forEach(field => field.style.display = 'none');
            yattFields.forEach(field => field.style.display = 'none');
            mchjFields.forEach(field => field.style.display = 'none');
        }
    }

    // Initialize field visibility
    toggleFields();

    // Add event listener to the seller_type field to update visibility on change
    if (sellerTypeField) {
        sellerTypeField.addEventListener('change', toggleFields);
    }
});
