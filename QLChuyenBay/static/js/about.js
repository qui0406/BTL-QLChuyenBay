function addComment(){
    let content = document.getElementById('floatingTextarea2');
    // Kiểm tra content nếu cần
    // if (content != null){

    fetch('/api/comments', {
        method: 'POST',  // Dấu : bị thiếu ở đây
        body: JSON.stringify({
            'content': content.value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(res => res.json())  // Chuyển đổi phản hồi thành JSON
    .then(data => {
        // Đảm bảo sử dụng đúng data thay vì comment_data
        if (data.status == 201) {
            let c = data.comment;
            console.log(c)
            let area = document.getElementById('cmtArea');
            area.innerHTML = `
                <div class="row comments">
                    <div class="col-md-1 col-xs-4">
                        <img class="rounded-circle img-fluid"
// loi  ne
                        src="${c.user.avatar}"
                        alt="">
                    </div>
                    <div class="col-md-11 col-xs-8">
                        <p>${c.content}</p>
                        <p><em>${c.created_date}</em></p>
                    </div>
                </div>` + area.innerHTML;
        } else if (data.status == 404) {
            alert(data.err_msg);  // Đảm bảo sử dụng data thay vì comment_data
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });

    // }
}
