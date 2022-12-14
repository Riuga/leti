export class Node {
	constructor(val, x, y) {
		this.value = val;
		this.left = null;
		this.right = null;
		this.parent = null;
		this.x = x;
		this.y = y;
		this.level;
	}

	addNode(n) {
		n.level++;
		if (n.value < this.value) {
			if (this.left === null) {
				this.left = n;
				this.left.parent = this;
				this.left.x = this.x - 500 / 2 ** this.level;
				this.left.y = this.y + 20 * this.level;
			} else {
				this.left.addNode(n);
			}
		} else if (n.value > this.value) {
			if (this.right === null) {
				this.right = n;
				this.right.parent = this;
				this.right.x = this.x + 500 / 2 ** this.level;
				this.right.y = this.y + 20 * this.level;
			} else {
				this.right.addNode(n);
			}
		}
	}

	findMinNode(n) {
		if (n.left === null) {
			return n;
		}

		return this.findMinNode(n.left);
	}

	removeNode(n) {
		if (n.left === null && n.right === null) {
			n = null;
			return n;
		}

		if (n.left === null) {
			n = n.right;
			return n;
		}

		if (n.right === null) {
			n = n.left;
			return n;
		}

		const newNode = this.findMinNode(n.right);
		newNode.left = n.left;
		newNode.parent.left = null;
		newNode.parent = n.parent;
		n = newNode;
	}

	inorder(output, points) {
		if (this.left != null) {
			this.left.inorder(output, points);
		}
		output.textContent += `${this.value} `;
		points.push({
			x: this.x,
			y: this.y,
			parent: this.parent,
			value: this.value,
		});
		if (this.right != null) {
			this.right.inorder(output, points);
		}
	}

	preorder(output) {
		output.textContent += `${this.value} `;
		if (this.left != null) {
			this.left.preorder(output);
		}
		if (this.right != null) {
			this.right.preorder(output);
		}
	}

	postorder(output) {
		if (this.left != null) {
			this.left.postorder(output);
		}
		if (this.right != null) {
			this.right.postorder(output);
		}
		output.textContent += `${this.value} `;
	}

	breadth(output, queue) {
		if (this.left) {
			queue.push(this.left);
		}
		if (this.right) {
			queue.push(this.right);
		}

		output.textContent += `${this.value} `
		if (queue.length != 0) {
			queue.shift().breadth(output, queue);
		}
	}

	search(val) {
		if (this.value == val) {
			return this;
		}

		if (val < this.value && this.left != null) {
			return this.left.search(val);
		}

		if (val > this.value && this.right != null) {
			return this.right.search(val);
		}

		return null;
	}
}
