var getDef = function(noun, attempted) {

	//http://api.pearson.com/v2/dictionaries/entries?headword=test

	$.getJSON("//api.pearson.com/v2/dictionaries/entries?headword="+noun, function(data){
		var list = document.createElement("ul");
		document.querySelector('#pearson-def').innerHTML = "";
		document.querySelector('#pearson-def').appendChild(list);
		if (data.count > 0) {
			data.results.forEach(function(result) {
				result.senses.forEach(function(sense){
					var def;
					if (sense.definition) 
						def = sense.definition;
					if (sense.translation) 
						def = sense.translation;
					if (def) {
						var listItem = document.createElement("li");
						listItem.innerHTML = def;
						list.appendChild(listItem);
					}
				})
			});
		}
	});

	$.ajax({
		url: "https://en.wiktionary.org/w/api.php",
		dataType: 'jsonp', 
		data: { 
			"action": "query",
			"format": "json",
			"titles": noun,
			"prop": "extracts|redirects",
			"redirects": 1
		},
		success: function(data) {
			// console.log(data);
			var html = "";
			if (data.query.pages[-1]) {
				if (!attempted) getDef(noun.charAt(0).toUpperCase() + noun.slice(1), true);
				else $('#noun-def').html("Not found.");
			} else {
				for (var obj in data.query.pages) {
					if (data.query.pages[obj].extract) 
						$('#noun-def').html(data.query.pages[obj].extract);
					else 
						$('#noun-def').html("Not found.");
				}
			}
			
		},
		error: function(error) {
			console.log(error);
			$('#noun-def').html("Not found.");

		}
	});
};

// http://stackoverflow.com/questions/2971550/how-to-push-different-local-git-branches-to-heroku-master
// git push indexi +HEAD:master