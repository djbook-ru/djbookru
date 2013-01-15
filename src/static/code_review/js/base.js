var CodeReview = {};

CodeReview.Comment = Backbone.Model.extend({

});

CodeReview.CommentList = Backbone.Collection.extend({

    model: CodeReview.Comment,

    initialize: function(options) {
        this.url = options.url;
    }
});

CodeReview.CommentView = Backbone.View.extend({
    tagName: 'div',
    className: 'comment media',
    template: _.template(
        '<a class="pull-left" href="#"><img class="media-object" src="<%= author_avatar %>"></a>'+
        '<div class="media-body"><%= content %></div>'
    ),

    initialize: function(options) {
        this.listenTo(this.model, 'destroy', this.remove);
        this.$placeholder = $('<div class="placeholder"></div>');
    },

    getPlaceholder: function(){
        this.$placeholder.attr('style', 'height: '+this.$el.outerHeight()+'px !important');
        return this.$placeholder;
    },

    render: function(){
        this.$el.html(this.template(this.model.toJSON()));
        return this;
    }
});

CodeReview.AppView = Backbone.View.extend({
    events: {
        'mouseenter .gutter .line': 'highlightRow',
        'mouseleave .gutter .line': 'unhighlightRow',
        'click .gutter .line': 'showForm',
        'click .comment-form .close': 'hideForm',
        'click .comment-form .send': 'sendForm'
    },

    initialize: function(options) {
        this.comments = options.comments;

        this.listenTo(this.comments, 'add', this.addOne);
        this.listenTo(this.comments, 'reset', this.addAll);
        this.listenTo(this.comments, 'all', this.render);

        this.comments.fetch();
    },

    render: function(){

    },

    sendForm: function(e){
        var $form = $(e.target).parents('.comment-form');

    },

    hideForm: function(e){
        var $form = $(e.target).parents('.comment-form');
        var $row = $form.prev();
        this._getGutter($row).next().remove();
        $form.remove();
    },

    showForm: function(e){
        var $el = $(e.target);
        var $row = this._getRow($el);

        $row.after(this._renderForm());
        $el.after('<div class="form-placeholder"></div>');
    },

    highlightRow: function(e){
        var $el = $(e.target);
        $el.addClass('highlighted');
        this._getRow($el).addClass('highlighted');
    },

    unhighlightRow: function(e){
        var $el = $(e.target);
        $el.removeClass('highlighted');
        this._getRow($el).removeClass('highlighted');
    },

    addOne: function(comment){
        var view = new CodeReview.CommentView({
            model: comment
        });
        var row = comment.get('row');
        this._getRow(row).after(view.render().el);

        this._getGutter(comment.get('row')).after(view.getPlaceholder());
    },

    addAll: function(){
        this.comments.each(this.addOne, this);
    },

    _renderForm: function(){
        return '<div class="comment-form"><textarea></textarea><button class="btn send">Send</button><button type="button" class="close pull-left">&times;</button></div>';
    },

    _getRow: function($gutterEl){
        if (_.isNumber($gutterEl)){
            return this.$('.code .container .line.number'+$gutterEl);
        }
        return this.$('.code .container .line.'+this._rowIndexCls($gutterEl));
    },

    _getGutter: function($row){
        if (_.isNumber($row)){
            return this.$('.gutter .line.number'+$row);
        }
        return this.$('.gutter .line.'+this._rowIndexCls($row));
    },

    _rowIndexCls: function($el){
        return $el.attr('class').match(/number\d+/g)[0];
    }
});