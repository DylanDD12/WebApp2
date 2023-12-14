// Open the first tab by default
document.getElementById("tab1").style.display = "block";
document.querySelector(".tab-button").classList.add("active");

function openTab(event, tabName, tabIndex) {
  // Get all elements with class "tab-content" and hide them
  const tabContents = document.getElementsByClassName("tab-content");
  for (let i = 0; i < tabContents.length; i++) {
    tabContents[i].style.display = "none";
  }

  // Get all elements with class "tab-button" and remove the "active" class
  const tabButtons = document.getElementsByClassName("tab-button");
  for (let i = 0; i < tabButtons.length; i++) {
    tabButtons[i].classList.remove("active");
  }

  // Show the current tab and set the button as active
  document.getElementById(tabName).style.display = "block";
  event.currentTarget.classList.add("active");

}
