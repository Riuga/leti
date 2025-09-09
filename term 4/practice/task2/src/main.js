import p5 from 'p5'
import { Tree } from './bst.js'
import { blackColors, whiteColors } from './colors.js'

// Формирование последовательного изображения фракталов (G шагов генерации) с отображением формирующихся уровней на дереве
// Клетки на основе креста
// Фрактал и дерево в разных окнах

new p5((p5) => {
  const width = 1000
  let fractalWidth = width / 2
  let fractals = []
  const tree = new Tree()
  let points
  let blackSquares
  let whiteSquares
  let colorCount = 0

  p5.setup = () => {
    p5.createCanvas(1600, 1600)
    blackSquares = p5.createGraphics(500, 500)
    whiteSquares = p5.createGraphics(500, 500)
    blackSquares.background(blackColors[colorCount % 10])
    tree.addValue(blackSquares.get(), blackColors[colorCount % 10])
    blackSquares.background(200)

    const fr = new Fractal(0, 0, fractalWidth, blackColors[colorCount % 10])
    fractals.push(fr)
  }

  p5.mousePressed = () => {
    let next = []
    for (let i = 0; i < fractals.length; i++) {
      let fr = fractals[i]
      let newFractals = fr.generate()
      next = next.concat(newFractals)
    }
    fractals = next
    colorCount++
    updateTree()
  }

  p5.draw = () => {
    p5.background(200)
    for (let i = 0; i < fractals.length; i++) {
      fractals[i].show(p5)
    }
    let pts = points
    if (pts) {
      pts.forEach((point) => {
        p5.push()
        p5.translate(point.x, point.y)
        p5.image(point.value, 0, 0, 100, 100)
        p5.pop()
        if (point.parent) {
          p5.stroke(51)
          p5.line(point.x, point.y + 10, point.parent.x, point.parent.y + 10)
        }
      })
    }
  }

  function updateTree() {
    for (let i = 0; i < fractals.length; i++) {
      if (whiteColors.includes(fractals[i].color)) {
        fractals[i].show(whiteSquares)
      } else {
        fractals[i].show(blackSquares)
      }
    }
    tree.addValue(whiteSquares.get(), whiteColors[colorCount])
    tree.addValue(blackSquares.get(), blackColors[colorCount])
    blackSquares.background(200)
    points = tree.getPoints()
  }

  function Fractal(x, y, r_, clr) {
    this.pos = p5.createVector(x, y)
    this.r = r_
    this.color = clr

    this.generate = () => {
      const squares = []
      for (let x = -1; x < 2; x++) {
        for (let y = -1; y < 2; y++) {
          if (blackColors.includes(this.color)) {
            let newR = this.r / 3
            if (x != 0 && y != 0) {
              squares.push(
                new Fractal(
                  this.pos.x + (x + 1) * newR,
                  this.pos.y + (y + 1) * newR,
                  newR,
                  blackColors[colorCount]
                )
              )
            } else {
              squares.push(
                new Fractal(
                  this.pos.x + (x + 1) * newR,
                  this.pos.y + (y + 1) * newR,
                  newR,
                  whiteColors[colorCount]
                )
              )
            }
          } else {
            squares.push(this)
          }
        }
      }

      return squares
    }

    this.show = (canvas) => {
      canvas.push()
      canvas.fill(this.color)
      canvas.translate(this.pos.x, this.pos.y)
      canvas.rect(0, 0, this.r, this.r)
      canvas.pop()
    }
  }
})
