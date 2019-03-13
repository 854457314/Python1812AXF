$(function () {
    $('.mine').width(innerWidth)

    $('#login-i').click(function () {
        // 设置cooking
        $cookie('back','mine',{expires:3,path:'/'})
        window.open('/login/','_self')
    })
})