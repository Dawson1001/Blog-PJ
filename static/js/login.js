window.onload = function () {
    <!-- JavaScript 代码，用来切换密码显示 -->

    // 获取复选框和密码输入框
    const showPasswordCheckbox = document.getElementById('showPassword');
    const passwordInput = document.getElementById('passwordInput');

    // 切换密码显示与隐藏
    showPasswordCheckbox.addEventListener('change', function () {
        const type = showPasswordCheckbox.checked ? 'text' : 'password';
        passwordInput.type = type;
    });
}