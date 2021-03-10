var title = document.querySelector('a');
var originalQueue = title.innerHTML;
var queue = title.innerHTML;

var currentLetterIndex = 0;
var generated = document.getElementsByClassName('generated')[0].innerHTML;
var newGenerated = "";

var start
var end;
var timeTaken;
var wpm;
var acc;
var mistakes = 0;
var wordCount;
var charCount;

var over = false;
var updateLoop;
var isRedo = false;
var uppercase = false;
setStatLoop();

//updates stats in page every 10 milliseconds
function setStatLoop() {
	updateLoop = window.setInterval(function() {
		if (currentLetterIndex === generated.length) {
			wordCount = generated.split(" ").length;
		} else {
			wordCount = generated.split(" ").length - generated.substring(currentLetterIndex).split(" ").length;
			charCount = generated.length - generated.substring(currentLetterIndex).length;
		}
		if (start) {
			timeTaken = (performance.now() - start) / 1000;
		} else {
			timeTaken = 0;
		}
		if (wordCount) {
			wpm = Math.floor((wordCount / timeTaken) * 60);
		} else {
			wpm = 0;
		}
		if (mistakes == 0) {
			acc = 100;
		} else {
			acc = Math.floor((charCount / (charCount + mistakes)) * 100);
		}
		updateStats();
	}, 100);
}

//sets stats in page to current values
function updateStats() {
    document.getElementsByClassName('stats')[0].innerHTML = "<pre> words: " + wordCount +
        " characters: " + charCount +
        " time: " + timeTaken.toFixed(2) +
        " mistakes: " + mistakes +
        " wpm: " + wpm +
        " acc: " + acc + "</pre>";
}
//retrieves key pressed
function getKey(e) {
    var location = e.location;
    var selector;
    if (location === KeyboardEvent.DOM_KEY_LOCATION_RIGHT) {
        selector = ['[data-key="' + e.keyCode + '-R"]']
    } else {
        var code = e.keyCode || e.which;
        selector = [
            '[data-key="' + code + '"]',
            '[data-char*="' + encodeURIComponent(String.fromCharCode(code)) + '"]'
        ].join(',');
    }
    return document.querySelector(selector);
}

//used to type heading on load
function pressKey(char) {
    var key = document.querySelector('[data-char*="' + char.toUpperCase() + '"]');
    if (!key) {
        return console.warn('No key for', char);
    }
    key.setAttribute('data-pressed', 'on');
    setTimeout(function() {
        key.removeAttribute('data-pressed');
    }, 200);
}

//advances the character on header typing
function next() {
    var c = queue[0];
    queue = queue.slice(1);
    title.innerHTML = originalQueue.slice(0, originalQueue.length - queue.length);
    pressKey(c);
    if (queue.length) {
        setTimeout(next, Math.random() * 200 + 50);
    }
}

title.innerHTML = "&nbsp;";
setTimeout(next, 500);

//Changes character at currentLetterIndex to green and increments to next character
function MoveForwardOne() {
	if (generated[currentLetterIndex] == " ") {
		newGenerated = newGenerated + '<span style="color:green;">' + "_" + '</span>';
	}
	else {
		newGenerated = newGenerated + '<span style="color:green;">' + generated[currentLetterIndex] + '</span>';
	}
    document.getElementsByClassName('generated')[0].innerHTML = newGenerated + generated.substring(currentLetterIndex + 1, generated.length);
    currentLetterIndex++;
}

function resetStats() {
	start = null;
	end = null;
	timeTaken = null;
	wpm = null;
	acc = null;
	mistakes = 0;
	wordCount = null;
	charCount = null;
}

function resetGame(newText) {
	clearInterval(updateLoop);
	document.getElementsByClassName('generated')[0].innerHTML = newText;
	resetStats();
	generated=document.getElementsByClassName('generated')[0].innerHTML;
	newGenerated="";
	currentLetterIndex = 0;
	over = false;
	isRedo=false;
	setStatLoop();
}
//retrieves pressed key and checks for correctness
document.body.addEventListener('keydown', function(e) {
    var key = getKey(e);
    if (key) {
        key.setAttribute('data-pressed', 'on');
		//resets current text
		if ((e.keyCode || e.which) == 8) {
			clearInterval(updateLoop);
			document.getElementsByClassName('generated')[0].innerHTML = generated;
			resetStats();
			currentLetterIndex=0;
			newGenerated = "";
			over = false;
			isRedo = true;
			setStatLoop();
			
		}
		//generates new text
		else if ((e.keyCode || e.which) == 13) {
			$.ajax(
			{
				type:'GET',
				contentType:'application/json;charset-utf-08',
				dataType:'json',
				url:'http://127.0.0.1:5000/reset',
				success:function(data) {
					resetGame(data.reply);
				}
			});
		}
        else if (currentLetterIndex < generated.length) {
            //check for period
            if ((e.keyCode || e.which) == 190) {
                if (generated[currentLetterIndex].charCodeAt(0) == 46) {
                    MoveForwardOne()
                }
            }
            //chcek for comma
            else if ((e.keyCode || e.which) == 188) {
                if (generated[currentLetterIndex].charCodeAt(0) == 44) {
                    MoveForwardOne()
                }
            }
            //check for colon or semi
            else if ((e.keyCode || e.which) == 186) {
                if (generated[currentLetterIndex].charCodeAt(0) == 59 || generated[currentLetterIndex].charCodeAt(0) == 58) {
                    MoveForwardOne()
                }
            }
            //check for question mark or slash
            else if ((e.keyCode || e.which) == 191) {
                if (generated[currentLetterIndex].charCodeAt(0) == 63) {
                    MoveForwardOne()
                }
            }
			//check for space
			else if ((e.keyCode || e.which) == 32) {
				if (generated[currentLetterIndex].charCodeAt(0) == 32) {
                    MoveForwardOne()
                }
			}
            //generic catch for everything else
            else if (generated[currentLetterIndex].toUpperCase().charCodeAt(0) === (e.keyCode || e.which)) {
                MoveForwardOne()
                if (currentLetterIndex === 1) {
                    start = performance.now()
                }
            }
            //check for shift
            else if ((e.keyCode || e.which) == 16) {
				uppercase = !uppercase;
			}
			//check for capslock
			else if ((e.keyCode || e.which) == 20) {
				uppercase = !uppercase;
			}
            //changes incorrect character to be red
            else {
				if (currentLetterIndex !== 0) {
					mistakes++;
					if (generated[currentLetterIndex] == " ") {
						newGenerated = newGenerated + '<span style="color:red;">' + "_" + '</span>';
					}
					else {
						newGenerated = newGenerated + '<span style="color:red;">' + generated[currentLetterIndex] + '</span>';
					}
					document.getElementsByClassName('generated')[0].innerHTML = newGenerated + generated.substring(currentLetterIndex + 1, generated.length);
					newGenerated = newGenerated.substring(0, newGenerated.length - 33);
				}
            }
        }
        //round is over, ends stat updating loops and sets final stats
        if (currentLetterIndex >= generated.length && !(over)) {
            clearInterval(updateLoop);
			wordCount++;
			updateStats();
			over = true;
			if (!(isRedo)) {
				var stats = [wordCount, charCount, wpm, acc];
				$.ajax(
				{
					type:'POST',
					contentType:'application/json;charset-utf-08',
					dataType:'json',
					url:'http://127.0.0.1:5000/stats?value='+stats,
					success:function(data) {
						var reply=data.reply;
						if (reply=="success") {
							return;
						}
						else{
							console.log("error occured")
						}
					}
				});
			}

        }
    }
});

//removes 'pressed' attribute
document.body.addEventListener('keyup', function(e) {
    var key = getKey(e);
    key && key.removeAttribute('data-pressed');
});

function size() {
    var size = keyboard.parentNode.clientWidth / 90;
    keyboard.style.fontSize = size + 'px';
}

var keyboard = document.querySelector('.keyboard');
window.addEventListener('resize', function(e) {
    size();
});
size();


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
