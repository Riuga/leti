// Обход в ширину.
// Реализовать визуализацию дерева. Указать теоретическую временную сложность для всех операций.
// С помощью реализованной структуры данных написать программу, позволяющую преобразовать запись из префиксной/инфиксной/постфиксной нотации
// в префиксную/инфиксную/постфиксную нотацию.

import { Tree } from "./bst.js";
import p5 from "p5";

new p5((p5) => {
  p5.setup = () => {
    p5.createCanvas(400, 600);
  }

  p5.draw = () => {
    p5.background(51);
  }
})

const tree = new Tree();

for (let i = 0; i < 10; i++) {
	tree.addValue(Math.floor(Math.random() * 100));
}

const inorder = document.getElementById("inorder");
const preorder = document.getElementById("preorder");
const postorder = document.getElementById("postorder");

tree.inorderTraverse(inorder);
tree.preorderTraverse(preorder);
tree.postorderTraverse(postorder);
console.log(tree);

