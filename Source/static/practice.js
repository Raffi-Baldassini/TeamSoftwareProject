//used for tping the title on load
var title = document.querySelector("a");
var originalQueue = title.innerHTML;
var queue = title.innerHTML;
//used for keeping track of position in text and current representation of text
var currentLetterIndex = 0;
var generated = document.getElementsByClassName("generated")[0].innerHTML;
var newGenerated = "";
//game spceific statistics
var start;
var end;
var timeTaken;
var wpm;
var acc;
var mistakes = 0;
var wordCount;
var charCount;
//state tracking variables
var over = false;
var updateLoop;
var isRedo = false;
var uppercase = false;
//for wpm highlighting
var wpm_day = 0;
var wpm_best = 0;
var wpm_span = "";
var close_wpm = "";

//checks if logged in and if so retrieves uID and WPM records
function displayProfileandGetInfoIfLoggedIN() {
  $.ajax({
    type: "GET",
    contentType: "application/json;charset-utf-08",
    dataType: "json",
    url: "/loggedinidwpm",
    success: function (data) {
      if (data.reply == "yes") {
        document.getElementById("profile-link").innerHTML =
          "<a class='nav-link' href='/profile'>Profile</a>";
        wpm_day = data.wpm_day;
        wpm_best = data.wpm_best;
      }
    },
  });
}

//updates stats in page every 10 milliseconds
function setStatLoop() {
  updateLoop = window.setInterval(function () {
    if (currentLetterIndex === generated.length) {
      wordCount = generated.split(" ").length;
    } else {
      wordCount =
        generated.split(" ").length -
        generated.substring(currentLetterIndex).split(" ").length;
      charCount =
        generated.length - generated.substring(currentLetterIndex).length;
    }
    if (start) {
      timeTaken = (performance.now() - start) / 1000;
    } else {
      timeTaken = 0;
    }
    if (charCount >= 5) {
      wpm = Math.floor((charCount / 5 / timeTaken) * 60);
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
  //highlights WPM if best-of day (pink) or best-of all-time (gold) is currently achieved
  if (wpm_best) {
    if (wpm > wpm_day && wpm <= wpm_best) {
      wpm_span = "<b style='color:#FF33EC;'>";
      close_wpm = "</b>";
    } else if (wpm > wpm_best) {
      wpm_span = "<b style='color:gold;'>";
      close_wpm = "</b>";
    }
  }
  document.getElementsByClassName("stats")[0].innerHTML =
    "words: " +
    wordCount +
    " characters: " +
    charCount +
    " time: " +
    timeTaken.toFixed(2) +
    " mistakes: " +
    mistakes +
    wpm_span +
    " wpm: " +
    wpm +
    close_wpm +
    " acc: " +
    acc;
  wpm_span = "";
  close_wpm = "";
}

//retrieves key pressed
function getKey(e) {
  var location = e.location;
  var selector;
  if (location === KeyboardEvent.DOM_KEY_LOCATION_RIGHT) {
    selector = ['[data-key="' + e.keyCode + '-R"]'];
  } else {
    var code = e.keyCode || e.which;
    selector = [
      '[data-key="' + code + '"]',
      '[data-char*="' + encodeURIComponent(String.fromCharCode(code)) + '"]',
    ].join(",");
  }
  return document.querySelector(selector);
}

//used to type title on load
function pressKey(char) {
  var key = document.querySelector('[data-char*="' + char.toUpperCase() + '"]');
  if (!key) {
    return console.warn("No key for", char);
  }
  key.setAttribute("data-pressed", "on");
  setTimeout(function () {
    key.removeAttribute("data-pressed");
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
  //spaces get underlined to avoid confusion
  if (generated[currentLetterIndex] == " ") {
    newGenerated =
      newGenerated +
      '<span style="color:green; text-decoration: underline;">' +
      " " +
      "</span>";
  }
  //general case
  else {
    newGenerated =
      newGenerated +
      '<span style="color:green;">' +
      generated[currentLetterIndex] +
      "</span>";
  }
  //If not on the last chracter of the text then the next character to be typed will be made bold and slightly larger
  if (currentLetterIndex < generated.length - 1) {
    document.getElementsByClassName("generated")[0].innerHTML =
      newGenerated +
      "<b style='font-size:19'>" +
      generated[currentLetterIndex + 1] +
      "</b>" +
      generated.substring(currentLetterIndex + 2, generated.length);
  } else {
    document.getElementsByClassName("generated")[0].innerHTML =
      newGenerated +
      generated.substring(currentLetterIndex + 1, generated.length);
  }
  currentLetterIndex++;
}

//used to reset game-specific stats
function resetStats() {
  start = null;
  end = null;
  timeTaken = null;
  wpm = null;
  acc = null;
  mistakes = 0;
  wordCount = null;
  charCount = null;
  displayProfileandGetInfoIfLoggedIN();
}

//reset all game-specific variables
function resetGame(newText) {
  clearInterval(updateLoop);
  document.getElementsByClassName("generated")[0].innerHTML = newText;
  resetStats();
  generated = document.getElementsByClassName("generated")[0].innerHTML;
  newGenerated = "";
  currentLetterIndex = 0;
  over = false;
  isRedo = false;
  setStatLoop();
}

//retrieves pressed key and checks for correctness
document.body.addEventListener("keydown", function (e) {
  var key = getKey(e);
  if (key) {
    key.setAttribute("data-pressed", "on");
    //resets current text
    if ((e.keyCode || e.which) == 8) {
      clearInterval(updateLoop);
      document.getElementsByClassName("generated")[0].innerHTML = generated;
      resetStats();
      currentLetterIndex = 0;
      newGenerated = "";
      over = false;
      isRedo = true;
      setStatLoop();
    }
    //generates new text
    else if ((e.keyCode || e.which) == 13) {
      $.ajax({
        type: "GET",
        contentType: "application/json;charset-utf-08",
        dataType: "json",
        url: "/reset",
        success: function (data) {
          resetGame(data.reply);
        },
      });
    } else if (currentLetterIndex < generated.length) {
      //check for period
      if ((e.keyCode || e.which) == 190) {
        if (generated[currentLetterIndex].charCodeAt(0) == 46) {
          MoveForwardOne();
        }
      }
      //chcek for comma
      else if ((e.keyCode || e.which) == 188) {
        if (generated[currentLetterIndex].charCodeAt(0) == 44) {
          MoveForwardOne();
        }
      }
      //check for colon or semi-colon
      else if ((e.keyCode || e.which) == 186) {
        if (
          generated[currentLetterIndex].charCodeAt(0) == 59 ||
          generated[currentLetterIndex].charCodeAt(0) == 58
        ) {
          MoveForwardOne();
        }
      }
      //check for apostrophe
      else if ((e.keyCode || e.which) == 192) {
        if (
          generated[currentLetterIndex].charCodeAt(0) == 39 ||
          generated[currentLetterIndex].charCodeAt(0) == 39
        ) {
          MoveForwardOne();
        }
      }
      //check for question mark or slash
      else if ((e.keyCode || e.which) == 191) {
        if (generated[currentLetterIndex].charCodeAt(0) == 63) {
          MoveForwardOne();
        }
      }
      //check for space
      else if ((e.keyCode || e.which) == 32) {
        if (generated[currentLetterIndex].charCodeAt(0) == 32) {
          MoveForwardOne();
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
      //the code obtained from a keypress is always the uppercase version of the letter so using the uppercase var and the
      //actual text like this is the best I could come up with
      //generic catch for upper-case
      else if (
        uppercase &&
        generated[currentLetterIndex].toUpperCase().charCodeAt(0) ==
          generated[currentLetterIndex].charCodeAt(0) &&
        generated[currentLetterIndex].toUpperCase().charCodeAt(0) ==
          (e.keyCode || e.which)
      ) {
        MoveForwardOne();
        if (currentLetterIndex === 1) {
          start = performance.now();
        }
      }
      //generic catch for lower-case
      else if (
        !uppercase &&
        generated[currentLetterIndex].toUpperCase().charCodeAt(0) !==
          generated[currentLetterIndex].charCodeAt(0) &&
        generated[currentLetterIndex].toUpperCase().charCodeAt(0) ==
          (e.keyCode || e.which)
      ) {
        MoveForwardOne();
        if (currentLetterIndex === 1) {
          start = performance.now();
        }
      }
      //changes incorrect character to be red
      else {
		mistakeBuffer = 31
        if (currentLetterIndex !== 0) {
          mistakes++;
          if (generated[currentLetterIndex] == " ") {
            newGenerated =
              newGenerated + '<b style="color:#8B0000; text-decoration: underline;">' + "_" + "</b>";
			  mistakeBuffer = 59
          } else {
            newGenerated =
              newGenerated +
              '<b style="color:#8B0000;">' +
              generated[currentLetterIndex] +
              "</b>";
          }
          document.getElementsByClassName("generated")[0].innerHTML =
            newGenerated +
            generated.substring(currentLetterIndex + 1, generated.length);
          newGenerated = newGenerated.substring(0, newGenerated.length - mistakeBuffer);
        }
      }
    }
    //round is over, ends stat updating loops and sets final stats
    if (currentLetterIndex >= generated.length && !over) {
      clearInterval(updateLoop);
      wordCount++;
      updateStats();
      over = true;
      //stats are only sent to back-end if text is completed on first try
      if (!isRedo) {
        var stats = [wordCount, charCount, wpm, acc];
        $.ajax({
          type: "POST",
          contentType: "application/json;charset-utf-08",
          dataType: "json",
          url: "/stats?value=" + stats,
          success: function (data) {
            var reply = data.reply;
            if (reply == "success") {
              return;
            } else {
              console.log("error occured");
            }
          },
        });
      }
    }
  }
});

//removes 'pressed' attribute, flips uppercase if shift or capslock interaction occurs
document.body.addEventListener("keyup", function (e) {
  var key = getKey(e);
  if ((e.keyCode || e.which) == 16) {
    uppercase = !uppercase;
  }
  if (!((e.keyCode || e.which) == 20)) {
    key && key.removeAttribute("data-pressed");
  } else {
    if (!uppercase) {
      key && key.removeAttribute("data-pressed");
    }
  }
});

//sets key-text size
function size() {
  var size = keyboard.parentNode.clientWidth / 90;
  keyboard.style.fontSize = size + "px";
}

var keyboard = document.querySelector(".keyboard");
window.addEventListener("resize", function (e) {
  size();
});

var currTheme = localStorage.getItem("theme");
if (currTheme == "dark") {
  document.documentElement.setAttribute("theme", "dark");
  document.getElementById("theme").checked = true;
} else {
  document.documentElement.setAttribute("theme", "");
  document.getElementById("theme").checked = false;
}

function changeTheme() {
  var x = document.getElementById("themeLabel");
  if (document.getElementById("theme").checked == true) {
    document.documentElement.setAttribute("theme", "dark");
    document.documentElement.classList.add("change");
    localStorage.setItem("theme", "dark");
    x.innerHTML = "Dark";
  } else {
    document.documentElement.setAttribute("theme", "");
    document.documentElement.classList.add("change");
    localStorage.setItem("theme", "");
    x.innerHTML = "Light";
  }
}
//sets size of keyboard text
size();
//begins the loop for updating stats
setStatLoop();
//and retrieves user information
displayProfileandGetInfoIfLoggedIN();
