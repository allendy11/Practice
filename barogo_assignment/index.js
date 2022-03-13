let drinkData = [
  {
    name: "water",
    price: 600,
    quantity: 3,
  },
  {
    name: "coffee",
    price: 700,
    quantity: 3,
  },
  {
    name: "coke",
    price: 1100,
    quantity: 3,
  },
];
let balance = { type: "", amount: 0 };

function insertMoney(money) {
  const { type, amount } = money;
  if (type === "card") {
    balance = { type: "card" };
    console.log("카드입니다.");
  } else if (type === "cash") {
    balance = { type: "cash", amount: balance.amount + amount };
    console.log(`현재금액은 ${balance.amount}원 입니다.`);
  } else {
    console.log("카드 또는 현금을 지불하세요");
    return;
  }
  availableBuy(balance);
}

function availableBuy(balance) {
  const { type, amount } = balance;
  let availableDrink = [];
  if (type === "card") {
    drinkData.forEach((el) => availableDrink.push(el.name));
  } else if (type === "cash") {
    drinkData
      .filter((el) => el.price <= amount)
      .forEach((ele) => availableDrink.push(ele.name));
  }
  availableDrink.forEach((el) => console.log(`${el} 구매 가능`));
}

function pushButton(button) {
  const { type, amount } = balance;
  if (type === "") {
    console.log("카드 또는 현금을 지불하세요.");
    return;
  }
  if (button === "return") {
    if (type === "card") {
      console.log("카드를 반환합니다.");
    } else if (type === "cash") {
      console.log(`현금 ${amount}원을 반환합니다.`);
    }
    balance = { type: "", amount: 0 };
  } else {
    const [drink] = drinkData.filter((el) => el.name === button);
    if (!drink) {
      console.log(`${button}을 찾을 수 없습니다.`);
      return;
    }

    if (type === "card" || amount >= drink.price) {
      getDrink(drink.name);
    } else {
      console.log(`금액이 부족합니다.`);
      console.log(`현재 금액: ${balance.amount}원`);
    }
  }
}

function getDrink(name) {
  const { type, amount } = balance;
  const [drink] = drinkData.filter((el) => el.name === name);
  const restDrink = drinkData.filter((el) => el.name !== name);
  if (checkQuantity(name)) {
    console.log(`${name} 나왔습니다.`);
    if (type === "cash") {
      balance = {
        type: balance.type,
        amount: balance.amount - drink.price,
      };
      console.log(`현재 금액: ${balance.amount}원`);
    }
    drink.quantity -= 1;
    const drinkData = [...restDrink, drink];
  } else {
    console.log(`${name} 품절입니다.`);
  }
}

function checkQuantity(name) {
  const [drink] = drinkData.filter((el) => el.name === name);
  if (drink.quantity < 1) {
    return false;
  } else {
    return true;
  }
}
