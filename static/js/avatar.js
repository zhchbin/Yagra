var holder = document.getElementById('holder'),
    tests = {
      filereader: typeof FileReader != 'undefined',
      dnd: 'draggable' in document.createElement('span'),
      formdata: !!window.FormData,
      progress: "upload" in new XMLHttpRequest
    }, 
    support = {
      filereader: document.getElementById('filereader'),
      formdata: document.getElementById('formdata'),
      progress: document.getElementById('progress')
    },
    acceptedTypes = {
      'image/png': true,
      'image/jpeg': true,
      'image/gif': true
    },
    progress = document.getElementById('uploadprogress'),
    fileupload = document.getElementById('upload');

"filereader formdata progress".split(' ').forEach(function (api) {
  if (tests[api] === false) {
    support[api].className = 'fail';
  } else {
    // FFS. I could have done el.hidden = true, but IE doesn't support
    // hidden, so I tried to create a polyfill that would extend the
    // Element.prototype, but then IE10 doesn't even give me access
    // to the Element object. Brilliant.
    support[api].className = 'hidden';
  }
});

function previewfile(file) {
  if (tests.filereader === true && acceptedTypes[file.type] === true) {
    var reader = new FileReader();
    reader.onload = function (event) {
      var image = new Image();
      image.src = event.target.result;
      image.width = 250; // a fake resize
      while (holder.firstChild)
        holder.removeChild(holder.firstChild);
      holder.appendChild(image);
    };

    reader.readAsDataURL(file);
  }
}

function readfiles(files) {
  var formData = tests.formdata ? new FormData() : null;
  for (var i = 0; i < files.length; i++) {
    if (tests.formdata) formData.append('filename', files[i]);
    previewfile(files[i]);
  }

  // now post a new XHR request
  if (tests.formdata) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/cgi-bin/avatar_upload.py');
    xhr.onload = function() {
      progress.value = progress.innerHTML = 100;
    };
    xhr.onreadystatechange = function() {
      if (xhr.readyState != 4 || xhr.status != 200)
        return;
      
      response = JSON.parse(xhr.responseText);
      if (response.success) {
        alert("您的头像更新成功啦！");
      } else {
        alert(response.message);
      }
    }

    if (tests.progress) {
      xhr.upload.onprogress = function (event) {
        if (event.lengthComputable) {
          var complete = (event.loaded / event.total * 100 | 0);
          progress.value = progress.innerHTML = complete;
        }
      }
    }

    xhr.send(formData);
  }
}

if (tests.dnd) { 
  holder.ondragover = function () { this.className = 'hover'; return false; };
  holder.ondragend = function () { this.className = ''; return false; };
  holder.ondrop = function (e) {
    this.className = '';
    e.preventDefault();
    readfiles(e.dataTransfer.files);
  }
}

fileupload.querySelector('input').onchange = function () {
  readfiles(this.files);
};

$.get('/cgi-bin/user_validation.py', function(response) {
  if (!response.success)
    return;
  $('#username').html(response.message);
  image_src = '/cgi-bin/user_avatar.py?username=' + response.message;
  $('#holder').empty().append('<img src="' + image_src + '" width=250></img>');
}).fail(function() {
  window.location = '/';
});

$('#logout_btn').click(function() {
  $.post('/cgi-bin/user_logout.py').always(function() {
    window.location = '/';
  });
});
