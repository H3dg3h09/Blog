/**
 * Created by Administrator on 2018/1/22.
 * author: 刘雅欠
 */
//打开登录模态框
function loginModal(type){
    if(type == 'admin'){
        $("#blogModal").find('.modal-dialog').css({'width':'400px'})
        $("#blogModal").modal({
            remote: "../../templates/login/admin_index.html"
        }).on('hidden.bs.modal',function(){
            $(this).removeData('bs.modal');
            $(this).find(".modal-content").children().remove();
        });
    }
}
//登录操作
//用户名，密码采用md5加密
//在原有字符串的基础上，用户名追加5个随机字符串，密码追加6个随机字符串
function login(type){
    var email = $('#login-name').val();
    var password = $('#login-password').val();
    var reg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(\.[a-zA-Z0-9_-])+/;
    //console.log(username+'||'+password);
    var data={
        "email":email,
        "passwrod":password
    }
    if(!email){
        layer.alert('请输入邮箱',{icon:3},'提示');
    }else if(!reg.test(email)){
        layer.alert('邮箱格式不正确',{icon:3},'提示');
    }else if(!password){
        layer.alert('请输入密码',{icon:3},'提示');
    }else if(password.length<6){
        layer.alert('密码不能少于6位',{icon:3},'提示');
    }else{
        $.ajax({
            type:'post',
            data:data,
            url:'/login',
            success:function(res){
                
            }
        })
    }


}
//生成随机数
//len随意数长度，传参时返回len长度的随意数，默认返回32位随意数
function randomString(len) {
    len = len || 32;
    /****默认去掉了容易混淆的字符oOLl,9gq,Vv,Uu,I1****/
    var $chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678';
    var maxPos = $chars.length;
    var pwd = '';
    for (var i = 0; i < len; i++) {
        pwd += $chars.charAt(Math.floor(Math.random() * maxPos));
    }
    return pwd;
}