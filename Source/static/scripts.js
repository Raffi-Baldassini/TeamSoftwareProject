function openLogin() {
  document.getElementById("account_popup").style.display = "block";
}

function closeLogin(){
  document.getElementById("account_popup").style.display = "none";
}

setTimeout(function() {
    $('#message_box_container').delay(2000).fadeOut(1000);
}, 3000);
