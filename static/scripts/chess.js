// submit textarea w/ 'Enter' key
let formPress = document.getElementById("entry");
formPress.addEventListener("keypress", function(event) {
  if (event.key === "Enter") {
    event.preventDefault();
    document.getElementById("button").click();
  }
});

// move focus to 'Continue' button, if present
if (document.getElementById("continue")) {
    document.getElementById("continue").focus();
};
