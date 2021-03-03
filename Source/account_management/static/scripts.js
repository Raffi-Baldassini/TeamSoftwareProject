function openLogin() {
  document.getElementById("account_popup").style.display = "block";
}

function closeLogin(){
  document.getElementById("account_popup").style.display = "none";
}

function changeTheme(){
	if(document.getElementById("theme").checked==true){
		document.documentElement.setAttribute("theme", "dark");
		document.documentElement.classList.add("change");
	}else{
		document.documentElement.setAttribute("theme", "");
		document.documentElement.classList.add("change");
	}
}



