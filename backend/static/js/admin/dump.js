// static/js/single_radio_selection.js
document.addEventListener('DOMContentLoaded', function () {
    const radioButtonContainer = document.querySelector('.tabular.inline-related'); // Replace with the container's actual ID

    // Function to add event listeners to radio buttons
    function applySingleSelection() {
        const radioButtons = document.querySelectorAll('input[type="radio"][name$="-is_answer"]');
        radioButtons.forEach(radio => {
            radio.addEventListener('change', function () {
                // Unselect all other radio buttons in the same inline group when one is selected
                radioButtons.forEach(btn => {
                    if (btn !== this) {
                        btn.checked = false;
                    }
                });
            });
        });
    }

    // Initial application for existing rows
    applySingleSelection();

    // Mutation observer to detect added rows
    const observer = new MutationObserver(mutations => {
        for (let mutation of mutations) {
            if (mutation.addedNodes.length > 0) {
                applySingleSelection(); // Reapply selection to handle the new row
            }
        }
    });

    // Start observing the container for added nodes
    if (radioButtonContainer) {
        observer.observe(radioButtonContainer, { childList: true, subtree: true });
    }

    const questionTypeSelect = document.querySelector('#id_question_type'); // Update with the actual ID for question type
    console.log(questionTypeSelect)
    // Helper function to remove all rows in the TabularInline
    function removeAllOptions() {
        const optionRows = document.querySelectorAll('.dynamic-question_options');
        optionRows.forEach(row => row.remove());
    }

    // Helper function to add a new row with specified text
    function addOptionRow(text) {
        const addButton = document.querySelector('.add-row a'); // Finds the "Add another" button for inline
        if (addButton) addButton.click(); // Triggers new row addition
        const lastRow = document.querySelectorAll('.dynamic-question_options').item(-1);
        if (lastRow) {
            const optionTextInput = lastRow.querySelector('input[name^="question_options-"]'); // Finds the option text input
            if (optionTextInput) optionTextInput.value = text;
        }
    }

    // Function to handle changes based on the question type
    function handleQuestionTypeChange() {
        const selectedType = questionTypeSelect.value;

        if (selectedType == '2') { // Assuming 'true_false' is the value for True/False
            removeAllOptions(); // Clear all current options
            addOptionRow('True');
            addOptionRow('False');
        } else if (selectedType == '1') { // Assuming 'multiple_choice' is the value for Multiple Choice
            removeAllOptions(); // Clear current options
            for (let i = 0; i < 4; i++) { // Add at least 4 options
                addOptionRow(`Option ${i + 1}`);
            }
        }
    }

    // Attach event listener to question type select
    if (questionTypeSelect) {
        questionTypeSelect.addEventListener('change', handleQuestionTypeChange);

        // Initial call to set the correct options based on the initial selection
        handleQuestionTypeChange();
    }
});
