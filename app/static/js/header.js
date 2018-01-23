/**
 * Created by Administrator on 2018/1/18.
 * author:刘雅欠
 */
 var headerHTML  = ' <div class="header-title container">'+
                        '<p class="">开源博客系统Blog_mini</p>'+
                        '<span class="">让每个人都轻松拥有可管理的个人博客！—By author</span>'+
                    '</div>'+
        '<nav class="navbar navbar-inverse" role="navigation">' +
             '<div class="container">' +
                '<div class="navbar-header">' +
                    '<button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#blog-navbar-collapse"  aria-expanded="false">' +
                        '<span class="sr-only">Toggle navigation</span>' +
                        '<span class="icon-bar"></span>' +
                        '<span class="icon-bar"></span>' +
                        '<span class="icon-bar"></span>' +
                    '</button>' +
                    '<a class="navbar-brand" href="#">Blog-Mini</a> ' +
                '</div>' +
                '<div class="collapse navbar-collapse" id="blog-navbar-collapse">' +
                    '<ul class="nav navbar-nav header-list">'+
                        '<li class="header-item active">'+
                            '<a class="" href="">'+
                                '<span class="glyphicon glyphicon-home"></span>'+
                                '首页'+
                            '</a>'+
                        '</li>'+
                        '<li  class="header-item dropdown">'+
                            '<a href="" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">'+
                                'Web开发<span class="caret"></span>'+
                            '</a>'+
                            '<ul class="dropdown-menu">' +
                                '<li><a href="">Python开发</a></li>' +
                                '<li class="divider"></li>' +
                                '<li><a href="">Python开发</a></li>' +
                                '<li class="divider"></li>' +
                                '<li><a href="">Python开发</a></li>' +
                            '</ul>'+
                        '</li>'+
                        '<li  class="header-item">'+
                            '<a class="" href="">'+
                                '数据库'+
                                '<span class="icon-right"></span>'+
                                    '<ul></ul>'+
                                '</a>'+
                        '</li>'+
                        '<li  class="header-item">'+
                            '<a class="" href="">'+
                                '网络技术'+
                                '<span class="icon-right"></span>'+
                                    '<ul></ul>'+
                                '</a>'+
                        '</li>'+
                        '<li  class="header-item">'+
                            '<a class="" href="">'+
                                '爱生活，爱自己'+
                                '<span class="icon-right"></span>'+
                                    '<ul></ul>'+
                                '</a>'+
                        '</li>'+
                        '<li  class="header-item">'+
                            '<a class="" href="">'+
                               'Linux世界'+
                                '<span class="icon-right"></span>'+
                                    '<ul></ul>'+
                                '</a>'+
                        '</li>' +
                    '</ul>' +
                    '<ul class="nav navbar-nav navbar-right">' +
                        '<li class="dropdown">'+
                            '<a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false"><span class="glyphicon glyphicon-user"></span>haroro <span class="caret"></span></a>' +
                            '<ul class="dropdown-menu">' +
                                '<li><a href="">发布的博客</a></li>' +
                                '<li><a href="#" onclick="loginModal(\'admin\')">登录到Blog</a></li>' +
                            '</ul>' +
                        '</li>'+
                    '</ul>' +
                 '</div>' +
             '</div>' +
        '</nav>';
    var blogModal =
        '<div class="modal" id="blogModal" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> ' +
            '<div class="modal-dialog"> ' +
                '<div class="modal-content">' +
                    '' +
                '</div>' +
            '</div>' +
        '</div>';
