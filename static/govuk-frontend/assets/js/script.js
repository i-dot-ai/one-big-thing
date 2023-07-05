function blendColors(color1, color2, amount) {
  // Convert color1 to RGB
  var r1 = parseInt(color1.substring(1, 3), 16)
  var g1 = parseInt(color1.substring(3, 5), 16)
  var b1 = parseInt(color1.substring(5, 7), 16)

  // Convert color2 to RGB
  var r2 = parseInt(color2.substring(1, 3), 16)
  var g2 = parseInt(color2.substring(3, 5), 16)
  var b2 = parseInt(color2.substring(5, 7), 16)

  // Calculate the blended color
  var r = Math.round(r1 + (r2 - r1) * amount)
  var g = Math.round(g1 + (g2 - g1) * amount)
  var b = Math.round(b1 + (b2 - b1) * amount)

  // Convert the blended color back to hexadecimal
  var hex = '#' + r.toString(16) + g.toString(16) + b.toString(16)

  return hex
}

const setupGraohs = () => {
  const graphScripts = document.querySelectorAll(
    'script[type="application/json"].govuk-graph'
  )

  // Iterate over each script tag and parse the JSON data
  graphScripts.forEach((script, i) => {
    const { data, layout } = JSON.parse(script.textContent)
    const total = data.length

    const newData = data.map((graph, i) => {
      const amount = (!!i ? i + 1 : i) / total
      //   const color = '#B62777'
      const color = blendColors('#00A20D', '#B62777', amount)

      console.log({ i, color, amount })

      const defaultProps = {
        ...data[0],
        marker: { color },
      }

      return { ...defaultProps, ...graph }
    })

    // Create a new element for the graph
    const graphDiv = document.createElement('div')
    // graphDiv.id = `graph-${script.id}`

    script.parentNode.insertBefore(graphDiv, script.nextSibling)

    // Render the graph using Plotly
    Plotly.newPlot(graphDiv, newData, layout)
  })
}

window.addEventListener('load', (event) => {
  setupGraohs()
})
