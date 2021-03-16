// Get the input field
var input = document.getElementById("follow");

// Execute a function when the user releases a key on the keyboard
input.addEventListener("keyup", function(event) {
  // Number 13 is the "Enter" key on the keyboard
  if (event.keyCode === 13) {
    // Cancel the default action, if needed
    event.preventDefault();
    // Trigger the button element with a click
    user = document.getElementById("follow").value
		$.ajax(
		{
			type:'POST',
			contentType:'application/json;charset-utf-08',
			dataType:'json',
			url:'/follow?value='+user,
			success:function(data) {
				var reply=data.reply;
				if (reply=="success") {
					console.log("success");
				}
				else{
					console.log("error occured")
				}
			}
		});
  }
});