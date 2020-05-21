var fs = require('fs');

function buildRegion(sourcePath, targetPath) {
	fs.readFile(sourcePath, 'utf8', function (err, contents) {
		let data = JSON.parse(contents);

		let res = [];

		data.forEach((n) => {
			res.push({ nr: n.nr, navn: n.navn, lat: n.visueltcenter[1], lon: n.visueltcenter[0] });
		});

		fs.writeFile(targetPath, JSON.stringify(res), 'utf8', function () {});
	});
}

function buildFood(sourcePath, targetPath) {
	fs.readFile(sourcePath, 'utf8', function (err, contents) {
		let data = JSON.parse(contents);

		data.forEach((i) => {
			i.stock = 20 + Math.round(Math.random() * 50);
		});

		fs.writeFile(targetPath, JSON.stringify(data), 'utf8', function () {});
	});
}

buildFood('./data/foodRAW.json', './data/foodDone.json');
