import p5 from 'p5'

let borderClr = '#000000'
let fillClr = '#FFFFFF'
let starRad1 = 20
let starRad2 = 40
let points = 5
let rollSpeed = 400
let spiralRadius = 5
let pulsation = false
let position = true

const borderClrApply = document
  .querySelector('#border-apply')
  .addEventListener('click', () => {
    borderClr = document.querySelector('#border-color').value
  })

const fillClrApply = document
  .querySelector('#color-apply')
  .addEventListener('click', () => {
    fillClr = document.querySelector('#fill-color').value
  })

const starRad1Apply = document
  .querySelector('#star1-apply')
  .addEventListener('click', () => {
    starRad1 = document.querySelector('#star-radius1').value
  })

const starRad2Apply = document
  .querySelector('#star2-apply')
  .addEventListener('click', () => {
    starRad2 = document.querySelector('#star-radius2').value
  })

const starPointsApply = document
  .querySelector('#points-apply')
  .addEventListener('click', () => {
    points = document.querySelector('#star-points').value
  })

const rollApply = document
  .querySelector('#roll-apply')
  .addEventListener('click', () => {
    rollSpeed = 1 / document.querySelector('#roll-speed').value
  })

const spiralRadiusApply = document
  .querySelector('#b-apply')
  .addEventListener('click', () => {
    spiralRadius = document.querySelector('#spiral-b').value
  })

const enablePulsation = document
  .querySelector('#pulsation')
  .addEventListener('click', () => {
    pulsation = !pulsation
  })

const changePosition = document
  .querySelector('#position')
  .addEventListener('click', () => {
    position = !position
  })

new p5((p5) => {
  let trajectory = []
  let i = 0

  p5.setup = () => {
    p5.createCanvas(1000, 1000)
  }

  p5.draw = () => {
    p5.background(250)
    let spiralPoints = spiral(spiralRadius)
    let z = spiralPoints.length - 1
    drawLines(spiralPoints, 51)
    p5.push()
    if (position) {
      p5.translate(spiralPoints[i].x, spiralPoints[i].y)
      p5.rotate(p5.frameCount / rollSpeed)
      star(0, 0, starRad1, starRad2, points, borderClr, fillClr)
      trajectory.push({
        x:
          (starRad1 - 5) * p5.cos(p5.frameCount / rollSpeed) +
          spiralPoints[i].x,
        y:
          (starRad1 - 5) * p5.sin(p5.frameCount / rollSpeed) +
          spiralPoints[i].y,
      })
      p5.pop()

      p5.beginShape()
      p5.stroke(255, 0, 0)
      for (let j = 1; j < trajectory.length; j++) {
        p5.line(
          trajectory[j].x,
          trajectory[j].y,
          trajectory[j - 1].x,
          trajectory[j - 1].y
        )
      }
      p5.endShape()
    } else {
      p5.translate(spiralPoints[z - i].x, spiralPoints[z - i].y)
      p5.rotate(p5.frameCount / rollSpeed)
      star(0, 0, starRad1, starRad2, points, borderClr, fillClr)
      trajectory.push({
        x:
          (starRad1 - 5) * p5.cos(p5.frameCount / rollSpeed) +
          spiralPoints[z - i].x,
        y:
          (starRad1 - 5) * p5.sin(p5.frameCount / rollSpeed) +
          spiralPoints[z - i].y,
      })
      p5.pop()

      p5.beginShape()
      p5.stroke(255, 0, 0)
      for (let j = 1; j < trajectory.length; j++) {
        p5.line(
          trajectory[j].x,
          trajectory[j].y,
          trajectory[j - 1].x,
          trajectory[j - 1].y
        )
      }
      p5.endShape()
    }

    i++

    if (i === spiralPoints.length) {
      i = 0
      trajectory = []
    }
  }

  function spiral(spiralRadius) {
    let points = []
    let a = 0
    let b = spiralRadius

    for (let theta = 0; theta < 55; theta += 0.1) {
      let r = a + b * theta
      let x = r * p5.cos(theta)
      let y = r * p5.sin(theta)
      points.push({ x: x + 400, y: y + 400 })
    }

    return points
  }

  function drawLines(spiralPoints, color) {
    p5.stroke(color)
    p5.strokeWeight(5)
    for (let i = 1; i < spiralPoints.length; i++) {
      p5.line(
        spiralPoints[i - 1].x,
        spiralPoints[i - 1].y,
        spiralPoints[i].x,
        spiralPoints[i].y
      )
      if (pulsation && i % 10 === 1) {
        starRad1 = Math.floor(Math.random() * 30)
        starRad1 = Math.floor(Math.random() * 30)
      }
    }
  }

  function star(x, y, radius1, radius2, npoints, borderClr, fillClr) {
    let angle = p5.TWO_PI / npoints
    let halfAngle = angle / 2.0

    let fill = fillClr.replace('#', '')
    const bigint = parseInt(fill, 16)
    const r = (bigint >> 16) & 255
    const g = (bigint >> 8) & 255
    const b = bigint & 255

    p5.beginShape()
    p5.stroke(borderClr)
    for (let a = 0; a < p5.TWO_PI; a += angle) {
      let sx = x + p5.cos(a) * radius2
      let sy = y + p5.sin(a) * radius2
      p5.vertex(sx, sy)
      sx = x + p5.cos(a + halfAngle) * radius1
      sy = y + p5.sin(a + halfAngle) * radius1
      p5.vertex(sx, sy)
    }

    p5.fill(r, g, b, 50)
    p5.endShape(p5.CLOSE)
  }
})
