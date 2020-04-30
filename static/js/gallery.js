window.addEventListener('load', function() {

	const words = document.getElementsByClassName('new-word');

	const gallery = document.getElementById('gallery');
	const progress = document.getElementById('progress');

	const pauseBtn = document.getElementById('pause');
	const resumeBtn = document.getElementById('resume');
	const nextBtn = document.getElementById('next');
	const prevBtn = document.getElementById('previous');
	const loading = document.getElementById('loading');

	const storedNoun = localStorage.getItem('noun');
	const storedPrefix = localStorage.getItem('prefix');

	//  check to see if previous url is stored in local host before adding previous button
	if (storedPrefix && storedNoun && isWordGallery &&
		storedPrefix != prefix && storedNoun != noun) {
		prevBtn.style.display = 'inline-block';
	}

	// recursively get text on screen to set timer length
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
	let timing = startSlideshow; // if true this counts down and updates the timiing
	let offset = 0;

	if (!startSlideshow) {
		document.getElementById('slideshow').onclick = function() {
			start = performance.now();
			timing = true;
			this.remove();
		};
	}


	function loadNextWord() {
		progress.style.background = 'transparent';
		loading.style.display = 'block';
			localStorage.setItem('prefix', prefix);
			localStorage.setItem('noun', noun);
		fetch('/random_gallery_word')
			.then(response => { return response.json(); })
			.then(json => {
				location.href = `${location.origin}/gallery/word/${json[0]}/${json[1]}`;
			});
	}

	const color = document.getElementsByClassName('new-word')[0].style.color;

	var wordInterval = setInterval(function() {
		if (timing) {
			if (performance.now() > start + time) {
				clearInterval(wordInterval);
				loadNextWord();
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
		location.href = `${location.origin}/gallery/word/${storedNoun}/${storedPrefix}`;
	};

	nextBtn.onclick = loadNextWord;
});