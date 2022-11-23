// Решить задачу с использованием принципа «Разделяй и властвуй».
// Определить теоретическую асимптотическую сложность решения.
// Эмпирически оценить временную сложность решения для «average-case».
// На квадрате земли 1 км2 располагаются улитки-гермафродиты.
// В момент времени каждая из улиток с постоянной скоростью 1 cм/с ползет к улитке, являющейся ближайшей к ней в момент
// времени t = 0, выбрав её в качестве спутника жизни.
// Определить время, через которое первая пара улиток достигнет друг друга или наличие
// ситуации, приводящей улиток в замешательство, наиболее эффективным способом

function generateSnails(side, chance) {
	const snails = [];

	for (let i = 0; i < side; i++) {
		for (let j = 0; j < side; j++) {
			if (Math.floor(Math.random() * chance) === 1) {
				snails.push([i, j]);
			}
		}
	}

	return snails;
}

function distanceBetweenSnails(s1, s2) {
	return (s2[0] - s1[0]) ** 2 + (s2[1] - s1[1]) ** 2;
}

function findMinDistance(snails, l, r) {
	if (r <= 1) {
		return [-1, -1, Infinity];
	}
	if (r - l === 1) {
		return [
			snails[l],
			snails[r],
			distanceBetweenSnails(snails[l], snails[r]),
		];
	}
	if (r - l === 2) {
		const d1 = distanceBetweenSnails(snails[l], snails[l + 1]);
		const d2 = distanceBetweenSnails(snails[l + 1], snails[r]);
		const d3 = distanceBetweenSnails(snails[l], snails[r]);

		if (d1 <= d2 && d1 <= d3) {
			return [snails[l], snails[l + 1], d1];
		}
		if (d2 <= d1 && d2 <= d3) {
			return [snails[l + 1], snails[r], d2];
		}
		return [snails[l], snails[r], d3];
	}

	const m = Math.floor(l + (r - l) / 2);
	const res1 = findMinDistance(snails, l, m);
	const res2 = findMinDistance(snails, m + 1, r);
	const d = Math.min(res1[2], res2[2]);

	let i = m;
	let j = m;

	while (i >= 1) {
		if (snails[m][0] - snails[i][0] < d) {
			i--;
		} else {
			break;
		}
	}

	while (j <= r) {
		if (snails[j][0] - snails[m][0] < d) {
			j += 1;
		} else {
			break;
		}
	}

	if (i < m) {
		i++;
	}

	const res3 = [-1, -1, Infinity];

	for (let a = i; a < m + 1; a++) {
		for (let b = m + 1; b < j; b++) {
			let d0 = distanceBetweenSnails(snails[a], snails[b]);
			if (d0 < res3[2]) {
				res3[0] = snails[a];
				res3[1] = snails[b];
				res3[2] = d0;
			}
		}
	}

	if (res1[2] <= res2[2] && res1[2] <= res3[2]) {
		return res1;
	}

	if (res2[2] <= res1[2] && res2[2] <= res3[2]) {
		return res2;
	}

	return res3;
}

function start() {
	const elt = document.getElementById("calculator");
	const calculator = Desmos.GraphingCalculator(elt);
	const timeP = document.getElementById("time");
	const side = document.getElementById("side").value;
	const v = document.getElementById("speed").value * 0.01;
	const chance = document.getElementById("chance").value;

	const snails = generateSnails(side, chance);
	const x = [];
	const y = [];

	snails.forEach((snail) => {
		x.push(snail[0]);
		y.push(snail[1]);
	});

	const closest = findMinDistance(snails, 0, snails.length - 1);
	const clsx = [closest[0][0], closest[1][0]];
	const clsy = [closest[0][1], closest[1][1]];

	calculator.setExpression({
		type: "table",
		columns: [
			{
				latex: "x",
				values: x,
			},
			{
				latex: "y",
				values: y,
				dragMode: Desmos.DragModes.XY,
			},
		],
	});

	calculator.setExpression({
		type: "table",
		columns: [
			{
				latex: "x",
				values: clsx,
			},
			{
				latex: "y",
				values: clsy,
				dragMode: Desmos.DragModes.XY,
			},
		],
	});

	timeP.textContent = `They will meet each other after ${
		Math.sqrt(closest[2]) / (2 * v)
	} seconds`;
}

const submit = document.getElementById("start");
submit.addEventListener("click", start);
