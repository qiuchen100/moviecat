;
var member_reg_ops = {
    init: function() {
        this.eventBind();
    },
    eventBind: function() {
        $(".reg-wrap .do-reg").click(function() {
            var btn_target = $(this);
            if (btn_target.hasClass("disabled")) {
                alert("正在处理，请不要重复点击！");
                return ;
            }
            var loginName = $("#loginName").val();
            var loginPwd = $("#loginPwd").val();
            var loginPwd2 = $("#loginPwd2").val();
            if (loginName == undefined || loginName.length < 1) {
                common_ops.alert('用户名不能为空！');
                return ;
            }
            if (loginPwd == undefined || loginPwd.length < 6) {
                common_ops.alert('密码不能为空且长度不能小于6！');
                return ;
            }
            if (loginPwd != loginPwd2) {
                common_ops.alert('两次输入的密码不相等！');
                return ;
            }
            btn_target.addClass("disabled");
            $.ajax({
                url: common_ops.buildUrl("/member/reg"),
                type: "POST",
                data: {
                    loginName: loginName,
                    loginPwd: loginPwd,
                    loginPwd2: loginPwd2,
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
    member_reg_ops.init();
});