var Status = {
  Signin: 'signin',
  Register: 'register'
};

$(function() {
  $('#toggle_btn').click(function () {
    var status = $(this).attr('data-status');
    $('#repeat_password').toggleClass('hidden');
    if (status == Status.Signin) {
      $(this).attr('data-status', Status.Register);
      $(this).html('我已经有账号了。'); 
      $('#submit_btn').html('注册');

    } else {
      $(this).attr('data-status', Status.Signin);
      $(this).html('还没有账号，赶紧注册个？');
      $('#submit_btn').html('登陆');
    }
  });

  $('#submit_btn').click(function() {
    var username = $('#input_username').val();
    var password = $('#input_password').val();
    var status = $('#toggle_btn').attr('data-status');
    if (status == Status.Signin) {
      $.post(
        '/cgi-bin/user_login.py',
        { username: username, password: password },
        function(response) {
          if (response.success) {
            window.location = '/avatar.html'
          } else {
            alert(response.message);
          }
        }
      )
    } else if (status == Status.Register) {
      var repeat_password = $('#repeat_password').val();
      if (repeat_password != password) {
        alert("两次密码输入不一致。");
        return;
      }
      if (password.trim().length < 6) {
        alert("密码至少要6位。");
        return;
      }
      $.post(
        '/cgi-bin/user_register.py',
        { username: username, password: password },
        function(response) {
          if (response.success) {
            alert('注册成功，请登陆。');
            window.location = '/';
          } else {
            alert(response.message);
          }
        }
      )

    }
  });
});
