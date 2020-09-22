const express = require('express')
const app = express()
const port = 3000

var os = require('os')
var hostname = os.hostname();

var pid = process.pid;

app.get('/', (req, res) => {
  res.send('<h1>Hello from process: ' + pid + ', Running on: ' + hostname + '</h1>')
})

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})
