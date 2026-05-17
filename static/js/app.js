const STATE = {
  cart: [],
  menu: [
    {
      id: 1,
      name: 'Smash Clássico',
      desc: '200g de carne smash, queijo cheddar e molho especial',
      emoji: '🍔',
      price: 28
    },
    {
      id: 2,
      name: 'Bacon Lover',
      desc: 'Hambúrguer com bacon caramelizado',
      emoji: '🥓',
      price: 34
    },
    {
      id: 3,
      name: 'Batata Frita',
      desc: 'Porção crocante',
      emoji: '🍟',
      price: 18
    }
  ]
};

function renderMenu() {
  const container = document.getElementById('menu-section');

  container.innerHTML = `
    <div class="items-grid">
      ${STATE.menu.map(item => `
        <div class="item-card">
          <div class="item-emoji-bg">${item.emoji}</div>

          <div class="item-body">
            <div class="item-name">${item.name}</div>
            <p>${item.desc}</p>

            <div style="display:flex;justify-content:space-between;align-items:center;margin-top:12px;">
              <div class="item-price">R$ ${item.price}</div>

              <button class="add-btn" onclick="addToCart(${item.id})">
                +
              </button>
            </div>
          </div>
        </div>
      `).join('')}
    </div>
  `;
}

function addToCart(id) {
  const item = STATE.menu.find(i => i.id === id);

  const existing = STATE.cart.find(i => i.id === id);

  if(existing) {
    existing.qty++;
  } else {
    STATE.cart.push({ ...item, qty: 1 });
  }

  updateCart();
}

function updateCart() {
  const badge = document.getElementById('cart-badge');

  const totalItems = STATE.cart.reduce((acc, item) => acc + item.qty, 0);

  badge.textContent = totalItems;

  const drawer = document.getElementById('drawer-items');

  drawer.innerHTML = STATE.cart.map(item => `
    <div style="padding:16px;border-bottom:1px solid #eee;">
      <strong>${item.name}</strong>
      <p>${item.qty}x — R$ ${item.price}</p>
    </div>
  `).join('');
}
renderMenu();   