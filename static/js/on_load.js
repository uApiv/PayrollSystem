function on_load_uapp(){
    //alert("1")
    var obj=document.getElementById("id_type")
    //obj.selectedIndex = -1;

    var index = obj.selectedIndex;
    //代表的是选中项的的值
    var val = obj.options[index].value;
    //代表的是选中项的text
    var txt = obj.options[index].text;
    //console.log(index);
    //console.log(val);
    //console.log(txt);
    if(val==="小时工"){
        document.getElementById('id_salary_pre_hour').removeAttribute('disabled')
        document.getElementById('id_salary').setAttribute('disabled', 'disabled')
        document.getElementById('id_com_rate').setAttribute('disabled', 'disabled')
    }
    else if(val==="委托员工"){
        document.getElementById('id_salary').removeAttribute('disabled')
        document.getElementById('id_com_rate').removeAttribute('disabled')
        document.getElementById('id_salary_pre_hour').setAttribute('disabled', 'disabled')
    }
    else if(val==="受薪雇员"){
        document.getElementById('id_salary').removeAttribute('disabled')
        document.getElementById('id_com_rate').setAttribute('disabled', 'disabled')
        document.getElementById('id_salary_pre_hour').setAttribute('disabled', 'disabled')
    }
    else if(val==="管理员"){
        document.getElementById('id_salary_pre_hour').setAttribute('disabled', 'disabled')
        document.getElementById('id_com_rate').setAttribute('disabled', 'disabled')
        document.getElementById('id_salary').setAttribute('disabled', 'disabled')
        document.getElementById('id_std_tax_d').setAttribute('disabled', 'disabled')
        document.getElementById('id_other_d').setAttribute('disabled', 'disabled')
        document.getElementById('id_hour_limit').setAttribute('disabled', 'disabled')
    }
}