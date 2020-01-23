window.addEventListener('load', function() {

	function inIframe () {
 	   try {
    	    return window.self !== window.top;
    	} catch (e) {
        	return true;
    	}
	}

	const inIFrame = inIframe();
	console.log('in iframe?', inIFrame);

	const words = document.getElementsByClassName('new-word');

	const gallery = document.getElementById('gallery-word');
	const progress = document.getElementById('progress');

	const pauseBtn = document.getElementById('pause');
	const resumeBtn = document.getElementById('resume');
	const nextBtn = document.getElementById('next');
	const prevBtn = document.getElementById('previous');
	const loading = document.getElementById('loading');


	if (!inIFrame) {
		if (!localStorage.getItem('prefix') || !localStorage.getItem('noun'))
			prevBtn.style.display = 'none';
	} else {
		prevBtn.style.display = 'none';
	}

	const color =  `hsla(${ getRandomInt(30,300) }, ${getRandomInt(60, 90)}%, ${getRandomInt(50, 80)}%, 1)`;
	words[0].style.color = color;

	function getText(element) {
		if (element.textContent) 
			text += element.textContent;
		if (element.children) {
			for (let i = 0; i < element.children.length; i++) {
				getText(element.children[i]);
			}
		}
	}

	let text = '';
	getText(gallery);
	let time = text.split(' ').length * 0.3 * 1000;
	let start = performance.now();
	let timing = true;
	let offset = 0;

	function reload() {
		progress.style.background = 'transparent';
		loading.style.display = 'block';
		if (!inIFrame) {
			localStorage.setItem('prefix', prefix);
			localStorage.setItem('noun', noun);
			window.location = window.location.href.split("?")[0];
		} else {
			location.reload();
		}
	}

	var wordInterval = setInterval(function() {
		if (timing) {
			if (performance.now() > start + time) {
				reload();
				clearInterval(wordInterval);
			} else {
				const pct =  100 - (performance.now() - start) / time * 100;
				progress.style.background = `linear-gradient(90deg, ${color} ${pct - 2}%, transparent ${pct + 2}%`;
			}
		}
	}, 1000 / 60);

	pauseBtn.onclick = function() {
		timing = false;
		offset = performance.now() - start;
	};

	resumeBtn.onclick = function() {
		timing = true;
		start = performance.now() - offset;
	};

	prevBtn.onclick = function() {
		location.href = `${location.href}?noun=${localStorage.getItem('noun')}&prefix=${localStorage.getItem('prefix')}`;
	};

	nextBtn.onclick = function() {
		reload();
	};
});