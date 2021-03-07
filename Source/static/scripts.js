function openLogin() {
  document.getElementById("account_popup").style.display = "block";
}

function closeLogin(){
  document.getElementById("account_popup").style.display = "none";
}

var currTheme = localStorage.getItem("theme");
if(currTheme=="dark"){
	document.documentElement.setAttribute("theme", "dark");
	document.getElementById("theme").checked=true;
}else{
	document.documentElement.setAttribute("theme", "");
	document.getElementById("theme").checked=false;
}


function changeTheme(){
	if(document.getElementById("theme").checked==true){
		document.documentElement.setAttribute("theme", "dark");
		document.documentElement.classList.add("change");
		localStorage.setItem("theme", "dark");
	}else{
		document.documentElement.setAttribute("theme", "");
		document.documentElement.classList.add("change");
		localStorage.setItem("theme", "");
	}
}

setTimeout(function() {
    $('#message_box_container').delay(2000).fadeOut(1000);
}, 3000);
