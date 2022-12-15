import { Tree } from "./bst.js";
import p5 from "p5";

const tree = new Tree();

const inorder = document.getElementById("inorder");
const preorder = document.getElementById("preorder");
const postorder = document.getElementById("postorder");
const breadth = document.getElementById("breadth");
const minimal = document.getElementById("min");
const maximum = document.getElementById("max");
const add = document.getElementById("add");
const del = document.getElementById("del");
const find = document.getElementById("find");
let points;

add.addEventListener("click", () => {
	let value = Number(document.getElementById("value").value);
	tree.addValue(value);
	updateOutput();
});

del.addEventListener("click", () => {
	let value = Number(document.getElementById("remove").value);
	tree.remove(value);
	updateOutput();
});

find.addEventListener("click", () => {
	let value = document.getElementById("search").value;
	const result = document.getElementById("search-result");
	let el = tree.getElement(value);
	if (el) {
		let prevous;
		let left;
		let right;
		el.parent ? (prevous = el.parent.value) : (prevous = "not exists");
		el.left ? (left = el.left.value) : (left = "not exists");
		el.right ? (right = el.right.value) : (right = "not exists");

		result.textContent = `Element is in tree. Next left element: ${left}. Next right element: ${right}. Prevous element: ${prevous}`;
	} else {
		result.textContent = "Element not found";
	}
});

function updateOutput() {
	inorder.textContent = "Inorder: ";
	preorder.textContent = "Preorder: ";
	postorder.textContent = "Postorder: ";
	breadth.textContent = "Breadth: ";
	tree.inorderTraverse(inorder);
	tree.preorderTraverse(preorder);
	tree.postorderTraverse(postorder);
	tree.breadthTraverse(breadth);
	minimal.textContent = `Min: ${tree.getMin()}`;
	maximum.textContent = `Max: ${tree.getMax()}`;

	points = tree.getPoints();
}

new p5((p5) => {
	p5.setup = () => {};

	p5.draw = () => {
		p5.createCanvas(1000, 1000);
		p5.background(51);
		let pts = points;
		if (pts) {
			pts.forEach((point) => {
				p5.fill(255);
				p5.noStroke();
				p5.textAlign(p5.CENTER);
				p5.text(point.value, point.x, point.y);
				p5.stroke(255);
				p5.noFill();
				p5.ellipse(point.x, point.y, 20, 20);
				if (point.parent) {
					p5.line(
						point.x,
						point.y + 10,
						point.parent.x,
						point.parent.y + 10
					);
				}
			});
		}
	};
});
