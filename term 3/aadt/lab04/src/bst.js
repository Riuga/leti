import { Node } from "./bstnode.js";

export class Tree {
	constructor() {
		this.root = null;
	}

	isEmpty() {
		return this.root ? false : true;
	}

	addValue(val) {
		const n = new Node(val);
		n.level = 1;

		if (this.isEmpty()) {
			this.root = n;
			this.root.x = 1000 / 2;
			this.root.y = 16;
		} else {
			this.root.addNode(n);
		}
	}

	getMin() {
		if (this.isEmpty()) {
			return;
		}

		let min = this.root;

		while (min.left) {
			min = min.left;
		}

		return min.value;
	}

	getMax() {
		if (this.isEmpty()) {
			return;
		}

		let max = this.root;

		while (max.right) {
			max = max.right;
		}

		return max.value;
	}

	getElement(val) {
		return this.root.search(val);
	}

	removeElement(val) {
		if (this.getElement(val) === null) {
			return;
		}

		this.root.removeNode(this.getElement(val));
	}

	inorderTraverse(output) {
		const points = [];
		this.root.inorder(output, points);
		return points;
	}

	preorderTraverse(output) {
		this.root.preorder(output);
	}

	postorderTraverse(output) {
		this.root.postorder(output);
	}

	breadthTraverse(output) {
		this.root.breadth(output, []);
	}
}
