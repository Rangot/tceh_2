/**
 * Created by Тёма on 16.05.2018.
 */
'use strict';

function func(num1,num2) {
    //document.getElementById('inp1').value;
    var num1 = document.getElementById('inp1').value;
    var num2 = document.getElementById('inp2').value;
    alert(num1 * num2);
}

function plus() {
    alert(Number(document.getElementById('inp3').value) + Number(document.getElementById('inp4').value));
}

function substract() {
    alert(Number(document.getElementById('inp3').value) - Number(document.getElementById('inp4').value));
}

function simple() {
    var num1 = Number(document.getElementById('inp5').value);
    for (var j=2)
}