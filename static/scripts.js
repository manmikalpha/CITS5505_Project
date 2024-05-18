
uploadImage = function() {
    var fileInput = document.getElementById('fileInput');
    var file = fileInput.files[0];
    var formData = new FormData();
    formData.append('file', file);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/upload', true);
    xhr.onload = function() {
        if (xhr.status === 200) {
            console.log('Image uploaded successfully');
        } else {
            console.log('Image upload failed');
        }
    };
    xhr.send(formData);
}

const userEmail =document.body.dataset.userEmail; ;
const url = `https://anonymous-animals.azurewebsites.net/avatar/${userEmail}`;
document.getElementById('avatar').src = url;
console.log(url);


 
