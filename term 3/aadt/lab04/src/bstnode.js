export class Node {
	constructor(val) {
		this.value = val;
		this.left = null;
		this.right = null;
		this.parent = null;
	}

	addNode(n) {
		if (n.value < this.value) {
			if (this.left === null) {
				this.left = n;
				n.parent = this;
			} else {
				this.left.addNode(n);
			}
		} else if (n.value > this.value) {
			if (this.right === null) {
				this.right = n;
				n.parent = this;
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

	inorder(output) {
		if (this.left != null) {
			this.left.inorder(output);
		}
		output.textContent += `${this.value} `;
		if (this.right != null) {
			this.right.inorder(output);
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
