
function skipPatentableValidation(elementId) {
    const selectElement = document.getElementById(elementId);
    selectElement.required = false;
}