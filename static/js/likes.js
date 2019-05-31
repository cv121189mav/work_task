$(document).ready(function () {
    var TEXT_DISLIKE = 'favorite_border';
    var TEXT_LIKE = 'favorite';

    $('.action-like').on('click', function (e) {
        e.preventDefault();
        var id = $(this).data('id');
        var like_id = '#like-' + id;
        var like = $(like_id);

        var href = `like_update/${$(this).data('id')}/`;
        $.ajax({
            url: href,
            success: function (result) {
                if (result.like) {
                    like.text(TEXT_LIKE)
                } else {
                    like.text(TEXT_DISLIKE)
                }
                $('#like-count-' + id).text(result.count)
            }
        })
    });
});
