(function() {
    function ModelChooser(html, modalUrl) {
        this.html = html;
        this.modalUrl = modalUrl;
    }
    ModelChooser.prototype.render = function(placeholder, name, id, initialState) {
        var html = this.html.replace(/__NAME__/g, name).replace(/__ID__/g, id);
        placeholder.outerHTML = html;
        var chooser = window.wagtail.ui.ModelChooser.setupWagtailWidget(id, this.modalUrl);
        chooser.setState(initialState);
        return chooser;
    };

    window.telepath.register('wagtailmodelchooser.widgets.ModelChooser', ModelChooser);
})();
