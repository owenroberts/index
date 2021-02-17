window.addEventListener('load', function() {

	const pauseBtn = document.getElementById('pause');
	const resumeBtn = document.getElementById('resume');
	const nextBtn = document.getElementById('next');
	const prevBtn = document.getElementById('previous');

	const storedNoun = localStorage.getItem('noun');
	const storedPrefix = localStorage.getItem('prefix');

	//  check to see if previous url is stored in local host before adding previous button
	if (storedPrefix && storedNoun && isWordGallery &&
		storedPrefix != prefix && storedNoun != noun) {
		prevBtn.style.display = 'inline-block';
	}

	if (!startSlideshow) {
		document.getElementById('slideshow').onclick = function() {
			Gallery.start = performance.now();
			Gallery.timing = true;
			this.remove();
		};
	}

	pauseBtn.onclick = function() {
		Gallery.timing = false;
		Gallery.offset = performance.now() - start;
	};

	resumeBtn.onclick = function() {
		Gallery.timing = true;
		Gallery.start = performance.now() - offset;
	};

	prevBtn.onclick = function() {
		// location.href = `${location.origin}/gallery/word/${storedNoun}/${storedPrefix}`;
		Gallery.update({
			noun: storedNoun,
			prefix: storedPrefix,
			
		});
	};

	nextBtn.onclick = Gallery.loadNextWord;

});