// ==UserScript==
// @name         百度文库创作中心测试
// @namespace    https://bbs.tampermonkey.net.cn/
// @version      0.1.2
// @description  try to take over the world!
// @author       Sakta_wdi
// @email        1742804029@qq.com
// @match        https://cuttlefish.baidu.com/ndecommtob/browse/index?_wkts_=**#/taskCenter/majorTask
// @match        https://cuttlefish.baidu.com/shopmis?_wkts_=**#/taskCenter/majorTask
// ==/UserScript==

(function() {
    'use strict';
    // 在页面上创建一个按钮
    const startButton = document.createElement('button');
    startButton.textContent = '生成多选框';
    startButton.style.position = 'fixed';
    startButton.style.top = '5px';
    startButton.style.right = 'calc(50vw)';
    startButton.style.zIndex = '9999';
    // 添加样式
    startButton.style.padding = '10px 20px';
    startButton.style.fontSize = '16px';
    startButton.style.backgroundColor = '#007bff'; // 蓝色背景颜色
    startButton.style.color = '#fff'; // 白色文字颜色
    startButton.style.border = 'none'; // 去除边框
    startButton.style.borderRadius = '5px'; // 圆角
    startButton.style.cursor = 'pointer'; // 鼠标指针样式为手型

    // 在页面上创建一个按钮
    const copyButton = document.createElement('button');
    copyButton.textContent = '一键复制';
    copyButton.style.position = 'fixed';
    copyButton.style.top = '5px';
    copyButton.style.right = 'calc(40vw)';
    copyButton.style.zIndex = '9999';
    // 添加样式
    copyButton.style.padding = '10px 20px';
    copyButton.style.fontSize = '16px';
    copyButton.style.backgroundColor = '#007bff'; // 蓝色背景颜色
    copyButton.style.color = '#fff'; // 白色文字颜色
    copyButton.style.border = 'none'; // 去除边框
    copyButton.style.borderRadius = '5px'; // 圆角
    copyButton.style.cursor = 'pointer'; // 鼠标指针样式为手型


    // 创建输入框元素
    const inputBox = document.createElement('input');
    inputBox.type = 'text'; // 设置输入框类型为文本
    inputBox.placeholder = ''; // 设置输入框的占位符
    inputBox.style.position = 'fixed';
    inputBox.style.minWidth = "calc(100vw)";
    inputBox.style.top = '50px';
    inputBox.style.zIndex = '9999';
    // 添加样式
    inputBox.style.border = '2px solid #ccc';
    inputBox.style.borderRadius = '5px';
    inputBox.style.padding = '10px';
    inputBox.style.fontSize = '16px';
    inputBox.style.backgroundColor = '#f9f9f9';
    inputBox.style.color = '#333';

    // 将添加到页面中
    document.body.appendChild(startButton);
    document.body.appendChild(inputBox);
    document.body.appendChild(copyButton);

    let cid = 99;
    let page = 1;
    let index = 0;

    // 给按钮添加点击事件监听器，点击按钮时执行功能
    startButton.addEventListener('click', startFeature);
    copyButton.addEventListener('click', copyFeature);

    function startFeature() {
        console.log("clicked");
        const contentContainers = document.querySelectorAll('.content');
        for (const container of contentContainers) {
            const rowContains = container.querySelectorAll('.doc-row');
            for (const rowContain of rowContains) {
                addCheckboxToContainer(rowContain);
            }
        }
        cid = findActivatedItemIndex();
        const inputElement = document.querySelector('.el-input__inner');
        page = inputElement.value - 1;
    }

    function findActivatedItemIndex() {
        const privilegeList = document.querySelector('.privilege-list');
        if (privilegeList) {
            const privilegeItems = privilegeList.querySelectorAll('.privilege-item-container');
            for (let i = 0; i < privilegeItems.length; i++) {
            if (privilegeItems[i].classList.contains('action')) {
                return i == 0?99:i - 1;
            }
            }
        }
        return -1;
    }

    function addCheckboxToContainer(container) {
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.style.marginRight = '5px';
        container.appendChild(checkbox);
        checkbox.addEventListener('change', function() {
            if (this.checked) {
                const parentContainer = this.parentNode
                const numberElement = parentContainer.querySelector('.number');
                const numberValue = parseInt(numberElement.textContent.trim());
                // const modifiedValue = numberValue - 1;
                //console.log("index:",modifiedValue);
                index = numberValue - 1;
                inputBox.value =  inputBox.value + "[" + cid +  "," + page + ","+ index + "],";
            }
        });
    }

     function copyFeature(){
        const valueWithoutLastCharacter = "[" + inputBox.value.substring(0, inputBox.value.length - 1) + "]";
        inputBox.value = valueWithoutLastCharacter;
        inputBox.select();
        document.execCommand('copy');
        window.getSelection().removeAllRanges();
        inputBox.value = inputBox.value.substring(1, inputBox.value.length - 1);
        inputBox.value = inputBox.value + ",";
     }
})();