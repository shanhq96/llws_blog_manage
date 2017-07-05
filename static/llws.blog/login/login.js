/**
 * Created by 33071 on 2017/7/5.
 * description:登录验证的js
 */
$(function () {
    $('#submit').on("click", function () {
        $.ajax({
            type: "post",
            url: "/login/check_login",
            data: {"username":$('#username').val(),"passwd":$('#passwd').val()},//TODO 加密密码
            dataType: "json",
            //contentType: "application/json; charset=utf-8",
            success: function (data) {
                if(data.status){
                    window.location.href="/index";
                }else {
                    alert("用户名或密码错误");
                }
                console.log(data);
            },
            error: function (error) {
                console.log(error);
            }
        });
    });
});