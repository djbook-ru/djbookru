jQuery(function($) {
    function drawRating($item) {
        $item.find('.rating').text($item.data('rating'));

        if ($item.data('has-vote')) {
            $item.find('a').prop('class', 'fa fa-thumbs-up');
        } else {
            $item.find('a').prop('class', 'fa fa-thumbs-o-up');
        }
    }

    $('.js-rating').each(function() {
        var $this = $(this),
            has_vote = $this.data('has-vote') === 'True';

        drawRating($this);

        $this.find('a').click(function() {
            var $a = $(this),
                $item = $a.parent();

            $.post($a.attr('href'), function(resp) {
                if (resp.error) {

                } else {
                    $item.data('rating', resp.rating);
                    $item.data('has-vote', resp.voted);
                    drawRating($item);
                }
            });
            return false;
        });
    });
});