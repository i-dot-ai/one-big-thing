fetch("/home/")
  .then(r => r.text())
  .then(t => {if (t.includes("Sign out")){location.href="/home/"}}) ;
