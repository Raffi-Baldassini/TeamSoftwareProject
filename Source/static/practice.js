        
		
		function getKey (e) {
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

        function pressKey (char) {
            var key = document.querySelector('[data-char*="' + char.toUpperCase() + '"]');
            if (!key) {
                return console.warn('No key for', char);
            }
            key.setAttribute('data-pressed', 'on');
            setTimeout(function () {
                key.removeAttribute('data-pressed');
            }, 200);
        }

        var h1 = document.querySelector('a');
        var originalQueue = h1.innerHTML;
        var queue = h1.innerHTML;
		
		var currentLetterIndex = 0;
		var generated = document.getElementsByClassName('generated')[0].innerHTML;
		var newGenerated = ""

        function next () {
            var c = queue[0];
            queue = queue.slice(1);
            h1.innerHTML = originalQueue.slice(0, originalQueue.length - queue.length);
            pressKey(c);
            if (queue.length) {
                setTimeout(next, Math.random() * 200 + 50);
            }
        }

        h1.innerHTML = "&nbsp;";
        setTimeout(next, 500);

		function MoveForwardOne() {
			newGenerated = newGenerated + '<span style="color:green;">'+generated[currentLetterIndex]+'</span>';
			document.getElementsByClassName('generated')[0].innerHTML = newGenerated + generated.substring(currentLetterIndex+1, generated.length);
			currentLetterIndex++;
		}
		
        document.body.addEventListener('keydown', function (e) {
            var key = getKey(e);
            if (!key) {
                return console.warn('No key for', e.keyCode);
            }

            key.setAttribute('data-pressed', 'on');
			//window.alert(e.keycode || e.which + " " + generated[currentLetterIndex].toUpperCase().charCodeAt(0));
			if ((e.keyCode || e.which) == 190) {
				if (generated[currentLetterIndex].charCodeAt(0) == 46){
					MoveForwardOne()
				}
			}
			if ((e.keyCode || e.which) == 188) {
				if (generated[currentLetterIndex].charCodeAt(0) == 44){
					MoveForwardOne()
				}
			}
			if ((e.keyCode || e.which) == 186) {
				if (generated[currentLetterIndex].charCodeAt(0) == 59 || generated[currentLetterIndex].charCodeAt(0) == 58){
					MoveForwardOne()
				}
			}
			if ((e.keyCode || e.which) == 191) {
				if (generated[currentLetterIndex].charCodeAt(0) == 63){
					MoveForwardOne()
				}
			}
			if ((e.keyCode || e.which) == 189) {
				if (generated[currentLetterIndex].charCodeAt(0) == 45){
					MoveForwardOne()
				}
			}
			if (generated[currentLetterIndex].toUpperCase().charCodeAt(0) === (e.keyCode || e.which)) {
				MoveForwardOne()
			} else {
				newGenerated = newGenerated + '<span style="color:red;">'+generated[currentLetterIndex]+'</span>';
				document.getElementsByClassName('generated')[0].innerHTML = newGenerated + generated.substring(currentLetterIndex+1, generated.length);
				newGenerated = newGenerated.substring(0, newGenerated.length - 33);
			}
        });

        document.body.addEventListener('keyup', function (e) {
            var key = getKey(e);
            key && key.removeAttribute('data-pressed');
        });

        function size () {
            var size = keyboard.parentNode.clientWidth / 90;
            keyboard.style.fontSize = size + 'px';
            console.log(size);
        }

        var keyboard = document.querySelector('.keyboard');
        window.addEventListener('resize', function (e) {
            size();
        });
        size();