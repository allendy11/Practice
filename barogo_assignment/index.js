let drink = [
  {
    name: "water",
    price: 600,
    quantity: a,
  },
  {
    name: "coffee",
    price: 700,
    quantity: b,
  },
  {
    name: "coke",
    price: 1100,
    quantity: c,
  },
];
const balance = 0;
function soldOut(drink) {
  if (drink.quantity < 1) {
    alert(`${drink.name}는 품절입니다.`);
  }
}
function insertMoney(money) {
  const {type, amount} = money
  if (type === "card") {
    drink.forEach((el) => {
      if (el.quantity >= 1) {
        alert(`${el.name} 구매 가능`);
      }
    });
  } else if (type === "cash") {
    balance += amount;
    drink.forEach((el) => {
      if (el.price <= balance && el.quantity >= 1) {
        alert(`${el.name} 구매 가능`);
      }
    });
  }
}
function pushButton(button, money) {
  const {type, amount} = money
  if (button === "return") {
    if (type === "card") {
      return money;
    } else if(type === 'cash') {
      
    }
  }
  else if(button === 'c')
}
