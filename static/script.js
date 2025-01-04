// 获取返回顶部按钮
const backToTopButton = document.getElementById("backToTop");
// 获取所有具有滚动条的元素
const scrollableElements = document.querySelectorAll("*");

window.onscroll = function() {
    if (document.body.scrollTop > 0 || document.documentElement.scrollTop > 0) {
        backToTopButton.style.display = "block";
    } else {
        backToTopButton.style.display = "none";
    }
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
