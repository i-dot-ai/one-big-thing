const loggedInString = " logged in at ";

fetch("/home/")
  .then(r => r.text())
  .then(t => {if (t.includes(loggedInString)){location.href="/home/"}}) ;
