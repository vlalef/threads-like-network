document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.edit-button').forEach(button => {
        button.addEventListener('click', editPost);
    });
    document.querySelectorAll('.like-button').forEach(button => {
        button.addEventListener('click', likePost);
    });
});

function editPost() {
    const postId = this.dataset.postId;
    const postDiv = document.querySelector(`.post[data-post-id="${postId}"]`);
    const contentDiv = postDiv.querySelector('.post-content');
    const currentContent = contentDiv.textContent;

    contentDiv.innerHTML = `
        <textarea class="form-control edit-textarea">${currentContent}</textarea>
        <div class="edit-buttons mt-2">
            <button class="btn btn-primary save-button me-2">Save</button>
            <button class="btn btn-secondary cancel-button">Cancel</button>
        </div>
    `;

    contentDiv.querySelector('.save-button').addEventListener('click', function() {
        const newContent = contentDiv.querySelector('.edit-textarea').value;

        fetch(`/edit/${postId}`, {
            method: 'PUT',
            body: JSON.stringify({
                content: newContent
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(result => {
            contentDiv.innerHTML = newContent;
        })
        .catch(error => {
            console.log('Error:', error);
            contentDiv.innerHTML = currentContent;
            alert('Error saving post. Please try again.');
        });
    });

    contentDiv.querySelector('.cancel-button').addEventListener('click', function() {
        contentDiv.innerHTML = currentContent;
    });
}

function likePost() {
    const postId = this.dataset.postId;
    const button = this;
    const postDiv = document.querySelector(`.post[data-post-id="${postId}"]`);
    const likeCountSpan = postDiv.querySelector('.like-count');

    fetch(`/like/${postId}`)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        likeCountSpan.textContent = data.like_count;

        if (data.liked) {
            button.textContent = 'Unlike';
            button.classList.add('liked');
        } else {
            button.textContent = 'Like';
            button.classList.remove('liked');
        }
    })
    .catch(error => {
        console.log('Error:', error);
        alert('Error updating like status. Please try again.');
    });
}