// 获取返回顶部按钮
const backToTopButton = document.getElementById("backToTop");

// 获取所有具有滚动条的元素
const scrollableElements = document.querySelectorAll("*");

// 当用户滚动时，显示或隐藏返回顶部按钮
window.onscroll = function() {
    if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) {
        backToTopButton.style.display = "block"; // 显示按钮
    } else {
        backToTopButton.style.display = "none"; // 隐藏按钮
    }
};

// 当点击按钮时，所有滚动元素都回到顶部
backToTopButton.onclick = function() {
    scrollableElements.forEach(element => {
        if (element.scrollTop !== undefined) {
            element.scrollTop = 0; // 将所有滚动元素的scrollTop设置为0
        }
    });

    // 同时滚动到页面顶部（不影响scrollable元素的回到顶部）
    window.scrollTo({
        top: 0,
        behavior: "smooth" // 平滑滚动
    });
};
