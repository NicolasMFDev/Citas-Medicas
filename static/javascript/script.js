const aside = document.getElementById('sidebar'),
      menu = document.getElementById('menu');

menu.onclick = () => aside.classList.toggle('expand');
