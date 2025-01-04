// 获取返回顶部按钮
const backToTopButton = document.getElementById("backToTop");
// 获取所有具有滚动条的元素
const scrollableElements = document.querySelectorAll("*");

window.onscroll = function() {
    backToTopButton.style.display = "block";
};

// 当点击按钮时，所有滚动元素都回到顶部
backToTopButton.onclick = function() {
    scrollableElements.forEach(element => {
        if (element.scrollTop !== undefined) {
            element.scrollTop = 0;
        }
    });

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
};
