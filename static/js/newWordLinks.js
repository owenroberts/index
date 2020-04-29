window.addEventListener('load', function() {
	const words = document.getElementsByClassName('new-word');
	for (let i = 0; i < words.length; i++) {
		const color =  `hsla(${ getRandomInt(50, 350) }, ${getRandomInt(60, 90)}%, ${getRandomInt(40, 60)}%, 1)`;
		const word = words[i];

		word.onmouseover = function() {
			word.style.color = color;
		};

		word.onmouseout = function() {
			word.style.color = 'black';
		};
	}
});