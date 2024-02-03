// menu 
function toggleSubMenu(subMenuId) {
  var subMenu = document.getElementById(subMenuId);
  subMenu.classList.toggle("show");
}

// report_generator reset
function resetForm() {
  document.getElementById("id_date_from").value = "";
  document.getElementById("id_date_to").value = "";
  document.getElementById("id_operation_type").value = "";
  document.getElementById("id_category").value = "";
}
