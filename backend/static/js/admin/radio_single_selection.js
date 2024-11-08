document.addEventListener('DOMContentLoaded', function () {
    // Initialize Select2 and set up change listener
    const selectElement = document.querySelector('#id_question_type');
    if (selectElement) {
        $(selectElement).select2().on('change', handleSelectChange);

        // Initial call to set correct options based on initial selection
        handleSelectChange({ target: selectElement });
    }

    // Function to handle change events for the question type select element
    function handleSelectChange(event) {
        const selectedValue = event.target.value;
        console.log('Selected value:', selectedValue);

        if (selectedValue === '2') { // Assuming '2' is True/False
            clickRemoveLastTwoOptions();
        } else if (selectedValue === '1') { // Assuming '1' is Multiple Choice
            removeAllOptions();
            for (let i = 0; i < 4; i++) {
                addOptionRow(`Option ${i + 1}`);
            }
        }
    }

    // Container for inline options, ensure this selector matches your structure
    const radioButtonContainer = document.querySelector('.tabular.inline-related');

    // Function to add radio button single-selection behavior
    function applySingleSelection() {
        const radioButtons = document.querySelectorAll('input[type="radio"][name$="-is_answer"]');
        radioButtons.forEach(radio => {
            radio.addEventListener('change', function () {
                radioButtons.forEach(btn => {
                    if (btn !== this) btn.checked = false;
                });
            });
        });
    }

    // Function to remove all existing option rows
    function removeAllOptions() {
        const optionRows = document.querySelectorAll('.dynamic-question_options');
        optionRows.forEach(row => row.remove());
    }
    
    // Function to add a new option row with specified text
    function addOptionRow(text) {
        const addButton = document.querySelector('.add-row a');
        if (addButton) addButton.click(); // Adds a new inline row

        const lastRow = document.querySelectorAll('.dynamic-question_options').item(-1);
        if (lastRow) {
            const optionTextInput = lastRow.querySelector('input[name$="-text"]'); // Adjust if needed
            if (optionTextInput) optionTextInput.value = text;
        }
    }
    function clickRemoveLastTwoOptions() {
        const optionRows = document.querySelectorAll('.dynamic-question_options');
        const rowsToRemove = Array.from(optionRows).slice(-2);
        
        rowsToRemove.forEach(row => {
            const removeButton = row.querySelector('.inline-deletelink');
            if (removeButton) {
                removeButton.click();
            }
        });
    }
    // Initial application for single-selection on load
    applySingleSelection();

    // MutationObserver to detect added rows in TabularInline
    const observer = new MutationObserver(mutations => {
        mutations.forEach(mutation => {
            if (mutation.addedNodes.length > 0) {
                applySingleSelection(); // Apply single selection on new rows
            }
        });
    });

    // Start observing the radio button container for dynamically added rows
    if (radioButtonContainer) {
        observer.observe(radioButtonContainer, { childList: true, subtree: true });
    }
    const event = new Event('change');
    // Dispatch the event on the select element
    selectElement.dispatchEvent(event);
});
