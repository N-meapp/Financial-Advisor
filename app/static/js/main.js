
$('#registrationForm').on('submit', function (e) {
  e.preventDefault(); // Prevent default form submit

  const formData = $(this).serialize(); // Serialize form

  $.ajax({
    type: 'POST',
    url: '',  // Current page
    data: formData,
    success: function (response) {
      $('#response').html('<p style="color:green;">Successfully submitted!</p>');
      $('#registrationForm')[0].reset();
    },
    error: function (xhr) {
      $('#response').html('<p style="color:red;">Something went wrong!</p>');
    }
  });
});

// js for add more goals and liabilities
// const addBtn = document.getElementById("add-goal-btn");
//   const formContainer = document.getElementById("goal-formset");
//   const totalForms = document.querySelector('input[name="form-TOTAL_FORMS"]');

//   addBtn.addEventListener("click", function () {
//       const currentFormCount = parseInt(totalForms.value);
//       const newForm = document.querySelectorAll(".goal-form")[0].cloneNode(true);

//       // Update input names and IDs
//       newForm.innerHTML = newForm.innerHTML.replace(/form-(\d)-/g, `form-${currentFormCount}-`);

//       formContainer.appendChild(newForm);
//       totalForms.value = currentFormCount + 1;
//   });



// simple navbar function

function ShowNavbar() {
  event.stopPropagation(); // ✅ Prevent the document click listener from firing

  const nav = document.getElementById('nav-items');
  const button = document.querySelector('.navbar-btn');

  console.log(button, 'buttton');


  // Toggle nav
  if (nav.style.display === 'block') {
    console.log('none');

    nav.style.display = 'none';
    button.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" fill="currentColor" class="bi bi-list" viewBox="0 0 16 16">
                        <path fill-rule="evenodd" d="M2.5 12a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5"/>
                    </svg>`
    // document.removeEventListener('click', outsideClickListener);
  } else {
    console.log('block');

    console.log(nav, 'naav');

    nav.style.display = 'block';
    button.textContent = '✖'; // Change to close icon

    // Use timeout to ensure the initial button click doesn't trigger the listener
    // setTimeout(() => {
    //     document.addEventListener('click', outsideClickListener);
    // }, 0);
  }


}


function hideNav() {
  nav.style.display = 'none';
  button.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" fill="currentColor" class="bi bi-list" viewBox="0 0 16 16">
        <path fill-rule="evenodd" d="M2.5 12a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5"/>
        </svg>`
  document.removeEventListener('click', outsideClickListener);
}


function outsideClickListener(event) {
   const nav = document.getElementById('nav-items');
    const button = document.querySelector('.navbar-btn');

   nav.style.display = 'none'
    button.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" fill="currentColor" class="bi bi-list" viewBox="0 0 16 16">
                        <path fill-rule="evenodd" d="M2.5 12a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5"/>
                    </svg>`
}