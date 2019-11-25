window.addEventListener('load', function() {
	let stop = false;
	let count = 0;

	const words = document.getElementsByClassName('new-word');
	const container = document.getElementById('words');
	const counter = document.getElementById('counter');
	const len = words.length;


	asyncLoop({
		length: len,
		functionToLoop: function(loop, i) {
			setTimeout(function() {
				words[i].style.display = "inline";
				container.appendChild(words[i])
				container.appendChild(document.createElement('br'));
				count++;
				if (counter)
					counter.textContent = count + " / " + len;
				loop();
			}, 2);
		},
		callback: function() {
			console.log("done!");
		}
	});

});