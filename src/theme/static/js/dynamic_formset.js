
// from https://www.brennantymrak.com/articles/django-dynamic-formsets-javascript
let mainForm = document.querySelectorAll("#main-form");
let container = document.querySelector("#form-container");
let addButton = document.querySelector("#add-form");
let totalForms = document.querySelector("#id_form-TOTAL_FORMS");
let formNum = mainForm.length - 1;
addButton.addEventListener('click', addForm);

function addForm(e) {
    e.preventDefault();

    let newForm = mainForm[0].cloneNode(true); //Clone the bird form
    let formRegex = RegExp(`form-(\\d){1}-`, 'g'); //Regex to find all instances of the form number

    formNum++; //Increment the form number
    newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formNum}-`); //Update the new form to have the correct form number
    container.insertBefore(newForm, addButton); //Insert the new form at the end of the list of forms

    totalForms.setAttribute('value', `${formNum + 1}`); //Increment the number of total forms in the management form
}
