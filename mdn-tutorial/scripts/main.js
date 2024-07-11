let myImage = document.querySelector("img");

myImage.onclick = function () {
    let mySrc = myImage.getAttribute("src");
    if (mySrc == "images/star.png") {
        myImage.setAttribute("src", "images/apple.png");
    } else {
        myImage.setAttribute("src", "images/star.png");
    }
};

let myButton = document.querySelector("button");
let myHeading = document.querySelector("h1");

if (!localStorage.getItem("name")) {
    setUserName();
  } else {
    let storedName = localStorage.getItem("name");
    myHeading.textContent = "I know you，" + storedName;
  }
  

function setUserName() {
    let myName = prompt("请输入你的名字。");
    if (!myName) {
      setUserName();
    } else {
    //   localStorage.setItem("name", myName);
      myHeading.textContent = "你好呀新来的，" + myName;
    }
  }
  

  myButton.onclick = function () {
    setUserName();
  };
  