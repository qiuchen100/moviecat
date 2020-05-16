;
var member_login_ops = {
    init: function() {
        this.eventBind();
    },
    eventBind: function() {
        $(".login-wrap .do-login").click(function() {
            const btn_target = $(this);
            if (btn_target.hasClass("disabled")) {
                alert("正在处理，请不要重复点击！");
                return ;
            }
            const loginName = $("#loginName").val();
            const loginPwd = $("#loginPwd").val();
            if (loginName == undefined || loginName.length < 1) {
                common_ops.alert('用户名不能为空！');
                return ;
            }
            if (loginPwd == undefined || loginPwd.length < 6) {
                common_ops.alert('密码不能为空且长度不能小于6！');
                return ;
            }
            btn_target.addClass("disabled");
            $.ajax({
                url: common_ops.buildUrl("/member/login"),
                type: "POST",
                data: {
                    loginName: loginName,
                    loginPwd: loginPwd
                },
                dataType: 'json',
                success: function (res) {
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = common_ops.buildUrl("/");
                        }
                    }
                    common_ops.alert(res.msg, callback);
                }
            })
        });
    }
};
$(document).ready(function() {
    member_login_ops.init();
});